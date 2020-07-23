/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2015 Damien George, Mark Shannon
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
#include <stdio.h>

#include "py/obj.h"
#include "py/runtime.h"
#include "image.h"
#include "font.h"

#define min(a,b) (((a)<(b))?(a):(b))
#define max(a,b) (((a)>(b))?(a):(b))

STATIC void mpython_image_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) { 
    // machine_image_obj_t *self = (machine_image_obj_t*)self_in;
    // mp_printf(print, "Image(");
    // if (kind == PRINT_STR)
    //     mp_printf(print, "\n    ");
    // mp_printf(print, "'");
    // for (int y = 0; y < self->height; ++y) {
    //     for (int x = 0; x < self->width; ++x) {
    //         // mp_printf(print, "%c", "0123456789"[self->getPixelValue(x, y)]);
    //     }
    //     mp_printf(print, ":");
    //     if (kind == PRINT_STR && y < self->height-1)
    //         mp_printf(print, "'\n    '");
    // }
    // mp_printf(print, "'");
    // if (kind == PRINT_STR)
    //     mp_printf(print, "\n");
    // mp_printf(print, ")"); 
}

color_t imageGetPixelValue(machine_image_obj_t *image, mp_int_t x, mp_int_t y)
{
    color_t c;
    c.r = image->data[y*image->width + x].r;
    c.g = image->data[y*image->width + x].g;
    c.b = image->data[y*image->width + x].b;
    return c;
}

void imageSetPixelValue(machine_image_obj_t *image, mp_int_t x, mp_int_t y, color_t color)
{
    image->data[y*image->width + x].r = color.r;
    image->data[y*image->width + x].g = color.g;
    image->data[y*image->width + x].b = color.b;
}

void imageFill(machine_image_obj_t *image, color_t val) {
    for (int i = 0; i < image->width * image->height; i++) {
        image->data[i].r = val.r;
        image->data[i].g = val.g;
        image->data[i].b = val.b;
    }
    image->brightness = 1;
}

void imageClear(machine_image_obj_t *image) {
    for (int i = 0; i < image->width * image->height; i++) {
        image->data[i].r = 0;
        image->data[i].g = 0;
        image->data[i].b = 0;
    }
}

mp_int_t imageWidth(machine_image_obj_t *image) {
        return image->width;
}

mp_int_t imageHeight(machine_image_obj_t *image) {
        return image->height;
}

machine_image_obj_t *imageCopy(machine_image_obj_t *src) {
    mp_int_t w = src->width;
    mp_int_t h = src->height;
    machine_image_obj_t *result = m_new_obj(machine_image_obj_t);
    result->base.type = &machine_image_type;
    result->height = h;
    result->width = w;
    result->brightness = src->brightness;
    result->data = calloc(w*h, sizeof(color_t));
    for(mp_int_t i = 0; i < w*h; i++)
    {
        result->data[i].r = src->data[i].r;
        result->data[i].g = src->data[i].g;
        result->data[i].b = src->data[i].b;
    }
    return result;
}

machine_image_obj_t *imageInvert(machine_image_obj_t *src) {
    mp_int_t w = src->width;
    mp_int_t h = src->height;
    machine_image_obj_t *result = m_new_obj(machine_image_obj_t);
    result->base.type = &machine_image_type;
    result->height = h;
    result->width = w;
    result->brightness = src->brightness;
    result->data = calloc(w*h, sizeof(color_t));
    for(mp_int_t i = 0; i < w*h; i++)
    {
        result->data[i].r = 255 - src->data[i].r;
        result->data[i+1].g = 255 - src->data[i+1].g;
        result->data[i+2].b = 255 - src->data[i+2].b;
    }

    return result;
}

machine_image_obj_t *image_make_new(mp_int_t w, mp_int_t h, mp_int_t bright)
{
    machine_image_obj_t *result = m_new_obj(machine_image_obj_t);
    result->base.type = &machine_image_type;
    result->height = h;
    result->width = w;
    result->brightness = bright;
    result->data = calloc(w*h, sizeof(color_t));     
    return result;
}

/* 从带亮度信息的字符串中提取图象
    例如：
    boat3 = Image("00000:"
              "00000:"
              "05050:"
              "05050:"
              "05050")
    或：
    boat3 = Image("00000:"
                  "000005665:"
                  "05050:"
                  "05050:"
                  "05050")
    或：boat = Image("05050:05050:05050:99999:09990")
    或：boat = Image("05050\n05050\n05050\n99999\09990")
    其中的数值代表对应点的亮度
 */
STATIC machine_image_obj_t *image_from_parsed_str(const char *s, mp_int_t len, mp_int_t bright, color_t color) {
    mp_int_t w = 0;
    mp_int_t h = 0;
    mp_int_t line_len = 0;
    machine_image_obj_t *result;
    /*First pass -- Establish metadata */
    for (int i = 0; i < len; i++) {   //提取w h
        char c = s[i];
        if (c == '\n' || c == ':') {
            w = max(line_len, w);
            line_len = 0;
            ++h;
        } else if (c == ' ') {
            ++line_len;
        } else if ('c' >= '0' && c <= '9') {
            ++line_len;
        } else {
            mp_raise_ValueError(MP_ERROR_TEXT("unexpected character in Image definition"));
        }
    }
    if (line_len) { //字符串到结束都没'\n' or ':'
        // Omitted trailing terminator
        ++h;
        w = max(line_len, w);
    }
    result = image_make_new(w, h, bright);
    imageClear(result);
    mp_int_t x = 0;
    mp_int_t y = 0;
    color_t col;
    /* Second pass -- Fill in data 提取点阵信息*/
    for (int i = 0; i < len; i++) {
        char c = s[i];
        if (c == '\n' || c == ':') { //w取自最大行宽，其它行以填0的方式扩充到此行宽
            col.r = 0;
            col.g = 0;
            col.b = 0;
            while (x < w) {
                imageSetPixelValue(result, x, y, col);
                x++;
            }
            ++y;
            x = 0;
        } else if (c == ' ') { //空格当0
            /* Treat spaces as 0 */
            col.r = 0;
            col.g = 0;
            col.b = 0;
            imageSetPixelValue(result, x, y, col);
            ++x;
        } else if ('c' >= '0' && c <= '9') {
            col = color;
            col.r  = col.r*(min((c-'0'),  255));
            col.g = col.g*(min((c-'0'), 255));
            col.b = col.b*(min((c-'0'), 255));
            imageSetPixelValue(result, x, y, col);
            ++x;
        }
    }
    if (y < h) {
        while (x < w) {
            col.r = 0;
            col.g = 0;
            col.b = 0;
            imageSetPixelValue(result, x, y, col);
            x++;
        }
    }
    return (machine_image_obj_t *)result;
}

