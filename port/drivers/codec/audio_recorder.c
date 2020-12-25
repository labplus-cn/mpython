/*
 * audio_recorder.c
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "esp_system.h"
#include "esp_log.h"
#include "py/stream.h"
#include "py/reader.h"
#include "py/runtime.h"
#include "extmod/vfs.h"

#include "audio_recorder.h"
#include "audio_renderer.h"
#include "http_client.h"
#include "driver/i2s.h"
#include "driver/adc.h"
#include "local_play.h"
#include "wave_head.h"
#include "mpconfigboard.h"

#define TAG "audio_recorder"

#define REC_BLOCK_LEN (4096)
#define REC_BLOCKS_PER_SECOND (4)

static recorder_t *recorder_instance = NULL;
extern HTTP_HEAD_VAL http_head[6];

void example_disp_buf(uint8_t* buf, int length)
{
    printf("======\n");
    for (int i = 0; i < length; i++) {
        printf("%02x ", buf[i]);
        if ((i + 1) % 8 == 0) {
            printf("\n");
        }
    }
    printf("======\n");
}

__attribute__ ((gnu_inline))inline void adc_data_scale( uint8_t* s_buff, uint32_t len)
{
    uint32_t j = 0;
    uint32_t dac_value;

    for (int i = 0; i < len; i += 2) {
        dac_value = ((((uint16_t) (s_buff[i + 1] & 0xf) << 8) | ((s_buff[i + 0]))));
        dac_value = (dac_value - 2047 - 300) << 4; 
        s_buff[j++] = dac_value & 0xff;
        s_buff[j++] = (dac_value >> 8) & 0xff;
    }
}


static void i2s_adc_data_scale1(int16_t * d_buff, uint8_t* s_buff, uint32_t len)
{
    uint32_t j = 0;

    #if MICROPY_BUILDIN_ADC
    uint16_t dac_value;
    int16_t tmp;

    for (int i = 0; i < len; i += 2) {
        dac_value = ((((uint16_t) (s_buff[i + 1] & 0xf) << 8) | ((s_buff[i + 0]))));
        tmp = dac_value - 2047 - 300; 
        d_buff[j++] = (tmp < 0)?(-tmp):tmp;
    }
    #else          
    renderer_config_t *renderer = renderer_get();

    if(renderer->bit_depth == I2S_BITS_PER_SAMPLE_16BIT) 
    {
        memcpy((uint8_t *)d_buff, s_buff, len);

        for (int i = 0; i < len/2; i++){

            d_buff[i] = (d_buff[i]< 0)?(-d_buff[i]):d_buff[i];
        }
        // printf("\r\n");
    }
    #endif
}

int cmpfunc (const void * a, const void * b)
{
   return ( *(int*)a - *(int*)b );
}

void recorder_init()
{
    if(!recorder_instance){
        recorder_instance = calloc(1, sizeof(recorder_t)); /* 1. Creat recorder.*/
    }
    /* 2. Create renderer. */
    renderer_config_t renderer_config;
    renderer_config.bit_depth  = I2S_BITS_PER_SAMPLE_16BIT; //I2S_BITS_PER_SAMPLE_8BIT; //I2S_BITS_PER_SAMPLE_16BIT;
    renderer_config.adc1_channel = ADC1_CHANNEL_2;
    renderer_config.channel_format = I2S_CHANNEL_FMT_ONLY_RIGHT; //I2S_CHANNEL_FMT_ONLY_RIGHT I2S_CHANNEL_FMT_RIGHT_LEFT
     renderer_config.sample_rate = 8000;
    renderer_config.mode = I2S_MODE_RX;    
    renderer_config.use_apll = true; 
    // renderer_config.i2s_channal_nums = 1;                                         
    renderer_init(&renderer_config); 
    renderer_start();
    // ESP_LOGE(TAG, "Create renderer, RAM left: %d", esp_get_free_heap_size()); 
}

