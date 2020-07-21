/*
 * audio_player.c
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/ringbuf.h"
#include "freertos/event_groups.h"

#include "esp_system.h"
#include "esp_log.h"
#include "esp_task.h"
#include "py/runtime.h"

// #include "controls.h"
#include "driver/gpio.h"
#include "audio_player.h"
#include "audio_renderer.h"
#include "http_client.h"
#include "local_play.h"
#include "helix_mp3_decoder.h"

#define TAG "audio_player"

TaskHandle_t mp3_decode_task_handel = NULL;
TaskHandle_t http_client_task_handel = NULL;
static player_t *player_instance = NULL;
double volume;
int player_status;
extern HTTP_HEAD_VAL http_head[6];
EventGroupHandle_t xEventGroup;

STATIC void clear_ringbuf(player_t *player)
{
    int ringBufRemainBytes = 0;
    size_t len;
    void *temp = NULL;

    while(1){
        ringBufRemainBytes = RINGBUF_SIZE - xRingbufferGetCurFreeSize(player->buf_handle); //
        if(ringBufRemainBytes >= 100)  //ring buffer remain data enough for decoder need
        { 
            temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, 100);
            if(temp != NULL)
                vRingbufferReturnItem(player->buf_handle, (void *)temp);
        }
        else{ 
            if(ringBufRemainBytes != 0){
                temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 50 / portTICK_PERIOD_MS, ringBufRemainBytes);
                if(temp != NULL)
                    vRingbufferReturnItem(player->buf_handle, (void *)temp);
            }  
            break;
        } 
    }
}

void player_init(void)
{
    // ESP_LOGE(TAG, "1. begin create player, RAM left  %d", esp_get_free_heap_size());
    if(!player_instance){ 
        player_instance = calloc(1, sizeof(player_t));  /* 1. Create player.*/ 
        xEventGroup = xEventGroupCreate();               
    }   
    player_instance->player_status = INITIALIZED;                                          
    player_instance->content_type = MIME_UNKNOWN;                                                                                
    player_instance->eof = false; 
    player_instance->volume = pow(10, (MIN_VOL_OFFSET + 80 / 2) / 20.0); 
    player_instance->buf_handle = xRingbufferCreate(RINGBUF_SIZE, RINGBUF_TYPE_BYTEBUF);
}

void player_deinit(void)
{
    vTaskDelay(100 / portTICK_PERIOD_MS);
    if(player_instance){
        if((player_instance->player_status == RUNNING) || (player_instance->player_status == PAUSED))
        {
            player_stop();
        }

        if (player_instance->buf_handle)
            vRingbufferDelete(player_instance->buf_handle);

        free(player_instance);
        player_instance = NULL;
        // http_param_handle_destroy();

        renderer_deinit();
        if(http_head[3].value != NULL){
            free((char *)http_head[3].value);
            http_head[3].value = NULL;
        }
        if(http_head[0].value != NULL){
            free((char *)http_head[0].value);
            http_head[0].value = NULL;
        }       
        if(http_head[1].value != NULL)
        {
            free((char *)http_head[1].value);
            http_head[1].value = NULL;
        }        
        // ESP_LOGE(TAG, "RAM left %d", esp_get_free_heap_size());
    }
    else{
        mp_warning(NULL, "No player.");
    }
}

void player_play(const char *url)
{ 
    if(player_instance){
        if(player_instance->player_status == RUNNING || player_instance->player_status == PAUSED){
            player_stop();
        }                                                                          
        player_instance->url = url;
        clear_ringbuf(player_instance);

        if(strstr(player_instance->url, "http") != NULL){   //1 web play
            player_instance->file_type = WEB_TYPE;

            /* config renderer. */
            renderer_config_t renderer_cfg;
            renderer_cfg.mode = I2S_MODE_TX; 
            renderer_cfg.use_apll = false;
            renderer_cfg.bit_depth  = 16;
            renderer_cfg.sample_rate = 22050;  
            renderer_cfg.i2s_channal_nums = 2; 
            renderer_cfg.channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT;
            renderer_init(&renderer_cfg);
            renderer_start();
            player_start();
            xTaskCreate(http_request_task, "http_request_task", 2800, player_instance, ESP_TASK_PRIO_MIN + 1, &http_client_task_handel );
        }
        else { //2 local play
            player_instance->file_type = LOCAL_TYPE;
            if((strstr(player_instance->url, ".mp3") != NULL)){
                player_instance->content_type = AUDIO_MPEG;
            }else if((strstr(player_instance->url, ".pcm") != NULL)){
                player_instance->content_type = AUDIO_PCM;
            }else if((strstr(player_instance->url, ".wav") != NULL)){
                player_instance->content_type = AUDIO_WAV;
                // ESP_LOGE(TAG, "wav file");
            }else if((strstr(player_instance->url, ".m4a") != NULL)){
                player_instance->content_type = AUDIO_MP4;
            }else if((strstr(player_instance->url, ".aac") != NULL)){
                player_instance->content_type = AUDIO_AAC;
            }
            else{
                mp_warning(NULL, "Not suport format.");
                return;
            }
            local_play(player_instance);
            // xTaskCreate(local_play_task, "local_play_task", 8192, player_instance, ESP_TASK_PRIO_MIN + 1, NULL );
            // ESP_LOGE(TAG, "4. Create local file read task, RAM left: %d", esp_get_free_heap_size());
        }
    }
    else
    {
        mp_raise_ValueError(MP_ERROR_TEXT("no player, please init player first"));
    }
}

