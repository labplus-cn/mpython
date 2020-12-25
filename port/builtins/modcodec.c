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
#include "wave_head.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_http_client.h"
#include "esp_task.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "freertos/timers.h"

#include <time.h>
#include <dirent.h>
#include "soc/io_mux_reg.h"
#include <math.h>
#include "audio_player.h"    
#include "helix_mp3_decoder.h"
#include "modcodec.h"
#include "audio_recorder.h"
#include "local_play.h"
#include "es8388.h"

// static const char *TAG = "audio";

/* ---------------player ------------------------*/
STATIC mp_obj_t audio_player_init(size_t n_args, const mp_obj_t *args)
{
    assert(0 <= n_args);

    #if !MICROPY_BUILDIN_DAC
    if (n_args == 1)
    {
        if(!es_i2c_obj){
            es_i2c_obj = (mp_obj_base_t *)args[0];
            audio_hal_codec_config_t cfg = AUDIO_CODEC_DEFAULT_CONFIG();
            es8388_init(cfg);
        }
    }
    else
        mp_raise_ValueError(MP_ERROR_TEXT("Need a i2c object param."));  
    #endif

    player_init();
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(audio_player_init_obj, 0, 1, audio_player_init);

STATIC mp_obj_t audio_player_deinit(void)
{
    player_deinit();
    return mp_const_none; 
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_player_deinit_obj, audio_player_deinit);

STATIC mp_obj_t audio_play(mp_obj_t url)
{
    const char *_url = mp_obj_str_get_str(url);
    // ESP_LOGE(TAG, "%s", _url);
    player_play(_url);
    
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(audio_play_obj, audio_play);

STATIC mp_obj_t audio_resume(void)
{
    player_resume();
    return mp_const_none;  
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_resume_obj, audio_resume);

STATIC mp_obj_t audio_stop(void)
{
    player_stop();
    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_stop_obj, audio_stop);

STATIC mp_obj_t audio_pause(void)
{
    player_pause();
    return  mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_pause_obj, audio_pause);

STATIC mp_obj_t audio_volume(mp_obj_t Volume)
{
    mp_int_t vol =  mp_obj_get_int(Volume);
    #if MICROPY_BUILDIN_DAC 
    player_set_volume(vol);
    #else
    es8388_set_voice_volume(vol);
    #endif
    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(audio_volume_obj, audio_volume);

STATIC mp_obj_t audio_get_status(void)
{
    player_status_t status = player_get_status();
    if(status == RUNNING || status == PAUSED){
        return MP_OBJ_NEW_SMALL_INT(1); 
    }     

    return MP_OBJ_NEW_SMALL_INT(0);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_get_status_obj, audio_get_status);

/* ------------------------recorder--------------------------*/
STATIC mp_obj_t audio_recorder_init(size_t n_args, const mp_obj_t *args)
{
    assert(0 <= n_args);

    #if !MICROPY_BUILDIN_DAC
    if (n_args == 1)
    {
        if(!es_i2c_obj){
            es_i2c_obj = (mp_obj_base_t *)args[0];
            audio_hal_codec_config_t cfg = AUDIO_CODEC_DEFAULT_CONFIG();
            es8388_init(cfg);
        }
    }
    else
        mp_raise_ValueError(MP_ERROR_TEXT("Need a i2c object param."));  
    #endif
    
    recorder_init();
    return mp_const_none; 
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(audio_recorder_init_obj, 0, 1, audio_recorder_init);

STATIC mp_obj_t audio_loudness(void)
{
    uint32_t loud = recorder_loudness();
    return MP_OBJ_NEW_SMALL_INT(loud); 
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_loudness_obj, audio_loudness);

STATIC mp_obj_t audio_record(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args)
{
    enum { ARG_file_name, ARG_record_time};
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_file_name,    MP_ARG_REQUIRED | MP_ARG_OBJ },
        { MP_QSTR_record_time,  MP_ARG_INT, {.u_int = 4} },
    };
    // parse args
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    recorder_record(mp_obj_str_get_str(args[ARG_file_name].u_obj), args[ARG_record_time].u_int); 

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(audio_record_obj, 0, audio_record);

STATIC mp_obj_t audio_recorder_deinit(void)
{
    recorder_deinit();
    
    return mp_const_none; 
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_recorder_deinit_obj, audio_recorder_deinit);

/* -------------xunfei--------------------*/
STATIC mp_obj_t audio_iat_config(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args)
{
    // enum {ARG_api_key, ARG_app_id, ARG_engine_type, ARG_aue};
    // static const mp_arg_t allowed_args[] = {
    //     { MP_QSTR_api_key,    MP_ARG_REQUIRED | MP_ARG_OBJ },
    //     { MP_QSTR_app_id,     MP_ARG_REQUIRED | MP_ARG_OBJ },
    //     { MP_QSTR_engine_type, MP_ARG_OBJ,  {.u_obj = MP_ROM_QSTR(MP_QSTR_sms16k)}},
    //     { MP_QSTR_aue, MP_ARG_OBJ,  {.u_obj = MP_ROM_QSTR(MP_QSTR_raw)}},
    // };
    // // parse args
    // mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    // api_key = mp_obj_str_get_str(args[ARG_api_key].u_obj);

    // recorder_t *recorder = get_recorder_handle();
    // if((recorder != NULL) && !(recorder->iat_config_flag))
    // {
    //     char *src = calloc(500, sizeof(char));
    //     int out;
    //     size_t n = 0;
    //     sprintf(src, "%s%s%s%s%s", "{\"aue\":\"", mp_obj_str_get_str(args[ARG_aue].u_obj), 
    //             "\",\"engine_type\":\"", mp_obj_str_get_str(args[ARG_engine_type].u_obj), "\"}");
    //     // ESP_LOGE(TAG, "%s", src);
    //     mbedtls_base64_encode(NULL, 0, &n, (const unsigned char *)src, strlen(src)); //get value n
    //     char *digest = calloc(n, sizeof(char));  //资源在http_client任务中处理完http head后释放。
    //     mbedtls_base64_encode((unsigned char *)digest, n, (size_t *)&out, (const unsigned char *)src, strlen(src));   
    //     http_head[1].value = (const char*)digest;  //x-param
    //     http_head[2].value = mp_obj_str_get_str(args[ARG_app_id].u_obj);
    //     free(src);

    //     recorder->iat_config_flag = true;
    //     recorder->iat_record_finish = false;
    // }
    // else{
    //     mp_warning(NULL, "Please init recorder first.");
    // }

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(audio_iat_config_obj, 0, audio_iat_config);

STATIC mp_obj_t audio_iat_record(mp_obj_t rec_time)
{
    // recorder_t *recorder = get_recorder_handle();
   
    // if(recorder != NULL){
    //     recorder->file_name = "tmp.pcm";
    //     recorder->recorde_time = mp_obj_get_int(rec_time) * 1000;
    //     iat_record(recorder->file_name); 
    //     recorder->iat_record_finish = true;
    //     // ESP_LOGE(TAG, "iat record finish.");
    // }
    // else{
    //     mp_warning(NULL, "Please init recorder first.");
    // }
    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(audio_iat_record_obj, audio_iat_record);

STATIC mp_obj_t audio_iat(void)
{
    // recorder_t *recorder = get_recorder_handle();
    // if(recorder != NULL && (recorder->iat_config_flag) && (recorder->iat_record_finish == true))
    // {
    //     char *src = calloc(300, sizeof(char));
    //     char *checksum = calloc(40, sizeof(char)); //资源在http_client任务中处理完http head后释放。
    //     char *cur_time = calloc(15, sizeof(char));

    //     struct timeval tv;
    //     gettimeofday(&tv, NULL);
    //     sprintf(cur_time, "%ld", tv.tv_sec + 946656001);
    //     http_head[0].value = (const char *)cur_time;
    //     // ESP_LOGE(TAG, "x-cur_time : %s", http_head[0].value);

    //     sprintf(src, "%s%s%s", api_key, http_head[0].value, http_head[1].value);
    //     mbedtls_md5_context md5_ctx;
    //     mbedtls_md5_init( &md5_ctx );
    //     mbedtls_md5_starts_ret( &md5_ctx );
    //     mbedtls_md5_update_ret(&md5_ctx, (const unsigned char *)src, strlen(src));
    //     free(src);
    //     vstr_t vstr;
    //     vstr_init_len(&vstr, 16);
    //     mbedtls_md5_finish_ret(&md5_ctx, (byte*)vstr.buf);
    //     mbedtls_md5_free(&md5_ctx);
    //     sprintf(checksum, "%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x",
    //                     vstr.buf[0],vstr.buf[1],vstr.buf[2],vstr.buf[3],vstr.buf[4],vstr.buf[5],vstr.buf[6],vstr.buf[7],
    //                     vstr.buf[8],vstr.buf[9],vstr.buf[10],vstr.buf[11],vstr.buf[12],vstr.buf[13],vstr.buf[14],vstr.buf[15]); 
    //     http_head[3].value = (const char *)checksum;
    //     // ESP_LOGE(TAG, "x-checksum : %s", http_head[3].value);

    //     // recorder->file_name = "tmp.pcm";
    //     // iat_record(recorder->file_name); 
    //     // // ESP_LOGE(TAG, "iat record finish.");

    //     http_param_t *http_param = get_http_param_handle();
    //     http_param->http_head = http_head;                                                 
    //     http_param->url = "http://api.xfyun.cn/v1/service/v1/iat"; 
    //     http_param->http_body_len = recorder->file_size;
    //     http_param->http_method = HTTP_METHOD_POST; 

    //     http_request_iat(recorder); //xunfei iat http request
    //     mp_obj_t return_json = mp_obj_new_str(http_param->http_read_buffer, strlen(http_param->http_read_buffer));
    //     free(http_param->http_read_buffer);
    //     return return_json;
    // }
    // else{
    //     mp_warning(NULL, "Please init recorder and config iat and record first.");
    // }
    
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_iat_obj, audio_iat);

STATIC mp_obj_t audio_webtts_config(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args)
{
    // player_t *player = get_player_handle();
    // if((player != NULL) && (!(player->webtts_config_flag)))
    // {
    //     enum { ARG_api_key, ARG_app_id, ARG_voice_name};
    //     static const mp_arg_t allowed_args[] = {
    //     { MP_QSTR_api_key,    MP_ARG_REQUIRED | MP_ARG_OBJ },
    //     { MP_QSTR_app_id,     MP_ARG_REQUIRED | MP_ARG_OBJ },
    //     { MP_QSTR_voice_name, MP_ARG_OBJ,  {.u_obj = MP_ROM_QSTR(MP_QSTR_aisxping)}},
    //     };
    //     // parse args
    //     mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    //     mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    //     api_key = mp_obj_str_get_str(args[ARG_api_key].u_obj);

    //     char *src = calloc(500, sizeof(char));
    //     int out;
    //     size_t n = 0;

    //     sprintf(src, "%s%s%s", "{\"auf\":\"audio/L16;rate=16000\",\"aue\":\"lame\",\"voice_name\":\"", 
    //             mp_obj_str_get_str(args[ARG_voice_name].u_obj), 
    //             "\",\"speed\":\"50\",\"volume\":\"100\",\"pitch\":\"50\",\"engine_type\":\"intp65\",\"text_type\":\"text\"}");
    //     mbedtls_base64_encode(NULL, 0, &n, (const unsigned char *)src, strlen(src));
    //     char *digest = calloc(n, sizeof(char));  //资源在play_destroy()中释放
    //     mbedtls_base64_encode((unsigned char *)digest, n, (size_t *)&out, (const unsigned char *)src, strlen(src));   
    //     free(src);
    //     http_head[1].value = (const char*)digest;
    //     http_head[2].value = mp_obj_str_get_str(args[ARG_app_id].u_obj);

    //     player->webtts_config_flag = true;
    // }
    // else
    // {
    //     mp_warning(NULL, "Please init player first.");
    // }
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(audio_webtts_config_obj, 0, audio_webtts_config);

STATIC mp_obj_t audio_webtts(mp_obj_t body)
{
    // player_t *player = get_player_handle();
    // if((player != NULL) && (player->webtts_config_flag))
    // {
    //     if(player->player_status != INITIALIZED){
    //         player_stop();
    //     }

    //     char *src = calloc(1000, sizeof(char));
    //     char *des = calloc(2000, sizeof(char)); //资源在http_client 中处理完body后释放
    //     char *checksum = calloc(40, sizeof(char)); //资源在http_client任务中处理完http head后释放。
    //     char *cur_time = calloc(15, sizeof(char));

    //     struct timeval tv;
    //     gettimeofday(&tv, NULL);
    //     sprintf(cur_time, "%ld", tv.tv_sec + 946656001);
    //     http_head[0].value = (const char *)cur_time;
    //     // ESP_LOGE(TAG, "x-cur_time : %s", http_head[0].value);

    //     sprintf(src, "%s%s%s", api_key, http_head[0].value, http_head[1].value);
    //     mbedtls_md5_context md5_ctx;
    //     mbedtls_md5_init( &md5_ctx );
    //     mbedtls_md5_starts_ret( &md5_ctx );
    //     mbedtls_md5_update_ret(&md5_ctx, (const unsigned char *)src, strlen(src));
    //     vstr_t vstr;
    //     vstr_init_len(&vstr, 16);
    //     mbedtls_md5_finish_ret(&md5_ctx, (byte*)vstr.buf);
    //     mbedtls_md5_free(&md5_ctx);
    //     sprintf(checksum, "%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x",
    //                     vstr.buf[0],vstr.buf[1],vstr.buf[2],vstr.buf[3],vstr.buf[4],vstr.buf[5],vstr.buf[6],vstr.buf[7],
    //                     vstr.buf[8],vstr.buf[9],vstr.buf[10],vstr.buf[11],vstr.buf[12],vstr.buf[13],vstr.buf[14],vstr.buf[15]); 
    //     http_head[3].value = (const char *)checksum;
    //     // ESP_LOGE(TAG, "x-checksum : %s", http_head[3].value);

    //     memset(src, 0, 1000);
    //     sprintf(src,"%s%s", "text=", (const char *)mp_obj_str_get_str(body));
    //     urlencode(src, des);
    //     free(src);

    //     player->eof = false;
    //     player->content_type = MIME_UNKNOWN;                                                                            
    //     player->url = "http://api.xfyun.cn/v1/service/v1/tts";
    //     // ESP_LOGE(TAG, "%s", des);
    //     http_param_t *http_param = get_http_param_handle();
    //     http_param->url = "http://api.xfyun.cn/v1/service/v1/tts";
    //     http_param->http_head = http_head; 
    //     http_param->http_body = des; 
    //     http_param->http_body_len = strlen(des);
    //     http_param->http_method = HTTP_METHOD_POST; 
    //     // player_begin();
    // }    
    // else
    // {
    //     mp_warning(NULL, "Please init player or config web tts first.");
    // }
    
    return mp_const_none;
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
    {MP_OBJ_NEW_QSTR(MP_QSTR_recorder_init), (mp_obj_t)&audio_recorder_init_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_loudness), (mp_obj_t)&audio_loudness_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_record), (mp_obj_t)&audio_record_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_recorder_deinit), (mp_obj_t)&audio_recorder_deinit_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_xunfei_iat_config), (mp_obj_t)&audio_iat_config_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_xunfei_iat_record), (mp_obj_t)&audio_iat_record_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_xunfei_iat), (mp_obj_t)&audio_iat_obj},
};

STATIC MP_DEFINE_CONST_DICT(mpython_audio_locals_dict, mpython_audio_locals_dict_table);

const mp_obj_module_t mp_module_audio = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mpython_audio_locals_dict,
};