/*
 * modcodec.h
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#ifndef MICROPY_INCLUDED_ESP32_MODCODEC_H
#define MICROPY_INCLUDED_ESP32_MODCODEC_H

#define I2S_NUM (0)
//i2s sample rate
#define DEFAULT_I2S_SAMPLE_RATE (16000)
//i2s data bits
#define DEFAULT_I2S_SAMPLE_BITS (16)
//I2S read buffer length
#define DEFAULT_I2S_READ_LEN (16 * 1024)
//I2S data format
#define DEFAULT_I2S_FORMAT (I2S_CHANNEL_FMT_RIGHT_LEFT)
//I2S channel number
#define DEFAULT_I2S_CHANNEL_NUM ((DEFAULT_I2S_FORMAT < I2S_CHANNEL_FMT_ONLY_RIGHT) ? (2) : (1))
//I2S built-in ADC unit
#define I2S_ADC_UNIT ADC_UNIT_1
//I2S built-in ADC channel
#define I2S_ADC_CHANNEL ADC1_CHANNEL_0

#endif // MICROPY_INCLUDED_ESP32_MODEXTBOARD_H
