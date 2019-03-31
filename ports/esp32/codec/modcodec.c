/*
 * modcodec.c
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#include <stdlib.h>
#include <string.h>
#include "esp_err.h"
#include <sys/stat.h>
#include <ctype.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/time.h>

#include "py/nlr.h"
#include "py/runtime.h"
#include "py/objstr.h"
#include "modmachine.h"
#include "mphalport.h"
#include "wav_head.h"
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
#include "mbedtls/md5.h"
#include "mbedtls/base64.h"

static const char *TAG = "audio";

HTTP_HEAD_VAL http_head[6] = {
    {"X-CurTime", NULL},
    {"X-Param", NULL},
    {"X-Appid",  NULL},
    {"X-CheckSum", NULL},
    {"X-Real-Ip", "127.0.0.1"},
    {"Content-Type", "application/x-www-form-urlencoded; charset=utf-8"}
};
static const char *api_key;
extern TaskHandle_t mp3_decode_task_handel;
extern TaskHandle_t http_client_task_handel;
//
STATIC void clear_ringbuf(player_t *player)
{
    int ringBufRemainBytes = 0;
    size_t len;
    void *temp = NULL;

    while(1){
        //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
        ringBufRemainBytes = RINGBUF_SIZE - xRingbufferGetCurFreeSize(player->buf_handle); //
        //xSemaphoreGive(player->ringbuf_sem);
        if(ringBufRemainBytes >= 100)  //ring buffer remain data enough for decoder need
        { 
            //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
            temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 500 / portTICK_PERIOD_MS, 100);
            //xSemaphoreGive(player->ringbuf_sem);
            if(temp != NULL)
                vRingbufferReturnItem(player->buf_handle, (void *)temp);
        }
        else{ 
            if(ringBufRemainBytes != 0){
                //xSemaphoreTake(player->ringbuf_sem, portMAX_DELAY);
                temp = xRingbufferReceiveUpTo(player->buf_handle,  &len, 50 / portTICK_PERIOD_MS, ringBufRemainBytes);
                //xSemaphoreGive(player->ringbuf_sem);
                if(temp != NULL)
                    vRingbufferReturnItem(player->buf_handle, (void *)temp);
            }  
            break;
        } 
    }
}

STATIC mp_obj_t audio_player_init(void)
{
    player_t *Player = get_player_handle();
    if(Player == NULL){
        /* 1. 创建播放器。*/
        //ESP_LOGE(TAG, " 0. Begin audio play, RAM left: %d", esp_get_free_heap_size());
        player_t *player = calloc(1, sizeof(player_t));
        player->command  = CMD_NONE;                  
        player->player_status = INITIALIZED;       
        player->buffer_pref = BUF_PREF_SAFE;                          
        player->ringbuf_size = RINGBUF_SIZE;          
        //player->ringbuf_sem = xSemaphoreCreateMutex();                                                                           
        player->media_stream.content_type = MIME_UNKNOWN;      
        player->media_stream.eof = false; 
        player->file_type = UNKNOW_TYPE;
        player->volume = pow(10, (MIN_VOL_OFFSET + 10 / 2) / 20.0); 
        //player->ringbuf_eventGroup = xEventGroupCreate();
        player->buf_handle = xRingbufferCreate(RINGBUF_SIZE, RINGBUF_TYPE_BYTEBUF);
        init_palyer_handle(player);
        // ESP_LOGE(TAG, "1. Create player, RAM left  %d", esp_get_free_heap_size());

        /* 2. 创建rendder对象并初始化（完成i2s dac初始化） */
        renderer_config_t *renderer_config = calloc(1, sizeof(renderer_config_t));
        renderer_config->bit_depth  = I2S_BITS_PER_SAMPLE_16BIT;
        renderer_config->i2s_num = I2S_NUM_0;
        renderer_config->sample_rate = 44100;
        renderer_config->sample_rate_modifier = 1.0;
        renderer_config->output_mode = DAC_BUILT_IN;                                               
        renderer_init(renderer_config); //I2S参数配置
        // ESP_LOGE(TAG, "2. Create renderer, RAM left: %d", esp_get_free_heap_size());
    }
    else
    {
        ESP_LOGE(TAG,"Player is initialized.");
        return MP_OBJ_NEW_SMALL_INT(-1);
    }
    
     return mp_const_none; 
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_player_init_obj, audio_player_init);

STATIC mp_obj_t audio_player_deinit(void)
{
    player_t *player = get_player_handle();
    if(player == NULL){
        ESP_LOGE(TAG,"Sorry, no player.");
        return MP_OBJ_NEW_SMALL_INT(-1);
    }
    audio_player_destroy();
    return mp_const_none; 
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_player_deinit_obj, audio_player_deinit);

