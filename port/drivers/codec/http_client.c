/*
 * http_client.c
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */


#include <string.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
// #include "freertos/event_groups.h"
#include "freertos/ringbuf.h"
#include "esp_log.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "audio_player.h"
#include "helix_mp3_decoder.h"

#include "esp_http_client.h"
#include "http_client.h"
#include "audio_recorder.h"
#include "local_file.h"
#include "wav_head.h"
#include "driver/i2s.h"
#include "audio_renderer.h"

#define BODY_READ_LEN 64

static const char *TAG = "HTTP_CLIENT";
extern HTTP_HEAD_VAL http_head[6];
extern TaskHandle_t mp3_decode_task_handel;
static http_param_t *http_param_instance = NULL;

/* Root cert for howsmyssl.com, taken from howsmyssl_com_root_cert.pem

   The PEM file was extracted from the output of this command:
   openssl s_client -showcerts -connect www.howsmyssl.com:443 </dev/null

   The CA root cert is the last cert given in the chain of certs.

   To embed it in the app binary, the PEM file is named
   in the component.mk COMPONENT_EMBED_TXTFILES variable.
*/
const char *cert_pem = "-----BEGIN CERTIFICATE----- \
MIIEkjCCA3qgAwIBAgIQCgFBQgAAAVOFc2oLheynCDANBgkqhkiG9w0BAQsFADA/ \
MSQwIgYDVQQKExtEaWdpdGFsIFNpZ25hdHVyZSBUcnVzdCBDby4xFzAVBgNVBAMT \
DkRTVCBSb290IENBIFgzMB4XDTE2MDMxNzE2NDA0NloXDTIxMDMxNzE2NDA0Nlow \
SjELMAkGA1UEBhMCVVMxFjAUBgNVBAoTDUxldCdzIEVuY3J5cHQxIzAhBgNVBAMT \
GkxldCdzIEVuY3J5cHQgQXV0aG9yaXR5IFgzMIIBIjANBgkqhkiG9w0BAQEFAAOC \
AQ8AMIIBCgKCAQEAnNMM8FrlLke3cl03g7NoYzDq1zUmGSXhvb418XCSL7e4S0EF \
q6meNQhY7LEqxGiHC6PjdeTm86dicbp5gWAf15Gan/PQeGdxyGkOlZHP/uaZ6WA8 \
SMx+yk13EiSdRxta67nsHjcAHJyse6cF6s5K671B5TaYucv9bTyWaN8jKkKQDIZ0 \
Z8h/pZq4UmEUEz9l6YKHy9v6Dlb2honzhT+Xhq+w3Brvaw2VFn3EK6BlspkENnWA \
a6xK8xuQSXgvopZPKiAlKQTGdMDQMc2PMTiVFrqoM7hD8bEfwzB/onkxEz0tNvjj \
/PIzark5McWvxI0NHWQWM6r6hCm21AvA2H3DkwIDAQABo4IBfTCCAXkwEgYDVR0T \
AQH/BAgwBgEB/wIBADAOBgNVHQ8BAf8EBAMCAYYwfwYIKwYBBQUHAQEEczBxMDIG \
CCsGAQUFBzABhiZodHRwOi8vaXNyZy50cnVzdGlkLm9jc3AuaWRlbnRydXN0LmNv \
bTA7BggrBgEFBQcwAoYvaHR0cDovL2FwcHMuaWRlbnRydXN0LmNvbS9yb290cy9k \
c3Ryb290Y2F4My5wN2MwHwYDVR0jBBgwFoAUxKexpHsscfrb4UuQdf/EFWCFiRAw \
VAYDVR0gBE0wSzAIBgZngQwBAgEwPwYLKwYBBAGC3xMBAQEwMDAuBggrBgEFBQcC \
ARYiaHR0cDovL2Nwcy5yb290LXgxLmxldHNlbmNyeXB0Lm9yZzA8BgNVHR8ENTAz \
MDGgL6AthitodHRwOi8vY3JsLmlkZW50cnVzdC5jb20vRFNUUk9PVENBWDNDUkwu \
Y3JsMB0GA1UdDgQWBBSoSmpjBH3duubRObemRWXv86jsoTANBgkqhkiG9w0BAQsF \
AAOCAQEA3TPXEfNjWDjdGBX7CVW+dla5cEilaUcne8IkCJLxWh9KEik3JHRRHGJo \
uM2VcGfl96S8TihRzZvoroed6ti6WqEBmtzw3Wodatg+VyOeph4EYpr/1wXKtx8/ \
wApIvJSwtmVi4MFU5aMqrSDE6ea73Mj2tcMyo5jMd6jmeWUHK8so/joWUoHOUgwu \
X4Po1QYz+3dszkDqMp4fklxBwXRsW10KXzPMTZ+sOPAveyxindmjkW8lGy+QsRlG \
PfZ+G6Z6h7mjem0Y+iWlkYcV4PIWL1iwBi8saCbGS5jN2p8M+X+Q7UNKEkROb3N6 \
KOqkqm57TH2H3eDJAkSnh6/DNFu0Qg== \
-----END CERTIFICATE-----";

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

