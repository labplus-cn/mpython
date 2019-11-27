/*
 * audio_recorder.c
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
#include "freertos/timers.h"
#include "esp_system.h"
#include "esp_log.h"
#include "esp_task.h"
#include "py/stream.h"
#include "py/reader.h"
#include "extmod/vfs.h"
#include <stdio.h>
#include "py/runtime.h"

#include "audio_recorder.h"
#include "audio_renderer.h"
#include "http_client.h"
#include "driver/i2s.h"
#include "driver/adc.h"
#include "local_file.h"

#define TAG "audio_recorder"
#define I2S_SAMPLE_BITS 16

static recorder_t *recorder_instance = NULL;
extern HTTP_HEAD_VAL http_head[6];

int cmpfunc (const void * a, const void * b)
{
   return ( *(int*)a - *(int*)b );
}

// static bool timer_expire;

// static void vTimerCallback( TimerHandle_t pxTimer )
// {
//     xTimerStop(pxTimer, portMAX_DELAY);
//     timer_expire =false;
// }

void recorder_task(void *pvParameters)
{
    // timer_expire = true;
    // TimerHandle_t recorder_timer;
    // recorder_timer = xTimerCreate(  "RecorderTimer",       // Just a text name, not used by the kernel.
    //                                 recorder_instance->recorde_time / portTICK_PERIOD_MS,   // The timer period in ticks.
    //                                 pdFALSE,        // The timers will auto-reload themselves when they expire.
    //                                 ( void * )1,  // Assign each timer a unique id equal to its array index.
    //                                 vTimerCallback // Each timer calls the same callback when it expires.
    //                             );

    // recorder_t *recorder = pvParameters;
    
    // renderer_config_t *renderer = renderer_get();
    // uint8_t *read_buff = calloc(renderer->i2s_read_buff_size, sizeof(uint8_t));
    // recorder->file = file_open(recorder->file_name, "w");
    // xTimerStart(recorder->recorder_timer, portMAX_DELAY);
    // int write_bytes;
    // recorder_t *recorder = get_recorder_handle();
    // while(recorder->timer_expire)  //wait record timer expire
    // {
    //     read_sound(read_buff);
        // file_write(recorder->file, &write_bytes, read_buff, renderer->i2s_read_buff_size);
    // }
    // xTimerDelete(recorder->recorder_timer, portMAX_DELAY);
    // file_close(recorder->file);
    vTaskDelete(NULL);
}

void init_recorder_handle(recorder_t *recorder)
{
    recorder_instance = recorder;
}

recorder_t *get_recorder_handle()
{
    return recorder_instance;
}

void audio_recorder_destroy()
{
    if(recorder_instance != NULL){
        free(recorder_instance);
        recorder_instance = NULL;
    }
    renderer_destroy();
    http_param_handle_destroy();
}

/*
void audio_recorder_quicksort(uint16_t *buff, uint16_t len)
{
    qsort(buff, len, sizeof(uint16_t), cmpfunc);
    for(int i = 0; i < len; i++)
        printf("%d\r\n", buff[i]);
}
*/

/********************************
 *函数名：swap
 *作用：交换两个数的值
 *参数：交换的两个数
 *返回值：无
 ********************************/
static void swap(uint16_t *a, uint16_t *b)  
{
    uint16_t temp;
    temp = *a;
    *a = *b;
    *b = temp;
}

/************************************
 *函数名：quicksort
 *作用：快速排序算法
 *参数：
 *返回值：无
 ************************************/
void audio_recorder_quicksort(uint16_t *buff, uint32_t maxlen, uint32_t begin, uint32_t end)
{
    int i, j;
    if(begin < end)
    {
        i = begin + 1;  // buff[begin]作为基准数，因此从array[begin+1]开始与基准数比较！
        j = end;        // buff[end]是数组的最后一位

        while(i < j)
        {
            if(buff[i] > buff[begin])  // 如果比较的数组元素大于基准数，则交换位置。
            {
                swap(&buff[i], &buff[j]);  // 交换两个数
                j--;
            }
            else
            {
                i++;  // 将数组向后移一位，继续与基准数比较。
            }
        }

        /* 跳出while循环后，i = j。
         * 此时数组被分割成两个部分  -->  buff[begin+1] ~ buff[i-1] < buff[begin]
         *                           -->  buff[i+1] ~ buff[end] > buff[begin]
         * 这个时候将数组buff分成两个部分，再将buff[i]与buff[begin]进行比较，决定buff[i]的位置。
         * 最后将buff[i]与buff[begin]交换，进行两个分割部分的排序！以此类推，直到最后i = j不满足条件就退出！
         */
        if(buff[i] >= buff[begin])  // 这里必须要取等“>=”，否则数组元素由相同的值时，会出现错误！
        {
            i--;
        }
        swap(&buff[begin], &buff[i]);  // 交换buff[i]与buff[begin]
        audio_recorder_quicksort(buff, maxlen, begin, i);
        audio_recorder_quicksort(buff, maxlen, j, end);
    }
}

