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
    const char *url;
    HTTP_HEAD_VAL *http_head;
    char *http_body;
    int http_body_len;
    esp_http_client_method_t http_method;
    char *http_read_buffer;
    content_type_t content_type;
}http_param_t;

void http_request_task(void *pvParameters);
void init_http_param_handle(http_param_t *http_param);
void http_param_handle_destroy();
http_param_t *get_http_param_handle();
int http_request_iat(void *data);

#endif //end _HTTP_CLIENT_H_
