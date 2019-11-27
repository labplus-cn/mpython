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
// #include "freertos/event_groups.h"
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

#define MAINBUF_SIZE1 2880 //2880 //1940
extern TaskHandle_t http_client_task_handel;

typedef struct{
    HMP3Decoder HMP3Decoder;
    MP3FrameInfo mp3FrameInfo;
    int samplerate;
    short *output;
    unsigned char *readBuf;
    int supply_bytes;
    int bytesleft;
    unsigned char *readPtr;
}mp3_decode_t;

static int read_ringbuf(mp3_decode_t *decoder)
{
    int ringBufRemainBytes = 0;
    size_t len;
    void *temp = NULL;
    player_t *player = get_player_handle();

    //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
    ringBufRemainBytes = RINGBUF_SIZE - xRingbufferGetCurFreeSize(player->buf_handle); //
    //xSemaphoreGive(player->ringbuf_sem);

    // ESP_LOGE(TAG, "ringBufRemainBytes = %d, supply_bytes = %d", ringBufRemainBytes, Supply_bytes);
    if(ringBufRemainBytes >= decoder->supply_bytes)  //ring buffer remain data enough for decoder need
    { 
        if(decoder->supply_bytes != 0){
            //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
            temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, decoder->supply_bytes);
            //xSemaphoreGive(player->ringbuf_sem);
        }
    }
    else{ 
        if(player->media_stream.eof){ //Stream end
            if(ringBufRemainBytes != 0){
                //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
                temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 50 / portTICK_PERIOD_MS, ringBufRemainBytes);
                //xSemaphoreGive(player->ringbuf_sem);
            }       
        }  
        else{ 
            renderer_zero_dma_buffer();
            return -1; //ring buffer中数据不够解码器请求，退出等数据补够
        }
    }  

    if (decoder->bytesleft > 0)  //解码缓存中还有数据没处理完，把它移到缓存头部
    {
        memmove(decoder->readBuf, decoder->readPtr, decoder->bytesleft); //数据移动缓存头部，补充进来的数据接到后面
        decoder->readPtr = decoder->readBuf + decoder->bytesleft;
    }

    if(temp != NULL){
        memcpy(decoder->readPtr, temp, len);
        decoder->bytesleft += len;
        //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
        vRingbufferReturnItem(player->buf_handle, (void *)temp);
        //xSemaphoreGive(player->ringbuf_sem);
    }

    if(ringBufRemainBytes == 0){ //结束的时机选这，保证所有数据可被解码
        return 1;
    }
    return 0;
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
                memcpy(decoder->readPtr, (char *)temp, 10);
                decoder->bytesleft += len;
                vRingbufferReturnItem(player->buf_handle, (void *)temp);
                decoder->supply_bytes = MAINBUF_SIZE1 - 10;
            }      
        }
    }  
    return 0;
}

static void mp3_decode(mp3_decode_t *decoder)
{
    renderer_config_t *renderer = renderer_get();
    player_t *player = get_player_handle();

    int offset = MP3FindSyncWord(decoder->readBuf, decoder->bytesleft); //搜索缓存中第一个有效数据帧
    //ESP_LOGE(TAG, "offset is %d ", offset);
    if (offset < 0)
    {
        //ESP_LOGE(TAG, "MP3FindSyncWord not find");
        decoder->bytesleft = 0; // All data not avalible, clear the buffer.
        decoder->supply_bytes = MAINBUF_SIZE1;
        decoder->readPtr = decoder->readBuf;
        return; 
    }
    else
    {
        decoder->readPtr = decoder->readBuf + offset;   //此位置读到有效数据帧
        decoder->bytesleft -= offset; 
        //ESP_LOGE(TAG, "begin decode......");
        //以下解码n帧，readPtr会递增，bytesleft递减
        int errs = MP3Decode(decoder->HMP3Decoder, &(decoder->readPtr), &(decoder->bytesleft), (short *)decoder->output, 0);
        decoder->supply_bytes = decoder->readPtr - decoder->readBuf; //需要补充的数据量
        if (errs != 0)
        {
            renderer_zero_dma_buffer();
            if(decoder->supply_bytes == 0){
                decoder->bytesleft -= 10;
                decoder->readPtr += 10;
                if(decoder->bytesleft <= 0)
                {
                    decoder->bytesleft = 0;
                    decoder->readPtr = decoder->readBuf;
                }
            }

            //ESP_LOGE(TAG, "MP3Decode failed ,code is %d ", errs);
            return;
        }
        //ESP_LOGE(TAG, "decode successed......");
        MP3GetLastFrameInfo(decoder->HMP3Decoder, &(decoder->mp3FrameInfo));
        if(decoder->samplerate != decoder->mp3FrameInfo.samprate)
        {
            decoder->samplerate = decoder->mp3FrameInfo.samprate;
            i2s_set_clk(renderer->i2s_num, decoder->samplerate, 16, decoder->mp3FrameInfo.nChans);
            // ESP_LOGE(TAG,"mp3file info---bitrate=%d, layer=%d, nChans=%d, samprate=%d, outputSamps=%d",
            //     decoder->mp3FrameInfo.bitrate, decoder->mp3FrameInfo.layer, decoder->mp3FrameInfo.nChans, 
            //     decoder->mp3FrameInfo.samprate, decoder->mp3FrameInfo.outputSamps);
        }
        for (int i = 0; i < decoder->mp3FrameInfo.outputSamps; ++i)
        {
            // decoder->output[i] = (short)((decoder->output[i]*255.0/65535) * player->volume); //16位－> 8位，加上直流分量，消除负值，使值范围在0-255.
            // // decoder->output[i] = (short)((decoder->output[i]*255.0/65535)); //16位－> 8位，加上直流分量，消除负值，使值范围在0-255.
            // decoder->output[i] = decoder->output[i] << 8;
            decoder->output[i] = (short)((decoder->output[i] + 32768) * player->volume);
            decoder->output[i] &= 0xff00;
            //ESP_LOGI(TAG, "%d", output[i]);
        }

        uint16_t bytesWritten;
        i2s_write(renderer->i2s_num, (unsigned char *)decoder->output, decoder->mp3FrameInfo.outputSamps * 2, (size_t *)(&bytesWritten), 1000 / portTICK_RATE_MS);
    }     
}