STATIC mp_obj_t mpython_image_make_new(const mp_obj_type_t *type_in, mp_uint_t n_args, mp_uint_t n_kw, const mp_obj_t *args) {
    (void)type_in;
    mp_arg_check_num(n_args, n_kw, 0, 3, false);
    machine_image_obj_t *result;
    color_t col;
    mp_int_t bright;
    switch (n_args) { //无参数，创建5x5点阵图
        case 0: {
            result = image_make_new(5, 5, 5);
            imageClear(result);
            return MP_OBJ_FROM_PTR(result);
        }

        case 1: { //1个参数，从字符或字符串表创建图象
            if (MP_OBJ_IS_STR(args[0])) {
                // arg is a string object
                mp_uint_t len;
                const char *str = mp_obj_str_get_data(args[0], &len);
                col.r = 20;
                col.g = 0;
                col.b = 0;
                // make image from string
                if (len == 1) {
                    /* For a single charater, return the font glyph */
                    return MP_OBJ_FROM_PTR(mpython_image_for_char(str[0], 1, col));
                } else {
                    /* Otherwise parse the image description string */
                    col.r = 20;
                    col.g = 0;
                    col.b = 0;
                    return MP_OBJ_FROM_PTR(image_from_parsed_str(str, len, 1, col));
                }
            } else {
                mp_raise_TypeError(MP_ERROR_TEXT("Image(s) takes a string"));
            } 
        }

        case 2: //参数1：字符 参数2：亮度或颜色
        { //2－3个参数，创建指定大小图像。并初始化
            if (MP_OBJ_IS_STR(args[0])) {
                // arg is a string object
                mp_uint_t len;
                const char *str = mp_obj_str_get_data(args[0], &len);
                if(mp_obj_is_integer(args[1]))
                {
                    bright = mp_obj_get_int(args[1]);
                    if (bright < 0 || bright > MAX_BRIGHTNESS) {
                        mp_raise_ValueError(MP_ERROR_TEXT("brightness out of bounds"));
                    }
                    bright = (bright > 1) ? 1 : bright;
                    col.r = 20;
                    col.g = 0;
                    col.b = 0;
                }
                else
                {
                    bright = 1;
                    mp_obj_t *elem;
                    mp_obj_get_array_fixed_n(args[1], 3, &elem);
                    col.r = mp_obj_get_int(elem[0]);
                    col.g = mp_obj_get_int(elem[1]);
                    col.b = mp_obj_get_int(elem[2]);
                }
                
                // make image from string
                if (len == 1) {
                    /* For a single charater, return the font glyph */
                    return MP_OBJ_FROM_PTR(mpython_image_for_char(str[0], bright, col));
                } else {
                    /* Otherwise parse the image description string */
                    return MP_OBJ_FROM_PTR(image_from_parsed_str(str, len, bright, col));
                }
            }
        }
        case 3:
        {
            mp_int_t w = mp_obj_get_int(args[0]);
            mp_int_t h = mp_obj_get_int(args[1]);
            machine_image_obj_t *image = image_make_new(w, h, 1);
            if (n_args == 2) {
                imageClear(image);
            } else {
                mp_buffer_info_t bufinfo;
                mp_get_buffer_raise(args[2], &bufinfo, MP_BUFFER_READ);

                if (w < 0 || h < 0 || (size_t)(w * h) != bufinfo.len) {
                    mp_raise_ValueError(MP_ERROR_TEXT("image data is incorrect size"));
                }
                for(mp_int_t i = 0; i < w*h; i++)
                {
                    image->data[i].r = ((uint8_t *)bufinfo.buf)[i];
                }
                // memcpy((uint8_t *)image->data, bufinfo.buf, bufinfo.len);
            }
            return MP_OBJ_FROM_PTR(image);
        }

        default: {
            mp_raise_TypeError(MP_ERROR_TEXT("Image() takes 0 to 3 arguments"));
        }
    }
}

static void clear_rect(machine_image_obj_t *img, mp_int_t x0, mp_int_t y0,mp_int_t x1, mp_int_t y1) {
    color_t col = {0, 0, 0};
    for (int i = x0; i < x1; ++i) {
        for (int j = y0; j < y1; ++j) {
            imageSetPixelValue(img, i, j, col);
        }
    }
}

