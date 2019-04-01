/*
 * http_client.h
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#ifndef _HTTP_CLIENT_H_
#define _HTTP_CLIENT_H_

typedef struct{
    const char *key;
    const char *value;
}HTTP_HEAD_VAL;

void http_request_task(void *pvParameters);

#endif //end _HTTP_CLIENT_H_