STATIC mp_obj_t audio_play(mp_obj_t url)
{
    const char *_url = mp_obj_str_get_str(url);
    // ESP_LOGE(TAG, "%s", _url);
    player_t *player = get_player_handle();
    if(player == NULL){
        ESP_LOGE(TAG, "Please init the player first.");
        return MP_OBJ_NEW_SMALL_INT(-1);
    }

    if(player->player_status == INITIALIZED )
    {                   
        player->media_stream.content_type = MIME_UNKNOWN;      
        player->media_stream.eof = false;                                                         
                            
        player->url = _url;
        player->http_head = NULL;                    
        player->http_body = NULL;  
        player->http_body_len = 0;
        player->http_method = HTTP_METHOD_GET;
        clear_ringbuf(player);
        audio_player_begin();

        return MP_OBJ_NEW_SMALL_INT(0);
    }
    else{
        ESP_LOGE(TAG,"In playing status, you need stop it first.");
    }
    return MP_OBJ_NEW_SMALL_INT(1);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(audio_play_obj, audio_play);

STATIC mp_obj_t audio_resume(void)
{
    player_t *player = get_player_handle();
    if(player == NULL){
        ESP_LOGE(TAG,"Sorry, no player.");
        return MP_OBJ_NEW_SMALL_INT(-1);
    }

    if(player->player_status == PAUSED){
        audio_player_start();
        vTaskResume( mp3_decode_task_handel );
        vTaskResume( http_client_task_handel );
    }

    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_resume_obj, audio_resume);

STATIC mp_obj_t audio_stop(void)
{
    player_t *player = get_player_handle();
    if(player == NULL){
        ESP_LOGE(TAG,"Sorry, no player.");
        return MP_OBJ_NEW_SMALL_INT(-1);
    }

    audio_player_stop();
    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_stop_obj, audio_stop);

STATIC mp_obj_t audio_pause(void)
{
    player_t *player = get_player_handle();
    if(player == NULL){
        ESP_LOGE(TAG,"Sorry, no player.");
        return MP_OBJ_NEW_SMALL_INT(-1);
    }
    audio_player_pause();
    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_pause_obj, audio_pause);

STATIC mp_obj_t audio_volume(mp_obj_t Volume)
{
    player_t *player = get_player_handle();
    if(player == NULL){
        ESP_LOGE(TAG,"Sorry, no player.");
        return MP_OBJ_NEW_SMALL_INT(-1);
    }

    mp_int_t vol =  mp_obj_get_int(Volume);
    vol = (vol > 100)? 100 : vol;
    vol = (vol < 0)? 0 : vol;
    player->volume = pow(10, (MIN_VOL_OFFSET + vol / 2) / 20.0);
    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(audio_volume_obj, audio_volume);

STATIC mp_obj_t audio_get_status(void)
{
    player_t *player = get_player_handle();
    if(player == NULL){
        ESP_LOGE(TAG,"Sorry, no player.");
        return MP_OBJ_NEW_SMALL_INT(-1);
    }

    if(player->player_status != INITIALIZED){
        return MP_OBJ_NEW_SMALL_INT(1); 
    }     
    else{
        return MP_OBJ_NEW_SMALL_INT(0);
    }
    
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_get_status_obj, audio_get_status);

STATIC mp_obj_t audio_webtts_config(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args)
{
    player_t *player = get_player_handle();
    if(player == NULL){
        ESP_LOGE(TAG,"Please init player first.");
        return MP_OBJ_NEW_SMALL_INT(-1);
    }
    if(player->webtts_config_flag){
        ESP_LOGE(TAG, "Web tts is configed.");
        return MP_OBJ_NEW_SMALL_INT(-1);
    }

    enum { ARG_api_key, ARG_app_id, ARG_voice_name};
    static const mp_arg_t allowed_args[] = {
    { MP_QSTR_api_key,    MP_ARG_REQUIRED | MP_ARG_OBJ },
    { MP_QSTR_app_id,     MP_ARG_REQUIRED | MP_ARG_OBJ },
    { MP_QSTR_voice_name, MP_ARG_OBJ,  {.u_obj = MP_ROM_QSTR(MP_QSTR_aisxping)}},
    };
    // parse args
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    api_key = mp_obj_str_get_str(args[ARG_api_key].u_obj);

    char *src = calloc(500, sizeof(char));
    int out;
    size_t n = 0;
    char tmp1[100] = "{\"auf\":\"audio/L16;rate=16000\",\"aue\":\"lame\",\"voice_name\":\"";
    char tmp2[100] = "\",\"speed\":\"50\",\"volume\":\"100\",\"pitch\":\"0\",\"engine_type\":\"intp65\",\"text_type\":\"text\"}";
    sprintf(src, "%s%s%s", tmp1, mp_obj_str_get_str(args[ARG_voice_name].u_obj), tmp2);
    mbedtls_base64_encode(NULL, 0, &n, (const unsigned char *)src, strlen(src));
    char *digest = calloc(n, sizeof(char));  //资源在play_destroy()中释放
    mbedtls_base64_encode((unsigned char *)digest, n, (size_t *)&out, (const unsigned char *)src, strlen(src));   
    free(src);
    http_head[1].value = (const char*)digest;
    http_head[2].value = mp_obj_str_get_str(args[ARG_app_id].u_obj);

    player->webtts_config_flag = true;

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(audio_webtts_config_obj, 0, audio_webtts_config);

STATIC mp_obj_t audio_webtts(mp_obj_t body)
{
    player_t *player = get_player_handle();
    if(player == NULL){
        ESP_LOGE(TAG, "Please init the player first.");
        return MP_OBJ_NEW_SMALL_INT(-1);
    }
    if(!player->webtts_config_flag){
        ESP_LOGE(TAG, "Please config the web tts first.");
        return MP_OBJ_NEW_SMALL_INT(-1);
    }

    if(player->player_status == INITIALIZED)
    { 
        char *src = calloc(1000, sizeof(char));
        char *des = calloc(2000, sizeof(char)); //资源在http_client 中处理完body后释放
        char *checksum = calloc(40, sizeof(char)); //资源在http_client任务中处理完http head后释放。
        char *cur_time = calloc(15, sizeof(char));

        struct timeval tv;
        gettimeofday(&tv, NULL);
        sprintf(cur_time, "%ld", tv.tv_sec + 946656001);
        http_head[0].value = (const char *)cur_time;
        ESP_LOGE(TAG, "x-cur_time : %s", http_head[0].value);

        sprintf(src, "%s%s%s", api_key, http_head[0].value, http_head[1].value);
        mbedtls_md5_context md5_ctx;
        mbedtls_md5_init( &md5_ctx );
        mbedtls_md5_starts_ret( &md5_ctx );
        mbedtls_md5_update_ret(&md5_ctx, (const unsigned char *)src, strlen(src));
        vstr_t vstr;
        vstr_init_len(&vstr, 16);
        mbedtls_md5_finish_ret(&md5_ctx, (byte*)vstr.buf);
        mbedtls_md5_free(&md5_ctx);
        sprintf(checksum, "%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x",
                        vstr.buf[0],vstr.buf[1],vstr.buf[2],vstr.buf[3],vstr.buf[4],vstr.buf[5],vstr.buf[6],vstr.buf[7],
                        vstr.buf[8],vstr.buf[9],vstr.buf[10],vstr.buf[11],vstr.buf[12],vstr.buf[13],vstr.buf[14],vstr.buf[15]); 
        http_head[3].value = (const char *)checksum;
        // ESP_LOGE(TAG, "x-checksum : %s", http_head[3].value);

        player->http_head = http_head;                                                  
        player->url = "http://api.xfyun.cn/v1/service/v1/tts";

        memset(src, 0, 1000);
        sprintf(src,"%s%s", "text=", (const char *)mp_obj_str_get_str(body));
        urlencode(src, des);
        free(src);
        // ESP_LOGE(TAG, "%s", des);
        player->http_body = des; 
        player->http_body_len = strlen(des);
        player->http_method = HTTP_METHOD_POST; 
        player->media_stream.eof = false;
        clear_ringbuf(player);
        audio_player_begin();

        return MP_OBJ_NEW_SMALL_INT(0);
    }
    else{
        ESP_LOGE(TAG,"In playing status, you need stop it first.");
    }     
    return MP_OBJ_NEW_SMALL_INT(1);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(webtts_obj, audio_webtts);

STATIC const mp_map_elem_t mpython_audio_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_audio)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_player_init), (mp_obj_t)&audio_player_init_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_player_deinit), (mp_obj_t)&audio_player_deinit_obj},
	{MP_OBJ_NEW_QSTR(MP_QSTR_play), (mp_obj_t)&audio_play_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_resume), (mp_obj_t)&audio_resume_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_stop), (mp_obj_t)&audio_stop_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_pause), (mp_obj_t)&audio_pause_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_set_volume), (mp_obj_t)&audio_volume_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_player_status), (mp_obj_t)&audio_get_status_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_xunfei_tts_config), (mp_obj_t)&audio_webtts_config_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_xunfei_tts), (mp_obj_t)&webtts_obj},
};

STATIC MP_DEFINE_CONST_DICT(mpython_audio_locals_dict, mpython_audio_locals_dict_table);

const mp_obj_module_t mp_module_audio = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mpython_audio_locals_dict,
};