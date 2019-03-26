/*
 * audio_player.c
 *
 *  Created on: 12.03.2017
 *      Author: michaelboeckling
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

TaskHandle_t mp3_decode_task_handel;
TaskHandle_t http_client_task_handel;
static player_t *player_instance = NULL;
double volume;
int player_status;

void audio_player_init(player_t *player, renderer_config_t *renderer)
{ 
    /* 1 创建一个播放器对象并初始化 */
    player_instance = player;
    // player_instance->ringbuf_eventGroup = xEventGroupCreate();
    // ESP_LOGE(TAG, "1. Create player, RAM left 1 %d", esp_get_free_heap_size());

    /* 2. 创建rendder对象并初始化（完成i2s dac初始化） */
    renderer_init(renderer); //I2S参数配置
    // ESP_LOGE(TAG, "2. Create renderer, RAM left: %d", esp_get_free_heap_size());

    /* 3. 创建ring buffer对象） */
    player_instance->buf_handle = xRingbufferCreate(RINGBUF_SIZE, RINGBUF_TYPE_BYTEBUF);
    // ESP_LOGE(TAG, "3. Create ringbuf, RAM left: %d", esp_get_free_heap_size());
    
    /* 4. 创建播放任务，网络或本地 获取音频数据，数据写入ringbuf*/
    if(strstr(player_instance->url, "http") != NULL){   //web play
        xTaskCreate(http_request_task, "http_request_task", 3072, player_instance, ESP_TASK_PRIO_MIN + 1, &http_client_task_handel );
        //http_request(); 
        ESP_LOGE(TAG, "4. Create http_request task, RAM left: %d", esp_get_free_heap_size());
    }
    else { // local play
        local_file_read(player_instance);
        // xTaskCreate(local_file_read_task, "local_file_read_task", 8192, player_instance, ESP_TASK_PRIO_MIN + 1, NULL );
        // ESP_LOGE(TAG, "4. Create local file read task, RAM left: %d", esp_get_free_heap_size());
    }
}

void create_decode_task(player_t *player)
{
    switch(player->media_stream.content_type){ //创建不同的解码任务
        case OCTET_STREAM:

        break;
        case AUDIO_AAC:
        
        break;
        case AUDIO_MP4:

        break;
        case AUDIO_MPEG:
            xTaskCreate(mp3_decoder_task, "mp3_decoder_task", HELIX_DECODER_TASK_STACK_DEPTH, player, ESP_TASK_PRIO_MIN + 1, &mp3_decode_task_handel );
            ESP_LOGE(TAG, "4. mp3 decoder task builded, RAM left: %d", esp_get_free_heap_size()); 
        break;
        default:
        break;
    }
}

void audio_player_destroy()
{
    //controls_destroy(config);

    vRingbufferDelete(player_instance->buf_handle);
    vSemaphoreDelete(player_instance->ringbuf_sem);
    // vEventGroupDelete(player_instance->ringbuf_eventGroup);
    free(player_instance);
    player_instance = NULL;

    renderer_destroy();
    // ESP_LOGE(TAG, "RAM left %d", esp_get_free_heap_size());
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
    player_instance->player_status = STOPPED;
}

void audio_player_pause()
{
    renderer_stop();
    player_instance->player_status = PAUSED;
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

