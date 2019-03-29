#ifndef _OLED_SH1106_H
#define _OLED_SH1106_H

#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "i2c_master.h"

/**
 *  @brife driver for ssd1106
 * 
 * 
 */
// register definitions
#define SET_CONTRAST            0x81
#define SET_ENTIRE_ON           0xa4
#define SET_ENTIRE_ON1          0xaf
#define SET_NORM_INV            0xa6
#define SET_DISP_OFF            0xae
#define SET_DISP_ON             0xaf
#define SET_MEM_ADDR            0x20
#define SET_COL_ADDR            0x21
#define SET_PAGE_ADDR           0x22
#define SET_DISP_START_LINE     0x40
#define SET_SEG_REMAP           0xa0
#define SET_MUX_RATIO           0xa8
#define SET_COM_OUT_DIR         0xc0
#define SET_DISP_OFFSET         0xd3
#define SET_COM_PIN_CFG         0xda
#define SET_DISP_CLK_DIV        0xd5
#define SET_PRECHARGE           0xd9
#define SET_VCOM_DESEL          0xdb
#define SET_CHARGE_PUMP         0x8d
#define SET_CHARGE_PUMP1        0xad
#define SET_COL_ADDR_L          0x02
#define SET_COL_ADDR_H          0x10
#define SET_PAGE_ADDR1          0xb0
#define SET_CONTRACT_CTRL       0x81
#define SET_DUTY                0x3f
#define SET_VCC_SOURCE          0x8b
#define SET_VPP                 0x33

#define SH1106_I2C_ADDRESS   0x3C // 011110+SA0+RW - 0x3C or 0x3D

#define OLED_WIDTH  128
#define OLED_HEIGHT 64
#define BLACK 0
#define WHITE 1
#define INVERSE 2

bool oled_init();
void oled_deinit();

void oled_drawPixel(int16_t x, int16_t y, int16_t color);

void oled_clear();

void oled_show();

void oled_print(const char * str, int x0, int y0);

extern const uint8_t img_panic[];
extern const uint8_t * ani_startup[25];
void oled_drawImg(const uint8_t * img);
void oled_drawAnimation(const uint8_t **pImgs, int len, int frameRate);
#endif