STATIC void image_blit(machine_image_obj_t *src, machine_image_obj_t *dest, mp_int_t x, mp_int_t y, mp_int_t w, mp_int_t h, mp_int_t xdest, mp_int_t ydest) {
    if (w < 0)
        w = 0;
    if (h < 0)
        h = 0;
    mp_int_t intersect_x0 = max(max(0, x), -xdest);
    mp_int_t intersect_y0 = max(max(0, y), -ydest);
    mp_int_t intersect_x1 = min(min(dest->width+x-xdest, src->width), x+w);
    mp_int_t intersect_y1 = min(min(dest->height+y-ydest, src->height), y+h);
    mp_int_t xstart, xend, ystart, yend, xdel, ydel;
    mp_int_t clear_x0 = max(0, xdest);
    mp_int_t clear_y0 = max(0, ydest);
    mp_int_t clear_x1 = min(dest->width, xdest+w);
    mp_int_t clear_y1 = min(dest->height, ydest+h);
    color_t col;
    if (intersect_x0 >= intersect_x1 || intersect_y0 >= intersect_y1) {
        // Nothing to copy
        clear_rect(dest, clear_x0, clear_y0, clear_x1, clear_y1);
        return;
    }
    if (x > xdest) {
        xstart = intersect_x0; xend = intersect_x1; xdel = 1;
    } else {
        xstart = intersect_x1-1; xend = intersect_x0-1; xdel = -1;
    }
    if (y > ydest) {
        ystart = intersect_y0; yend = intersect_y1; ydel = 1;
    } else {
        ystart = intersect_y1-1; yend = intersect_y0-1; ydel = -1;
    }
    for (int i = xstart; i != xend; i += xdel) {
        for (int j = ystart; j != yend; j += ydel) {
            col = imageGetPixelValue(src, i, j);
            imageSetPixelValue(dest, i+xdest-x, j+ydest-y, col);
        }
    }
    // Adjust intersection rectange to dest
    intersect_x0 += xdest-x;
    intersect_y0 += ydest-y;
    intersect_x1 += xdest-x;
    intersect_y1 += ydest-y;
    // Clear four rectangles in the cleared area surrounding the copied area.
    clear_rect(dest, clear_x0, clear_y0, intersect_x0, intersect_y1);
    clear_rect(dest, clear_x0, intersect_y1, intersect_x1, clear_y1);
    clear_rect(dest, intersect_x1, intersect_y0, clear_x1, clear_y1);
    clear_rect(dest, intersect_x0, clear_y0, clear_x1, intersect_y0);
}

machine_image_obj_t *image_shift(machine_image_obj_t *self, mp_int_t x, mp_int_t y) {
    machine_image_obj_t *result = image_make_new(self->width, self->width, 0);
    result->brightness = self->brightness;
    image_blit(self, result, x, y, self->width, self->width, 0, 0);
    return result;
}

STATIC machine_image_obj_t *image_crop(machine_image_obj_t *img, mp_int_t x, mp_int_t y, mp_int_t w, mp_int_t h) {
    if (w < 0)
        w = 0;
    if (h < 0)
        h = 0;
    machine_image_obj_t *result = image_make_new(w, h, 0);
    result->brightness = img->brightness;
    image_blit(img, result, x, y, w, h, 0, 0);
    return (machine_image_obj_t *)result;
}

mp_obj_t mpython_image_width(mp_obj_t self_in) {
    machine_image_obj_t *self = (machine_image_obj_t*)self_in;
    return MP_OBJ_NEW_SMALL_INT(self->width);
}
MP_DEFINE_CONST_FUN_OBJ_1(mpython_image_width_obj, mpython_image_width);

mp_obj_t mpython_image_height(mp_obj_t self_in) {
    machine_image_obj_t *self = (machine_image_obj_t*)self_in;
    return MP_OBJ_NEW_SMALL_INT(self->height);
}
MP_DEFINE_CONST_FUN_OBJ_1(mpython_image_height_obj, mpython_image_height);

mp_obj_t mpython_image_get_pixel(mp_obj_t self_in, mp_obj_t x_in, mp_obj_t y_in) {
    machine_image_obj_t *self = (machine_image_obj_t*)self_in;
    mp_int_t x = mp_obj_get_int(x_in);
    mp_int_t y = mp_obj_get_int(y_in);
    color_t col;
    if (x < 0 || y < 0) {
        mp_raise_ValueError(MP_ERROR_TEXT("index cannot be negative"));
    }
    if (x < self->width && y < self->height) {
        col = imageGetPixelValue(self, x, y);
        mp_obj_t tuple[3] = {
            tuple[0] = mp_obj_new_int(col.r),
            tuple[1] = mp_obj_new_int(col.g),
            tuple[2] = mp_obj_new_int(col.b),
        };
        return mp_obj_new_tuple(3, tuple);
    }
    mp_raise_ValueError(MP_ERROR_TEXT("index too large"));
}
MP_DEFINE_CONST_FUN_OBJ_3(mpython_image_get_pixel_obj, mpython_image_get_pixel);

/* Raise an exception if not mutable */
static void check_mutability(machine_image_obj_t *self) {
    // if (self->base.five) {
    //     mp_raise_TypeError(MP_ERROR_TEXT("image cannot be modified (try copying first)"));
    // }
}


