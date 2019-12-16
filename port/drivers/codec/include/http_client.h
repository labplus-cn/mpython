/*
 * http_client.h
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#ifndef _HTTP_CLIENT_H_
#define _HTTP_CLIENT_H_
#include "audio_player.h"

typedef struct{
    const char *key;
    const char *value;
}HTTP_HEAD_VAL;

typedef struct{
    HTTP_HEAD_VAL *http_head;
    char *http_body;
    int http_body_len;
    esp_http_client_method_t http_method;
    char *http_read_buffer;
    content_type_t content_type;
    uint32_t content_size;
    uint32_t has_read_size;
}http_param_t;

int http_init();
void http_deinit();
void http_request_task(void *pvParameters);
http_param_t *get_http_param_handle();
void http_param_handle_destroy();
int http_request_iat(void *data);

#endif //end _HTTP_CLIENT_H_
