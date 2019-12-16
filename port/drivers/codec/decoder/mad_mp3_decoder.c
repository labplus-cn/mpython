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
#include "mad_mp3_decoder.h"
#include "mad.h"
#include "decoder.h"
#include "driver/i2s.h"

#define TAG "mad_decoder"

#define MAINBUF_SIZE1 2880 //2880 //1940
extern TaskHandle_t http_client_task_handel;

static enum  mad_flow input(struct mad_stream *stream)
{
    int ringBufRemainBytes = 0;
    size_t len;
    void *temp = NULL;
    player_t *player = get_player_handle();
	uint16_t remain_bytes, supply_bytes;
	
	remain_bytes = stream->bufend - stream->next_frame;
    // supply_bytes = MAINBUF_SIZE1 - remain_bytes;

    // ringBufRemainBytes = RINGBUF_SIZE - xRingbufferGetCurFreeSize(player->buf_handle); 

    // // ESP_LOGE(TAG, "ringBufRemainBytes = %d, supply_bytes = %d", ringBufRemainBytes, supply_bytes);
    // /* 1 从ringbuf中读解码器需要的数据量 */
    // if (ringBufRemainBytes > 0)
    // {
    //     if(ringBufRemainBytes >= supply_bytes)  //ring buffer remain data enough for decoder need
    //     { 
    //         if(supply_bytes != 0){
    //             temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, supply_bytes);
    //         }
    //     }
    //     else{ 
    //         temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 50 / portTICK_PERIOD_MS, ringBufRemainBytes);     
    //     }  
        
    //     /* 2 把ringbuf中读到的数据移到解码缓存 */
    //     memmove(decoder->readBuf, stream->next_frame, remain_bytes); //数据移动缓存头部，补充进来的数据接到后面

    //     if(temp != NULL){
    //         memcpy(&(decoder->readBuf[remain_bytes]), temp, len);
    //         vRingbufferReturnItem(player->buf_handle, (void *)temp);
    //         mad_stream_buffer(stream, (unsigned char*)decoder->readBuf, len + remain_bytes);
    //         return MAD_FLOW_CONTINUE;
    //     }
    // }
        
    return MAD_FLOW_STOP; //ringbuff无数据
}

//Routine to print out an error
static enum mad_flow error(void *data, struct mad_stream *stream, struct mad_frame *frame) {
    printf("dec err 0x%04x (%s)\n", stream->error, mad_stream_errorstr(stream));
    return MAD_FLOW_CONTINUE;
}

/*
static int proccess_tag()
{
    int tag_len;
    int ringBufRemainBytes = 0;
    size_t len;
    uint8_t *temp = NULL;
    player_t *player = get_player_handle();

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
            // else //无tag头 把前面读到的10字节加入解码buff
            // {
            //     memcpy(decoder->readPtr, (char *)temp, 10);
            //     decoder->bytesleft += len;
            //     vRingbufferReturnItem(player->buf_handle, (void *)temp);
            //     decoder->supply_bytes = MAINBUF_SIZE1 - 10;
            // }      
        }
    }  
    return 0;
} */

void mp3_decoder_task(void *pvParameters)
{
    player_t *player = pvParameters;
    int state;

    ESP_LOGE(TAG, "Enter mp3 decode task.");
    struct mad_decoder *decoder =  (struct mad_decoder *)m_new_obj(struct mad_decoder);
    if(decoder)
    {
        decoder->sync = (struct _sync *)m_new_obj(struct _sync);
        if(decoder->sync)
        {
            decoder->sync->stream = (struct mad_stream *)m_new_obj(struct mad_stream);
            decoder->sync->frame = (struct mad_frame *)m_new_obj(struct mad_frame);
            decoder->sync->synth = (struct mad_synth *)m_new_obj(struct mad_synth);
            if(decoder->sync->stream)
                decoder->sync->stream->main_data = (void *)m_new(unsigned char, MAD_BUFFER_MDLEN);
            if(decoder->sync->synth)
            {
                decoder->sync->synth->filter = (void *)m_new(mad_fixed_t, 2 * 36 * 32);
                decoder->sync->synth->pcm = (struct mad_pcm *)m_new_obj(struct mad_pcm);
                if(decoder->sync->synth->pcm)
                {
                    decoder->sync->synth->pcm->samples = (void *)m_new(mad_fixed_t, 2 * 1152);
                }
            }
            if(decoder->sync->frame)
            {
                decoder->sync->frame->sbsample = (void *)m_new(mad_fixed_t, 2 * 36 * 32);
                decoder->sync->frame->overlap = (void *)m_new(mad_fixed_t, 2 * 32 * 18);
            }
        }
    }
 
    if (!decoder || !decoder->sync || !decoder->sync->stream || !decoder->sync->frame || decoder->sync->synth 
        || !decoder->sync->stream->main_data || !decoder->sync->synth->filter || !decoder->sync->synth->pcm 
        || !decoder->sync->synth->pcm->samples || !decoder->sync->frame->sbsample || !decoder->sync->frame->overlap ) 
    { 
        ESP_LOGE(TAG, "MAD: malloc(stream) failed, mad_fixed_t size: %d\n", sizeof(mad_fixed_t));
        return; 
    }

    // proccess_tag(decoder);
    ESP_LOGE(TAG, "mp3 decode task has create 1........, RAM left: %d", esp_get_free_heap_size());
    int decode_status = 0;
    while(1)
    {
        switch (player->player_status)
        {
        case RUNNING:
            // // calls mad_stream_buffer internally
            // if (input(stream) == MAD_FLOW_STOP ) {
            //     renderer_zero_dma_buffer();
            //     vTaskDelay(5 / portTICK_PERIOD_MS);
            //     break;
            // }

            // // decode frames until MAD complains
            // while(1) {
            //     // returns 0 or -1
            //     ret = mad_frame_decode(frame, stream);
            //     if (ret == -1) {
            //         if (!MAD_RECOVERABLE(stream->error)) //decoder buffer has no datas, need supply.
            //             break;
            //         error(NULL, stream, frame);  //print error.
            //         continue;
            //     }
            //     mad_synth_frame(synth, frame); //output decoder datas, we can write data to i2s in this fumtion.
            // }
            // // ESP_LOGI(TAG, "RAM left %d", esp_get_free_heap_size());
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
    } 

    ESP_LOGE(TAG, "helix decoder stack: %d\n", uxTaskGetStackHighWaterMark(NULL));
    ESP_LOGE(TAG, "10. mp3 decode task will delete, RAM left: %d", esp_get_free_heap_size()); 
    vTaskDelete(NULL);
}