mp_obj_t mpython_image_set_pixel(mp_uint_t n_args, const mp_obj_t *args) {
    (void)n_args;
    machine_image_obj_t *self = (machine_image_obj_t*)args[0];
    // check_mutability(self);
    mp_int_t x = mp_obj_get_int(args[1]);
    mp_int_t y = mp_obj_get_int(args[2]);
    color_t col;
    mp_int_t bright;
    if(mp_obj_is_integer(args[3]))
    {
        bright = mp_obj_get_int(args[3]);
        if (bright < 0 || bright > MAX_BRIGHTNESS) {
            mp_raise_ValueError(MP_ERROR_TEXT("brightness out of bounds"));
        }
        bright = (bright > 1) ? 1 : bright;
        col.r = 20;
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
    

    if (x < 0 || y < 0) {
        mp_raise_ValueError(MP_ERROR_TEXT("index cannot be negative"));
    }

    self->brightness = bright;
    
    if (x < self->width && y < self->height) {
        imageSetPixelValue(self, x, y, col);
        return mp_const_none;
    }
    mp_raise_ValueError(MP_ERROR_TEXT("index too large"));
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(mpython_image_set_pixel_obj, 4, 4, mpython_image_set_pixel);

mp_obj_t mpython_image_fill(mp_obj_t self_in, mp_obj_t n_in) {
    machine_image_obj_t *self = (machine_image_obj_t*)self_in;
    check_mutability(self);
    color_t col;
    if(mp_obj_is_integer(n_in))
    {
        mp_int_t n = mp_obj_get_int(n_in);
        if (n < 0 || n > MAX_BRIGHTNESS) {
            mp_raise_ValueError(MP_ERROR_TEXT("brightness out of bounds"));
        }
        n = (n > 1) ? 1 : n;
        self->brightness = n;
        col.r = 20;
        col.g =  0;
        col.b = 0;
    }
    else
    {
        self->brightness = 1;
        mp_obj_t *elem;
        mp_obj_get_array_fixed_n(n_in, 3, &elem);
        col.r = mp_obj_get_int(elem[0]);
        col.g = mp_obj_get_int(elem[1]);
        col.b = mp_obj_get_int(elem[2]);
    }
    imageFill(self, col);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(mpython_image_fill_obj, mpython_image_fill);

mp_obj_t mpython_image_blit(mp_uint_t n_args, const mp_obj_t *args) {
    machine_image_obj_t *self = (machine_image_obj_t*)args[0];
    check_mutability(self);

    mp_obj_t src = args[1];
    if (mp_obj_get_type(src) != &machine_image_type) {
        mp_raise_TypeError(MP_ERROR_TEXT("expecting an image"));
    }
    if (n_args == 7) {
        mp_raise_TypeError(MP_ERROR_TEXT("must specify both offsets"));
    }
    mp_int_t x = mp_obj_get_int(args[2]);
    mp_int_t y = mp_obj_get_int(args[3]);
    mp_int_t w = mp_obj_get_int(args[4]);
    mp_int_t h = mp_obj_get_int(args[5]);
    if (w < 0 || h < 0) {
        mp_raise_ValueError(MP_ERROR_TEXT("size cannot be negative"));
    }
    mp_int_t xdest;
    mp_int_t ydest;
    if (n_args == 6) {
        xdest = 0;
        ydest = 0;
    } else {
        xdest = mp_obj_get_int(args[6]);
        ydest = mp_obj_get_int(args[7]);
    }
    image_blit((machine_image_obj_t *)src, self, x, y, w, h, xdest, ydest);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(mpython_image_blit_obj, 6, 8, mpython_image_blit);

mp_obj_t mpython_image_crop(mp_uint_t n_args, const mp_obj_t *args) {
    (void)n_args;
    machine_image_obj_t *self = (machine_image_obj_t*)args[0];
    mp_int_t x0 = mp_obj_get_int(args[1]);
    mp_int_t y0 = mp_obj_get_int(args[2]);
    mp_int_t x1 = mp_obj_get_int(args[3]);
    mp_int_t y1 = mp_obj_get_int(args[4]);
    return image_crop(self, x0, y0, x1, y1);
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(mpython_image_crop_obj, 5, 5, mpython_image_crop);

mp_obj_t mpython_image_shift_left(mp_obj_t self_in, mp_obj_t n_in) {
    machine_image_obj_t *self = (machine_image_obj_t*)self_in;
    mp_int_t n = mp_obj_get_int(n_in);
    return image_shift(self, n, 0);
}
MP_DEFINE_CONST_FUN_OBJ_2(mpython_image_shift_left_obj, mpython_image_shift_left);

mp_obj_t mpython_image_shift_right(mp_obj_t self_in, mp_obj_t n_in) {
    machine_image_obj_t *self = (machine_image_obj_t*)self_in;
    mp_int_t n = mp_obj_get_int(n_in);
    return image_shift(self, -n, 0);
}
MP_DEFINE_CONST_FUN_OBJ_2(mpython_image_shift_right_obj, mpython_image_shift_right);

mp_obj_t mpython_image_shift_up(mp_obj_t self_in, mp_obj_t n_in) {
    machine_image_obj_t *self = (machine_image_obj_t*)self_in;
    mp_int_t n = mp_obj_get_int(n_in);
    return image_shift(self, 0, n);
}
MP_DEFINE_CONST_FUN_OBJ_2(mpython_image_shift_up_obj, mpython_image_shift_up);

mp_obj_t mpython_image_shift_down(mp_obj_t self_in, mp_obj_t n_in) {
    machine_image_obj_t *self = (machine_image_obj_t*)self_in;
    mp_int_t n = mp_obj_get_int(n_in);
    return image_shift(self, 0, -n);
}
MP_DEFINE_CONST_FUN_OBJ_2(mpython_image_shift_down_obj, mpython_image_shift_down);

mp_obj_t mpython_image_copy(mp_obj_t self_in) {
    machine_image_obj_t *self = (machine_image_obj_t*)self_in;
    return imageCopy(self);
}
MP_DEFINE_CONST_FUN_OBJ_1(mpython_image_copy_obj, mpython_image_copy);

mp_obj_t mpython_image_invert(mp_obj_t self_in) {
    machine_image_obj_t *self = (machine_image_obj_t*)self_in;
    return imageInvert(self);
}
MP_DEFINE_CONST_FUN_OBJ_1(mpython_image_invert_obj, mpython_image_invert);


STATIC const mp_map_elem_t mpython_image_locals_dict_table[] = {
    { MP_OBJ_NEW_QSTR(MP_QSTR_width), (mp_obj_t)&mpython_image_width_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_height), (mp_obj_t)&mpython_image_height_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_get_pixel), (mp_obj_t)&mpython_image_get_pixel_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_set_pixel), (mp_obj_t)&mpython_image_set_pixel_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_shift_left), (mp_obj_t)&mpython_image_shift_left_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_shift_right), (mp_obj_t)&mpython_image_shift_right_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_shift_up), (mp_obj_t)&mpython_image_shift_up_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_shift_down), (mp_obj_t)&mpython_image_shift_down_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_copy), (mp_obj_t)&mpython_image_copy_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_crop), (mp_obj_t)&mpython_image_crop_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_invert), (mp_obj_t)&mpython_image_invert_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_fill), (mp_obj_t)&mpython_image_fill_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_blit), (mp_obj_t)&mpython_image_blit_obj },
 
    { MP_OBJ_NEW_QSTR(MP_QSTR_HEART), (mp_obj_t)&mpython_const_image_heart_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_HEART_SMALL), (mp_obj_t)&mpython_const_image_heart_small_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_HAPPY), (mp_obj_t)&mpython_const_image_happy_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_SMILE), (mp_obj_t)&mpython_const_image_smile_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_SAD), (mp_obj_t)&mpython_const_image_sad_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CONFUSED), (mp_obj_t)&mpython_const_image_confused_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ANGRY), (mp_obj_t)&mpython_const_image_angry_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ASLEEP), (mp_obj_t)&mpython_const_image_asleep_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_SURPRISED), (mp_obj_t)&mpython_const_image_surprised_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_SILLY), (mp_obj_t)&mpython_const_image_silly_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_FABULOUS), (mp_obj_t)&mpython_const_image_fabulous_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_MEH), (mp_obj_t)&mpython_const_image_meh_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_YES), (mp_obj_t)&mpython_const_image_yes_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_NO), (mp_obj_t)&mpython_const_image_no_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CLOCK12), (mp_obj_t)&mpython_const_image_clock12_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CLOCK1), (mp_obj_t)&mpython_const_image_clock1_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CLOCK2), (mp_obj_t)&mpython_const_image_clock2_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CLOCK3), (mp_obj_t)&mpython_const_image_clock3_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CLOCK4), (mp_obj_t)&mpython_const_image_clock4_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CLOCK5), (mp_obj_t)&mpython_const_image_clock5_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CLOCK6), (mp_obj_t)&mpython_const_image_clock6_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CLOCK7), (mp_obj_t)&mpython_const_image_clock7_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CLOCK8), (mp_obj_t)&mpython_const_image_clock8_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CLOCK9), (mp_obj_t)&mpython_const_image_clock9_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CLOCK10), (mp_obj_t)&mpython_const_image_clock10_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CLOCK11), (mp_obj_t)&mpython_const_image_clock11_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ARROW_N), (mp_obj_t)&mpython_const_image_arrow_n_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ARROW_NE), (mp_obj_t)&mpython_const_image_arrow_ne_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ARROW_E), (mp_obj_t)&mpython_const_image_arrow_e_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ARROW_SE), (mp_obj_t)&mpython_const_image_arrow_se_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ARROW_S), (mp_obj_t)&mpython_const_image_arrow_s_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ARROW_SW), (mp_obj_t)&mpython_const_image_arrow_sw_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ARROW_W), (mp_obj_t)&mpython_const_image_arrow_w_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ARROW_NW), (mp_obj_t)&mpython_const_image_arrow_nw_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_TRIANGLE), (mp_obj_t)&mpython_const_image_triangle_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_TRIANGLE_LEFT), (mp_obj_t)&mpython_const_image_triangle_left_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_CHESSBOARD), (mp_obj_t)&mpython_const_image_chessboard_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_DIAMOND), (mp_obj_t)&mpython_const_image_diamond_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_DIAMOND_SMALL), (mp_obj_t)&mpython_const_image_diamond_small_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_SQUARE), (mp_obj_t)&mpython_const_image_square_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_SQUARE_SMALL), (mp_obj_t)&mpython_const_image_square_small_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_RABBIT), (mp_obj_t)&mpython_const_image_rabbit },
    { MP_OBJ_NEW_QSTR(MP_QSTR_COW), (mp_obj_t)&mpython_const_image_cow_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_MUSIC_CROTCHET), (mp_obj_t)&mpython_const_image_music_crotchet_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_MUSIC_QUAVER), (mp_obj_t)&mpython_const_image_music_quaver_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_MUSIC_QUAVERS), (mp_obj_t)&mpython_const_image_music_quavers_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_PITCHFORK), (mp_obj_t)&mpython_const_image_pitchfork_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_XMAS), (mp_obj_t)&mpython_const_image_xmas_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_PACMAN), (mp_obj_t)&mpython_const_image_pacman_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_TARGET), (mp_obj_t)&mpython_const_image_target_obj },
    // { MP_OBJ_NEW_QSTR(MP_QSTR_ALL_CLOCKS), (mp_obj_t)&mpython_const_image_all_clocks_tuple_obj }, 
    // { MP_OBJ_NEW_QSTR(MP_QSTR_ALL_ARROWS), (mp_obj_t)&mpython_const_image_all_arrows_tuple_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_TSHIRT), (mp_obj_t)&mpython_const_image_tshirt_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_ROLLERSKATE), (mp_obj_t)&mpython_const_image_rollerskate_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_DUCK), (mp_obj_t)&mpython_const_image_duck_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_HOUSE), (mp_obj_t)&mpython_const_image_house_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_TORTOISE), (mp_obj_t)&mpython_const_image_tortoise_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_BUTTERFLY), (mp_obj_t)&mpython_const_image_butterfly_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_STICKFIGURE), (mp_obj_t)&mpython_const_image_stickfigure_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_GHOST), (mp_obj_t)&mpython_const_image_ghost_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_SWORD), (mp_obj_t)&mpython_const_image_sword_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_GIRAFFE), (mp_obj_t)&mpython_const_image_giraffe_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_SKULL), (mp_obj_t)&mpython_const_image_skull_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_UMBRELLA), (mp_obj_t)&mpython_const_image_umbrella_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_SNAKE), (mp_obj_t)&mpython_const_image_snake_obj },
};

