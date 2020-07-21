/*
 * helix_mp3_decoder->c
 *
 *  
 *      Author: jiang
 */

#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "freertos/event_groups.h"
#include "freertos/ringbuf.h"
#include "py/runtime.h"

#include "audio_renderer.h"
#include "audio_player.h"
#include "helix_mp3_decoder.h"
#include "mp3common.h"
#include "mp3dec.h"
#include "coder.h"
#include "driver/i2s.h"

#define TAG "helix_decoder"
#include "mpconfigboard.h"

#define MAINBUF_SIZE1 2880 //2880 //1940
#define OUTP_SIZE (1152 * 4)
#define output MP_STATE_PORT(mp3DecOutBuf)
#define readBuf MP_STATE_PORT(mp3DecReadBuf)
extern TaskHandle_t http_client_task_handel;
extern EventGroupHandle_t xEventGroup;

typedef struct{
    HMP3Decoder HMP3Decoder;
    MP3FrameInfo mp3FrameInfo;
    int samplerate;
    int bytesleft;
}mp3_decode_t;

/* before use this function, need move the left bytes to the buff head, and the left bytes num. */
static int read_ringbuf(mp3_decode_t *decoder)
{
    int ringBufRemainBytes = 0;
    size_t len = 0;
    void *temp = NULL;
    int supply_bytes;
    player_t *player = get_player_handle();

    supply_bytes = MAINBUF_SIZE1 - decoder->bytesleft;
    ringBufRemainBytes = RINGBUF_SIZE - xRingbufferGetCurFreeSize(player->buf_handle); 

    /* 1 从ringbuf中读解码器需要的数据量 */
    if (ringBufRemainBytes > 0)
    {
        if(ringBufRemainBytes >= supply_bytes)  //ring buffer remain data enough for decoder need
        { 
            if(supply_bytes != 0){
                temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, supply_bytes);
            }
        }
        else{ 
            temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 50 / portTICK_PERIOD_MS, ringBufRemainBytes);     
        }  

        if(temp != NULL){
            memcpy(readBuf + decoder->bytesleft, temp, len);
            decoder->bytesleft += len;
            vRingbufferReturnItem(player->buf_handle, (void *)temp);
        }
    }
    // ESP_LOGE(TAG, "ringBufRemainBytes = %d, supply_bytes = %d, left bytes: %d", ringBufRemainBytes, supply_bytes, decoder->bytesleft);
    return decoder->bytesleft;
}

static int proccess_tag(mp3_decode_t *decoder)
{
    int tag_len;
    int ringBufRemainBytes = 0;
    size_t len;
    uint8_t *temp = NULL;
    player_t *player = get_player_handle();

    //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
    ringBufRemainBytes = RINGBUF_SIZE - xRingbufferGetCurFreeSize(player->buf_handle); //
    if(ringBufRemainBytes >= 10)
    {
        temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, 10);
        if(temp != NULL)
        {
            // ESP_LOGE(TAG, "mp3 TAG? : %x %x %x %x", temp[0], temp[1],temp[2],temp[3]);
            if (memcmp((char *)temp, "ID3", 3) == 0) //mp3? 有标签头，读取所有标签帧并去掉。
            { 
                //获取ID3V2标签头长，以确定MP3数据起始位置
                tag_len = ((temp[6] & 0x7F) << 21) | ((temp[7] & 0x7F) << 14) | ((temp[8] & 0x7F) << 7) | (temp[9] & 0x7F); 
                // ESP_LOGE(TAG, "tag_len: %d %x %x %x %x", tag_len, temp[6], temp[7], temp[8], temp[9]);
                vRingbufferReturnItem(player->buf_handle, (void *)temp);
                do
                {
                    ringBufRemainBytes = RINGBUF_SIZE - xRingbufferGetCurFreeSize(player->buf_handle);
                    if(tag_len <= ringBufRemainBytes) //ring buf中数据多于tag_len，把tag数据读完并退出
                    {
                        temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, tag_len);
                        if(temp != NULL)
                        {
                            vRingbufferReturnItem(player->buf_handle, (void *)temp);
                            return 0;
                        }
                    }
                    else 
                    {
                        temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, ringBufRemainBytes);
                        if(temp != NULL)
                        {
                            vRingbufferReturnItem(player->buf_handle, (void *)temp);
                            tag_len -= len;
                        }
                    }
                } while(tag_len > 0);
            } 
            else //无tag头 把前面读到的10字节加入解码buff
            {
                memcpy(readBuf, (char *)temp, len);
                decoder->bytesleft = len;
                vRingbufferReturnItem(player->buf_handle, (void *)temp);
            }      
        }
    }  
    return 0;
}