static int http_request(esp_http_client_handle_t client, int *content_length)
{
    esp_err_t err;
    player_t *player = get_player_handle();
    if(client == NULL)
    {
        // ESP_LOGE(TAG, "client is Null.");
         return -1;
    }

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

    if(http_param_instance->http_body != NULL && http_param_instance->http_body_len > 0){
        esp_http_client_write(client, http_param_instance->http_body, http_param_instance->http_body_len);
        free(http_param_instance->http_body); 
    }

    *content_length =  esp_http_client_fetch_headers(client);
    if(*content_length <= 0){
        player->media_stream.eof = true;
        // ESP_LOGE(TAG, "Failed to get content. content_length = %d", *content_length);
        return -1;
    }

    // ESP_LOGE(TAG, "mp3 content len : %d", *content_length);
    return 0;
}

/* 从http body读数据，直到把ring bufffer填满 */
static int http_get_data(esp_http_client_handle_t client, int *total_read_len, int content_length)
{
    int read_len, free_size;
    int timeoutCnt = 0;
    uint8_t buffer[BODY_READ_LEN];
    player_t *player = get_player_handle();

    //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
    free_size = xRingbufferGetCurFreeSize(player->buf_handle); //get ringbuf free size
    // xSemaphoreGive(player->ringbuf_sem); 
    if(free_size > 0){ 
        while((free_size >= BODY_READ_LEN) && (*total_read_len < content_length)) 
        {
            if((*total_read_len + BODY_READ_LEN) > content_length)
                read_len = esp_http_client_read(client, (char *)buffer, content_length - *total_read_len); 
            else
                read_len = esp_http_client_read(client, (char *)buffer, BODY_READ_LEN); 

            if(read_len > 0){
                //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
                xRingbufferSend(player->buf_handle, (const void *)buffer, (size_t)read_len, 100/portTICK_PERIOD_MS);
                // xSemaphoreGive(player->ringbuf_sem); 
                free_size -= read_len;
                *total_read_len += read_len;
                timeoutCnt = 0;
            }
            else { //client 没有读到数据，网络不正常？
                timeoutCnt++;
                // ESP_LOGE(TAG, "timeoutCnt = %d", timeoutCnt);  
                if(timeoutCnt > 500){
                    // ESP_LOGE(TAG, "Http read data timeoutCnt.");
                    return -1;
                }
                vTaskDelay(50 / portTICK_PERIOD_MS);
            }
        } 
        /* ring buffer中剩余空间小于BODY_READ_LEN, 继续读不够BODY_READ_LEN的字节,只在数据最后操作*/
        if((free_size > 0) || ((*total_read_len + free_size) > content_length)) 
        { 
            if((*total_read_len + free_size) > content_length)
                read_len = esp_http_client_read(client, (char *)buffer, content_length - *total_read_len); 
            else
                read_len = esp_http_client_read(client, (char *)buffer, free_size); 
            if(read_len > 0)
            {
                //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
                xRingbufferSend(player->buf_handle, (const void *)buffer, (size_t)read_len, 100/portTICK_PERIOD_MS);  
                // xSemaphoreGive(player->ringbuf_sem); 
                *total_read_len += read_len; 
            } 
        }
        //ESP_LOGE(TAG, "Ringbuf is full! total_read_len = %d, content_length = %d", *total_read_len, content_length);     
    } 
    return 0;
}

static int get_content_type(esp_http_client_handle_t client, int content_length)
{
    int total_read_len = 0;
    int read_len;
    uint8_t buffer[BODY_READ_LEN];
    // player_t *player = get_player_handle();

    if(http_param_instance->content_type == AUDIO_TEXT){
        // ESP_LOGE(TAG,"Not audio stream!");
        while(total_read_len < content_length){
            read_len = esp_http_client_read(client, (char *)buffer, BODY_READ_LEN); 
            total_read_len += read_len;
            printf("%s", (char *)buffer);
        }
        return -1;
    } 
    return 0;     
}