STATIC MP_DEFINE_CONST_DICT(mpython_image_locals_dict, mpython_image_locals_dict_table);


#define THE_FONT defaultFont

#define ASCII_START 32
#define ASCII_END 126
/* 获取字符在字符点阵中的索引 */
STATIC const unsigned char *get_font_data_from_char(char c) {
    if (c < ASCII_START || c > ASCII_END) {
        c = '?';
    }
    int offset = (c-ASCII_START) * 5;
    return THE_FONT + offset;
}

STATIC mp_int_t get_pixel_from_font_data(const unsigned char *data, int x, int y) {
    /* The following logic belongs in mpythonFont */
    return ((data[y]>>(4-x))&1);
}

void mpython_image_set_from_char(machine_image_obj_t *img, char c, color_t color) {
    const unsigned char *data = get_font_data_from_char(c);
    mp_int_t i;
    color_t col;
    for (int x = 0; x < 5; ++x) {
        for (int y = 0; y < 5; ++y) {
            i = get_pixel_from_font_data(data, x, y);
            col.r = i*color.r;
            col.g = i*color.g;
            col.b = i*color.b;
            imageSetPixelValue(img, x, y, col);
        }
    }
}


machine_image_obj_t *mpython_image_for_char(char c, mp_int_t bright, color_t color) {
    machine_image_obj_t *result = image_make_new(5, 5, bright);
    mpython_image_set_from_char(result, c, color);
    return (machine_image_obj_t *)result;
}

