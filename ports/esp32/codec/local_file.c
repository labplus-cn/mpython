/*
 * local_file.h
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
#include "wav_head.h"

#include "local_file.h"

#define BODY_READ_LEN 64
#define READ_BUFF_LEN 2048
static const char *TAG = "LOCAL_FILE";
static int err;
// extern int player_status;

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

int file_read(mp_obj_t File, int *read_bytes, uint8_t *buf, uint16_t len) 
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

int file_write(mp_obj_t File, int *write_bytes, uint8_t *buf, uint16_t len)
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

    //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
    free_size = xRingbufferGetCurFreeSize(player->buf_handle); //get ringbuf free size
    // xSemaphoreGive(player->ringbuf_sem); 
    // ESP_LOGE(TAG, "file read task 1..");
    if(free_size > 0){ 
        while(free_size >= BODY_READ_LEN)  // ring buffer中剩余空间大于BODY_READ_LEN 
        {
            flag = file_read(File, &read_len, buffer, BODY_READ_LEN);
            //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
            xRingbufferSend(player->buf_handle, (const void *)buffer, (size_t)read_len, 100/portTICK_PERIOD_MS);
            // xSemaphoreGive(player->ringbuf_sem); 
            free_size -= read_len;
            // ESP_LOGE(TAG, "free_size = %d", free_size);
            if(flag == -1){  //文件结束
                // ESP_LOGE(TAG, "file read end 1.");
                return -1;
            }
        } 
        /* ring buffer中剩余空间小于BODY_READ_LEN */
        if(free_size > 0){ //继续读不够BODY_READ_LEN的字节,只在数据最后操作
            flag = file_read(File, &read_len, buffer, BODY_READ_LEN);
            //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
            xRingbufferSend(player->buf_handle, (const void *)buffer, (size_t)read_len, 100/portTICK_PERIOD_MS);  
            // xSemaphoreGive(player->ringbuf_sem); 
            if(flag == -1){  //文件结束
                // ESP_LOGE(TAG, "file read end 2.");
                return -1;
            }
        }
        //ESP_LOGE(TAG, "Ringbuf is full! total_read_len = %d, content_length = %d", total_read_len, content_length);     
    }     
    return 0;
}

static  int proccess_tag(mp_obj_t File, uint8_t *buffer)
{
    int read_len, tag_len, flag;
    player_t *player = get_player_handle();

    //处理ID3V2标签头
    flag = file_read(File, &tag_len, buffer, 10);
    if(flag == -1){
        return -1;
    }
    // ESP_LOGE(TAG, "mp3 TAG? : %x %x %x %x", buffer[0], buffer[1],buffer[2],buffer[3]);
    
    if (memcmp((char *)buffer, "ID3", 3) == 0) //mp3? 有标签头，读取所有标签帧并去掉。
    { 
        //获取ID3V2标签头长，以确定MP3数据起始位置
        tag_len = ((buffer[6] & 0x7F) << 21) | ((buffer[7] & 0x7F) << 14) | ((buffer[8] & 0x7F) << 7) | (buffer[9] & 0x7F); 
        // ESP_LOGE(TAG, "tag_len: %d %x %x %x %x", tag_len, buffer[6], buffer[7], buffer[8], buffer[9]);
        while(tag_len >= BODY_READ_LEN)
        {
            flag = file_read(File, &read_len, buffer, BODY_READ_LEN);
            tag_len -= read_len;
        } 
        if(tag_len > 0){
           flag = file_read(File, &read_len, buffer, tag_len);
           if(flag == -1) return -1;
        } 
        // file_read(buffer, 10, &read_len);  //test first frame data head
        // ESP_LOGE(TAG, "audio first frame head: %x %x %x %x", buffer[0], buffer[1],buffer[2],buffer[3]);
    }
    else //无tag头 把前面读到的10字节加入ringbuf
    {
        // ESP_LOGE(TAG, "No mp3 tag."); 
        //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
        xRingbufferSend(player->buf_handle, (const void *)buffer, (size_t)tag_len, 200/portTICK_PERIOD_MS);
        //xSemaphoreGive(player->ringbuf_sem);
    } 

    return 0; 
}

