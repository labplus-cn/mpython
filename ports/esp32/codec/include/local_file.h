/*
 * local_file.h
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#ifndef _LOCAL_FILE_H_
#define _LOCAL_FILE_H_

void local_file_read_task(void *pvParameters);
int file_read(uint8_t *buff, int read_len, int *len);
void local_file_read(player_t *player);

#endif //end _LOCAL_FILE_H_
