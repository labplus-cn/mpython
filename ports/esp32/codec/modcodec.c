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
#include "esp_task.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "freertos/ringbuf.h"
#include "freertos/timers.h"

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
#include "audio_recorder.h"
#include "local_file.h"
#include "driver/i2s.h"
#include "driver/adc.h"
#include "wav_head.h"

//static const char *TAG = "audio";

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

STATIC void record_to_file(void)
{
    renderer_config_t *renderer = renderer_get();
    recorder_t *recorder = get_recorder_handle();

    mp_obj_t F = file_open(recorder->file_name, "w");
    int write_bytes;
    uint8_t *read_buff = calloc(renderer->i2s_read_buff_size, sizeof(uint8_t));
    uint8_t *write_buff = calloc(renderer->i2s_read_buff_size, sizeof(uint8_t));
    wav_header_t *wav_header = calloc(1, sizeof(wav_header_t));
    wav_head_init(wav_header, renderer->sample_rate, renderer->bit_depth, renderer->i2s_channal_nums, 32 * recorder->recorde_time);
    file_write(F, &write_bytes, (uint8_t *)wav_header, sizeof(wav_header_t));
    // ESP_LOGE(TAG, "i2s_read_buff_size: %d, datasize:%d", renderer->i2s_read_buff_size, 32 * recorder->recorde_time); //samplerate:16000 32byts/ms
    free(wav_header);
    int i = 0;
    uint16_t record_times = 32 * recorder->recorde_time / renderer->i2s_read_buff_size; //caculate record loops
    // ESP_LOGE(TAG, "i2s_read times: %d", record_times); 
    renderer_adc_enable(renderer->i2s_num);    
    while(i < record_times)
    {
        renderer_read_raw(read_buff, renderer->i2s_read_buff_size);
        i2s_adc_data_scale(write_buff, read_buff, renderer->i2s_read_buff_size);
        file_write(F, &write_bytes, write_buff, renderer->i2s_read_buff_size);
        i++;
    }
    renderer_adc_disable(renderer->i2s_num);
    free(read_buff);
    free(write_buff);
    file_close(F);
}

STATIC void iat_record(const char *file_name)
{
    renderer_config_t *renderer = renderer_get();
    recorder_t *recorder = get_recorder_handle();

    mp_obj_t F = file_open(file_name, "wb");
    int write_bytes; //,read_bytes;
    char *read_buff = calloc(renderer->i2s_read_buff_size, sizeof(uint8_t));
    uint8_t *write_buff = calloc(renderer->i2s_read_buff_size + 2000, sizeof(uint8_t));
    char *des = calloc(renderer->i2s_read_buff_size + 2000, sizeof(char));

    char *tmp = "audio=";
    urlencode(tmp, read_buff);
    file_write(F, &write_bytes, (uint8_t *)read_buff, (uint16_t)strlen(read_buff));
    recorder->file_size = strlen(tmp);
     
    int out;
    size_t n = 0;  
    int i = 0;
    uint16_t record_times = 32 * 2000 / renderer->i2s_read_buff_size; //caculate record loops
    renderer_adc_enable(renderer->i2s_num); 
    while(i < record_times)
    {
        renderer_read_raw((uint8_t *)read_buff, renderer->i2s_read_buff_size);
        i2s_adc_data_scale((uint8_t *)read_buff, (uint8_t *)read_buff, renderer->i2s_read_buff_size);
        mbedtls_base64_encode(NULL, 0, &n, (const unsigned char *)read_buff, renderer->i2s_read_buff_size);
        memset(write_buff, 0, renderer->i2s_read_buff_size + 2000);
        mbedtls_base64_encode((unsigned char *)write_buff, n, (size_t *)&out, (const unsigned char *)read_buff, renderer->i2s_read_buff_size); 
        memset(des, 0, renderer->i2s_read_buff_size + 2000);
        urlencode((char *)write_buff, des);
        //ESP_LOGE(TAG, "%s", des);
        file_write(F, &write_bytes, (uint8_t *)des, strlen(des));  
        recorder->file_size += write_bytes; 
        i++;
    } 
    // ESP_LOGE(TAG, "%d", recorder->file_size);

    /* test base64 and urlencode result. compare with xunfei iat example encode result*/
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

    renderer_adc_disable(renderer->i2s_num);
    free(read_buff);
    free(write_buff);
    free(des);
    file_close(F);
}

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
        /* 1. Create player.*/
        player_t *player = calloc(1, sizeof(player_t));
        player->command  = CMD_NONE;                  
        player->player_status = INITIALIZED;       
        player->buffer_pref = BUF_PREF_SAFE;                          
        player->ringbuf_size = RINGBUF_SIZE;          
        //player->ringbuf_sem = xSemaphoreCreateMutex(); 
        player->media_stream.content_type = MIME_UNKNOWN;                                                                                
        player->media_stream.eof = false; 
        player->file_type = UNKNOW_TYPE;
        player->volume = pow(10, (MIN_VOL_OFFSET + 80 / 2) / 20.0); 
        //player->ringbuf_eventGroup = xEventGroupCreate();
        player->buf_handle = xRingbufferCreate(RINGBUF_SIZE, RINGBUF_TYPE_BYTEBUF);
        init_palyer_handle(player);
        // ESP_LOGE(TAG, "1. Create player, RAM left  %d", esp_get_free_heap_size());

        /* 2. Create renderer. */
        renderer_config_t *renderer_config = calloc(1, sizeof(renderer_config_t));
        renderer_config->bit_depth  = I2S_BITS_PER_SAMPLE_16BIT;
        renderer_config->i2s_num = I2S_NUM_0;
        renderer_config->sample_rate = 44100;
        renderer_config->sample_rate_modifier = 1.0;
        renderer_config->mode = DAC_BUILT_IN; 
        renderer_config->i2s_channal_nums = 2;                                                
        renderer_init(renderer_config); //I2S参数配置
        // ESP_LOGE(TAG, "2. Create renderer, RAM left: %d", esp_get_free_heap_size());
        /* 3. Create http raram handle.*/
        http_param_t *http_param = calloc(1, sizeof(http_param_t));
        init_http_param_handle(http_param);
    }
    else
    {
        mp_raise_msg(&mp_type_RuntimeError, "Player is initialized.");
    }
    
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_player_init_obj, audio_player_init);