void recorder_record(const char *filename, int time)
{
    // #define read_buff MP_STATE_PORT(record_buf)
    if (recorder_instance)
    {
        renderer_config_t *renderer = renderer_get();
        recorder_instance->file_name = filename;

        mp_obj_t F = file_open(recorder_instance->file_name, "w");
        int write_bytes;

        if ( time > 4)
        {
            mp_warning(NULL, "Record time too long, will limit to 5s.");
            time = 4;
        }
        // uint32_t data_len = renderer->sample_rate * (renderer->bit_depth / 8) * renderer->i2s_channal_nums * time;
        uint8_t blocks = time * REC_BLOCKS_PER_SECOND;
        uint32_t data_len = REC_BLOCK_LEN * blocks;
        
        /* ESP_LOGE(TAG, "renderer info: samplerate:%d, bitdepth:%d,ch nums:%d, rec datasize:%d", renderer->sample_rate, renderer->bit_depth, \
                  renderer->i2s_channal_nums, data_len); */

        /* make wav head */
        wav_header_t *wav_header = calloc(1, sizeof(wav_header_t));
        if (!wav_header)
            mp_raise_ValueError(MP_ERROR_TEXT("Can not alloc enough memory to make wav head."));
        wav_head_init(wav_header, renderer->sample_rate, renderer->bit_depth, renderer->i2s_channal_nums, data_len);
        file_write(F, &write_bytes, (uint8_t *)wav_header, sizeof(wav_header_t));
        free(wav_header);

        uint8_t *read_buff[blocks];
        for (int i = 0; i < blocks; i++){
            read_buff[i] = (uint8_t *)m_new(uint8_t, REC_BLOCK_LEN);
            if (!read_buff[i])
                mp_raise_ValueError(MP_ERROR_TEXT("Can not alloc enough memory to record."));
        }

        #if MICROPY_BUILDIN_ADC
        renderer_adc_enable();
        #endif 
        for(int i = 0; i < blocks; i++){
            renderer_read_raw(read_buff[i], REC_BLOCK_LEN);
            // example_disp_buf((uint8_t*) read_buff[i], 64);
            #if MICROPY_BUILDIN_ADC
            adc_data_scale( read_buff[i], REC_BLOCK_LEN);
            #endif
        }  
        for(int i = 0; i < blocks; i++)
            file_write(F, &write_bytes, read_buff[i], REC_BLOCK_LEN);
        file_close(F);
        #if MICROPY_BUILDIN_ADC
        renderer_adc_disable();
        #endif

        for(int i = 0; i < blocks; i++)
        {
            if(read_buff[i])
                m_del(uint8_t, read_buff[i], REC_BLOCK_LEN); 
        }

        // uint32_t data_len = renderer->sample_rate * (renderer->bit_depth / 8) * renderer->i2s_channal_nums * time;
        // uint16_t read_buf_len = 1024*3;
        // read_buff = (uint8_t *)m_new(uint8_t, read_buf_len); 
        // if (!read_buff)
        //     mp_raise_ValueError(MP_ERROR_TEXT("Can not alloc enough memory to record."));
        // // uint8_t *write_buff = calloc(renderer->i2s_read_buff_size, sizeof(uint8_t));
        // wav_header_t *wav_header = calloc(1, sizeof(wav_header_t));
        // if (!wav_header)
        //     mp_raise_ValueError(MP_ERROR_TEXT("Can not alloc enough memory to make wav head."));
        // wav_head_init(wav_header, renderer->sample_rate, renderer->bit_depth, renderer->i2s_channal_nums, data_len);
        // file_write(F, &write_bytes, (uint8_t *)wav_header, sizeof(wav_header_t));
        // // ESP_LOGE(TAG, "i2s_read_buff_size: %d, datasize:%d", renderer->i2s_read_buff_size, 32 * recorder->recorde_time); //samplerate:16000 32byts/ms
        // free(wav_header);
        // int i = 0;
        // uint16_t record_times = data_len / read_buf_len; //caculate record loops
        // ESP_LOGE(TAG, "i2s_read times: %d", record_times); 
        // renderer_adc_enable();    
        // while(i < record_times)
        // {
        //     renderer_read_raw(read_buff, read_buf_len);
        //     // example_disp_buf((uint8_t*) read_buff, 64);
        //     adc_data_scale(read_buff, read_buf_len);
        //     file_write(F, &write_bytes, read_buff, read_buf_len);
        //     i++;
        // }
        // renderer_adc_disable();
        // if(read_buff)
        //     m_del(uint8_t, read_buff, data_len); 
        // file_close(F);
    }
    else{
        mp_warning(NULL, "Please init recorder first.");
    }
    #undef read_buff
}

