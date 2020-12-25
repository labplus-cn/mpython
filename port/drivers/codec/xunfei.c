/*
 * audio_recorder.c
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "esp_system.h"
#include "esp_log.h"
#include "py/stream.h"
#include "py/reader.h"
#include "py/runtime.h"
#include "extmod/vfs.h"

#include "audio_recorder.h"
#include "audio_renderer.h"
#include "http_client.h"
#include "driver/i2s.h"
#include "driver/adc.h"
#include "local_play.h"
#include "wave_head.h"
#include "url_codec.h"
#include "mbedtls/md5.h"
#include "mbedtls/base64.h"

#define TAG "xunfei"

STATIC void iat_record(const char *file_name)
{
    // renderer_config_t *renderer = renderer_get();
    // recorder_t *recorder = get_recorder_handle();

    // mp_obj_t F = file_open(file_name, "wb");
    // int write_bytes; //,read_bytes;
    // char *read_buff = calloc(renderer->i2s_read_buff_size, sizeof(uint8_t));
    // uint8_t *write_buff = calloc(renderer->i2s_read_buff_size + 2000, sizeof(uint8_t));
    // char *des = calloc(renderer->i2s_read_buff_size + 2000, sizeof(char));

    // char *tmp = "audio=";
    // urlencode(tmp, read_buff);
    // file_write(F, &write_bytes, (uint8_t *)read_buff, (uint16_t)strlen(read_buff));
    // recorder->file_size = strlen(tmp);
     
    // int out;
    // size_t n = 0;  
    // int i = 0;
    // uint16_t record_times = 32 * recorder->recorde_time / renderer->i2s_read_buff_size; //caculate record loops
    // renderer_adc_enable(); 
    // while(i < record_times)
    // {
    //     renderer_read_raw((uint8_t *)read_buff, renderer->i2s_read_buff_size);
    //     i2s_adc_data_scale((uint8_t *)read_buff, (uint8_t *)read_buff, renderer->i2s_read_buff_size);
    //     mbedtls_base64_encode(NULL, 0, &n, (const unsigned char *)read_buff, renderer->i2s_read_buff_size);
    //     memset(write_buff, 0, renderer->i2s_read_buff_size + 2000);
    //     mbedtls_base64_encode((unsigned char *)write_buff, n, (size_t *)&out, (const unsigned char *)read_buff, renderer->i2s_read_buff_size); 
    //     memset(des, 0, renderer->i2s_read_buff_size + 2000);
    //     urlencode((char *)write_buff, des);
    //     //ESP_LOGE(TAG, "%s", des);
    //     file_write(F, &write_bytes, (uint8_t *)des, strlen(des));  
    //     recorder->file_size += write_bytes; 
    //     i++;
    // } 
    // ESP_LOGE(TAG, "%d", recorder->file_size);

    // /* test base64 and urlencode result. compare with xunfei iat example encode result*/
    // mp_obj_t f = file_open("3.wav", "rb"); 
    // while(1)
    // {
    //     err = file_read(f, &read_bytes, (uint8_t *)read_buff, renderer->i2s_read_buff_size);
    //     mbedtls_base64_encode(NULL, 0, &n, (const unsigned char *)read_buff, read_bytes);
    //     memset(write_buff, 0, renderer->i2s_read_buff_size + 2000);
    //     mbedtls_base64_encode((unsigned char *)write_buff, n, (size_t *)&out, (const unsigned char *)read_buff, read_bytes); 
    //     memset(des, 0, renderer->i2s_read_buff_size + 2000);
    //     urlencode((char *)write_buff, (char *)des);
    //     // ESP_LOGE(TAG, "%s", des);
    //     file_write(F, &write_bytes, (uint8_t *)des, strlen(des));   
    //     recorder->file_size += write_bytes;
    //     if(err == -1)
    //     break;
    // }   

    // renderer_adc_disable();
    // free(read_buff);
    // free(write_buff);
    // free(des);
    // file_close(F);
}

