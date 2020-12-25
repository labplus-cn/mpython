/*
 * http_client.c
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */


#include <string.h>
#include <stdlib.h>
#include "py/runtime.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "freertos/event_groups.h"
#include "freertos/ringbuf.h"
#include "esp_log.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "audio_player.h"
#include "helix_mp3_decoder.h"

#include "esp_http_client.h"
#include "http_client.h"
#include "audio_recorder.h"
#include "local_play.h"
#include "wave_head.h"
#include "driver/i2s.h"
#include "audio_renderer.h"

#define BODY_READ_LEN 64

static const char *TAG = "HTTP_CLIENT";

HTTP_HEAD_VAL http_head[6] = {
    {"X-CurTime", NULL},
    {"X-Param", NULL},
    {"X-Appid",  NULL},
    {"X-CheckSum", NULL},
    {"X-Real-Ip", "127.0.0.1"},
    {"Content-Type", "application/x-www-form-urlencoded; charset=utf-8"}
};
// static const char *api_key;
esp_http_client_handle_t client = NULL;
extern TaskHandle_t mp3_decode_task_handel;
static http_param_t *http_param_instance = NULL;
extern EventGroupHandle_t xEventGroup;

static void http_param_init()
{
    if (!http_param_instance)
    {
        http_param_instance = calloc(1, sizeof(http_param_t));
        if (!http_param_instance)
            mp_raise_ValueError(MP_ERROR_TEXT("Can not calloc http_param."));
    }
 
    http_param_instance->http_head = NULL;                    
    http_param_instance->http_body = NULL;  
    http_param_instance->http_body_len = 0;
    http_param_instance->http_method = HTTP_METHOD_GET; 
}

static int process_wav_tag()
{
    uint8_t *temp = NULL;
    size_t len;
    int ringBufRemainBytes = 0;
    player_t *player = get_player_handle();
    wav_info_t *wav_info = calloc(1, sizeof(wav_info_t));

    ringBufRemainBytes = RINGBUF_SIZE - xRingbufferGetCurFreeSize(player->buf_handle); //
    if(ringBufRemainBytes >= 36)
    {
        temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, 36);
        if(temp != NULL)
        {
            // ESP_LOGE(TAG, "wav file? : %x %x %x %x", temp[0], temp[1],temp[2],temp[3]);
            if (strstr((char *)temp, "WAVE") != NULL) //WAV file。
            { 
                wav_head_parser((const uint8_t *)temp, wav_info);
                vRingbufferReturnItem(player->buf_handle, (void *)temp);
                // ESP_LOGE(TAG, "sampleRate: %d, bits: %d, channel: %d", wav_info->sampleRate, wav_info->bits, wav_info->channels);
                renderer_set_clk(wav_info->sampleRate, wav_info->bits, wav_info->channels);
                if(wav_info->fmtSubchunckSize == 16)
                    temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, 8);
                else 
                    temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, 10);

                free(wav_info);
                vRingbufferReturnItem(player->buf_handle, (void *)temp);

                return 0; 
            }     
        }
    }

    free(wav_info);
    return -1;
}

