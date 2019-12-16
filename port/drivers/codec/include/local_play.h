/*
 * local_play.h
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#ifndef _LOCAL_PLAY_H_
#define _LOCAL_PLAY_H_

void local_play_task(void *pvParameters);
void local_play(void *pvParameters);

mp_obj_t file_open(const char *filename, const char *mode);
void file_close(mp_obj_t File);
int file_read(mp_obj_t File, int *read_bytes, uint8_t *buf, uint32_t len);
int file_write(mp_obj_t File, int *write_bytes, uint8_t *buf, uint32_t len);

#endif //end _LOCAL_FILE_H_
