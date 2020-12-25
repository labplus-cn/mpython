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
#include <time.h>
#include "esp_system.h"
#include "timeutils.h"
#include "esp_http_client.h"
#include "esp_task.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "freertos/ringbuf.h"
#include "freertos/timers.h"

#include <dirent.h>
#include "soc/io_mux_reg.h"
#include <math.h>
#include "audio_player.h"    
#include "http_client.h"
#include "url_codec.h"
#include "mbedtls/version.h"
#include "mbedtls/md5.h"
#include "mbedtls/base64.h"
#include "mbedtls/sha256.h"
#include "driver/i2s.h"
#include "url_codec.h"
// #include "cJSON.h"
#include "esp_websocket_client.h"
#include "websocket_client.h"


static const char *TAG = "xunfeiAI";
typedef enum{
    TTS = 1,
    IAT,
}VO_MODE;

char *week[] = {"Mon, ", "Tues, ", "Wed, ", "Thur, ","Fri, ", "Sat, ","Sun, "};
char *month[] = {"", " Jan ", " Feb ", " Mar ", " Apr "," May ", " June "," July ", " Aug ", " Sept ", " Oct "," Nov ", " Dec "};

typedef struct{
    char *appid;
    char *apikey;
    char *APISecret;
    VO_MODE mode;
    char *url;
}ws_param_t;

ws_param_t ws_param = {
    .appid = NULL,
    .apikey = NULL,
    .APISecret = NULL,
    .url = NULL
};

esp_websocket_client_handle_t ws_client_handle = NULL;

STATIC void hmac_sha256(const char *msg, const char *key, unsigned char out[32])
{
    uint8_t k_ipad[64];
    uint8_t k_opad[64];
    int i;
    mbedtls_sha256_context context;
    uint8_t key_len = strlen(key);
    uint16_t msg_len = strlen(msg);

    memset(k_ipad, 0, sizeof k_ipad);
    memset(k_opad, 0, sizeof k_opad);
    memcpy(k_ipad, key, key_len);
    memcpy(k_opad, key, key_len);

    for (i = 0; i < 64; i++) 
    {
        k_ipad[i] ^= 0x36;
        k_opad[i] ^= 0x5c;
    }
    mbedtls_sha256_init(&context);
    mbedtls_sha256_starts_ret(&context, 0);
    mbedtls_sha256_update_ret(&context, k_ipad, 64);
    mbedtls_sha256_update(&context, (const unsigned char *)msg, msg_len);
    mbedtls_sha256_finish_ret(&context, out);

    mbedtls_sha256_init(&context);
    mbedtls_sha256_starts_ret(&context, 0);
    mbedtls_sha256_update_ret(&context, k_opad, 64);
    mbedtls_sha256_update(&context, out, 32);
    mbedtls_sha256_finish(&context, out);
}

STATIC void get_date(char *date)
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    timeutils_struct_time_t tm;
    timeutils_seconds_since_2000_to_struct_time(tv.tv_sec, &tm);
    // date: Tue, 15 Oct 2019 07:00:50 GMT 
    sprintf(date, "%s%02d%s%d%s%02d%s%02d%s%02d%s", week[tm.tm_wday], tm.tm_mday, month[tm.tm_mon], tm.tm_year, " ",tm.tm_hour,":", tm.tm_min, ":", tm.tm_sec, " GMT");
}

STATIC void record_to_file(void)
{

}