static esp_err_t _http_event_handler(esp_http_client_event_t *evt)
{
    // player_t *player = get_player_handle();

    switch(evt->event_id) {
        case HTTP_EVENT_ERROR:
            ESP_LOGD(TAG, "HTTP_EVENT_ERROR");
            break;
        case HTTP_EVENT_ON_CONNECTED:
            ESP_LOGD(TAG, "HTTP_EVENT_ON_CONNECTED");
            break;
        case HTTP_EVENT_HEADER_SENT:
            ESP_LOGD(TAG, "HTTP_EVENT_HEADER_SENT");
            break;
        case HTTP_EVENT_ON_HEADER:
            //ESP_LOGE(TAG, "HTTP_EVENT_ON_HEADER, key=%s, value=%s", evt->header_key, evt->header_value);
            if(strcmp(evt->header_key, "Content-Type") == 0) 
            {
                // ESP_LOGE(TAG, "HTTP_EVENT_ON_HEADER, key=%s, value=%s", evt->header_key, evt->header_value);
                if (strcmp(evt->header_value, "application/octet-stream") == 0) http_param_instance->content_type = AUDIO_WAV;
                else if (strcmp(evt->header_value, "audio/aac") == 0) http_param_instance->content_type = AUDIO_AAC;
                else if (strcmp(evt->header_value, "audio/mp4") == 0) http_param_instance->content_type = AUDIO_MP4;
                else if (strcmp(evt->header_value, "audio/x-m4a") == 0) http_param_instance->content_type = AUDIO_MP4;
                else if (strcmp(evt->header_value, "audio/mpeg") == 0) http_param_instance->content_type = AUDIO_MPEG;
                else if (strcmp(evt->header_value, "text/plain") == 0) http_param_instance->content_type = AUDIO_TEXT;
                else http_param_instance->content_type = MIME_UNKNOWN;
                // ESP_LOGE(TAG, "media type: %x", http_param_instance->content_type);
            }
            break;
        case HTTP_EVENT_ON_DATA:
            ESP_LOGD(TAG, "HTTP_EVENT_ON_DATA, len=%d", evt->data_len);
            if (!esp_http_client_is_chunked_response(evt->client)) {
                // Write out data
                // printf("%.*s", evt->data_len, (char*)evt->data);
            }

            break;
        case HTTP_EVENT_ON_FINISH:
            ESP_LOGD(TAG, "HTTP_EVENT_ON_FINISH");
            break;
        case HTTP_EVENT_DISCONNECTED:
            ESP_LOGD(TAG, "HTTP_EVENT_DISCONNECTED");
            break;
    }
    return ESP_OK;
}

static int http_request()
{
    esp_err_t err;
    player_t *player = get_player_handle();

    /* 如果有head数据 */
    if(http_param_instance->http_head != NULL){
        for(int i = 0; i < 6; i++)
            esp_http_client_set_header(client, http_param_instance->http_head[i].key, http_param_instance->http_head[i].value);
        // free((char *)http_head[3].value);
        // free((char *)http_head[0].value);
        // free((char *)http_head[1].value);
    }

    if ((err = esp_http_client_open(client, http_param_instance->http_body_len)) != ESP_OK) {
        // ESP_LOGE(TAG, "Failed to open HTTP connection");
        return -1;
    }

    /* 如果有body数据，测发送 */
    if(http_param_instance->http_body != NULL && http_param_instance->http_body_len > 0){
        esp_http_client_write(client, http_param_instance->http_body, http_param_instance->http_body_len);
        free(http_param_instance->http_body); 
    }

    http_param_instance->content_size =  esp_http_client_fetch_headers(client); //获得respone 数据长度
    if(http_param_instance->content_size <= 0){
        player->eof = true;
        // ESP_LOGE(TAG, "Failed to get content. http_param_instance->content_size = %d", http_param_instance->content_size);
        return -1;
    }

    // ESP_LOGE(TAG, "mp3 content len : %d", http_param_instance->content_size);
    return 0;
}

/* 从http body读数据，直到把ring bufffer填满 */
static int http_get_data()
{
    int read_len, free_size;
    int timeoutCnt = 0;
    uint8_t buffer[BODY_READ_LEN];
    player_t *player = get_player_handle();

    free_size = xRingbufferGetCurFreeSize(player->buf_handle); //get ringbuf free size
    if(free_size > 0){ 
        while((free_size >= BODY_READ_LEN) && (http_param_instance->has_read_size < http_param_instance->content_size)) //ringbuf有空闲且数据未获取完
        {
            if((http_param_instance->has_read_size + BODY_READ_LEN) > http_param_instance->content_size) //未读的数据不够BODY_READ_LEN
                read_len = esp_http_client_read(client, (char *)buffer, http_param_instance->content_size - http_param_instance->has_read_size); 
            else
                read_len = esp_http_client_read(client, (char *)buffer, BODY_READ_LEN); 

            if(read_len > 0){
                xRingbufferSend(player->buf_handle, (const void *)buffer, (size_t)read_len, 100/portTICK_PERIOD_MS);
                free_size -= read_len;
                http_param_instance->has_read_size += read_len;
                timeoutCnt = 0;
            }
            else { //client 没有读到数据，网络不正常？
                timeoutCnt++;
                // ESP_LOGE(TAG, "timeoutCnt = %d", timeoutCnt);  
                if(timeoutCnt > 500){
                    // ESP_LOGE(TAG, "Http read data timeoutCnt.");
                    return -1; //获取数据超时,后续需停止播放。
                }
                vTaskDelay(50 / portTICK_PERIOD_MS);
            }
        } 
        /* ring buffer中剩余空间小于BODY_READ_LEN, 继续读不够BODY_READ_LEN的字节,只在数据最后操作*/
        if((free_size > 0) || ((http_param_instance->has_read_size + free_size) > http_param_instance->content_size)) 
        { 
            if((http_param_instance->has_read_size + free_size) > http_param_instance->content_size)
                read_len = esp_http_client_read(client, (char *)buffer, http_param_instance->content_size - http_param_instance->has_read_size); 
            else
                read_len = esp_http_client_read(client, (char *)buffer, free_size); 
            if(read_len > 0)
            {
                xRingbufferSend(player->buf_handle, (const void *)buffer, (size_t)read_len, 100/portTICK_PERIOD_MS);   
                http_param_instance->has_read_size += read_len; 
            } 
        }
        // ESP_LOGE(TAG, "Ringbuf is full! has_read_size = %d, content_size = %d", http_param_instance->has_read_size, http_param_instance->content_size);     
    } 
    return 0;
}