player_t *get_player_handle()
{
    return player_instance;
}

void player_start()
{
    if(player_instance)
    {
        player_instance->player_status = RUNNING;
    }
    else
    {
       mp_warning(NULL, "No player.");
    }    
}

void player_stop()
{
    EventBits_t uxBits;
    if(player_instance)
    { 
        renderer_stop();
        player_instance->player_status = STOPPED;

        //等待播放任务结束
        uxBits = xEventGroupWaitBits(
                    xEventGroup,    // The event group being tested.
                    BIT_0 | BIT_1,  // The bits within the event group to wait for.
                    pdTRUE,         // BIT_0 and BIT_4 should be cleared before returning.
                    pdTRUE,         // wait for both bits, either bit will do.
                    portMAX_DELAY ); // Wait a maximum of 100ms for either bit to be set.

        if( ( uxBits & BIT_1) !=  BIT_1 )
        {
            mp_warning(NULL, "Cant not stop player.");
        }
    }
    else
    {
       mp_warning(NULL, "No player.");
    }
}

void player_pause()
{
    if(player_instance)
    {
        if( player_instance->player_status == RUNNING){
            renderer_stop();
            player_instance->player_status = PAUSED;
        }
    }
    else
    {
        mp_warning(NULL, "No player.");
    }
    
}

void player_resume()
{
    if(player_instance)
    {
        if(player_instance->player_status == PAUSED){
            player_start();
            vTaskResume( mp3_decode_task_handel );
            vTaskResume( http_client_task_handel );
            renderer_start();
        }
    }
    else
    {
        mp_warning(NULL, "No player.");
    }      
}

void player_set_volume(int _vol)
{
    int vol = _vol;
    if(player_instance){
        vol = (vol > 100)? 100 : vol;
        vol = (vol < 0)? 0 : vol;
        player_instance->volume = pow(10, (MIN_VOL_OFFSET + vol / 2) / 20.0);
    }
}

player_status_t player_get_status()
{
    if(player_instance){
        return player_instance->player_status;
    }
    else
    {
        mp_warning(NULL, "No player.");
    }
    return 0;
}

int create_decode_task(player_t *player)
{
    int err = 0;
    if( player_instance->file_type == WEB_TYPE)
    {
        http_param_t *http_param = get_http_param_handle();
        switch(http_param->content_type){ //创建不同的解码任务
            case OCTET_STREAM:
                err = -1;
            break;
            case AUDIO_AAC:
                err = -1;
            break;
            case AUDIO_MP4:
                err = -1;
            break;
            case AUDIO_MPEG:
                xTaskCreate(mp3_decoder_task, "mp3_decoder_task", DECODER_TASK_STACK_DEPTH, player, ESP_TASK_PRIO_MIN + 1, &mp3_decode_task_handel );
                if (!mp3_decode_task_handel)
                    err = -1;
                // ESP_LOGE(TAG, "4. mp3 decoder task builded, RAM left: %d", esp_get_free_heap_size()); 
            break;
            default:
                err = -1;
            break;
        }
    }
    else if(player_instance->file_type == LOCAL_TYPE)
    {
        if(player->content_type == AUDIO_MPEG){
                xTaskCreate(mp3_decoder_task, "mp3_decoder_task", DECODER_TASK_STACK_DEPTH, player, ESP_TASK_PRIO_MIN + 1, &mp3_decode_task_handel );
                if (!mp3_decode_task_handel)
                    err = -1;
                // ESP_LOGE(TAG, "4. mp3 decoder task builded, RAM left: %d", esp_get_free_heap_size()); 
        }
    }
    return err;
}

/*
void web_radio_gpio_handler_task(void *pvParams)
{
    gpio_handler_param_t *params = pvParams;
    web_radio_t *config = params->user_data;
    xQueueHandle gpio_evt_queue = params->gpio_evt_queue;

    uint32_t io_num;
    for (;;) {
        if (xQueueReceive(gpio_evt_queue, &io_num, portMAX_DELAY)) {
            ESP_LOGI(TAG, "GPIO[%d] intr, val: %d", io_num, gpio_get_level(io_num));

            switch (get_player_status()) {
                case RUNNING:
                    ESP_LOGI(TAG, "stopping player");
                    web_radio_stop(config);
                    break;

                case STOPPED:
                    ESP_LOGI(TAG, "starting player");
                    web_radio_start(config);
                    break;

                default:
                    ESP_LOGI(TAG, "player state: %d", get_player_status());
            }
        }
    }
}
*/