/* 调整整体亮度，fval：亮度倍数 */
void mpython_image_dim(machine_image_obj_t *lhs, mp_float_t fval) {
    if (fval < 0)
        mp_raise_ValueError(MP_ERROR_TEXT("brightness multiplier must not be negative"));

    lhs->brightness = min((int)(lhs->brightness*fval+0.5), MAX_BRIGHTNESS);
}

/* 两个图像加减（对应像素点加减），图像须一样大 */
machine_image_obj_t *mpython_image_sum(machine_image_obj_t *lhs, machine_image_obj_t *rhs, bool add) {
    mp_int_t h = lhs->height;
    mp_int_t w = lhs->width;
    if (rhs->height != h || lhs->width != w) {
        mp_raise_ValueError(MP_ERROR_TEXT("images must be the same size"));
    }
    machine_image_obj_t *result = image_make_new(w, h, 9);
    // color_t c1, c2;
    // for (int x = 0; x < w; ++x) {
    //     for (int y = 0; y < h; ++y) {
    //         int val;
    //         int lval = lhs->getPixelValue(x,y);
    //         int rval = rhs->getPixelValue(x,y);
    //         if (add)
    //             val = min(lval + rval, MAX_BRIGHTNESS);
    //         else
    //             val = max(0, lval - rval);
    //         result->setPixelValue(x, y, val);
    //     }
    // }
    return result;
}

STATIC mp_obj_t image_binary_op(mp_uint_t op, mp_obj_t lhs_in, mp_obj_t rhs_in) {
    if (mp_obj_get_type(lhs_in) != &machine_image_type) {
        return MP_OBJ_NULL; // op not supported
    }
    machine_image_obj_t *lhs = (machine_image_obj_t *)lhs_in;
    switch(op) {
    case MP_BINARY_OP_ADD:
    case MP_BINARY_OP_SUBTRACT:
        break;
    case MP_BINARY_OP_MULTIPLY:
         mpython_image_dim(lhs, mp_obj_get_float(rhs_in));
         return lhs;
    case MP_BINARY_OP_TRUE_DIVIDE:
        mpython_image_dim(lhs, 1.0/mp_obj_get_float(rhs_in));
        return lhs;
    default:
        return MP_OBJ_NULL; // op not supported
    }
    if (mp_obj_get_type(rhs_in) != &machine_image_type) {
        return MP_OBJ_NULL; // op not supported
    }
    return mpython_image_sum(lhs, (machine_image_obj_t *)rhs_in, op == MP_BINARY_OP_ADD);
}


const mp_obj_type_t machine_image_type = {
    { &mp_type_type },
    .name = MP_QSTR_MPIMAGE,
    .print = mpython_image_print,
    .make_new = mpython_image_make_new,
    .call = NULL,
    .unary_op = NULL,
    .binary_op = image_binary_op,
    .attr = NULL,
    .subscr = NULL,
    .getiter = NULL,
    .iternext = NULL,
    .buffer_p = {NULL},
    .protocol = NULL,
    .parent = NULL,
    .locals_dict = (mp_obj_dict_t*)&mpython_image_locals_dict,
};