static void print_respone()
{
    int has_read_size = 0;
    int read_len;
    char *buffer = calloc(BODY_READ_LEN, sizeof(char));
    if (!buffer)
    {
        mp_raise_ValueError(MP_ERROR_TEXT("Can not calloc buffer."));
    }
    
    // ESP_LOGE(TAG,"Not audio stream!");
    while(has_read_size < http_param_instance->content_size){
        read_len = esp_http_client_read(client, buffer, BODY_READ_LEN); 
        has_read_size += read_len;
        printf("%s", (char *)buffer);
    }
    free(buffer);
}

void http_request_task(void *pvParameters)
{
    player_t *player = pvParameters;
    int http_err = 0;
    int ringBufRemainBytes = 0;
    uint8_t *temp = NULL;
    size_t len;
    short *output= NULL; 
    size_t write_bytes;
    int err = 0;

    http_param_init();

    esp_http_client_config_t config = {
        .url = player->url, //"http://httpbin.org/get"
        .event_handler = _http_event_handler,
        .method = http_param_instance->http_method,
    };

    // if(strstr(player->url, "https") != NULL)
    //     config.cert_pem = cert_pem;

    client = esp_http_client_init(&config);
    if(!client){
        if (http_param_instance)
        {
            free(http_param_instance);
            http_param_instance = NULL;
        }
        mp_raise_ValueError(MP_ERROR_TEXT("http client init fail."));
    }

    if(http_request() != 0) //发出http请求
    {
        http_err = -1;
        goto abort;
    }

    if(http_param_instance->content_type == AUDIO_TEXT) //请求回应的是文本，打印之
        print_respone();

    if(http_get_data(client) != 0) //创建解码任务前，先把ringbuff填满
    {
        http_err = -1; //超时出错
        goto abort;
    }

    if(http_param_instance->content_type == AUDIO_WAV)
    {
        if(process_wav_tag() == -1)
        {
            http_err = -1;
            goto abort;
        }
        output = calloc(2048, sizeof(uint8_t));
    }else if(http_param_instance->content_type == AUDIO_MPEG)
    {
        if(create_decode_task(player) != 0)
        {
            http_err = -1;
            goto abort;
        }
    }

    // ESP_LOGE(TAG, "3.1. http request run, RAM left: %d, has_read_size = %d", esp_get_free_heap_size(), http_param_instance->has_read_size);
   
    /* 3种情况退出循环：1 长时间取不到数据 2 数据读完 3 收到指令 */ 
    while(http_param_instance->has_read_size < http_param_instance->content_size) 
    {  
        switch (player->player_status)
        {
        case RUNNING:
            err = http_get_data(client);
            if(err == -1)
            {
                player->player_status = STOPPED; 
                break;
            }
            if(http_param_instance->content_type == AUDIO_WAV) //wav音频直接送I2S
            {
                ringBufRemainBytes = RINGBUF_SIZE - xRingbufferGetCurFreeSize(player->buf_handle);
                if(ringBufRemainBytes > 2048){
                    temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, 2048);   
                }else{
                    temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, ringBufRemainBytes);   
                }
                memcpy((uint8_t *)output, temp, len);
                vRingbufferReturnItem(player->buf_handle, (void *)temp);

                for (int i = 0; i < len/2; i++)
                {
                    output[i] = (short)((output[i] + 32768) * player->volume);
                    output[i] &= 0xff00;
                }
                renderer_write(output, len, &write_bytes, 1000 / portTICK_RATE_MS); //portMAX_DELAY                
            }
            break;
        case STOPPED:
            err = -1;
            break;
        case PAUSED:
            vTaskSuspend( NULL );
            break;
        default:
            break;
        }

        if (err == -1)
            break;
        vTaskDelay(50 / portTICK_PERIOD_MS);
    }

    abort:
    if(err != -1)
    {
        player->player_status = END;  //正常播放结束
    }
    
    if(client){
        esp_http_client_close(client);
        esp_http_client_cleanup(client);
    }
    if (http_param_instance)
    {
        free(http_param_instance);
        http_param_instance = NULL;
    }
    if(output != NULL)
        free(output);

    xEventGroupSetBits(
            xEventGroup,    // The event group being updated.
            BIT_0);// The bits being set.
    // ESP_LOGE(TAG, "http request stack: %d\n", uxTaskGetStackHighWaterMark(NULL));
    // ESP_LOGE(TAG, "5. http request task will delete, RAM left: %d", esp_get_free_heap_size());
    vTaskDelete(NULL); 
}

