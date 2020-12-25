/*
 * local_play.h
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#include <string.h>
#include <stdio.h>
#include "py/runtime.h"
#include "py/stream.h"
#include "py/reader.h"
#include "extmod/vfs.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
// #include "freertos/event_groups.h"
#include "freertos/ringbuf.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_task.h"
#include "nvs_flash.h"
#include "audio_player.h"
#include "helix_mp3_decoder.h"
#include "audio_renderer.h"
#include "driver/i2s.h"
#include "wave_head.h"

#include "local_play.h"
#include "mpconfigboard.h"

#define BODY_READ_LEN 64
#define READ_BUFF_LEN 2048
// static const char *TAG = "LOCAL_FILE";
extern TaskHandle_t mp3_decode_task_handel;


mp_obj_t file_open(const char *filename, const char *mode)
{
    mp_obj_t arg[2];
    
    arg[0] = mp_obj_new_str(filename, strlen(filename));
    arg[1] = mp_obj_new_str(mode, strlen(mode));

    return mp_vfs_open(2, arg, (mp_map_t*)&mp_const_empty_map);
}

void file_close(mp_obj_t File) {
    mp_stream_close(File);
}

int file_read(mp_obj_t File, int *read_bytes, uint8_t *buf, uint32_t len) 
{
    int errcode;

    *read_bytes = mp_stream_rw(File, buf, len, &errcode, MP_STREAM_RW_READ | MP_STREAM_RW_ONCE);
    if (errcode != 0) {
        // TODO handle errors properly
        file_close(File);
        return MP_READER_EOF;
    }
    if (*read_bytes < len) {
        file_close(File);
        return MP_READER_EOF;
    }

    return 0;
}

int file_write(mp_obj_t File, int *write_bytes, uint8_t *buf, uint32_t len)
{
    int errcode;

    *write_bytes = mp_stream_rw(File, buf, len, &errcode, MP_STREAM_RW_WRITE | MP_STREAM_RW_ONCE);
    if (errcode != 0) {
        // TODO handle errors properly
        file_close(File);
        return MP_READER_EOF;
    }
    if (*write_bytes < len) {
        file_close(File);
        return MP_READER_EOF;
    }

    return 0;    
}

static int data_read(mp_obj_t File, uint8_t *buffer)
{
    int read_len = 0, free_size, flag;
    player_t *player = get_player_handle();

    free_size = xRingbufferGetCurFreeSize(player->buf_handle); //get ringbuf free size
    if(free_size > 0){ 
        while(free_size >= BODY_READ_LEN)  // ring buffer中剩余空间大于BODY_READ_LEN 
        {
            flag = file_read(File, &read_len, buffer, BODY_READ_LEN);
            xRingbufferSend(player->buf_handle, (const void *)buffer, (size_t)read_len, 100/portTICK_PERIOD_MS);
            free_size -= read_len;
            if(flag == -1){  //文件结束
                // ESP_LOGE(TAG, "file read end 1.");
                return -1;
            }
        } 
        /* ring buffer中剩余空间小于BODY_READ_LEN */
        if(free_size > 0){ //继续读不够BODY_READ_LEN的字节,只在数据最后操作
            flag = file_read(File, &read_len, buffer, BODY_READ_LEN);
            xRingbufferSend(player->buf_handle, (const void *)buffer, (size_t)read_len, 100/portTICK_PERIOD_MS);  
            if(flag == -1){  //文件结束
                // ESP_LOGE(TAG, "file read end 2.");
                return -1;
            }
        }
        //ESP_LOGE(TAG, "Ringbuf is full! total_read_len = %d, content_length = %d", total_read_len, content_length);     
    }     
    return 0;
}

