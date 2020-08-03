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

#include <string.h>

#include "py/runtime.h"
#include "py/gc.h"
#include "py/objstr.h"
#include "image.h"
#include "modesp.h"
#include "driver/gpio.h"
#include "modmachine.h"
#include "rgb_display.h"
#include "py/mphal.h"

#define min(a,b) (((a)<(b))?(a):(b))

#define ASYNC_MODE_STOPPED 0
#define ASYNC_MODE_ANIMATION 1
#define ASYNC_MODE_CLEAR 2
#define DEFAULT_PRINT_SPEED 400
// Delay in ms in between moving display one column to the left.
#define DEFAULT_SCROLL_SPEED       150
#define MILLISECONDS_PER_MACRO_TICK 6

void mpython_display_animate(machine_display_obj_t *self, mp_obj_t iterable, mp_int_t delay, bool clear, bool wait);
void mpython_display_show(machine_display_obj_t *display, machine_image_obj_t *image);

void mpython_display_show(machine_display_obj_t *display, machine_image_obj_t *image) {
    mp_int_t w = min(image->width, 5);
    mp_int_t h = min(image->height, 5);
    mp_int_t x = 0;
    color_t color;
    mp_int_t bright = image->brightness;
    if (bright < 0 || bright > MAX_BRIGHTNESS) {
        mp_raise_ValueError(MP_ERROR_TEXT("brightness out of bounds"));
    }
    bright = (bright > 1) ? 1 : bright;
    for (; x < w; ++x) {
        mp_int_t y = 0;
        for (; y < h; ++y) {
            color = imageGetPixelValue(image, x, y);
            display->image_buffer[y][x].r = color.r*bright;
            display->image_buffer[y][x].g = color.g*bright;
            display->image_buffer[y][x].b = color.b*bright;            
        }
        for (; y < 5; ++y) { //如果image小于5＊5,清除display大于image区域
            display->image_buffer[y][x].r = 0;
            display->image_buffer[y][x].g = 0;
            display->image_buffer[y][x].b = 0;
        }
    }
    for (; x < 5; ++x) {
        for (mp_int_t y = 0; y < 5; ++y) {
            display->image_buffer[y][x].r = 0;
            display->image_buffer[y][x].g = 0;
            display->image_buffer[y][x].b = 0;
        }
    }
    gpio_set_direction(display->pin, GPIO_MODE_INPUT_OUTPUT);
    mp_hal_delay_us(50);
    esp_neopixel_write(display->pin, (uint8_t *)(display->image_buffer), 75, 1);
}