int http_request_iat(void *data)
{
    recorder_t *recorder = data;
    esp_http_client_handle_t client = NULL;

    esp_http_client_config_t config = {
        .url = recorder->url, 
        .event_handler = _http_event_handler,
        .method = http_param_instance->http_method,
    };

    if((client = esp_http_client_init(&config)) == NULL){
        return -1;
    }

    esp_err_t err;
    if(http_param_instance->http_head != NULL){
        for(int i = 0; i < 6; i++)
            esp_http_client_set_header(client, http_param_instance->http_head[i].key, http_param_instance->http_head[i].value);
        // free((char *)http_head[3].value);
        // free((char *)http_head[0].value);
    }

    if ((err = esp_http_client_open(client, recorder->file_size)) != ESP_OK) { //http_param_instance->http_body_len
        // ESP_LOGE(TAG, "Failed to open HTTP connection");
        return -1;
    }
    mp_obj_t f = file_open(recorder->file_name, "rb");
    char *read_buff = calloc(1023, sizeof(char));
    int read_bytes;
    int read_err = 0;
    while(recorder->file_size > 0){
        read_err = file_read(f, &read_bytes, (uint8_t *)read_buff, 1023);
        esp_http_client_write(client, read_buff, read_bytes);
        recorder->file_size -= read_bytes;
        // ESP_LOGE(TAG, "%s", read_buff);
        if(read_err == -1)
            break;
    }
    file_close(f);
    free(read_buff);
    http_param_instance->content_size =  esp_http_client_fetch_headers(client);
    http_param_instance->http_read_buffer = calloc(500, sizeof(char));
    //  ESP_LOGE(TAG, "content_len1: %d, content_type: %d.", content_size, http_param_instance->content_type);
    if((http_param_instance->content_type == AUDIO_TEXT) && (http_param_instance->content_size > 0))
    {
        // ESP_LOGE(TAG, "content_len: %d, content_type: %d.", http_param_instance->content_size, http_param_instance->content_type);
        esp_http_client_read(client, (char *)http_param_instance->http_read_buffer, http_param_instance->content_size); 
        // printf("%s", (char *)http_param_instance->http_read_buffer);
    } 

    esp_http_client_close(client);
    esp_http_client_cleanup(client);

    return 0;
}

void init_http_param_handle(http_param_t *http_param)
{
    http_param_instance = http_param;
}

http_param_t *get_http_param_handle()
{
    return http_param_instance;
}

void http_param_handle_destroy()
{
    if(http_param_instance != NULL)
    {
        free(http_param_instance);
        http_param_instance = NULL;
    }
}
