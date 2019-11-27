/*
 * audio_renderer.h
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#ifndef INCLUDE_AUDIO_RENDERER_H_
#define INCLUDE_AUDIO_RENDERER_H_

#include "freertos/FreeRTOS.h"
#include "driver/i2s.h"
#include "driver/adc.h"
//#include "common_component.h"

typedef enum {
    ADC_BUILT_IN, DAC_BUILT_IN, ADC_DAC_BUILT_IN,
} _i2s_mode_t;

#define RENDERER_DEFAULT(){                     \
        .bit_depth  = I2S_BITS_PER_SAMPLE_16BIT,    \
        .i2s_num = I2S_NUM_0,                       \
        .sample_rate = 44100,                       \
        .sample_rate_modifier = 1.0,                \
        .mode = DAC_BUILT_IN,                \
};
    
typedef struct
{
    _i2s_mode_t mode;
    int sample_rate;
    float sample_rate_modifier;
    i2s_bits_per_sample_t bit_depth;
    i2s_port_t i2s_num;
    adc_unit_t adc_num;
    adc_channel_t adc_channel_num;
    uint8_t i2s_channal_nums;

    uint32_t i2s_read_buff_size;
    bool use_apll;
} renderer_config_t;

/* ESP32 is Little Endian, I2S is Big Endian.
 *
 * Samples produced by a decoder will probably be LE,
 * and I2S recordings BE.
 */
typedef enum
{
    PCM_INTERLEAVED, PCM_LEFT_RIGHT
} pcm_buffer_layout_t;

typedef enum
{
    PCM_BIG_ENDIAN, PCM_LITTLE_ENDIAN
} pcm_endianness_t;

typedef struct
{
    uint32_t sample_rate;
    i2s_bits_per_sample_t bit_depth;
    uint8_t num_channels;
    pcm_buffer_layout_t buffer_format;
    pcm_endianness_t endianness; // currently unused
} pcm_format_t;

/* generic renderer interface */
// void render_samples(char *buf, uint32_t len, pcm_format_t *format);

void renderer_init(renderer_config_t *config);
void renderer_start();
void renderer_stop();
void renderer_destroy();

void renderer_zero_dma_buffer();
renderer_config_t *renderer_get();

void renderer_adc_enable();
void renderer_adc_disable();
void renderer_read_raw(uint8_t *buff, uint32_t len);
void i2s_adc_data_scale(uint8_t * d_buff, uint8_t* s_buff, uint32_t len);
void i2s_adc_data_scale1(uint16_t * d_buff, uint8_t* s_buff, uint32_t len);

#endif /* INCLUDE_AUDIO_RENDERER_H_ */
