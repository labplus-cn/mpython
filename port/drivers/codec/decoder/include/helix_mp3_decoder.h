/*
 * helix_mp3_decoder.h
 *
 *  
 *      
 */
#ifndef __helix_mp3_decoder_h__
#define __helix_mp3_decoder_h__

#define DECODER_TASK_STACK_DEPTH 2000

int mp3_file_data_proccess(const char *buf, size_t len);
void mp3_decoder_task(void *pvParameters);

#endif //__helix_mp3_decoder_h__
