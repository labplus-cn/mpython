/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2015 Mark Shannon
 * Copyright (c) 2015-2017 Damien P. George
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
#ifndef MICROPY_INCLUDED_IMAGE_H
#define MICROPY_INCLUDED_IMAGE_H

#include "py/runtime.h"
#include "py/obj.h"

#define MAX_BRIGHTNESS 9

typedef struct _color_t{
    uint8_t g;
    uint8_t r;
    uint8_t b;
} color_t;

typedef struct _machine_image_obj_t {
    mp_obj_base_t base;
    uint8_t height;
    uint8_t width;
    uint8_t brightness;
    color_t color; 
    color_t *data;
} machine_image_obj_t;

/* Thiese are internal methods and it is up to the caller to validate the inputs */
color_t imageGetPixelValue(machine_image_obj_t *image, mp_int_t x, mp_int_t y);
void imageSetPixelValue(machine_image_obj_t *image, mp_int_t x, mp_int_t y, color_t color);
void imageFill(machine_image_obj_t *image, color_t val);
void imageClear(machine_image_obj_t *image);
mp_int_t imageHeight(machine_image_obj_t *image);
mp_int_t imageWidth(machine_image_obj_t *image);
machine_image_obj_t *imageCopy(machine_image_obj_t *image);
machine_image_obj_t *imageInvert(machine_image_obj_t *image);


/** Return a facade object that presents the string as a sequence of images */
mp_obj_t mpython_string_facade(mp_obj_t string, mp_int_t bright, color_t color, bool repeat);

void mpython_image_set_from_char(machine_image_obj_t *img, char c, color_t color);
machine_image_obj_t *mpython_image_for_char(char c, mp_int_t bright, color_t color);
mp_obj_t mpython_image_slice(machine_image_obj_t *img, mp_int_t start, mp_int_t width, mp_int_t stride);
/* ref exists so that we can pull a string out of an object and not have it GC'ed while oterating over it */
mp_obj_t scrolling_string_image_iterable(const char* str, mp_uint_t len, mp_obj_t ref, bool monospace, bool repeat, mp_int_t bright, color_t color);

// extern const monochrome_5by5_t mpython_blank_image;
// extern const monochrome_5by5_t mpython_const_image_heart_obj;

// #define BLANK_IMAGE (machine_image_obj_t *)(&mpython_blank_image)
// #define HEART_IMAGE (machine_image_obj_t *)(&mpython_const_image_heart_obj)

void mpython_image_dim(machine_image_obj_t *lhs, mp_float_t fval);
machine_image_obj_t *mpython_image_sum(machine_image_obj_t *lhs, machine_image_obj_t *rhs, bool add);

extern const mp_obj_type_t machine_image_type;
extern const machine_image_obj_t blank_image;
#define BLANK_IMAGE (machine_image_obj_t *)(&blank_image)

extern const machine_image_obj_t mpython_const_image_heart_obj;
extern const machine_image_obj_t mpython_const_image_heart_small_obj;
extern const machine_image_obj_t mpython_const_image_happy_obj;
extern const machine_image_obj_t mpython_const_image_smile_obj;
extern const machine_image_obj_t mpython_const_image_sad_obj;
extern const machine_image_obj_t mpython_const_image_confused_obj;
extern const machine_image_obj_t mpython_const_image_angry_obj;
extern const machine_image_obj_t mpython_const_image_asleep_obj;
extern const machine_image_obj_t mpython_const_image_surprised_obj;
extern const machine_image_obj_t mpython_const_image_silly_obj;
extern const machine_image_obj_t mpython_const_image_fabulous_obj;
extern const machine_image_obj_t mpython_const_image_meh_obj;
extern const machine_image_obj_t mpython_const_image_yes_obj;
extern const machine_image_obj_t mpython_const_image_no_obj;
extern const machine_image_obj_t mpython_const_image_clock12_obj;
extern const machine_image_obj_t mpython_const_image_clock1_obj;
extern const machine_image_obj_t mpython_const_image_clock2_obj;
extern const machine_image_obj_t mpython_const_image_clock3_obj;
extern const machine_image_obj_t mpython_const_image_clock4_obj;
extern const machine_image_obj_t mpython_const_image_clock5_obj;
extern const machine_image_obj_t mpython_const_image_clock6_obj;
extern const machine_image_obj_t mpython_const_image_clock7_obj;
extern const machine_image_obj_t mpython_const_image_clock8_obj;
extern const machine_image_obj_t mpython_const_image_clock9_obj;
extern const machine_image_obj_t mpython_const_image_clock10_obj;
extern const machine_image_obj_t mpython_const_image_clock11_obj;
extern const machine_image_obj_t mpython_const_image_arrow_n_obj;
extern const machine_image_obj_t mpython_const_image_arrow_ne_obj;
extern const machine_image_obj_t mpython_const_image_arrow_e_obj;
extern const machine_image_obj_t mpython_const_image_arrow_se_obj;
extern const machine_image_obj_t mpython_const_image_arrow_s_obj;
extern const machine_image_obj_t mpython_const_image_arrow_sw_obj;
extern const machine_image_obj_t mpython_const_image_arrow_w_obj;
extern const machine_image_obj_t mpython_const_image_arrow_nw_obj;
extern const machine_image_obj_t mpython_const_image_triangle_obj;
extern const machine_image_obj_t mpython_const_image_triangle_left_obj;
extern const machine_image_obj_t mpython_const_image_chessboard_obj;
extern const machine_image_obj_t mpython_const_image_diamond_obj;
extern const machine_image_obj_t mpython_const_image_diamond_small_obj;
extern const machine_image_obj_t mpython_const_image_square_small_obj;
extern const machine_image_obj_t mpython_const_image_rabbit;
extern const machine_image_obj_t mpython_const_image_cow_obj;
extern const machine_image_obj_t mpython_const_image_music_crotchet_obj;
extern const machine_image_obj_t mpython_const_image_music_quaver_obj;
extern const machine_image_obj_t mpython_const_image_music_quavers_obj;
extern const machine_image_obj_t mpython_const_image_pitchfork_obj;
extern const machine_image_obj_t mpython_const_image_xmas_obj;
extern const machine_image_obj_t mpython_const_image_pacman_obj;
extern const machine_image_obj_t mpython_const_image_target_obj;
extern const machine_image_obj_t mpython_const_image_all_clocks_tuple_obj;
extern const machine_image_obj_t mpython_const_image_all_arrows_tuple_obj;
extern const machine_image_obj_t mpython_const_image_tshirt_obj;
extern const machine_image_obj_t mpython_const_image_rollerskate_obj;
extern const machine_image_obj_t mpython_const_image_duck_obj;
extern const machine_image_obj_t mpython_const_image_house_obj;
extern const machine_image_obj_t mpython_const_image_tortoise_obj;
extern const machine_image_obj_t mpython_const_image_butterfly_obj;
extern const machine_image_obj_t mpython_const_image_stickfigure_obj;
extern const machine_image_obj_t mpython_const_image_giraffe_obj;
extern const machine_image_obj_t mpython_const_image_sword_obj;
extern const machine_image_obj_t mpython_const_image_skull_obj;
extern const machine_image_obj_t mpython_const_image_umbrella_obj;
extern const machine_image_obj_t mpython_const_image_snake_obj;
extern const machine_image_obj_t mpython_const_image_square_obj;
extern const machine_image_obj_t mpython_const_image_ghost_obj;

#endif // MICROPY_INCLUDED_IMAGE_H