mp_obj_t mpython_display_show_func(mp_uint_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {

    // Cancel any animations.
    MP_STATE_PORT(async_data)[0] = NULL;
    MP_STATE_PORT(async_data)[1] = NULL;

    static const mp_arg_t show_allowed_args[] = {
        { MP_QSTR_image,    MP_ARG_REQUIRED | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_delay,    MP_ARG_INT, {.u_int = DEFAULT_PRINT_SPEED} },
        { MP_QSTR_clear,    MP_ARG_KW_ONLY | MP_ARG_BOOL, {.u_bool = false} },
        { MP_QSTR_wait,     MP_ARG_KW_ONLY | MP_ARG_BOOL, {.u_bool = true} },
        { MP_QSTR_loop,     MP_ARG_KW_ONLY | MP_ARG_BOOL, {.u_bool = false} },
        { MP_QSTR_bright,   MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 1} },
        { MP_QSTR_color,    MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
    };

    // Parse the args.
    machine_display_obj_t *self = (machine_display_obj_t*)pos_args[0];
    mp_arg_val_t args[MP_ARRAY_SIZE(show_allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(show_allowed_args), show_allowed_args, args);

    mp_obj_t image = args[0].u_obj;
    mp_int_t delay = args[1].u_int;
    bool clear = args[2].u_bool;
    bool wait = args[3].u_bool;
    bool loop = args[4].u_bool;
    mp_int_t bright = args[5].u_int;
    bright = (bright > 1) ? 1 : bright;
    mp_obj_t color = args[6].u_obj;
    color_t col;
    if(color != MP_OBJ_NULL)
    {
        mp_obj_t *elem;
        mp_obj_get_array_fixed_n(color, 3, &elem);
        col.r = mp_obj_get_int(elem[0]);
        col.g = mp_obj_get_int(elem[1]);
        col.b = mp_obj_get_int(elem[2]);
    }
    else
    {
        col.r = 20;
        col.g = 0;
        col.b = 0;
    }
    

    // 1. int or float Convert to string from an integer or float if applicable
    if (mp_obj_is_integer(image) || mp_obj_is_float(image)) {
        image = mp_obj_str_make_new(&mp_type_str, 1, 0, &image);
    }

    if (MP_OBJ_IS_STR(image)) {  //2. string
        // arg is a string object
        mp_uint_t len;
        const char *str = mp_obj_str_get_data(image, &len);
        if (len == 0) {
            // There are no chars; do nothing.
            return mp_const_none;
        } else if (len == 1) {
            if (!clear && !loop) {
                // A single char; convert to an image and print that.
                image = mpython_image_for_char(str[0], bright, col);
                goto single_image_immediate;
            }
        }
        image = mpython_string_facade(image, bright, col, loop); //具有迭代特性
    } else if (mp_obj_get_type(image) == &machine_image_type) { // 3. image
        if (!clear && !loop) {
            goto single_image_immediate;
        }
        image = mp_obj_new_tuple(1, &image);
    }

    // iterable:
    if (args[4].u_bool) { /*loop*/
        // image = mpython_repeat_iterator(image);
    }
    mpython_display_animate(self, image, delay, clear, wait);
    return mp_const_none;

single_image_immediate:
    mpython_display_show(self, (machine_image_obj_t *)image);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_KW(mpython_display_show_obj, 1, mpython_display_show_func);

static uint8_t async_mode;
static mp_obj_t async_iterator = NULL;
// Record if an error occurs in async animation. Unfortunately there is no way to report this.
static volatile bool wakeup_event = false;
static mp_uint_t async_delay = 1000;
static mp_uint_t async_tick = 0;
static bool async_clear = false;

STATIC void async_stop(void) {
    async_iterator = NULL;
    async_mode = ASYNC_MODE_STOPPED;
    async_tick = 0;
    async_delay = 1000;
    async_clear = false;
    MP_STATE_PORT(async_data)[0] = NULL;
    MP_STATE_PORT(async_data)[1] = NULL;
    wakeup_event = true;
}

STATIC void wait_for_event() {
    while (!wakeup_event) {
        // allow CTRL-C to stop the animation
        if (MP_STATE_VM(mp_pending_exception) != MP_OBJ_NULL) {
            async_stop();
            return;
        }
        // __WFI();
    }
    wakeup_event = false;
}

#define DISPLAY_TICKER_SLOT 1

static void draw_object(mp_obj_t obj) {
    machine_display_obj_t *display = (machine_display_obj_t*)MP_STATE_PORT(async_data)[0];
    if (obj == MP_OBJ_STOP_ITERATION) {
        if (async_clear) {
            mpython_display_show(display, BLANK_IMAGE);
            async_clear = false;
        } else {
            async_stop();
        }
    } else if (mp_obj_get_type(obj) == &machine_image_type) {
        mpython_display_show(display, (machine_image_obj_t *)obj);
    } else if (MP_OBJ_IS_STR(obj)) {
        mp_uint_t len;
        const char *str = mp_obj_str_get_data(obj, &len);
        if (len == 1) {
            // mpython_display_show(display, mpython_image_for_char(str[0]));
        } else {
            async_stop();
        }
    } else {
        MP_STATE_VM(mp_pending_exception) = mp_obj_new_exception_msg(&mp_type_TypeError, MP_ERROR_TEXT("not an image"));
        async_stop();
    }
}

static void mpython_display_update(void) {
    async_tick += MILLISECONDS_PER_MACRO_TICK; //更新间隔
    if (async_tick < async_delay*10) { //async_delay
        return;
    }
    async_tick = 0;
    switch (async_mode) {
        case ASYNC_MODE_ANIMATION:
        {
            if (MP_STATE_PORT(async_data)[0] == NULL || MP_STATE_PORT(async_data)[1] == NULL) {
                async_stop();
                break;
            }
            /* WARNING: We are executing in an interrupt handler.
             * If an exception is raised here then we must hand it to the VM. */
            mp_obj_t obj;
            // nlr_buf_t nlr;
            // gc_lock();
            // if (nlr_push(&nlr) == 0) {
            //     obj = mp_iternext_allow_raise(async_iterator); //执行一次迭代操作后的结果，如滚动
            //     nlr_pop();
            //     gc_unlock();
            // } else {
            //     gc_unlock();
            //     if (!mp_obj_is_subclass_fast(MP_OBJ_FROM_PTR(((mp_obj_base_t*)nlr.ret_val)->type),
            //         MP_OBJ_FROM_PTR(&mp_type_StopIteration))) {
            //         // An exception other than StopIteration, so set it for the VM to raise later
            //         // If memory error, write an appropriate message.
            //         if (mp_obj_get_type(nlr.ret_val) == &mp_type_MemoryError) {
            //             mp_printf(&mp_plat_print, "Allocation in interrupt handler");
            //         }
            //         MP_STATE_VM(mp_pending_exception) = MP_OBJ_FROM_PTR(nlr.ret_val);
            //     }
            //     obj = MP_OBJ_STOP_ITERATION;
            // }
            obj = mp_iternext_allow_raise(async_iterator); //执行一次迭代操作后的结果，如滚动
            draw_object(obj);
            break;
        }
        case ASYNC_MODE_CLEAR:
            mpython_display_show(&mpython_display_obj, BLANK_IMAGE);
            async_stop();
            break;
    }
}

#define GREYSCALE_MASK ((1<<MAX_BRIGHTNESS)-2)

/* This is the top-level animation/display callback.  It is not a registered
 * callback. */
void mpython_display_tick(void) {
    /* Do nothing if the display is not active. */
    if (!mpython_display_obj.active) {
        return;
    }

    mpython_display_update();
}

/* 配置成动画显示 */
void mpython_display_animate(machine_display_obj_t *self, mp_obj_t iterable, mp_int_t delay, bool clear, bool wait) {
    // Reset the repeat state.
    MP_STATE_PORT(async_data)[0] = NULL;
    MP_STATE_PORT(async_data)[1] = NULL;
    async_iterator = mp_getiter(iterable, NULL);  //获取迭代器
    async_delay = delay;
    async_clear = clear;
    MP_STATE_PORT(async_data)[0] = self; // so it doesn't get GC'd
    MP_STATE_PORT(async_data)[1] = async_iterator;
    wakeup_event = false;
    mp_obj_t obj = mp_iternext_allow_raise(async_iterator); //执行一次迭代操作后的结果，如滚动返回（操作后的image）
    draw_object(obj);
    async_tick = 0;
    async_mode = ASYNC_MODE_ANIMATION;
    if (wait) {
        wait_for_event();
    }
}

void mpython_display_scroll(machine_display_obj_t *self, const char* str, mp_int_t bright, color_t color) {
    mp_obj_t iterable = scrolling_string_image_iterable(str, strlen(str), NULL, false, false, bright, color);
    mpython_display_animate(self, iterable, DEFAULT_SCROLL_SPEED, false, true);
}

mp_obj_t mpython_display_scroll_func(mp_uint_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    static const mp_arg_t scroll_allowed_args[] = {
        { MP_QSTR_text, MP_ARG_REQUIRED | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_delay, MP_ARG_INT, {.u_int = DEFAULT_SCROLL_SPEED} },
        { MP_QSTR_wait, MP_ARG_KW_ONLY | MP_ARG_BOOL, {.u_bool = true} },
        { MP_QSTR_monospace, MP_ARG_KW_ONLY | MP_ARG_BOOL, {.u_bool = false} },
        { MP_QSTR_loop, MP_ARG_KW_ONLY | MP_ARG_BOOL, {.u_bool = false} },
        { MP_QSTR_bright,   MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 1} },
        { MP_QSTR_color,    MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
    };
    // Parse the args.
    machine_display_obj_t *self = (machine_display_obj_t*)pos_args[0];
    mp_arg_val_t args[MP_ARRAY_SIZE(scroll_allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(scroll_allowed_args), scroll_allowed_args, args);
    mp_int_t bright = args[5].u_int;
    bright = (bright > 1) ? 1 : bright;
    mp_obj_t color = args[6].u_obj;
    color_t col;
    if(color != MP_OBJ_NULL)
    {
        mp_obj_t *elem;
        mp_obj_get_array_fixed_n(color, 3, &elem);
        col.r = mp_obj_get_int(elem[0]);
        col.g = mp_obj_get_int(elem[1]);
        col.b = mp_obj_get_int(elem[2]);
    }
    else
    {
        col.r = 20;
        col.g = 0;
        col.b = 0;
    }
    mp_uint_t len;
    mp_obj_t object_string = args[0].u_obj;
    if (mp_obj_is_integer(object_string) || mp_obj_is_float(object_string)) {
        object_string = mp_obj_str_make_new(&mp_type_str, 1, 0, &object_string);
    }
    const char* str = mp_obj_str_get_data(object_string, &len);
    mp_obj_t iterable = scrolling_string_image_iterable(str, len, args[0].u_obj, args[3].u_bool /*monospace?*/, args[4].u_bool /*loop*/, bright, col);
    mpython_display_animate(self, iterable, args[1].u_int /*delay*/, false/*clear*/, args[2].u_bool/*wait?*/);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_KW(mpython_display_scroll_obj, 1, mpython_display_scroll_func);

mp_obj_t mpython_display_on_func(mp_obj_t obj) {
    // machine_display_obj_t *self = (machine_display_obj_t*)obj;

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mpython_display_on_obj, mpython_display_on_func);

mp_obj_t mpython_display_off_func(mp_obj_t obj) {
    // machine_display_obj_t *self = (machine_display_obj_t*)obj;

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mpython_display_off_obj, mpython_display_off_func);

mp_obj_t mpython_display_is_on_func(mp_obj_t obj) {
    machine_display_obj_t *self = (machine_display_obj_t*)obj;
    if (self->active) {
        return mp_const_true;
    }
    else {
        return mp_const_false;
    }
}
MP_DEFINE_CONST_FUN_OBJ_1(mpython_display_is_on_obj, mpython_display_is_on_func);

void mpython_display_clear(void) {
    // Reset repeat state, cancel animation and clear screen.
    wakeup_event = false;
    async_mode = ASYNC_MODE_CLEAR;
    async_tick = async_delay - MILLISECONDS_PER_MACRO_TICK;
    wait_for_event();
}

mp_obj_t mpython_display_clear_func(mp_obj_t self) {
    (void)self;
    mpython_display_clear();
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mpython_display_clear_obj, mpython_display_clear_func);

void mpython_display_set_pixel(machine_display_obj_t *display, mp_int_t x, mp_int_t y, mp_int_t bright, color_t color) {
    if (x < 0 || y < 0 || x > 4 || y > 4) {
        mp_raise_ValueError(MP_ERROR_TEXT("index out of bounds"));
    }
    if (bright < 0 || bright > MAX_BRIGHTNESS) {
        mp_raise_ValueError(MP_ERROR_TEXT("brightness out of bounds"));
    }
    mp_int_t _bright = (bright > 1) ? 1 : bright;
    display->image_buffer[y][x].r = _bright*color.r;
    display->image_buffer[y][x].g = _bright*color.g;
    display->image_buffer[y][x].b = _bright*color.b;
    gpio_set_direction(display->pin, GPIO_MODE_INPUT_OUTPUT);
    mp_hal_delay_us(50);
    esp_neopixel_write(display->pin, (uint8_t *)(display->image_buffer), 75, 1);
}

STATIC mp_obj_t mpython_display_set_pixel_func(mp_uint_t n_args, const mp_obj_t *args) {
    (void)n_args;
    machine_display_obj_t *self = (machine_display_obj_t*)args[0];
    color_t col;
    mp_int_t bright;
    if(mp_obj_is_integer(args[3]))
    {
        bright = mp_obj_get_int(args[3]);
        if (bright < 0 || bright > MAX_BRIGHTNESS) {
            mp_raise_ValueError(MP_ERROR_TEXT("brightness out of bounds"));
        }
        bright = (bright > 1) ? 1 : bright;
        col.r =  20;
        col.g = 0;
        col.b = 0;
    }
    else
    {
        bright = 1;
        mp_obj_t *elem;
        mp_obj_get_array_fixed_n(args[3], 3, &elem);
        col.r = mp_obj_get_int(elem[0]);
        col.g = mp_obj_get_int(elem[1]);
        col.b = mp_obj_get_int(elem[2]);
    }
    
    mpython_display_set_pixel(self, mp_obj_get_int(args[1]), mp_obj_get_int(args[2]), bright, col);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(mpython_display_set_pixel_obj, 4, 4, mpython_display_set_pixel_func);

color_t mpython_display_get_pixel(machine_display_obj_t *display, mp_int_t x, mp_int_t y) {
    if (x < 0 || y < 0 || x > 4 || y > 4) {
        mp_raise_ValueError(MP_ERROR_TEXT("index out of bounds"));
    }
    color_t col;
    col.r = display->image_buffer[y][x].r;
    col.g = display->image_buffer[y][x].g;
    col.b = display->image_buffer[y][x].b;
    return col;
}

STATIC mp_obj_t mpython_display_get_pixel_func(mp_obj_t self_in, mp_obj_t x_in, mp_obj_t y_in) {
    machine_display_obj_t *self = (machine_display_obj_t*)self_in;
    color_t col = mpython_display_get_pixel(self, mp_obj_get_int(x_in), mp_obj_get_int(y_in));
    mp_obj_t tuple[3] = {
        tuple[0] = mp_obj_new_int(col.r),
        tuple[1] = mp_obj_new_int(col.g),
        tuple[2] = mp_obj_new_int(col.b),
     };
    return mp_obj_new_tuple(3, tuple);
}
MP_DEFINE_CONST_FUN_OBJ_3(mpython_display_get_pixel_obj, mpython_display_get_pixel_func);

STATIC mp_obj_t mpython_display_init(mp_obj_t self) {
    (void)self;
    //  mp_raise_ValueError(MP_ERROR_TEXT("hello "));
    mpython_display_show(&mpython_display_obj,  BLANK_IMAGE);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mpython_display_init_obj, mpython_display_init);

STATIC const mp_map_elem_t mpython_display_locals_dict_table[] = {
    { MP_OBJ_NEW_QSTR(MP_QSTR___init__),  (mp_obj_t)&mpython_display_init_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_get_pixel),  (mp_obj_t)&mpython_display_get_pixel_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_set_pixel),  (mp_obj_t)&mpython_display_set_pixel_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_show), (mp_obj_t)&mpython_display_show_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_scroll), (mp_obj_t)&mpython_display_scroll_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_clear), (mp_obj_t)&mpython_display_clear_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_on),  (mp_obj_t)&mpython_display_on_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_off),  (mp_obj_t)&mpython_display_off_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_is_on),  (mp_obj_t)&mpython_display_is_on_obj },
};

STATIC MP_DEFINE_CONST_DICT(mpython_display_locals_dict, mpython_display_locals_dict_table);

STATIC const mp_obj_type_t mpython_display_type = {
    { &mp_type_type },
    .name = MP_QSTR_mpythonDisplay,
    .print = NULL,
    .make_new = NULL,
    .call = NULL,
    .unary_op = NULL,
    .binary_op = NULL,
    .attr = NULL,
    .subscr = NULL,
    .getiter = NULL,
    .iternext = NULL,
    .buffer_p = {NULL},
    .protocol = NULL,
    .parent = NULL,
    .locals_dict = (mp_obj_dict_t*)&mpython_display_locals_dict,
};

machine_display_obj_t mpython_display_obj = {
    {&mpython_display_type},
    {{{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}}, {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}}, {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}}, 
     {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}}, {{0,0,0},{0,0,0},{0,0,0},{0,0,0},{0,0,0}}},
    .bright = 0,
    .pin = GPIO_NUM_25,
    .nums = 25,
    .timing = 1,
    .active = 1,
};
