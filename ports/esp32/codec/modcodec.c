/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2018 Zhang Kaihua(apple_eat@126.com)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
#include <stdlib.h>
#include <string.h>
#include "esp_err.h"
#include <sys/stat.h>
#include <ctype.h>
#include <stdio.h>
#include <unistd.h>

#include "py/nlr.h"
#include "py/runtime.h"
#include "py/objstr.h"
#include "modmachine.h"
#include "mphalport.h"
#include "wav_head.h"
#include "modcodec.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_http_client.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "freertos/ringbuf.h"

#include <time.h>
#include <dirent.h>
#include "soc/io_mux_reg.h"
#include <math.h>

#include "audio_player.h"    
#include "helix_mp3_decoder.h"
#include "modcodec.h"
#include "http_client.h"
#include "url_codec.h"

static const char *TAG = "codec";
static HTTP_HEAD_VAL http_head[6];
extern TaskHandle_t mp3_decode_task_handel;
extern TaskHandle_t http_client_task_handel;
extern double volume;
extern int player_status;
//
STATIC mp_obj_t codec_play(mp_obj_t url)
{
    if(get_player_handle() == NULL)
    {
        const char *_url = mp_obj_str_get_str(url);
        //ESP_LOGE(TAG, "%s", _url);
        //ESP_LOGE(TAG, " 0. Begin audio play, RAM left: %d", esp_get_free_heap_size());
        player_t *player = calloc(1, sizeof(player_t));
        player->command  = CMD_NONE;                  
        player->player_status = RUNNING;       
        player->buffer_pref = BUF_PREF_SAFE;                          
        player->ringbuf_size = RINGBUF_SIZE;          
        player->ringbuf_sem = xSemaphoreCreateMutex();                                            
        player->http_head = NULL;                    
        player->http_body = NULL;    
        player->http_method = HTTP_METHOD_GET;                               
        player->media_stream.content_type = MIME_UNKNOWN;      
        player->media_stream.eof = false;                                                         
        player->url = _url;                             

        renderer_config_t *renderer_config = calloc(1, sizeof(renderer_config_t));
        renderer_config->bit_depth  = I2S_BITS_PER_SAMPLE_16BIT;
        renderer_config->i2s_num = I2S_NUM_0;
        renderer_config->sample_rate = 44100;
        renderer_config->sample_rate_modifier = 1.0;
        renderer_config->output_mode = DAC_BUILT_IN;
        volume = pow(10, (MIN_VOL_OFFSET + 50 / 2) / 20.0);
        player_status = 0;
        audio_player_init(player, renderer_config);

        return MP_OBJ_NEW_SMALL_INT(0);
    }
    else{
        ESP_LOGE(TAG,"In playing status, you need stop it first.");
    }
    return MP_OBJ_NEW_SMALL_INT(1);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(audio_play_obj, codec_play);

STATIC mp_obj_t codec_resume(void)
{
    audio_player_start();
    vTaskResume( mp3_decode_task_handel );
    vTaskResume( http_client_task_handel );
    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_resume_obj, codec_resume);

STATIC mp_obj_t codec_stop(void)
{
    audio_player_stop();
    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_stop_obj, codec_stop);

STATIC mp_obj_t codec_pause(void)
{
    audio_player_pause();
    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_pause_obj, codec_pause);

STATIC mp_obj_t codec_volume(mp_obj_t Volume)
{
    player_t *player = get_player_handle();
    mp_int_t vol =  mp_obj_get_int(Volume);
    vol = (vol > 100)? 100 : vol;
    vol = (vol < 0)? 0 : vol;
    volume = pow(10, (MIN_VOL_OFFSET + vol / 2) / 20.0);
    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(audio_volume_obj, codec_volume);

STATIC mp_obj_t codec_get_status(void)
{
    player_t *player = get_player_handle();

    if(player_status == 1){
        return MP_OBJ_NEW_SMALL_INT(1); 
    }     
    else{
        return MP_OBJ_NEW_SMALL_INT(0);
    }
    
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_get_status_obj, codec_get_status);

STATIC mp_obj_t codec_webtts(mp_obj_t head, mp_obj_t body)
{
    if(get_player_handle() == NULL)
    { 
        http_head[0].key = "X-CurTime";
        http_head[1].key = "X-Param";
        http_head[2].key = "X-Appid";
        http_head[3].key = "X-CheckSum";
        http_head[4].key = "X-Real-Ip";
        http_head[5].key = "Content-Type";

        mp_obj_t key;
        mp_obj_t value;
        for(int i = 0; i < 6; i++){
            key = mp_obj_new_str(http_head[i].key, strlen(http_head[i].key));
            value = mp_obj_dict_get(head, key);
            http_head[i].value = mp_obj_str_get_str(value);
            // ESP_LOGE(TAG, "%s:%s", http_head[i].key,http_head[i].value);
        }

        player_t *player = calloc(1, sizeof(player_t));
        player->command  = CMD_NONE;                  
        player->player_status = RUNNING;       
        player->buffer_pref = BUF_PREF_SAFE;                          
        player->ringbuf_size = RINGBUF_SIZE;          
        player->ringbuf_sem = xSemaphoreCreateMutex();                                               
        player->http_head = http_head;                                                     
        player->media_stream.content_type = MIME_UNKNOWN;      
        player->media_stream.eof = false;                                                         
        player->url = "http://api.xfyun.cn/v1/service/v1/tts";
            
        char *src = calloc(1800, sizeof(char));
        char *des = calloc(1800, sizeof(char));
        sprintf(src,"%s%s", "text=", mp_obj_str_get_str(body));
        urlencode(src, des);
        free(src);
        // ESP_LOGE(TAG, "%s", des);
        player->http_body = des; 
        player->http_body_len = strlen(des);
        player->http_method = HTTP_METHOD_POST;

        renderer_config_t *renderer_config = calloc(1, sizeof(renderer_config_t));
        renderer_config->bit_depth  = I2S_BITS_PER_SAMPLE_16BIT;
        renderer_config->i2s_num = I2S_NUM_0;
        renderer_config->sample_rate = 44100;
        renderer_config->sample_rate_modifier = 1.0;
        renderer_config->output_mode = DAC_BUILT_IN;
        volume = pow(10, (MIN_VOL_OFFSET + 50 / 2) / 20.0);
        player_status = 0;
        audio_player_init(player, renderer_config); 

        return MP_OBJ_NEW_SMALL_INT(0);
    }
    else{
        ESP_LOGE(TAG,"In playing status, you need stop it first.");
    }     
    return MP_OBJ_NEW_SMALL_INT(1);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(webtts_obj, codec_webtts);

STATIC const mp_map_elem_t mpython_codec_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_cocdec)},
	{MP_OBJ_NEW_QSTR(MP_QSTR_audio_play), (mp_obj_t)&audio_play_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_audio_resume), (mp_obj_t)&audio_resume_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_audio_stop), (mp_obj_t)&audio_stop_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_audio_pause), (mp_obj_t)&audio_pause_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_audio_volume), (mp_obj_t)&audio_volume_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_audio_status), (mp_obj_t)&audio_get_status_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_web_tts), (mp_obj_t)&webtts_obj},
};

STATIC MP_DEFINE_CONST_DICT(mpython_codec_locals_dict, mpython_codec_locals_dict_table);

const mp_obj_module_t mp_module_codec = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mpython_codec_locals_dict,
};