uint32_t recorder_loudness()
{
    // renderer_config_t *renderer = renderer_get();
    uint32_t len = 32; //320bytes: record 10ms
    int16_t *d_buff = calloc(len/2, sizeof(uint16_t));
    uint8_t *read_buff = calloc(len, sizeof(uint8_t)); 
    
    renderer_read_raw(read_buff, len);

    i2s_adc_data_scale1(d_buff, read_buff, len);
    audio_recorder_quicksort((uint16_t *)d_buff, len/2, 0, len/2 - 1);

    // uint32_t sum = d_buff[len/2-2] - d_buff[1];
    uint16_t loudness = d_buff[len/2 - 2];
    free(read_buff);
    free(d_buff);

    #if MICROPY_BUILDIN_ADC
    return loudness;
    #else          
    return loudness >> 4;
    #endif
}

void recorder_deinit()
{
    if (recorder_instance){
        free(recorder_instance);
        recorder_instance = NULL;
    }

    renderer_deinit();
}

recorder_t *get_recorder_handle()
{
    return recorder_instance;
}

/********************************
 *函数名：swap
 *作用：交换两个数的值
 *参数：交换的两个数
 *返回值：无
 ********************************/
static void swap(uint16_t *a, uint16_t *b)  
{
    uint16_t temp;
    temp = *a;
    *a = *b;
    *b = temp;
}

/************************************
 *函数名：quicksort
 *作用：快速排序算法
 *参数：
 *返回值：无
 ************************************/
void audio_recorder_quicksort(uint16_t *buff, uint32_t maxlen, uint32_t begin, uint32_t end)
{
    int i, j;
    if(begin < end)
    {
        i = begin + 1;  // buff[begin]作为基准数，因此从array[begin+1]开始与基准数比较！
        j = end;        // buff[end]是数组的最后一位

        while(i < j)
        {
            if(buff[i] > buff[begin])  // 如果比较的数组元素大于基准数，则交换位置。
            {
                swap(&buff[i], &buff[j]);  // 交换两个数
                j--;
            }
            else
            {
                i++;  // 将数组向后移一位，继续与基准数比较。
            }
        }

        /* 跳出while循环后，i = j。
         * 此时数组被分割成两个部分  -->  buff[begin+1] ~ buff[i-1] < buff[begin]
         *                           -->  buff[i+1] ~ buff[end] > buff[begin]
         * 这个时候将数组buff分成两个部分，再将buff[i]与buff[begin]进行比较，决定buff[i]的位置。
         * 最后将buff[i]与buff[begin]交换，进行两个分割部分的排序！以此类推，直到最后i = j不满足条件就退出！
         */
        if(buff[i] >= buff[begin])  // 这里必须要取等“>=”，否则数组元素由相同的值时，会出现错误！
        {
            i--;
        }
        swap(&buff[begin], &buff[i]);  // 交换buff[i]与buff[begin]
        audio_recorder_quicksort(buff, maxlen, begin, i);
        audio_recorder_quicksort(buff, maxlen, j, end);
    }
}
