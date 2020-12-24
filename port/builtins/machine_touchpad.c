/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2017 Nick Moore
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


#include <stdio.h>

#include "esp_log.h"

#include "driver/gpio.h"
#include "driver/touch_pad.h"

#include "py/runtime.h"
#include "py/mphal.h"
#include "modmachine.h"

typedef struct _mtp_obj_t {
    mp_obj_base_t base;
    gpio_num_t gpio_id;
    touch_pad_t touchpad_id;
} mtp_obj_t;

STATIC const mtp_obj_t touchpad_obj[] = {
    {{&machine_touchpad_type}, GPIO_NUM_4, TOUCH_PAD_NUM0},
    {{&machine_touchpad_type}, GPIO_NUM_0, TOUCH_PAD_NUM1},
    {{&machine_touchpad_type}, GPIO_NUM_2, TOUCH_PAD_NUM2},
    {{&machine_touchpad_type}, GPIO_NUM_15, TOUCH_PAD_NUM3},
    {{&machine_touchpad_type}, GPIO_NUM_13, TOUCH_PAD_NUM4},
    {{&machine_touchpad_type}, GPIO_NUM_12, TOUCH_PAD_NUM5},
    {{&machine_touchpad_type}, GPIO_NUM_14, TOUCH_PAD_NUM6},
    {{&machine_touchpad_type}, GPIO_NUM_27, TOUCH_PAD_NUM7},
    {{&machine_touchpad_type}, GPIO_NUM_33, TOUCH_PAD_NUM8},
    {{&machine_touchpad_type}, GPIO_NUM_32, TOUCH_PAD_NUM9},
};

static bool is_touchpad_intr_enabled = false;
static bool is_touchpad_all_released = true;
static esp_timer_handle_t touchpad_timer = NULL;
static uint16_t touchpad_inactive_timeout[10] = {0};

STATIC mp_obj_t mtp_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw,
    const mp_obj_t *args) {

    mp_arg_check_num(n_args, n_kw, 1, 1, true);
    gpio_num_t pin_id = machine_pin_get_id(args[0]);
    const mtp_obj_t *self = NULL;
    for (int i = 0; i < MP_ARRAY_SIZE(touchpad_obj); i++) {
        if (pin_id == touchpad_obj[i].gpio_id) {
            self = &touchpad_obj[i];
            break;
        }
    }
    if (!self) {
        mp_raise_ValueError(MP_ERROR_TEXT("invalid pin for touchpad"));
    }

    static int initialized = 0;
    if (!initialized) {
        touch_pad_init();
        touch_pad_set_fsm_mode(TOUCH_FSM_MODE_TIMER);
        initialized = 1;
    }
    esp_err_t err = touch_pad_config(self->touchpad_id, 0);
    if (err == ESP_OK) {
        return MP_OBJ_FROM_PTR(self);
    }
    mp_raise_ValueError(MP_ERROR_TEXT("Touch pad error"));
}

STATIC mp_obj_t mtp_config(mp_obj_t self_in, mp_obj_t value_in) {
    mtp_obj_t *self = self_in;
    uint16_t value = mp_obj_get_int(value_in);
    esp_err_t err = touch_pad_config(self->touchpad_id, value);
    if (err == ESP_OK) {
        return mp_const_none;
    }
    mp_raise_ValueError(MP_ERROR_TEXT("Touch pad error"));
}
MP_DEFINE_CONST_FUN_OBJ_2(mtp_config_obj, mtp_config);

STATIC mp_obj_t mtp_read(mp_obj_t self_in) {
    mtp_obj_t *self = self_in;
    uint16_t value;
    esp_err_t err = touch_pad_read(self->touchpad_id, &value);
    if (err == ESP_ERR_INVALID_STATE) { // when touchpad has been short-circuited, do not raise error
        return MP_OBJ_NEW_SMALL_INT(0);
    }   
    if (err == ESP_OK) {
        return MP_OBJ_NEW_SMALL_INT(value);
    }
    mp_raise_ValueError(MP_ERROR_TEXT("Touch pad error"));
}
MP_DEFINE_CONST_FUN_OBJ_1(mtp_read_obj, mtp_read);

