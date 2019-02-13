/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2018 Zhang Kaihua(apple_eat@126.com)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
#include <stdlib.h>
#include <string.h>
#include "esp_err.h"

#include "py/nlr.h"
#include "py/runtime.h"
#include "py/objstr.h"
#include "modmachine.h"
#include "mphalport.h"
#include "wav_head.h"
#include "driver/i2s.h"
#include "modcodec.h"
#include "esp_log.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include <stdio.h>
#include <time.h>
#include <dirent.h>
#include "sys/stat.h"
#include "soc/io_mux_reg.h"
#include <math.h>
#include "mp3dec.h"
#include "coder.h"
#include "mp3common.h"

#define EXAMPLE_I2S_BUF_DEBUG (1)
static const char *TAG = "CODEC";

#define I2S_NUM (0)
//i2s sample rate
#define DEFAULT_I2S_SAMPLE_RATE (16000)
//i2s data bits
#define DEFAULT_I2S_SAMPLE_BITS (16)
//I2S read buffer length
#define DEFAULT_I2S_READ_LEN (16 * 1024)
//I2S data format
#define DEFAULT_I2S_FORMAT (I2S_CHANNEL_FMT_RIGHT_LEFT)
//I2S channel number
#define DEFAULT_I2S_CHANNEL_NUM ((DEFAULT_I2S_FORMAT < I2S_CHANNEL_FMT_ONLY_RIGHT) ? (2) : (1))
//I2S built-in ADC unit
#define I2S_ADC_UNIT ADC_UNIT_1
//I2S built-in ADC channel
#define I2S_ADC_CHANNEL ADC1_CHANNEL_0

#define MAINBUF_SIZE 1940
#define MIN_VOL_OFFSET -50

#define CCCC(c1, c2, c3, c4) ((c4 << 24) | (c3 << 16) | (c2 << 8) | c1)
#define PIN_PD 4

#define PLAYMODE_REPEAT 0
#define PLAYMODE_REPEAT_PLAYLIST 1
#define PLAYMODE_PLAYLIST 2
#define PLAYMODE_RANDOM 3

#define MUSICDB_FN_LEN 128
#define MUSICDB_TITLE_LEN 128
typedef enum
{
    NONE = 0,
    WAV,
    MP3,
    APE,
    FLAC
} musicType_t;

typedef struct
{
    bool paused, started;
    uint16_t totalTime;
    uint16_t currentTime;
    int sampleRate;
    int bitsPerSample;
    char title[128];
    char author[128];
    char album[128];
    char fileName[128];
    FILE *filePtr;
    int playMode;
    int volume; //0 - 100%
    double volumeMultiplier;
    musicType_t musicType;
    bool musicChanged;
} playerState_t;

playerState_t playerState = {
    .paused = false,
    .started = true,
    .totalTime = 0,
    .currentTime = 0,
    .title = "",
    .author = "",
    .album = "",
    .playMode = PLAYMODE_RANDOM,
    .volume = 50,
    .volumeMultiplier = pow(10, -25 / 20.0),
    .musicType = NONE,
    .musicChanged = true
};

/* mp3解码器用静态内存分配方式，约消耗34K RAM */
MP3DecInfo mp3DecInfo;
FrameHeader fh;
SideInfo si;
ScaleFactorInfo sfi;
HuffmanInfo hi;
DequantInfo di;
IMDCTInfo mi;
SubbandInfo sbi;
HMP3Decoder hMP3Decoder;
MP3FrameInfo mp3FrameInfo;
unsigned char readBuf[MAINBUF_SIZE];
uint16_t output[1153 * 4];
int bytesLeft;
unsigned long music_data_index;
int samplerate ;

/**
 * @brief debug buffer data
 */
void example_disp_buf(uint8_t *buf, int length)
{
#if EXAMPLE_I2S_BUF_DEBUG
    printf("======\n");
    for (int i = 0; i < length; i++)
    {
        printf("%02x ", buf[i]);
        if ((i + 1) % 8 == 0)
        {
            printf("\n");
        }
    }
    printf("======\n");
#endif
}

/**
 * @brief Scale data to 16bit/32bit for I2S DMA output.
 *        DAC can only output 8bit data value.
 *        I2S DMA will still send 16 bit or 32bit data, the highest 8bit contains DAC data.
 */
STATIC int example_i2s_dac_data_scale(uint8_t *d_buff, uint8_t *s_buff, uint32_t len)
{
    uint32_t j = 0;
#if (DEFAULT_I2S_SAMPLE_BITS == 16)
    for (int i = 0; i < len; i++)
    {
        d_buff[j++] = 0;
        d_buff[j++] = s_buff[i];
        d_buff[j++] = 0;
        d_buff[j++] = s_buff[i];
    }
    return (len * 4);
#else
    for (int i = 0; i < len; i++)
    {
        d_buff[j++] = 0;
        d_buff[j++] = 0;
        d_buff[j++] = 0;
        d_buff[j++] = s_buff[i];
    }
    return (len * 4);
#endif
}

