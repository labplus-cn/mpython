/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2015 Damien P. George
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
#include "py/runtime.h"
#include "py/obj.h"
#include "image.h"

#define SMALL_IMAGE(dat) \
{ \
    {&machine_image_type}, \
    .height = 5, \
    .width = 5, \
    .brightness = 1, \
    .color = {0,0,0}, \
    .data = (color_t *)dat, \
}

const color_t mpython_const_image_heart_data[25] = {
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0},  
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_heart_obj = SMALL_IMAGE(mpython_const_image_heart_data);

const color_t mpython_const_image_heart_small_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_heart_small_obj = SMALL_IMAGE(mpython_const_image_heart_small_data);

// // smilies
const color_t mpython_const_image_happy_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_happy_obj = SMALL_IMAGE(mpython_const_image_happy_data);

const color_t mpython_const_image_smile_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_smile_obj = SMALL_IMAGE(mpython_const_image_smile_data);

const color_t mpython_const_image_sad_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_sad_obj = SMALL_IMAGE(mpython_const_image_sad_data);

const color_t mpython_const_image_confused_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_confused_obj = SMALL_IMAGE(mpython_const_image_confused_data);

const color_t mpython_const_image_angry_data[25] = {
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_angry_obj = SMALL_IMAGE(mpython_const_image_angry_data);

const color_t mpython_const_image_asleep_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_asleep_obj = SMALL_IMAGE(mpython_const_image_asleep_data);

const color_t mpython_const_image_surprised_data[25] = {
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_surprised_obj = SMALL_IMAGE(mpython_const_image_surprised_data);

const color_t mpython_const_image_silly_data[25] = {
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_silly_obj = SMALL_IMAGE(mpython_const_image_silly_data);

const color_t mpython_const_image_fabulous_data[25] = {
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_fabulous_obj = SMALL_IMAGE(mpython_const_image_fabulous_data);

const color_t mpython_const_image_meh_data[25] = {
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_meh_obj = SMALL_IMAGE(mpython_const_image_meh_data);

// // yes/no
const color_t mpython_const_image_yes_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_yes_obj = SMALL_IMAGE(mpython_const_image_yes_data);

const color_t mpython_const_image_no_data[25] = {
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_no_obj = SMALL_IMAGE(mpython_const_image_no_data);

// // clock hands
const color_t mpython_const_image_clock12_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_clock12_obj = SMALL_IMAGE(mpython_const_image_clock12_data);

const color_t mpython_const_image_clock1_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_clock1_obj = SMALL_IMAGE(mpython_const_image_clock1_data);

const color_t mpython_const_image_clock2_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_clock2_obj = SMALL_IMAGE(mpython_const_image_clock2_data);

const color_t mpython_const_image_clock3_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_clock3_obj = SMALL_IMAGE(mpython_const_image_clock3_data);

const color_t mpython_const_image_clock4_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_clock4_obj = SMALL_IMAGE(mpython_const_image_clock4_data);

const color_t mpython_const_image_clock5_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_clock5_obj = SMALL_IMAGE(mpython_const_image_clock5_data);

const color_t mpython_const_image_clock6_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_clock6_obj = SMALL_IMAGE(mpython_const_image_clock6_data);

const color_t mpython_const_image_clock7_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_clock7_obj = SMALL_IMAGE(mpython_const_image_clock7_data);

const color_t mpython_const_image_clock8_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_clock8_obj = SMALL_IMAGE(mpython_const_image_clock8_data);

const color_t mpython_const_image_clock9_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_clock9_obj = SMALL_IMAGE(mpython_const_image_clock9_data);

const color_t mpython_const_image_clock10_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_clock10_obj = SMALL_IMAGE(mpython_const_image_clock10_data);

const color_t mpython_const_image_clock11_data[25] = {
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_clock11_obj = SMALL_IMAGE(mpython_const_image_clock11_data);


// // arrows
const color_t mpython_const_image_arrow_n_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_arrow_n_obj = SMALL_IMAGE(mpython_const_image_arrow_n_data);

const color_t mpython_const_image_arrow_ne_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_arrow_ne_obj = SMALL_IMAGE(mpython_const_image_arrow_ne_data);

const color_t mpython_const_image_arrow_e_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_arrow_e_obj = SMALL_IMAGE(mpython_const_image_arrow_e_data);

const color_t mpython_const_image_arrow_se_data[25] = {
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_arrow_se_obj = SMALL_IMAGE(mpython_const_image_arrow_se_data);
                          
const color_t mpython_const_image_arrow_s_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_arrow_s_obj = SMALL_IMAGE(mpython_const_image_arrow_s_data);

const color_t mpython_const_image_arrow_sw_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_arrow_sw_obj = SMALL_IMAGE(mpython_const_image_arrow_sw_data);

const color_t mpython_const_image_arrow_w_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_arrow_w_obj = SMALL_IMAGE(mpython_const_image_arrow_w_data);

const color_t mpython_const_image_arrow_nw_data[25] = {
    {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_arrow_nw_obj = SMALL_IMAGE(mpython_const_image_arrow_nw_data);

// // geometry
const color_t mpython_const_image_triangle_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_triangle_obj = SMALL_IMAGE(mpython_const_image_triangle_data);


const color_t mpython_const_image_triangle_left_data[25] = {
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_triangle_left_obj = SMALL_IMAGE(mpython_const_image_triangle_left_data);

const color_t mpython_const_image_chessboard_data[25] = {
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_chessboard_obj = SMALL_IMAGE(mpython_const_image_chessboard_data);

const color_t mpython_const_image_diamond_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_diamond_obj = SMALL_IMAGE(mpython_const_image_diamond_data);

const color_t mpython_const_image_diamond_small_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_diamond_small_obj = SMALL_IMAGE(mpython_const_image_diamond_small_data);

const color_t mpython_const_image_square_data[25] = {
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_square_obj = SMALL_IMAGE(mpython_const_image_square_data);

const color_t mpython_const_image_square_small_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_square_small_obj = SMALL_IMAGE(mpython_const_image_square_small_data);

// // animals
const color_t mpython_const_image_data[25] = {
    {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_rabbit = SMALL_IMAGE(mpython_const_image_data);

const color_t mpython_const_image_cow_data[25] = {
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_cow_obj = SMALL_IMAGE(mpython_const_image_cow_data);

// // musical notes
const color_t mpython_const_image_music_crotchet_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_music_crotchet_obj = SMALL_IMAGE(mpython_const_image_music_crotchet_data);

const color_t mpython_const_image_music_quaver_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_music_quaver_obj = SMALL_IMAGE(mpython_const_image_music_quaver_data);

const color_t mpython_const_image_music_quavers_data[25] = {
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_music_quavers_obj = SMALL_IMAGE(mpython_const_image_music_quavers_data);

// // other icons
const color_t mpython_const_image_pitchfork_data[25] = {
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_pitchfork_obj = SMALL_IMAGE(mpython_const_image_pitchfork_data);

const color_t mpython_const_image_xmas_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_xmas_obj = SMALL_IMAGE(mpython_const_image_xmas_data);

const color_t mpython_const_image_pacman_data[25] = {
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_pacman_obj = SMALL_IMAGE(mpython_const_image_pacman_data);

const color_t mpython_const_image_target_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_target_obj = SMALL_IMAGE(mpython_const_image_target_data);


// /*
// The following images were designed by Abbie Brooks.
// */
const color_t mpython_const_image_tshirt_data[25] = {
    {0,20,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_tshirt_obj = SMALL_IMAGE(mpython_const_image_tshirt_data);

const color_t mpython_const_image_rollerskate_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_rollerskate_obj = SMALL_IMAGE(mpython_const_image_rollerskate_data);

const color_t mpython_const_image_duck_data[25] = {
    {0,0,0}, {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_duck_obj = SMALL_IMAGE(mpython_const_image_duck_data);

const color_t mpython_const_image_house_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_house_obj = SMALL_IMAGE(mpython_const_image_house_data);

const color_t mpython_const_image_tortoise_data[25] = {
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_tortoise_obj = SMALL_IMAGE(mpython_const_image_tortoise_data);

const color_t mpython_const_image_butterfly_data[25] = {
    {0,20,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_butterfly_obj = SMALL_IMAGE(mpython_const_image_butterfly_data);

const color_t mpython_const_image_stickfigure_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_stickfigure_obj = SMALL_IMAGE(mpython_const_image_stickfigure_data);

const color_t mpython_const_image_ghost_data[25] = {
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,20,0}
};
const machine_image_obj_t mpython_const_image_ghost_obj = SMALL_IMAGE(mpython_const_image_ghost_data);

const color_t mpython_const_image_sword_data[25] = {
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_sword_obj = SMALL_IMAGE(mpython_const_image_sword_data);

const color_t mpython_const_image_giraffe_data[25] = {
    {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_giraffe_obj = SMALL_IMAGE(mpython_const_image_giraffe_data);

const color_t mpython_const_image_skull_data[25] = {
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_skull_obj = SMALL_IMAGE(mpython_const_image_skull_data);

const color_t mpython_const_image_umbrella_data[25] = {
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_umbrella_obj = SMALL_IMAGE(mpython_const_image_umbrella_data);

const color_t mpython_const_image_snake_data[25] = {
    {0,20,0}, {0,20,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
    {0,20,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,20,0}, 
    {0,0,0}, {0,20,0}, {0,0,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,20,0}, {0,20,0}, {0,20,0}, {0,0,0}, 
    {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t mpython_const_image_snake_obj = SMALL_IMAGE(mpython_const_image_snake_data);

