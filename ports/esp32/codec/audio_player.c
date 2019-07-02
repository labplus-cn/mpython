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

#include "esp_system.h"
#include "esp_log.h"
#include "esp_task.h"

// #include "controls.h"
#include "driver/gpio.h"
#include "audio_player.h"
#include "audio_renderer.h"
#include "http_client.h"
#include "local_file.h"
#include "helix_mp3_decoder.h"

#define TAG "audio_player"

TaskHandle_t mp3_decode_task_handel = NULL;
TaskHandle_t http_client_task_handel = NULL;
static player_t *player_instance = NULL;
double volume;
int player_status;
extern HTTP_HEAD_VAL http_head[6];

void audio_player_begin(void)
{ 
    /* 4. 创建播放任务，网络或本地 获取音频数据，数据写入ringbuf*/
    if(strstr(player_instance->url, "http") != NULL){   //web play
        player_instance->file_type = WEB_TYPE;
        http_param_t *http_param = get_http_param_handle();                                              
        http_param->url = player_instance->url;       
        xTaskCreate(http_request_task, "http_request_task", 3072, player_instance, ESP_TASK_PRIO_MIN + 1, &http_client_task_handel );
        //http_request(); 
        // ESP_LOGE(TAG, "4. Create http_request task, RAM left: %d", esp_get_free_heap_size());
    }
    else { // local play
        player_instance->file_type = LOCAL_TYPE;
        local_file_read(player_instance);
        // xTaskCreate(local_file_read_task, "local_file_read_task", 8192, player_instance, ESP_TASK_PRIO_MIN + 1, NULL );
        //ESP_LOGE(TAG, "4. Create local file read task, RAM left: %d", esp_get_free_heap_size());
    }
}

int create_decode_task(player_t *player)
{
    int err = 0;
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
            xTaskCreate(mp3_decoder_task, "mp3_decoder_task", HELIX_DECODER_TASK_STACK_DEPTH, player, ESP_TASK_PRIO_MIN + 1, &mp3_decode_task_handel );
            // ESP_LOGE(TAG, "4. mp3 decoder task builded, RAM left: %d", esp_get_free_heap_size()); 
        break;
        default:
            err = -1;
        break;
    }
    return err;
}

void audio_player_destroy()
{
    if(player_instance != NULL)
    {
        if(player_instance->buf_handle != NULL)
        {
            vRingbufferDelete(player_instance->buf_handle);
            //vSemaphoreDelete(player_instance->ringbuf_sem);
            // vEventGroupDelete(player_instance->ringbuf_eventGroup);
        }
        free(player_instance);
        player_instance = NULL;
    }

    http_param_handle_destroy();

    renderer_destroy();
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

void init_palyer_handle(player_t *Player)
{
    player_instance = Player;
}

player_t *get_player_handle()
{
    return player_instance;
}

void audio_player_start()
{
    renderer_start();
    player_instance->player_status = RUNNING;
}

void audio_player_stop()
{
    if( player_instance->player_status == RUNNING ||  player_instance->player_status == PAUSED){
        renderer_stop();
        player_instance->player_status = STOPPED;
        while(1){
            vTaskDelay(50 / portTICK_PERIOD_MS);
            if(player_instance->player_status == INITIALIZED)
                break;
        }
    }
}

void audio_player_pause()
{
    if( player_instance->player_status == RUNNING){
        renderer_stop();
        player_instance->player_status = PAUSED;
    }
}

player_status_t get_player_status()
{
    return player_instance->player_status;
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