STATIC mp_obj_t xunfei_iat_init(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args)
{
    enum { ARG_app_id, ARG_api_key, ARG_api_secret, ARG_text, ARG_api_language};
    static const mp_arg_t allowed_args[] = {
    { MP_QSTR_app_id,        MP_ARG_REQUIRED | MP_ARG_OBJ },
    { MP_QSTR_api_key,       MP_ARG_REQUIRED | MP_ARG_OBJ },
    { MP_QSTR_api_secret,    MP_ARG_REQUIRED | MP_ARG_OBJ },
    { MP_QSTR_text,          MP_ARG_REQUIRED | MP_ARG_OBJ },
    { MP_QSTR_language,      MP_ARG_KW_ONLY | MP_ARG_OBJ , {.u_obj = MP_ROM_QSTR(MP_QSTR_zh_cn)}},
    // { MP_QSTR_api_vcn,       MP_ARG_OBJ , {.u_obj = MP_ROM_QSTR(MP_QSTR_xiaoyan)}},
    };
    // parse args
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args); 

    esp_log_level_set("*", ESP_LOG_ERROR);

    char *url = "wss://ws-api.xfyun.cn/v2/iat";
    // 生成RFC1123格式的时间戳 
    char *date = calloc(40, sizeof(char));
    get_date(date);

    // 拼接字符串
    char *signature_origin = calloc(200, sizeof(char));
    sprintf(signature_origin, "%s%s%s%s%s", "host: ws-api.xfyun.cn\n", "date: ", date, "\n", "GET /v2/iat HTTP/1.1");
    // ESP_LOGE(TAG, "%s", signature_origin);

    // 进行hmac-sha256进行加密
    unsigned char o[32];
    const char *app_sec = mp_obj_str_get_str(args[ARG_api_secret].u_obj);
    hmac_sha256(signature_origin, app_sec, o);
    free(signature_origin);

    int out;
    size_t n = 0; 
    mbedtls_base64_encode(NULL, 0, &n, (const unsigned char *)o, 32);
    unsigned char signature_sha[n];
    mbedtls_base64_encode(signature_sha, n, (size_t *)&out, (const unsigned char *)o, 32); 
    // ESP_LOGE(TAG, "base64: %s", (char *)signature_sha);
    
    char *authorization_origin = calloc(200, sizeof(char));
    const char *apikey =  mp_obj_str_get_str(args[ARG_api_key].u_obj);
    sprintf(authorization_origin, "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"", apikey,  "hmac-sha256", "host date request-line", signature_sha); 
    // ESP_LOGE(TAG, "authorization_origin: %s", authorization_origin);
    n = 0;
    size_t authorization_origin_len = strlen(authorization_origin);
    mbedtls_base64_encode(NULL, 0, &n, (const unsigned char *)authorization_origin, authorization_origin_len);
    unsigned char *authorization = calloc(n, sizeof(unsigned char));
    mbedtls_base64_encode(authorization, n, (size_t *)&out, (const unsigned char *)authorization_origin, authorization_origin_len); 
    ESP_LOGE(TAG, "authorization base64: %s", (char *)authorization);

    char *v = calloc(500, sizeof(char));
    char *p = calloc(500, sizeof(char));
    // 将请求的鉴权参数组合为字典,转为请求参数格式后，执行urlencode
    // v = {
    //     "authorization": authorization,
    //     "date": date,
    //     "host": "ws-api.xfyun.cn"
    // }
    sprintf(v, "authorization=%s&date=%s&host=ws-api.xfyun.cn", authorization, date);
    // ESP_LOGE(TAG, "authorization param: %s", v); 
    free(authorization);
    urlencode(v, p);

    memset(v, 0, 500);
    // 合并成url url = url + "?" + urlencode(v)
    sprintf(v, "%s?%s", url, p);
    ws_param.url = v;
    ESP_LOGE(TAG, "authorization param: %s", v);
    free(date);
    free(p);

    websocket_client_start(v);

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(xunfei_iat_init_obj, 4, xunfei_iat_init);


STATIC mp_obj_t xunfei_iat(mp_obj_t url)
{

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(xunfei_iat_obj, xunfei_iat);

STATIC mp_obj_t xunfei_tts(void)
{
    return MP_OBJ_NEW_SMALL_INT(0);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(xunfei_tts_obj, xunfei_tts);

STATIC const mp_map_elem_t mpython_xunfeiAI_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_xunfeiAI)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_xunfei_iat_init), (mp_obj_t)&xunfei_iat_init_obj},
	{MP_OBJ_NEW_QSTR(MP_QSTR_xunfei_tts), (mp_obj_t)&xunfei_tts_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_xunfei_iat), (mp_obj_t)&xunfei_iat_obj},
};

STATIC MP_DEFINE_CONST_DICT(mpython_xunfeiAI_locals_dict, mpython_xunfeiAI_locals_dict_table);

const mp_obj_module_t mp_module_xunfeiAI = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mpython_xunfeiAI_locals_dict,
};