static void mp3_decode(mp3_decode_t *decoder)
{
    player_t *player = get_player_handle();
    int len;

    len = read_ringbuf(decoder);
    // ESP_LOGE(TAG, "ringbuf len %d", len);
    if(len == 0) //ringbuf has no data
    {
        renderer_zero_dma_buffer();
        vTaskDelay(5 / portTICK_PERIOD_MS);
        return;
    }

    int offset = MP3FindSyncWord(readBuf, decoder->bytesleft); //搜索缓存中第一个有效数据帧
    if (offset < 0)
    {
        // ESP_LOGE(TAG, "MP3FindSyncWord not find");
        decoder->bytesleft = 0; // All data not avalible, clear the buffer.
        return; 
    }
    if (offset >= 0) {
        if (offset > 0)
        {
            //去除头部无效数据
            decoder->bytesleft -= offset; 
            memmove(readBuf, readBuf + offset,  decoder->bytesleft);
            len = read_ringbuf(decoder);
            // ESP_LOGE(TAG, "ringbuf len 1 %d", len);
            if(len == 0) //ringbuf has no data
            {
                renderer_zero_dma_buffer();
                vTaskDelay(5 / portTICK_PERIOD_MS);
                return;
            }   
        }   
        // ESP_LOGE(TAG, "begin decode......");
        //以下解码n帧，readPtr会递增，bytesleft递减
        unsigned char *readPtr;
        readPtr = readBuf;
        int ret = MP3Decode(decoder->HMP3Decoder, &readPtr, &(decoder->bytesleft), (short *)output, 0);
        if (ret == ERR_MP3_NONE) 
        {
            // ESP_LOGE(TAG, "decode successed......");
            MP3GetLastFrameInfo(decoder->HMP3Decoder, &(decoder->mp3FrameInfo));
            if(decoder->samplerate != decoder->mp3FrameInfo.samprate)
            {
                decoder->samplerate = decoder->mp3FrameInfo.samprate;
                renderer_set_clk(decoder->samplerate, 16, decoder->mp3FrameInfo.nChans);
                // ESP_LOGE(TAG,"mp3file info---bitrate=%d, layer=%d, nChans=%d, samprate=%d, outputSamps=%d",
                //     decoder->mp3FrameInfo.bitrate, decoder->mp3FrameInfo.layer, decoder->mp3FrameInfo.nChans, 
                //     decoder->mp3FrameInfo.samprate, decoder->mp3FrameInfo.outputSamps);
            }
            #if MICROPY_BUILDIN_DAC //内置DAC需转正数，加上间量处理
            for (int i = 0; i < decoder->mp3FrameInfo.outputSamps; ++i)
            {
                // output[i] = (short)((output[i]*255.0/65535) * player->volume); //16位－> 8位，加上直流分量，消除负值，使值范围在0-255.
                // // output[i] = (short)((output[i]*255.0/65535)); //16位－> 8位，加上直流分量，消除负值，使值范围在0-255.
                // output[i] = output[i] << 8;
                output[i] = (short)((output[i] + 32768) * player->volume);
                output[i] &= 0xff00;
                //ESP_LOGI(TAG, "%d", output[i]);
            }
            #endif

            uint16_t bytesWritten;
            renderer_write((unsigned char *)output, decoder->mp3FrameInfo.outputSamps * 2, (size_t *)(&bytesWritten), 1000 / portTICK_RATE_MS);
            memmove(readBuf, readPtr, decoder->bytesleft);
        }
        else
        {
            // ESP_LOGE(TAG, "decode err: %d", ret);  
            renderer_zero_dma_buffer();
            if (ret == ERR_MP3_INDATA_UNDERFLOW) {
                //printf("ERR_MP3_INDATA_UNDERFLOW\n");
                decoder->bytesleft = 0; // All data not avalible, clear the buffer.
            } else if (ret == ERR_MP3_MAINDATA_UNDERFLOW) {
                /* do nothing - next call to decode will provide more mainData */
                //printf("ERR_MP3_MAINDATA_UNDERFLOW, continue to find sys words, left: %d\n", left);
                if (decoder->bytesleft > 0) {
                    memmove(readBuf, readPtr,  decoder->bytesleft);
                }
            } else {
                //printf("unknown error: %d, left: %d\n", ret, left);
                // skip this frame
                if (decoder->bytesleft > 0) {
                    readPtr++;
                    decoder->bytesleft--;
                    memmove(readBuf, readPtr,  decoder->bytesleft);
                }
            }
        }
    }  
}

void mp3_decoder_task(void *pvParameters)
{
    player_t *player = pvParameters;
    mp3_decode_t *decoder;

    decoder = calloc(1, sizeof(mp3_decode_t));
    if(decoder)
    {
        readBuf = (unsigned char *)m_new(char, MAINBUF_SIZE1); //(MAINBUF_SIZE1, sizeof(char));
        output = (short *)m_new(char, OUTP_SIZE);
        decoder->HMP3Decoder = MP3InitDecoder();
    }
    if(!decoder || !readBuf || !output || !decoder->HMP3Decoder)
    {
        mp_raise_ValueError(MP_ERROR_TEXT("No enought memory for decoder."));
    }

    decoder->bytesleft = 0;
    decoder->samplerate = 0;

    proccess_tag(decoder);
    // ESP_LOGE(TAG, "mp3 decode task has created, RAM left: %d", esp_get_free_heap_size());
    int decode_status = 0;
    while(1)
    {
        switch (player->player_status)
        {
        case RUNNING:
            mp3_decode(decoder);
            break;
        case STOPPED:
            decode_status = -1;
            break;
        case PAUSED:
            vTaskSuspend( NULL );
            break;
        default:
            break;
        }

        if(decode_status == -1)
        {
            if (decoder->bytesleft > 0) //正常结束，需把缓存剩余的数据解码完
              mp3_decode(decoder); 
            renderer_zero_dma_buffer();
            break;
        }
    } 

    if (readBuf){
        m_del(char, readBuf, MAINBUF_SIZE1);
    }
    if (output){
        m_del(char, output, OUTP_SIZE);
    }    
    MP3FreeDecoder(decoder->HMP3Decoder);
    if (decoder){
        free(decoder);
        decoder = NULL;
    } 
    xEventGroupSetBits(
            xEventGroup,    // The event group being updated.
            BIT_1);// The bits being set.
    // ESP_LOGE(TAG, "helix decoder stack: %d", uxTaskGetStackHighWaterMark(NULL));
    // ESP_LOGE(TAG, "10. mp3 decode task will delete, RAM left: %d", esp_get_free_heap_size()); 
    vTaskDelete(NULL);
}