STATIC mp_obj_t dac_init(mp_obj_t sampleRate, mp_obj_t bitsWidth)
{
    uint32_t _sampleRate = mp_obj_get_int(sampleRate);
    int _bitsWidth = mp_obj_get_int(bitsWidth);

    i2s_config_t i2s_config = {
        .mode = I2S_MODE_MASTER | I2S_MODE_TX | I2S_MODE_DAC_BUILT_IN,
        .sample_rate = _sampleRate,
        .bits_per_sample = _bitsWidth,
        .communication_format = I2S_COMM_FORMAT_I2S_MSB,
        .channel_format = DEFAULT_I2S_FORMAT,
        .intr_alloc_flags = 0,
        .dma_buf_count = 2,
        .dma_buf_len = 1024,
        //.use_apll = true
    };
    i2s_driver_uninstall(I2S_NUM);
    //install and start i2s driver
    i2s_driver_install(I2S_NUM, &i2s_config, 0, NULL);
    //init DAC pad
    i2s_set_dac_mode(I2S_DAC_CHANNEL_BOTH_EN);

	mp3DecInfo.FrameHeaderPS = &fh;
	mp3DecInfo.SideInfoPS = &si;
	mp3DecInfo.ScaleFactorInfoPS = &sfi;
	mp3DecInfo.HuffmanInfoPS = &hi;
	mp3DecInfo.DequantInfoPS = &di;
	mp3DecInfo.IMDCTInfoPS = &mi;
	mp3DecInfo.SubbandInfoPS = &sbi;
	hMP3Decoder = &mp3DecInfo;

    samplerate = 0;
    i2s_zero_dma_buffer(0);

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(dac_init_obj, dac_init);

STATIC mp_obj_t I2S_read(mp_obj_t len)
{
    uint16_t buff_len = mp_obj_get_int(len);
    uint16_t byteReads;
    uint8_t buffer[buff_len];
    i2s_read(I2S_NUM, (void *)buffer, buff_len, (size_t *)&byteReads, 5000);

    return mp_obj_new_bytes((const byte *)buffer, buff_len);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(I2S_read_obj, I2S_read);

STATIC mp_obj_t I2S_write(mp_obj_t buff)
{
    size_t len;
    const char *s_buf = mp_obj_str_get_data(buff, &len);
    //ESP_LOGI(TAG, "dat len = %d..........", len);
    uint8_t d_buf[len * 2];
    example_i2s_dac_data_scale(d_buf, (uint8_t *)s_buf, len);
    //example_disp_buf((uint8_t*) s_buf, 100);
    uint16_t bytesWritten;
    i2s_write(I2S_NUM, (const void *)d_buf, len * 2, (size_t *)&bytesWritten, 500);

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(I2S_write_obj, I2S_write);

// STATIC mp_obj_t MP3DecodeInit(void)
// {
//     // ESP_LOGI(TAG, "MP3 start decoding");
    
//     // readBuf = malloc(MAINBUF_SIZE);
//     // if (readBuf == NULL){
//     //     ESP_LOGE(TAG, "ReadBuf malloc failed");
//     //     return MP_OBJ_NEW_SMALL_INT(-1);
//     // }
//     // output = malloc(1153 * 4);
//     // if (output == NULL){
//     //     free(readBuf);
//     //     ESP_LOGE(TAG, "OutBuf malloc failed");
// 	// 	return MP_OBJ_NEW_SMALL_INT(-1);
//     // }
//     // hMP3Decoder = MP3InitDecoder();
//     // if (hMP3Decoder == 0)
//     // {
//     //     free(readBuf);
//     //     free(output);
//     //     ESP_LOGE(TAG, "Memory not enough");
// 	// 	return MP_OBJ_NEW_SMALL_INT(-2);
//     // }

//     // playerState.currentTime = 0;
// 	// bytesLeft = 0;

//     // samplerate = 0;
//     // i2s_zero_dma_buffer(0);
// 	//处理ID3V2标签头,此工作丢到python层面去做
//     // char tag[10];
//     // int tag_len = 0;
//     // memcpy(tag, music, 10);
//     // if (memcmp(tag, "ID3", 3) == 0)
//     // { //mp3?
//     //     //获取ID3V2标签头长，以确定MP3数据起始位置
//     //     tag_len = ((tag[6] & 0x7F) << 21) | ((tag[7] & 0x7F) << 14) | ((tag[8] & 0x7F) << 7) | (tag[9] & 0x7F);
//     //     ESP_LOGI(TAG, "tag_len: %d %x %x %x %x", tag_len, tag[6], tag[7], tag[8], tag[9]);
//     // }
//     // else
//     // {
//     //     ESP_LOGE(TAG, "Not an mp3 file.");
//     //     return;
//     // }
// 	return MP_OBJ_NEW_SMALL_INT(MAINBUF_SIZE);
// }
// STATIC MP_DEFINE_CONST_FUN_OBJ_0(mp3_decode_init_obj, MP3DecodeInit);

STATIC mp_obj_t mp3Decode(mp_obj_t mp3Data)
{
	/* 向readBuf中补充数据 */
	size_t len;
    const char *s_buf = mp_obj_str_get_data(mp3Data, &len);
	// for(int i = 0; i < 10; i++)
	// ESP_LOGE(TAG, "%d ", *(s_buf+i));
	// ESP_LOGE(TAG, "read len is %d ", len);
	bytesLeft = MAINBUF_SIZE - len;
	if (bytesLeft < MAINBUF_SIZE)
	{
		memmove(readBuf, readBuf + len, bytesLeft); //数据移动缓存头部，补充进来的数据接到后面
		memcpy(readBuf + bytesLeft, s_buf, len);
		bytesLeft = MAINBUF_SIZE;
		// for (int i = 0; i < 32; i++)
		//     ESP_LOGI(TAG, "%d", (uint8_t) * (readBuf + i));
	}
        //搜索缓存中第一帧帧头
	unsigned char *readPtr = readBuf;
	int offset = MP3FindSyncWord(readBuf, bytesLeft);
	if (offset < 0)
	{
		ESP_LOGE(TAG, "MP3FindSyncWord not find");
		bytesLeft = 0;
		return MP_OBJ_NEW_SMALL_INT(MAINBUF_SIZE);  //缓存中无MP3帧
	}
	else
	{
		readPtr += offset;   //data start point
		bytesLeft -= offset; //in buffer
		//以下解码n帧，readPtr会递增，bytesLeft递减
		int errs = MP3Decode(hMP3Decoder, &readPtr, &bytesLeft, (short *)output, 0);
		if (errs != 0)
		{
			ESP_LOGE(TAG, "MP3Decode failed ,code is %d ", errs);
			return MP_OBJ_NEW_SMALL_INT(MAINBUF_SIZE - bytesLeft);  //缓存中无MP3帧;
		}
		MP3GetLastFrameInfo(hMP3Decoder, &mp3FrameInfo);
		//   playerState.currentTime = (ftell(mp3File) - tag_len) * 8 / mp3FrameInfo.bitrate;
		if(samplerate!=mp3FrameInfo.samprate)
		{
			samplerate=mp3FrameInfo.samprate;
			i2s_set_clk(0,samplerate,16,mp3FrameInfo.nChans);
			playerState.sampleRate = mp3FrameInfo.samprate;
			playerState.bitsPerSample = 16;
			//ESP_LOGI(TAG,"mp3file info---bitrate=%d,layer=%d,nChans=%d,samprate=%d,outputSamps=%d",mp3FrameInfo.bitrate,mp3FrameInfo.layer,mp3FrameInfo.nChans,mp3FrameInfo.samprate,mp3FrameInfo.outputSamps);
		}
		for (int i = 0; i < mp3FrameInfo.outputSamps*2; ++i)
		{
			//output[i] *= playerState.volumeMultiplier;   //调整音量
			output[i] = (uint16_t)(output[i]*255.0/65535+128); //16位－> 8位，加上直流分量，消除负值，使值范围在0-255.
			output[i] = output[i] << 8;
			//ESP_LOGI(TAG, "%d", output[i]);
		}

		uint16_t bytesWritten;
		i2s_write(I2S_NUM, (const char *)output, mp3FrameInfo.outputSamps * 2, (size_t *)(&bytesWritten), 1000 / portTICK_RATE_MS);
		return MP_OBJ_NEW_SMALL_INT(MAINBUF_SIZE - bytesLeft);  //缓存中无MP3帧;
	}

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(mp3_decode_obj, mp3Decode);

STATIC mp_obj_t MP3DecodeEnd(void)
{
	i2s_zero_dma_buffer(0);
	i2s_driver_uninstall(I2S_NUM);

	ESP_LOGI(TAG, "end mp3 decode ..");
	return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(mp3_decode_end_obj, MP3DecodeEnd);

STATIC const mp_map_elem_t mpython_codec_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_cocdec)},
    //{ MP_OBJ_NEW_QSTR(MP_QSTR___init__), (mp_obj_t)&music___init___obj },
    {MP_OBJ_NEW_QSTR(MP_QSTR_dac_init), (mp_obj_t)&dac_init_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_I2S_read), (mp_obj_t)&I2S_read_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_I2S_write), (mp_obj_t)&I2S_write_obj},
	//{MP_OBJ_NEW_QSTR(MP_QSTR_mp3_decode_init), (mp_obj_t)&mp3_decode_init_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_mp3_decode), (mp_obj_t)&mp3_decode_obj},
	{MP_OBJ_NEW_QSTR(MP_QSTR_mp3_decode_end), (mp_obj_t)&mp3_decode_end_obj},
};

STATIC MP_DEFINE_CONST_DICT(mpython_codec_locals_dict, mpython_codec_locals_dict_table);

const mp_obj_module_t mp_module_codec = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mpython_codec_locals_dict,
};