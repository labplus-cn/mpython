/*
 * local_file.h
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#ifndef _LOCAL_FILE_H_
#define _LOCAL_FILE_H_

void local_file_read_task(void *pvParameters);
void local_file_read(void *pvParameters);

mp_obj_t file_open(const char *filename, const char *mode);
void file_close(mp_obj_t File);
int file_read(mp_obj_t File, int *read_bytes, uint8_t *buf, uint16_t len);
int file_write(mp_obj_t File, int *write_bytes, uint8_t *buf, uint16_t len);

#endif //end _LOCAL_FILE_H_
