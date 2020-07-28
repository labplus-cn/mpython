/*
 * audio_player.h
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#ifndef INCLUDE_AUDIO_PLAYER_H_
#define INCLUDE_AUDIO_PLAYER_H_

#include <sys/types.h>
#include "audio_renderer.h"
#include "freertos/ringbuf.h"
#include "freertos/semphr.h"
#include "py/reader.h"
#include "esp_http_client.h"
// #include "http_client.h"
// #include "freertos/event_groups.h"

#define BIT_0    ( 1 << 0 )
#define BIT_1    ( 1 << 1 )

#define RINGBUF_SIZE 3880
#define FILE_DATA_READ_LEN 100
#define MIN_VOL_OFFSET -50 //50

// int audio_stream_consumer(const char *recv_buf, ssize_t bytes_read, void *user_data);
typedef enum {
    UNKNOW_TYPE = 0,
    LOCAL_TYPE, 
    WEB_TYPE
} audio_type_t;

typedef enum {
    UNINITIALIZED, INITIALIZED, RUNNING, STOPPED, PAUSED, END
} player_status_t, component_status_t;

typedef enum {
    CMD_NONE, CMD_START, CMD_STOP, CMD_PAUSE,
} player_command_t;

typedef enum {
    BUF_PREF_FAST, BUF_PREF_SAFE
} buffer_pref_t;

typedef enum
{
    MIME_UNKNOWN = 1, OCTET_STREAM, AUDIO_PCM, AUDIO_WAV, AUDIO_AAC, AUDIO_MP4, AUDIO_MPEG, AUDIO_TEXT
} content_type_t;

typedef struct { 
    player_status_t player_status;
    const char *url;
    audio_type_t file_type;
    content_type_t content_type;
    bool eof;
    double volume;
    bool webtts_config_flag;
    RingbufHandle_t *buf_handle;    //环形缓存结构
    int ringbuf_size;
} player_t;

void player_init(void);
void player_deinit(void);
void player_play(const char *url);
void player_start();
void player_stop();
void player_pause();
void player_resume();
void player_set_volume(int _vol);
player_status_t player_get_status();

player_t *get_player_handle();
int create_decode_task(player_t *player);

#endif /* INCLUDE_AUDIO_PLAYER_H_ */