STATIC void machine_touchpad_timer_cb(void *args)
{
    int inactive_pad_num = 0;
    for (int i = 0; i < MP_ARRAY_SIZE(touchpad_obj);i++) {
        if (touchpad_inactive_timeout[i]) {
            touchpad_inactive_timeout[i]--;
            if (touchpad_inactive_timeout[i] == 0) {
                mp_obj_t handler = MP_STATE_PORT(machine_touchpad_irq_handler)[i];
                mp_sched_schedule(handler, mp_obj_new_int(0));
                inactive_pad_num++;
            }
        }
    }
    // all touchpad released
    if (inactive_pad_num == 10 && is_touchpad_all_released == false) {
        is_touchpad_all_released = true;
        esp_timer_stop(touchpad_timer);
    }
}

STATIC void machine_touchpad_isr_handler(void *arg) 
{
    static uint32_t pre_pad_intr = 0;
    uint32_t pad_intr = touch_pad_get_status();
    //clear interrupt
    touch_pad_clear_status();

    // debounce
    if (pre_pad_intr != pad_intr) {
        pre_pad_intr = pad_intr;
        return;
    }
    
    for (int i = 0; i < MP_ARRAY_SIZE(touchpad_obj); i++) {
        mp_obj_t handler = MP_STATE_PORT(machine_touchpad_irq_handler)[i];
        if ((pad_intr >> i) & 0x01 && handler != MP_OBJ_NULL) {
            if (touchpad_inactive_timeout[i] == 0) {
                mp_sched_schedule(handler, mp_obj_new_int(1));
            }
            touchpad_inactive_timeout[i] = 10;   // 50ms
        }
    } 

    if (is_touchpad_all_released == true) {
        is_touchpad_all_released = false;
        esp_timer_start_periodic(touchpad_timer, 10*1000);
    }
    mp_hal_wake_main_task_from_isr();    
}

// touchpad.irq(handler=None, threshold=400)
STATIC mp_obj_t machine_touchpad_irq(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum { ARG_handler, ARG_threshold};
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_handler, MP_ARG_OBJ, {.u_obj = mp_const_none} },
        { MP_QSTR_threshold, MP_ARG_INT, {.u_int = 400} },
    };
    mtp_obj_t *self = MP_OBJ_TO_PTR(pos_args[0]);
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (n_args > 1 || kw_args->used != 0) {
        // configure irq
        mp_obj_t handler = args[ARG_handler].u_obj;
        uint32_t threshold = args[ARG_threshold].u_int;
        if (handler == mp_const_none) {
            handler = MP_OBJ_NULL;
        }
        // if (threshold < 30 || threshold > 100) {
        //     mp_raise_ValueError(MP_ERROR_TEXT("threshold value out of range"));
        // }
        MP_STATE_PORT(machine_touchpad_irq_handler)[self->touchpad_id] = handler;
        touch_pad_set_thresh(self->touchpad_id, threshold);
        // touch_pad_isr_deregister()
        if (is_touchpad_intr_enabled == false) {
            touch_pad_isr_register(machine_touchpad_isr_handler, NULL);
            touch_pad_intr_enable();
            is_touchpad_intr_enabled = true;
            is_touchpad_all_released = true;

            const esp_timer_create_args_t timer_args = {
                .callback = machine_touchpad_timer_cb,
                .name = "touchpad timer"
            };
            ESP_ERROR_CHECK(esp_timer_create(&timer_args, &touchpad_timer));
            // esp_timer_start_periodic(touchpad_timer, 25*1000);
        }
    }
    // return the irq object
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(machine_touchpad_irq_obj, 1, machine_touchpad_irq);

STATIC const mp_rom_map_elem_t mtp_locals_dict_table[] = {
    // instance methods
    { MP_ROM_QSTR(MP_QSTR_config), MP_ROM_PTR(&mtp_config_obj) },
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&mtp_read_obj) },
    { MP_ROM_QSTR(MP_QSTR_irq), MP_ROM_PTR(&machine_touchpad_irq_obj)},
};

STATIC MP_DEFINE_CONST_DICT(mtp_locals_dict, mtp_locals_dict_table);

const mp_obj_type_t machine_touchpad_type = {
    { &mp_type_type },
    .name = MP_QSTR_TouchPad,
    .make_new = mtp_make_new,
    .locals_dict = (mp_obj_t)&mtp_locals_dict,
};
