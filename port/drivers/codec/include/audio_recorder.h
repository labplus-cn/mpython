/*
 * audio_player.h
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#ifndef INCLUDE_AUDIO_RECORDER_H_
#define INCLUDE_AUDIO_RECORDER_H_

#include <sys/types.h>
#include "audio_renderer.h"
#include "freertos/semphr.h"
#include "freertos/timers.h"
#include "py/reader.h"
#include "esp_http_client.h"
#include "http_client.h"
#include "audio_player.h"

typedef struct {
    TimerHandle_t recorder_timer;
    bool timer_expire;
    const char *file_name;
    uint32_t file_size;
    mp_obj_t file;
    uint32_t recorde_time;
    uint32_t record_buff_size;
    bool save_to_file;
    bool iat_config_flag;
    bool iat_record_finish;
    content_type_t content_type;
    char *url;
} recorder_t;

void recorder_init();
void recorder_deinit();
void recorder_record(const char *filename, int time);
uint32_t recorder_loudness();
recorder_t *get_recorder_handle();

// void audio_recorder_quicksort(uint16_t *buff, uint16_t len);
void audio_recorder_quicksort(uint16_t *buff, uint32_t maxlen, uint32_t begin, uint32_t end);

#endif /* INCLUDE_AUDIO_PLAYER_H_ */