STATIC mp_obj_t audio_player_deinit(void)
{
    player_t *player = get_player_handle();
    if(player != NULL){
        if(player->player_status != INITIALIZED || player->player_status != UNINITIALIZED)
            audio_player_stop();
        audio_player_destroy();  
    }
    else{
        mp_raise_msg(&mp_type_RuntimeError, "Sorry, player is in playing status, can't release.");
    }
    return mp_const_none; 
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_player_deinit_obj, audio_player_deinit);

STATIC mp_obj_t audio_play(mp_obj_t url)
{
    const char *_url = mp_obj_str_get_str(url);
    // ESP_LOGE(TAG, "%s", _url);
    player_t *player = get_player_handle();
    if(player != NULL){
        if(player->player_status != INITIALIZED){
            audio_player_stop();
        }
                    
        player->media_stream.eof = false; 
        player->media_stream.content_type = MIME_UNKNOWN;                                                                            
        player->url = _url;
        clear_ringbuf(player);

        http_param_t *http_param = get_http_param_handle();    
        http_param->url = _url;
        http_param->http_head = NULL;                    
        http_param->http_body = NULL;  
        http_param->http_body_len = 0;
        http_param->http_method = HTTP_METHOD_GET; 
        audio_player_begin();
    }
    else
    {
        mp_raise_ValueError("no player, please init player first");
    }
    
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(audio_play_obj, audio_play);

STATIC mp_obj_t audio_resume(void)
{
    player_t *player = get_player_handle();
    if(player != NULL){
        if(player->player_status == PAUSED){
            audio_player_start();
            vTaskResume( mp3_decode_task_handel );
            vTaskResume( http_client_task_handel );
        }
    }
    else
    {
        mp_raise_ValueError("No player.");
    }   
    return mp_const_none;  
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_resume_obj, audio_resume);

STATIC mp_obj_t audio_stop(void)
{
    player_t *player = get_player_handle();
    if(player != NULL){
        audio_player_stop();
    }
    else
    {
        mp_raise_ValueError("No player.");
    }
    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_stop_obj, audio_stop);

STATIC mp_obj_t audio_pause(void)
{
    player_t *player = get_player_handle();
    if(player != NULL)
    {
        audio_player_pause();
    }
    else
    {
        mp_raise_ValueError("No player.");
    }
    return  mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_pause_obj, audio_pause);

STATIC mp_obj_t audio_volume(mp_obj_t Volume)
{
    player_t *player = get_player_handle();
    if(player != NULL){
        mp_int_t vol =  mp_obj_get_int(Volume);
        vol = (vol > 100)? 100 : vol;
        vol = (vol < 0)? 0 : vol;
        player->volume = pow(10, (MIN_VOL_OFFSET + vol / 2) / 20.0);
    }
    return mp_const_none;   
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(audio_volume_obj, audio_volume);

STATIC mp_obj_t audio_get_status(void)
{
    player_t *player = get_player_handle();
    if(player != NULL){
        if(player->player_status != INITIALIZED){
            return MP_OBJ_NEW_SMALL_INT(1); 
        }     
        else{
            return MP_OBJ_NEW_SMALL_INT(0);
        } 
    }
    return MP_OBJ_NEW_SMALL_INT(0);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_get_status_obj, audio_get_status);

STATIC mp_obj_t audio_webtts_config(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args)
{
    player_t *player = get_player_handle();
    if((player != NULL) && (!(player->webtts_config_flag)))
    {
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

        sprintf(src, "%s%s%s", "{\"auf\":\"audio/L16;rate=16000\",\"aue\":\"lame\",\"voice_name\":\"", 
                mp_obj_str_get_str(args[ARG_voice_name].u_obj), 
                "\",\"speed\":\"50\",\"volume\":\"100\",\"pitch\":\"50\",\"engine_type\":\"intp65\",\"text_type\":\"text\"}");
        mbedtls_base64_encode(NULL, 0, &n, (const unsigned char *)src, strlen(src));
        char *digest = calloc(n, sizeof(char));  //资源在play_destroy()中释放
        mbedtls_base64_encode((unsigned char *)digest, n, (size_t *)&out, (const unsigned char *)src, strlen(src));   
        free(src);
        http_head[1].value = (const char*)digest;
        http_head[2].value = mp_obj_str_get_str(args[ARG_app_id].u_obj);

        player->webtts_config_flag = true;
    }
    else
    {
        mp_raise_ValueError("Not init player or config completef.");
    }
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(audio_webtts_config_obj, 0, audio_webtts_config);

STATIC mp_obj_t audio_webtts(mp_obj_t body)
{
    player_t *player = get_player_handle();
    if((player != NULL) && (player->webtts_config_flag))
    {
        if(player->player_status != INITIALIZED){
            audio_player_stop();
        }

        char *src = calloc(1000, sizeof(char));
        char *des = calloc(2000, sizeof(char)); //资源在http_client 中处理完body后释放
        char *checksum = calloc(40, sizeof(char)); //资源在http_client任务中处理完http head后释放。
        char *cur_time = calloc(15, sizeof(char));

        struct timeval tv;
        gettimeofday(&tv, NULL);
        sprintf(cur_time, "%ld", tv.tv_sec + 946656001);
        http_head[0].value = (const char *)cur_time;
        // ESP_LOGE(TAG, "x-cur_time : %s", http_head[0].value);

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

        memset(src, 0, 1000);
        sprintf(src,"%s%s", "text=", (const char *)mp_obj_str_get_str(body));
        urlencode(src, des);
        free(src);

        player->media_stream.eof = false;
        player->media_stream.content_type = MIME_UNKNOWN;                                                                            
        player->url = "http://api.xfyun.cn/v1/service/v1/tts";
        // ESP_LOGE(TAG, "%s", des);
        http_param_t *http_param = get_http_param_handle();
        http_param->url = "http://api.xfyun.cn/v1/service/v1/tts";
        http_param->http_head = http_head; 
        http_param->http_body = des; 
        http_param->http_body_len = strlen(des);
        http_param->http_method = HTTP_METHOD_POST; 
        clear_ringbuf(player);
        audio_player_begin();
    }    
    else
    {
        mp_raise_ValueError("Please init player and config tts first.");
    }
    
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(webtts_obj, audio_webtts);

STATIC mp_obj_t audio_recorder_init(void)
{
    recorder_t *recorder = get_recorder_handle();
    if(recorder == NULL){
        /* 1. Creat recorder.*/
        recorder_t *Recorder = calloc(1, sizeof(recorder_t));
        init_recorder_handle(Recorder);

        /* 2. Create renderer. */
        renderer_config_t *renderer_config = calloc(1, sizeof(renderer_config_t));
        renderer_config->bit_depth  = I2S_BITS_PER_SAMPLE_16BIT;
        renderer_config->i2s_num = I2S_NUM_0;
        renderer_config->adc_num = ADC_UNIT_1;
        renderer_config->adc_channel_num = ADC1_CHANNEL_2;
        renderer_config->sample_rate = 16000;
        renderer_config->sample_rate_modifier = 1.0;
        renderer_config->mode = ADC_BUILT_IN; 
        renderer_config->i2s_channal_nums = 1;    
        renderer_config->i2s_read_buff_size = 3*1024;                                          
        renderer_init(renderer_config); 
        // ESP_LOGE(TAG, "Create renderer, RAM left: %d", esp_get_free_heap_size());
        renderer_start();
        /* 3. Create http param handle.*/
        http_param_t *http_param = calloc(1, sizeof(http_param_t));
        init_http_param_handle(http_param);
    }
    else
    {
        mp_raise_msg(&mp_type_RuntimeError, "Recorder is initialized.");
    }
    
    return mp_const_none; 
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_recorder_init_obj, audio_recorder_init);

STATIC mp_obj_t audio_loudness(void)
{
    renderer_config_t *renderer = renderer_get();
    uint32_t len = 32; //320bytes: record 10ms
    uint16_t *d_buff = calloc(len/2, sizeof(uint16_t));
    uint8_t *read_buff = calloc(len, sizeof(uint8_t)); 

    renderer_adc_enable(renderer->i2s_num);    
    renderer_read_raw(read_buff, len);
    renderer_adc_disable(renderer->i2s_num);

    i2s_adc_data_scale1(d_buff, read_buff, len);
    audio_recorder_quicksort(d_buff, len/2, 0, len/2 - 1);
    // for(int i = 0; i < len/2; i++)
    //     printf("%d\n", d_buff[i]);
    // int i;
    // uint32_t sum1 = 0;
    // uint32_t sum2 = 0;
    // for(i = 0; i < 10; i++){
    //     sum1 += d_buff[i+1];
    //     sum2 += d_buff[len/2 - 2 - i];
    // }

    // uint32_t sum = (sum2 -sum1)/10;
    uint32_t sum = d_buff[len/2-2] - d_buff[1];
    free(read_buff);
    free(d_buff);
    return MP_OBJ_NEW_SMALL_INT(sum);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_loudness_obj, audio_loudness);

STATIC mp_obj_t audio_record(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args)
{
    enum { ARG_file_name, ARG_record_time};
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_file_name,    MP_ARG_REQUIRED | MP_ARG_OBJ },
        { MP_QSTR_record_time,  MP_ARG_INT, {.u_int = 5} },
    };
    // parse args
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    recorder_t *recorder = get_recorder_handle();
    recorder->file_name = mp_obj_str_get_str(args[ARG_file_name].u_obj);
    recorder->recorde_time = args[ARG_record_time].u_int * 1000;

    record_to_file();  

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(audio_record_obj, 0, audio_record);

STATIC mp_obj_t audio_iat_config(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args)
{
    enum {ARG_api_key, ARG_app_id, ARG_engine_type, ARG_aue};
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_api_key,    MP_ARG_REQUIRED | MP_ARG_OBJ },
        { MP_QSTR_app_id,     MP_ARG_REQUIRED | MP_ARG_OBJ },
        { MP_QSTR_engine_type, MP_ARG_OBJ,  {.u_obj = MP_ROM_QSTR(MP_QSTR_sms16k)}},
        { MP_QSTR_aue, MP_ARG_OBJ,  {.u_obj = MP_ROM_QSTR(MP_QSTR_raw)}},
    };
    // parse args
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);
    api_key = mp_obj_str_get_str(args[ARG_api_key].u_obj);

    recorder_t *recorder = get_recorder_handle();
    if((recorder != NULL) && !(recorder->iat_config_flag))
    {
        char *src = calloc(500, sizeof(char));
        int out;
        size_t n = 0;
        sprintf(src, "%s%s%s%s%s", "{\"aue\":\"", mp_obj_str_get_str(args[ARG_aue].u_obj), 
                "\",\"engine_type\":\"", mp_obj_str_get_str(args[ARG_engine_type].u_obj), "\"}");
        // ESP_LOGE(TAG, "%s", src);
        mbedtls_base64_encode(NULL, 0, &n, (const unsigned char *)src, strlen(src)); //get value n
        char *digest = calloc(n, sizeof(char));  //资源在http_client任务中处理完http head后释放。
        mbedtls_base64_encode((unsigned char *)digest, n, (size_t *)&out, (const unsigned char *)src, strlen(src));   
        http_head[1].value = (const char*)digest;  //x-param
        http_head[2].value = mp_obj_str_get_str(args[ARG_app_id].u_obj);
        free(src);

        recorder->iat_config_flag = true;
    }
    else{
        mp_raise_ValueError("Not init recorder or config completef.");
    }

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(audio_iat_config_obj, 0, audio_iat_config);

STATIC mp_obj_t audio_iat(void)
{
    recorder_t *recorder = get_recorder_handle();
    if(recorder != NULL && (recorder->iat_config_flag))
    {
        char *src = calloc(300, sizeof(char));
        char *checksum = calloc(40, sizeof(char)); //资源在http_client任务中处理完http head后释放。
        char *cur_time = calloc(15, sizeof(char));

        struct timeval tv;
        gettimeofday(&tv, NULL);
        sprintf(cur_time, "%ld", tv.tv_sec + 946656001);
        http_head[0].value = (const char *)cur_time;
        // ESP_LOGE(TAG, "x-cur_time : %s", http_head[0].value);

        sprintf(src, "%s%s%s", api_key, http_head[0].value, http_head[1].value);
        mbedtls_md5_context md5_ctx;
        mbedtls_md5_init( &md5_ctx );
        mbedtls_md5_starts_ret( &md5_ctx );
        mbedtls_md5_update_ret(&md5_ctx, (const unsigned char *)src, strlen(src));
        free(src);
        vstr_t vstr;
        vstr_init_len(&vstr, 16);
        mbedtls_md5_finish_ret(&md5_ctx, (byte*)vstr.buf);
        mbedtls_md5_free(&md5_ctx);
        sprintf(checksum, "%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x",
                        vstr.buf[0],vstr.buf[1],vstr.buf[2],vstr.buf[3],vstr.buf[4],vstr.buf[5],vstr.buf[6],vstr.buf[7],
                        vstr.buf[8],vstr.buf[9],vstr.buf[10],vstr.buf[11],vstr.buf[12],vstr.buf[13],vstr.buf[14],vstr.buf[15]); 
        http_head[3].value = (const char *)checksum;
        // ESP_LOGE(TAG, "x-checksum : %s", http_head[3].value);

        recorder->file_name = "tmp.pcm";
        iat_record(recorder->file_name); 
        // ESP_LOGE(TAG, "iat record finish.");

        http_param_t *http_param = get_http_param_handle();
        http_param->http_head = http_head;                                                 
        http_param->url = "http://api.xfyun.cn/v1/service/v1/iat"; 
        http_param->http_body_len = recorder->file_size;
        http_param->http_method = HTTP_METHOD_POST; 

        http_request_iat(recorder); //xunfei iat http request
        mp_obj_t return_json = mp_obj_new_str(http_param->http_read_buffer, strlen(http_param->http_read_buffer));
        free(http_param->http_read_buffer);
        return return_json;
    }
    else{
        mp_raise_ValueError("Please init recorder and config iat first.");
    }
    
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_iat_obj, audio_iat);

STATIC mp_obj_t audio_recorder_deinit(void)
{
    audio_recorder_destroy();
    
    return mp_const_none; 
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(audio_recorder_deinit_obj, audio_recorder_deinit);

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
    {MP_OBJ_NEW_QSTR(MP_QSTR_xunfei_iat), (mp_obj_t)&audio_iat_obj},
};

STATIC MP_DEFINE_CONST_DICT(mpython_audio_locals_dict, mpython_audio_locals_dict_table);

const mp_obj_module_t mp_module_audio = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mpython_audio_locals_dict,
};