void http_request_task(void *pvParameters)
{
    int total_read_len = 0;
    int content_length = 0;
    player_t *player = pvParameters;
    esp_http_client_handle_t client = NULL;
    int http_err = 0;
    int ringBufRemainBytes = 0;
    uint8_t *temp = NULL;
    size_t len;
    short *output= NULL; 
    size_t write_bytes;

    esp_http_client_config_t config = {
        .url = http_param_instance->url, //"http://httpbin.org/get", //
        .event_handler = _http_event_handler,
        .method = http_param_instance->http_method,
    };

    if(strstr(player->url, "https") != NULL)
        config.cert_pem = cert_pem;
    client = esp_http_client_init(&config);
    if(client == NULL)
    {
        http_err = -1;
        goto abort;
    }

    if(http_request(client, &content_length) != 0)
    {
        http_err = -1;
        goto abort;
    }

    if(get_content_type(client,  content_length) != 0)
    {
        http_err = -1;
        goto abort;
    }

    if(http_get_data(client, &total_read_len, content_length) != 0) /*创建解码任务前，先把ringbuff填满*/
    {
        http_err = -1;
        goto abort;
    }

    audio_player_start();
    renderer_config_t *renderer = renderer_get();
    if(http_param_instance->content_type == AUDIO_WAV)
    {
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
                    i2s_set_clk(renderer->i2s_num, wav_info->sampleRate, wav_info->bits, wav_info->channels);
                    if(wav_info->fmtSubchunckSize == 16)
                        temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, 8);
                    else 
                        temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, 10);

                    free(wav_info);
                    vRingbufferReturnItem(player->buf_handle, (void *)temp);

                    output = calloc(2048, sizeof(uint8_t)); 
                } 
                else
                {
                    http_err = -1;
                    goto abort;
                }      
            }
        } 
    }else if(http_param_instance->content_type == AUDIO_MPEG)
    {
        if(create_decode_task(player) != 0)
        {
            http_err = -1;
            goto abort;
        }
    }

    // ESP_LOGE(TAG, "3.1. http request run, RAM left: %d, total_read_len = %d", esp_get_free_heap_size(), total_read_len);
    /* 3种情况退出循环：1 长时间取不到数据 2 数据读完 3 收到指令 */
    int err; 
    while(total_read_len < content_length) 
    {  
        if(player->player_status == RUNNING){
            err = http_get_data(client, &total_read_len, content_length);
            if(http_param_instance->content_type == AUDIO_WAV)
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
                i2s_write(renderer->i2s_num, output, len, &write_bytes, 1000 / portTICK_RATE_MS); //portMAX_DELAY                
            }
            if(err == -1){
                player->player_status = STOPPED;
                break;
            }  
        }else if(player->player_status == STOPPED){
            break;
        }else if(player->player_status == PAUSED){
            vTaskSuspend( NULL );
        }
        vTaskDelay(50 / portTICK_PERIOD_MS);
    }

    //ESP_LOGE(TAG, "total_read_len = %d", total_read_len);
    abort:
    player->media_stream.eof = true;
    // ESP_LOGE(TAG, "HTTP Stream reader Status = %d, content_length = %d total_readlen = %d",
    //                 esp_http_client_get_status_code(client),
    //                 esp_http_client_get_content_length(client), total_read_len);
    if(client != NULL){
        esp_http_client_close(client);
        esp_http_client_cleanup(client);
    }
    //audio_player_destroy();
    // ESP_LOGE(TAG, "5. http_err: %d", http_err); 
    // ESP_LOGE(TAG, "http request stack: %d\n", uxTaskGetStackHighWaterMark(NULL));
    // ESP_LOGE(TAG, "5. http request task will delete, RAM left: %d", esp_get_free_heap_size()); 
    if((http_err == -1) || (http_param_instance->content_type == AUDIO_WAV)){
        if(output != NULL)
            free(output);
        renderer_zero_dma_buffer();
        renderer_stop();
        player->media_stream.eof = true;
        player->player_status = INITIALIZED;
        vTaskDelete(NULL);
    }
    else{
        // ESP_LOGE(TAG, "Http tast suppended."); 
        vTaskSuspend( NULL );
    }
}

int http_request_iat(void *data)
{
    recorder_t *recorder = data;
    esp_http_client_handle_t client = NULL;

    esp_http_client_config_t config = {
        .url = http_param_instance->url, 
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
    int content_length =  esp_http_client_fetch_headers(client);
    http_param_instance->http_read_buffer = calloc(500, sizeof(char));
    //  ESP_LOGE(TAG, "content_len1: %d, content_type: %d.", content_length, http_param_instance->content_type);
    if((http_param_instance->content_type == AUDIO_TEXT) && (content_length > 0))
    {
        // ESP_LOGE(TAG, "content_len: %d, content_type: %d.", content_length, http_param_instance->content_type);
        esp_http_client_read(client, (char *)http_param_instance->http_read_buffer, content_length); 
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