void local_file_read(void *pvParameters)
{
    mp_obj_t file;
    uint8_t buffer[BODY_READ_LEN];
    err = 0;
    player_t *player = pvParameters;

    if((strstr(player->url, ".mp3") != NULL)){
        player->media_stream.content_type = AUDIO_MPEG;
    }else if((strstr(player->url, ".pcm") != NULL)){
        player->media_stream.content_type = AUDIO_PCM;
    }else if((strstr(player->url, ".wav") != NULL)){
        player->media_stream.content_type = AUDIO_WAV;
        // ESP_LOGE(TAG, "wav file");
    }else if((strstr(player->url, ".m4a") != NULL)){
        player->media_stream.content_type = AUDIO_MP4;
    }else if((strstr(player->url, ".aac") != NULL)){
        player->media_stream.content_type = AUDIO_AAC;
    }
    else{
        // ESP_LOGE(TAG, "Not music file!.");
        err = -1;
        goto abort;
    }

    file = file_open(player->url, "r");
    if(player->media_stream.content_type == AUDIO_MPEG){
        if(data_read(file, buffer) == -1) //read mp3 data to ringbuff before mp3 decode task build
        {
            // ESP_LOGE(TAG, "Have no mp3 data.");
            err = -1;
            goto abort;
        }
    }

    audio_player_start();
    renderer_config_t *renderer = renderer_get();
    int read_bytes, flag;
    size_t write_bytes;
    uint8_t *read_buff = calloc(READ_BUFF_LEN, sizeof(uint8_t));
    short *output = calloc(READ_BUFF_LEN, sizeof(uint8_t)); 
  
    if(player->media_stream.content_type == AUDIO_MPEG){
        create_decode_task(player);
    }else if( player->media_stream.content_type == AUDIO_PCM)
    {
        i2s_set_clk(renderer->i2s_num, 16000,16, 1);
    }else if(player->media_stream.content_type == AUDIO_WAV){
        wav_info_t *wav_info = calloc(1, sizeof(wav_info_t));
        file_read(file, &read_bytes, read_buff,  36);
        wav_head_parser((const uint8_t *)read_buff, wav_info);
        // ESP_LOGE(TAG, "sampleRate: %d, bits: %d, channel: %d", wav_info->sampleRate, wav_info->bits, wav_info->channels);
        i2s_set_clk(renderer->i2s_num, wav_info->sampleRate, wav_info->bits, wav_info->channels);
        if(wav_info->fmtSubchunckSize == 16)
            file_read(file, &read_bytes, read_buff,  8);
        else if(wav_info->fmtSubchunckSize == 18)
            file_read(file, &read_bytes, read_buff,  10);
        free(wav_info);
    }
    while(1) 
    {     
        if(player->player_status == RUNNING)
        {
            if(player->media_stream.content_type == AUDIO_MPEG)
            {
                if(data_read(file, buffer) == -1){  //往ringbuf填数据
                    player->media_stream.eof = true;
                    // ESP_LOGE(TAG, "File read end.");
                    break;
                }
            }
            else if((player->media_stream.content_type == AUDIO_PCM) || (player->media_stream.content_type == AUDIO_WAV))
            {
                flag = file_read(file, &read_bytes, read_buff, READ_BUFF_LEN);
                memcpy((uint8_t *)output, read_buff, read_bytes);
                for (int i = 0; i < read_bytes/2; i++)
                {
                    // output[i] = (short)((output[i]*255.0/65535) * player->volume); //16位－> 8位，加上直流分量，消除负值，使值范围在0-255.
                    // output[i] = output[i] << 8;
                    // // output[i] = ((output[i] >> 8) + 128) * player->volume;
                    // // printf("%d", output[i]);
                    output[i] = (short)((output[i] + 32768) * player->volume);
                    output[i] &= 0xff00;
                }
                i2s_write(renderer->i2s_num, output, read_bytes, &write_bytes, 1000 / portTICK_RATE_MS); //portMAX_DELAY
                if(flag == -1)
                {
                    renderer_zero_dma_buffer();
                    renderer_stop();
                    player->media_stream.eof = true;
                    player->player_status = INITIALIZED;
                    break;
                }
                //vTaskDelay(10);
            }
        }

        if(player->player_status == STOPPED){
            // ESP_LOGE(TAG, "Recieved stop command, break.");
            break;
        }
        vTaskDelay(20 / portTICK_PERIOD_MS);
    }

    free(read_buff);
    free(output);
    abort:
    if(err == -1)
    {
        player->player_status = INITIALIZED;
    }
    // ESP_LOGE(TAG, "mp task stack: %d\n", uxTaskGetStackHighWaterMark(NULL));
    // ESP_LOGE(TAG, "5. local file read task will delete, RAM left: %d", esp_get_free_heap_size());
    vTaskDelay(1 / portTICK_PERIOD_MS); 
}

void local_file_read_task(void *pvParameters)
{  
    uint8_t buffer[BODY_READ_LEN];
    player_t *player = pvParameters;
    mp_obj_t file;

    if((strstr(player->url, ".mp3") != NULL)){
        player->media_stream.content_type = AUDIO_MPEG;
    }else if((strstr(player->url, ".wav") != NULL)){
        player->media_stream.content_type = OCTET_STREAM;
    }else if((strstr(player->url, ".m4a") != NULL)){
        player->media_stream.content_type = AUDIO_MP4;
    }else if((strstr(player->url, ".aac") != NULL)){
        player->media_stream.content_type = AUDIO_AAC;
    }
    else{
        ESP_LOGE(TAG, "Not music file!.");
        goto abort;
    }

    file = file_open(player->url, "r");

    if(proccess_tag(file, buffer) == -1){
        goto abort;
    }  

    data_read(file, buffer);
    audio_player_start();
    create_decode_task(player);
    // ESP_LOGE(TAG, "3.3. local file read task run, RAM left: %d", esp_get_free_heap_size()); 
    
    while(1) 
    {     
        if(player->player_status == RUNNING)
        {
            if(data_read(file, buffer) == -1){  //往ringbuf填数据
                player->media_stream.eof = true;
                // ESP_LOGE(TAG, "File read end.");
                break;
            }
        }

        if(player->player_status == STOPPED){
            // ESP_LOGE(TAG, "Recieved stop command, break.");
            break;
        }
        vTaskDelay(50 / portTICK_PERIOD_MS);
    }

    abort:
    // ESP_LOGE(TAG, "5. local file read task will delete, RAM left: %d", esp_get_free_heap_size());
    vTaskDelete(NULL);    
}