void local_play(void *pvParameters)
{
    mp_obj_t file = NULL;
    uint8_t *buffer = NULL;
    player_t *player = pvParameters;
   
    int read_bytes, flag;
    size_t write_bytes;
    uint8_t *read_buff = NULL;
    short *output = NULL; 

    /* config renderer. */
    renderer_config_t renderer_cfg;
    renderer_cfg.mode = I2S_MODE_TX; 
    renderer_cfg.use_apll = false; 

    file = file_open(player->url, "r");                                              

    if(player->content_type == AUDIO_MPEG){ 
        buffer = calloc(BODY_READ_LEN, sizeof(uint8_t));
        renderer_cfg.bit_depth  = 16;
        renderer_cfg.sample_rate = 22050;  
        renderer_cfg.i2s_channal_nums = 2; 
        renderer_cfg.channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT;
        renderer_init(&renderer_cfg);
        // ESP_LOGE(TAG, "3. ringbuf and renderer is create, RAM left: %d", esp_get_free_heap_size());

        if(data_read(file, buffer) == -1) //read mp3 data to ringbuff before mp3 decode task build
        {
            // ESP_LOGE(TAG, "Have no mp3 data.");
        }

        create_decode_task(player);
        // ESP_LOGE(TAG, "3. local mpeg file play rendderer has init, RAM left: %d", esp_get_free_heap_size());
    }
    else
    {
        read_buff = calloc(READ_BUFF_LEN, sizeof(uint8_t));
        output = calloc(READ_BUFF_LEN, sizeof(uint8_t));

        if( player->content_type == AUDIO_PCM)
        {
            renderer_cfg.bit_depth  = I2S_BITS_PER_SAMPLE_16BIT;
            renderer_cfg.sample_rate = 16000;
            renderer_init(&renderer_cfg);
            renderer_set_clk(16000,16, 1); //PCM 只处理16000 16 1 这种音频
        }else if(player->content_type == AUDIO_WAV){
            wav_info_t *wav_info = calloc(1, sizeof(wav_info_t));
            file_read(file, &read_bytes, read_buff,  36);
            wav_head_parser((const uint8_t *)read_buff, wav_info);
            // ESP_LOGE(TAG, "sampleRate: %d, bits: %d, channel: %d", wav_info->sampleRate, wav_info->bits, wav_info->channels);

            renderer_cfg.bit_depth  = wav_info->bits;
            renderer_cfg.sample_rate = wav_info->sampleRate;  
            renderer_cfg.i2s_channal_nums = wav_info->channels; 
            if (wav_info->channels == 2)
                renderer_cfg.channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT;
            else
                renderer_cfg.channel_format = I2S_CHANNEL_FMT_ONLY_RIGHT;
            
            renderer_init(&renderer_cfg);
            // renderer_set_clk(wav_info->sampleRate, wav_info->bits, wav_info->channels);
            if(wav_info->fmtSubchunckSize == 16)
                file_read(file, &read_bytes, read_buff,  8);
            else if(wav_info->fmtSubchunckSize == 18)
                file_read(file, &read_bytes, read_buff,  10);
            free(wav_info);
        }  
    }

    player_start();
    renderer_start();
    // ESP_LOGE(TAG, "9. Create renderer, RAM left: %d", esp_get_free_heap_size());
    while(1) 
    {     
        if(player->player_status == RUNNING)
        {
            if(player->content_type == AUDIO_MPEG)
            {
                if(data_read(file, buffer) == -1){  //往ringbuf填数据， -1 文件结束
                    player->eof = true;
                    // ESP_LOGE(TAG, "File read end.");
                    player->player_status = END;
                }
            }
            else if((player->content_type == AUDIO_PCM) || (player->content_type == AUDIO_WAV))
            {
                flag = file_read(file, &read_bytes, read_buff, READ_BUFF_LEN);
                memcpy((uint8_t *)output, read_buff, read_bytes);
                #if MICROPY_BUILDIN_DAC //使用内建DAC，要把数据转为正数，音量调节只能用软件方法
                for (int i = 0; i < read_bytes/2; i++)
                {
                    // output[i] = (short)((output[i]*255.0/65535) * player->volume); //16位－> 8位，加上直流分量，消除负值，使值范围在0-255.
                    // output[i] = output[i] << 8;
                    // // output[i] = ((output[i] >> 8) + 128) * player->volume;
                    // // printf("%d", output[i]);
                    output[i] = (short)((output[i] + 32768) * player->volume);  //内置DAC需处理正数
                    output[i] &= 0xff00; //只处理高8位
                }
                #endif 

                renderer_write(output, read_bytes, &write_bytes, 1000 / portTICK_RATE_MS); //portMAX_DELAY
                if(flag == -1)
                {
                    vTaskDelay(200 / portTICK_PERIOD_MS); 
                    renderer_zero_dma_buffer();
                    renderer_stop();
                    player->eof = true;
                    player->player_status = STOPPED;
                    break;
                }
                //vTaskDelay(10);
            }
        }

        if((player->player_status == STOPPED) || (player->player_status == END)){
            // ESP_LOGE(TAG, "Recieved stop command, break.");
            break;
        }
        vTaskDelay(20 / portTICK_PERIOD_MS);
    }

    if(read_buff)
        free(read_buff);
    if(output)
        free(output);
    if(buffer)
        free(buffer);
    // renderer_deinit();

    // ESP_LOGE(TAG, "local play end, RAM left: %d", esp_get_free_heap_size());
    vTaskDelay(1 / portTICK_PERIOD_MS); 
}