void mp3_decoder_task(void *pvParameters)
{
    player_t *player = pvParameters;
    mp3_decode_t *decoder;
    int state;

    // ESP_LOGE(TAG, "Enter mp3 decode task.");
    decoder = calloc(1, sizeof(mp3_decode_t));
    if(decoder == NULL)
        goto abort;
    decoder->readBuf = malloc(MAINBUF_SIZE1);
    if (decoder->readBuf == NULL){
        // ESP_LOGE(TAG, "readBuf malloc failed");
        goto abort;
    }
    decoder->output = malloc(1153 * 4);
    if (decoder->output == NULL){
        free(decoder->readBuf);
        // ESP_LOGE(TAG, "OutBuf malloc failed");
		goto abort;
    }
    decoder->HMP3Decoder = MP3InitDecoder();
    if (decoder->HMP3Decoder == 0)
    {
        free(decoder->readBuf);
        free(decoder->output);
        mp_raise_ValueError("Memory not enough for mp3 decode");
        // ESP_LOGE(TAG, "Memory not enough for mp3 decode.");
		goto abort;
    }

    decoder->supply_bytes = MAINBUF_SIZE1;
    decoder->bytesleft = 0;
    decoder->readPtr = decoder->readBuf;
    decoder->samplerate = 0;

    proccess_tag(decoder);
    while(1)
    {
        state = read_ringbuf(decoder);
        if(state == -1){ //ringbuf remain bytes < decode need bytes
            vTaskDelay(1 / portTICK_PERIOD_MS);
            continue;
        }

        mp3_decode(decoder);
        
        if((player->player_status == STOPPED) || ((player->media_stream.eof) && (state == 1) && (decoder->bytesleft == 0)))
            break;
        else if(player->player_status == PAUSED){
            vTaskSuspend( NULL );
        }
    } 

    //vTaskDelay(10 / portTICK_PERIOD_MS);
    free(decoder->readBuf);
    free(decoder->output);
    MP3FreeDecoder(decoder->HMP3Decoder);
    free(decoder);

    abort:
    renderer_zero_dma_buffer();
    renderer_stop();
    if(player->file_type == WEB_TYPE)
    {
        if(http_client_task_handel != NULL){
            player->player_status = INITIALIZED;
            vTaskDelete(http_client_task_handel);
            http_client_task_handel = NULL;
            // ESP_LOGE(TAG, "play status: %d", player->player_status); 
        }
    }
    else if ( player->file_type == LOCAL_TYPE) {
        player->player_status = INITIALIZED;
    }
    
    // ESP_LOGE(TAG, "helix decoder stack: %d\n", uxTaskGetStackHighWaterMark(NULL));
    // ESP_LOGE(TAG, "6. mp3 decode task will delete, RAM left: %d", esp_get_free_heap_size()); 
    vTaskDelete(NULL);
}