const color_t blank_data[25] =
                         {{0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
                          {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
                          {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
                          {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, 
                          {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}, {0,0,0}
};
const machine_image_obj_t blank_image = {
    {&machine_image_type},
    .height = 5,
    .width = 5,
    .brightness = 0,
    .color = {0,0,0},
    .data = (color_t *)blank_data,
};

/* 记录一个待滚动字符串 */
typedef struct _scrolling_string_t {
    mp_obj_base_t base;
    char const *str;
    machine_image_obj_t *image;
    mp_uint_t len;
    mp_obj_t ref;
    bool monospace;
    bool repeat;
} scrolling_string_t;

typedef struct _scrolling_string_iterator_t {
    mp_obj_base_t base;
    mp_obj_t ref;
    machine_image_obj_t *img; /* 视窗图像（当前显示在点阵上的图像，滚动的过程就是更新此图偈 */
    char const *next_char; /* 下一个待显示字符 */
    char const *start; /* 记录待滚动字符串的起始位置（滚动不一定从字符串的第一个字符开始 */
    char const *end;  /* 流动结束字符串 */
    uint8_t offset;
    uint8_t offset_limit;
    bool monospace;
    bool repeat;
    char right;
} scrolling_string_iterator_t;

extern const mp_obj_type_t mpython_scrolling_string_type;
extern const mp_obj_type_t mpython_scrolling_string_iterator_type;

/* 创建一个滚动字符串对象 */
mp_obj_t scrolling_string_image_iterable(const char* str, mp_uint_t len, mp_obj_t ref, bool monospace, bool repeat, mp_int_t bright, color_t color) {
    scrolling_string_t *result = m_new_obj(scrolling_string_t);
    result->base.type = &mpython_scrolling_string_type;
    result->str = str;
    result->len = len;
    result->ref = ref;
    result->monospace = monospace;
    result->repeat = repeat;
    result->image = image_make_new(5, 5, bright);
    result->image->color = color;
    return result;
}

/* 测试某列是否为非空白列，是返回1 */
STATIC int font_column_non_blank(const unsigned char *font_data, unsigned int col) {
    for (int y = 0; y < 5; ++y) {
        if (get_pixel_from_font_data(font_data, col, y)) {
            return 1;
        }
    }
    return 0;
}

/* 查找最右边非空白列，Not strictly the rightmost non-blank column, but the rightmost in columns 2,3 or 4. */
STATIC unsigned int rightmost_non_blank_column(const unsigned char *font_data) {
    if (font_column_non_blank(font_data, 4)) {
        return 4;
    }
    if (font_column_non_blank(font_data, 3)) {
        return 3;
    }
    return 2;
}


static void restart(scrolling_string_iterator_t *iter) {
    iter->next_char = iter->start;
    iter->offset = 0;
    if (iter->start < iter->end) {
        iter->right = *iter->next_char;
        if (iter->monospace) {
            iter->offset_limit = 5;
        } else {
            iter->offset_limit = rightmost_non_blank_column(get_font_data_from_char(iter->right)) + 1;
        }
    } else {
        iter->right = ' ';
        iter->offset_limit = 5;
    }
}

/* 迭代器创建 */
STATIC mp_obj_t get_mpython_scrolling_string_iter(mp_obj_t o_in, mp_obj_iter_buf_t *iter_buf) {
    (void)iter_buf; // not big enough to hold scrolling_string_iterator_t
    scrolling_string_t *str = (scrolling_string_t *)o_in;
    scrolling_string_iterator_t *result = m_new_obj(scrolling_string_iterator_t);
    result->base.type = &mpython_scrolling_string_iterator_type;
    result->img = str->image;   
    result->start = str->str;
    result->ref = str->ref;
    result->monospace = str->monospace;
    result->end = result->start + str->len;
    result->repeat = str->repeat;
    restart(result);
    return result;
}

/* 字符串滚动，一次滚动一列，须处理两个字符各有一部分显示在视窗这种情况 */
STATIC mp_obj_t mpython_scrolling_string_iter_next(mp_obj_t o_in) {
    color_t col;
    scrolling_string_iterator_t *iter = (scrolling_string_iterator_t *)o_in;
    if (iter->next_char == iter->end && iter->offset == 5) {
        if (iter->repeat) {
            restart(iter);
            imageClear(iter->img);
        } else {
            return MP_OBJ_STOP_ITERATION;
        }
    }
    for (int x = 0; x < 4; x++) { /* n+1列点移动n列 */
        for (int y = 0; y < 5; y++) {
            col = imageGetPixelValue(iter->img, x+1, y);          
            imageSetPixelValue(iter->img, x, y, col);
        }
    }
    col.r = 0;
    col.g = 0;
    col.b = 0;
    for (int y = 0; y < 5; y++) { /* 清空第5列 */
        imageSetPixelValue(iter->img, 4, y, col);
    }
    const unsigned char *font_data;
    if (iter->offset < iter->offset_limit) {
        font_data = get_font_data_from_char(iter->right);
        for (int y = 0; y < 5; ++y) { /* 把下一个字符第offset列，更新到视窗图像第5列 */
            int pix = get_pixel_from_font_data(font_data, iter->offset, y);
            if(pix == 1)
                col = iter->img->color;
            else 
            {
                col.r = 0;
                col.g = 0;
                col.b = 0;
            }
            imageSetPixelValue(iter->img, 4, y, col);
        }
    } else if (iter->offset == iter->offset_limit) {
        ++iter->next_char;
        if (iter->next_char == iter->end) {
            iter->right = ' ';
            iter->offset_limit = 5;
            iter->offset = 0;
        } else {
            iter->right = *iter->next_char;
            font_data = get_font_data_from_char(iter->right);
            if (iter->monospace) {
                iter->offset = -1;
                iter->offset_limit = 5;
            } else {
                iter->offset = -font_column_non_blank(font_data, 0);
                iter->offset_limit = rightmost_non_blank_column(font_data)+1;
            }
        }
    }
    ++iter->offset;
    return iter->img; //返回更新好的待显示在视窗的图像
}

const mp_obj_type_t mpython_scrolling_string_type = { //基类，用于创建迭代器
    { &mp_type_type },
    .name = MP_QSTR_ScrollingString,
    .print = NULL,
    .make_new = NULL,
    .call = NULL,
    .unary_op = NULL,
    .binary_op = NULL,
    .attr = NULL,
    .subscr = NULL,
    .getiter = get_mpython_scrolling_string_iter, //迭代器创建函数
    .iternext = NULL,
    .buffer_p = {NULL},
    .protocol = NULL,
    .parent = NULL,
    .locals_dict = NULL,
};

const mp_obj_type_t mpython_scrolling_string_iterator_type = {
    { &mp_type_type },
    .name = MP_QSTR_iterator,
    .print = NULL,
    .make_new = NULL,
    .call = NULL,
    .unary_op = NULL,
    .binary_op = NULL,
    .attr = NULL,
    .subscr = NULL,
    .getiter = mp_identity_getiter,
    .iternext = mpython_scrolling_string_iter_next, //迭代器的next操作
    .buffer_p = {NULL},
    .protocol = NULL,
    .parent = NULL,
    .locals_dict = NULL,
};

/** Facade types to present a string as a sequence of images.
 * These are necessary to avoid allocation during iteration,
 * which may happen in interrupt handlers.
 * 以下实现对字符串中的某个字符转image,并利用迭代器实现按索引递境转换
 */

typedef struct _string_image_facade_t {
    mp_obj_base_t base;
    mp_obj_t string;
    machine_image_obj_t *image;
    bool repeat;
} string_image_facade_t;

/* 把string_image_facade_t 结构中字符指定索引字符转为image */
static mp_obj_t string_image_facade_subscr(mp_obj_t self_in, mp_obj_t index_in, mp_obj_t value) {
    if (value == MP_OBJ_SENTINEL) {
        // Fill in image
        string_image_facade_t *self = (string_image_facade_t *)self_in;
        mp_uint_t len;
        const char *text = mp_obj_str_get_data(self->string, &len);
        mp_uint_t index = mp_get_index(self->base.type, len, index_in, false);
        mpython_image_set_from_char(self->image, text[index], self->image->color);
        return self->image;
    } else {
        return MP_OBJ_NULL; // op not supported
    }
}

/* 返回string_image_facade_t中字符长 */
static mp_obj_t facade_unary_op(mp_uint_t op, mp_obj_t self_in) {
    string_image_facade_t *self = (string_image_facade_t *)self_in;
    switch (op) {
        case MP_UNARY_OP_LEN:
            return mp_obj_len(self->string);
        default: return MP_OBJ_NULL; // op not supported
    }
}

static mp_obj_t mpython_facade_iterator(mp_obj_t iterable_in, mp_obj_iter_buf_t *iter_buf);

const mp_obj_type_t string_image_facade_type = { //string_image_facade的父类
    { &mp_type_type },
    .name = MP_QSTR_Facade,
    .print = NULL,
    .make_new = NULL,
    .call = NULL,
    .unary_op = facade_unary_op, //操作：返回字符串长
    .binary_op = NULL,
    .attr = NULL,
    .subscr = string_image_facade_subscr, //操作：按索引转字符为image
    .getiter = mpython_facade_iterator, //操作：制作一个迭代器
    .iternext = NULL,
    .buffer_p = {NULL},
    .protocol = NULL,
    .parent = NULL,
    NULL
};


typedef struct _facade_iterator_t {  //结构：用于记录迭代器当前迭代位置信息。
    mp_obj_base_t base;
    mp_obj_t string;
    mp_uint_t index;
    machine_image_obj_t *image;
    bool repeat;
} facade_iterator_t;

/* 新建一个string_image_facade_t对象*/
mp_obj_t mpython_string_facade(mp_obj_t string, mp_int_t bright, color_t color, bool repeat) {
    string_image_facade_t *result = m_new_obj(string_image_facade_t);
    result->base.type = &string_image_facade_type;
    result->string = string;
    result->image = image_make_new(5, 5, bright);
    result->image->color = color;
    result->repeat = repeat;
    return (mp_obj_t)result;
}

/* 迭代器的next操作，实现把string的下一个字符转image */
static mp_obj_t mpython_facade_iter_next(mp_obj_t iter_in) {
    facade_iterator_t *iter = (facade_iterator_t *)iter_in;
    mp_uint_t len;
    const char *text = mp_obj_str_get_data(iter->string, &len);
    if (iter->index >= len) {
        if (iter->repeat) {
            iter->index = 0;
        }
        else  
            return MP_OBJ_STOP_ITERATION;
    }
    mpython_image_set_from_char(iter->image, text[iter->index], iter->image->color);
    iter->index++;
    return iter->image;
}

const mp_obj_type_t mpython_facade_iterator_type = { //基类，实现记录和获取下一个字符
    { &mp_type_type }, 
    .name = MP_QSTR_iterator,
    .print = NULL,
    .make_new = NULL,
    .call = NULL,
    .unary_op = NULL,
    .binary_op = NULL,
    .attr = NULL,
    .subscr = NULL,
    .getiter = mp_identity_getiter,
    .iternext = mpython_facade_iter_next,
    .buffer_p = {NULL},
    .protocol = NULL,
    .parent = NULL,
    NULL
};

/* 制作一个迭代器，实现按索引迭代转字符串中字符为image */
static mp_obj_t mpython_facade_iterator(mp_obj_t iterable_in, mp_obj_iter_buf_t *iter_buf) {
    // assert(sizeof(facade_iterator_t) <= sizeof(mp_obj_iter_buf_t));
    (void)iter_buf;
    facade_iterator_t *result = m_new_obj(facade_iterator_t);
    string_image_facade_t *iterable = (string_image_facade_t *)iterable_in;
    result->base.type = &mpython_facade_iterator_type;
    result->string = iterable->string;
    result->image = iterable->image;
    result->repeat = iterable->repeat;
    result->index = 0;
    return result;
}