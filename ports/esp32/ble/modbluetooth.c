#include <stdio.h>
#include <string.h>

#include "py/obj.h"
#include "py/objstr.h"
#include "py/runtime.h"
#include "mphalport.h"

#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/timers.h"

#include "./include/mpython_ble_gap_profile.h"
#include "./include/mpython_ble_service_hidd.h"
#include "./include/mpython_ble_service_board.h"

/**
 * ble_init(name='mpython')
 */
STATIC mp_obj_t ble_init(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args)
{
    const char *device_name = "mpython";
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_name, MP_ARG_OBJ, {.u_obj = mp_const_none} }
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (n_args != 0 || kw_args->used != 0) {
        if (args[0].u_obj != mp_const_none) {
            size_t len;
            mpython_ble_peripheral_init(mp_obj_str_get_data(args[0].u_obj, &len));
            return mp_const_none;
        }
    }
    mpython_ble_peripheral_init(device_name);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(ble_init_obj, 0, ble_init);

/**
 * bluetooth_start_advertising()
 */
STATIC mp_obj_t bluetooth_start_advertising(void)
{
    mpython_ble_gap_start_advertising();
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(bluetooth_start_advertising_obj, bluetooth_start_advertising);

/**
 * bluetooth_stop_advertising();
 */
STATIC mp_obj_t bluetooth_stop_advertising(void)
{
    mpython_ble_gap_stop_advertising();
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(bluetooth_stop_advertising_obj, bluetooth_stop_advertising);

/**
 * ble_board_send(buff)
 */
STATIC mp_obj_t ble_board_send(mp_obj_t buff)
{
    mp_buffer_info_t buffinfo;
    mp_get_buffer_raise(buff, &buffinfo, MP_BUFFER_READ);

    if (buffinfo.len <= 16) {
        board_service_send_notify(buffinfo.buf, buffinfo.len);
    }
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(ble_board_send_obj, ble_board_send);


/**
 * ble_board_register_output_callback(callback)
 */
static mp_obj_t ble_board_write_handler = mp_const_none;
static void ble_board_write_callback(uint8_t *value, uint8_t len)
{
    mp_obj_t arg = mp_obj_new_str_copy(&mp_type_bytes, value, len);
    mp_sched_schedule(ble_board_write_handler, arg);
}

STATIC mp_obj_t ble_board_register_output_callback(mp_obj_t callback)
{
    ble_board_write_handler = callback;
    board_service_register_output_callback(ble_board_write_callback);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(ble_board_register_ouput_callback_obj, ble_board_register_output_callback);


/**
 * hidd_send_consumer(ble.HID_CONSUMER_xxx, keyPressed=true)
 */
STATIC mp_obj_t ble_hidd_send_consumer(mp_obj_t key_cmd, mp_obj_t key_pressed)
{
    uint8_t cmd = mp_obj_get_int(key_cmd);
    bool pressed = mp_obj_is_true(key_pressed);
    esp_hidd_send_consumer_value(cmd, pressed);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(ble_hidd_send_consumer_obj, ble_hidd_send_consumer);


/**
 * hidd_send_keyboard(keys = [key1...], modifier = KEY_MASK_NONE)
 */
STATIC mp_obj_t ble_hidd_send_keyboard(size_t n_args, const mp_obj_t * pos_args, mp_map_t *kw_args)
{
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_keys, MP_ARG_OBJ, {.u_obj = mp_const_none} },
        { MP_QSTR_modifier, MP_ARG_INT, {.u_int = 0} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    uint8_t modifier = 0;
    uint8_t key_codes[6] = {0};
    uint8_t key_num = 0;
    if (n_args !=0 || kw_args->used != 0) {
        mp_obj_t *keys;
        mp_uint_t len;
        if (!mp_obj_equal(args[0].u_obj, mp_const_none)) {
            mp_obj_get_array(args[0].u_obj, &len, &keys);
            
            len = (len < 6) ? len : 6;
            for (int i = 0; i < len; i++) {
                key_codes[i] = (uint8_t)mp_obj_get_int(keys[i]);
            }
            key_num = len;
        }
        modifier = (uint8_t)(args[1].u_int);
    }

    esp_hidd_send_keyboard_value(modifier, key_codes, key_num);

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(ble_hidd_send_keyboard_obj, 0, ble_hidd_send_keyboard);

/**
 * hidd_send_mouse(button = HID_MOUSE_xxx, x = 0, y = 0, wheel = 0)
 */
STATIC mp_obj_t hidd_send_mouse(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args)
{
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_button, MP_ARG_INT, {.u_int = 0} },
        { MP_QSTR_x, MP_ARG_INT, {.u_int = 0} },
        { MP_QSTR_y, MP_ARG_INT, {.u_int = 0} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    mouse_cmd_t btn = (mouse_cmd_t)args[0].u_int;
    int8_t x = args[1].u_int;
    int8_t y = args[2].u_int;

    esp_hidd_send_mouse_value(btn, x, y);

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(hidd_send_mouse_obj, 0, hidd_send_mouse);

const mp_rom_map_elem_t ble_locals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_ble)},
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&ble_init_obj)},
    { MP_ROM_QSTR(MP_QSTR_start_advertising), MP_ROM_PTR(&bluetooth_start_advertising_obj)},
    { MP_ROM_QSTR(MP_QSTR_stop_advertising), MP_ROM_PTR(&bluetooth_stop_advertising_obj)},
    { MP_ROM_QSTR(MP_QSTR_board_send), MP_ROM_PTR(&ble_board_send_obj)},
    { MP_ROM_QSTR(MP_QSTR_board_register_output_callback), MP_ROM_PTR(&ble_board_register_ouput_callback_obj) },
    { MP_ROM_QSTR(MP_QSTR_hidd_send_consumer), MP_ROM_PTR(&ble_hidd_send_consumer_obj)},
    { MP_ROM_QSTR(MP_QSTR_hidd_send_keyboard), MP_ROM_PTR(&ble_hidd_send_keyboard_obj)},
    { MP_ROM_QSTR(MP_QSTR_hidd_send_mouse), MP_ROM_PTR(&hidd_send_mouse_obj)},

    { MP_ROM_QSTR(MP_QSTR_KEY_MASK_NONE), MP_ROM_INT(0)},
    { MP_ROM_QSTR(MP_QSTR_KEY_MASK_L_CTRL), MP_ROM_INT(LEFT_CONTROL_KEY_MASK)},
    { MP_ROM_QSTR(MP_QSTR_KEY_MASK_L_SHIFT), MP_ROM_INT(LEFT_SHIFT_KEY_MASK)},
    { MP_ROM_QSTR(MP_QSTR_KEY_MASK_L_ALT), MP_ROM_INT(LEFT_ALT_KEY_MASK)},
    { MP_ROM_QSTR(MP_QSTR_KEY_MASK_L_GUI), MP_ROM_INT(LEFT_GUI_KEY_MASK)},
    { MP_ROM_QSTR(MP_QSTR_KEY_MASK_R_CTRL), MP_ROM_INT(RIGHT_CONTROL_KEY_MASK)},
    { MP_ROM_QSTR(MP_QSTR_KEY_MASK_R_SHIFT), MP_ROM_INT(RIGHT_SHIFT_KEY_MASK)},
    { MP_ROM_QSTR(MP_QSTR_KEY_MASK_R_ALT), MP_ROM_INT(RIGHT_ALT_KEY_MASK)},
    { MP_ROM_QSTR(MP_QSTR_KEY_MASK_R_GUI), MP_ROM_INT(RIGHT_GUI_KEY_MASK)},

    { MP_ROM_QSTR(MP_QSTR_HID_KEY_A), MP_ROM_INT(HID_KEY_A)},   //             4    // Keyboard a and A
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_B), MP_ROM_INT(HID_KEY_B)},   //              5    // Keyboard b and B
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_C), MP_ROM_INT(HID_KEY_C)},   //              6    // Keyboard c and C
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_D), MP_ROM_INT(HID_KEY_D)},   //              7    // Keyboard d and D
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_E), MP_ROM_INT(HID_KEY_E)},   //              8    // Keyboard e and E
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F), MP_ROM_INT(HID_KEY_F)},   //              9    // Keyboard f and F
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_G), MP_ROM_INT(HID_KEY_G)},   //              10   // Keyboard g and G
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_H), MP_ROM_INT(HID_KEY_H)},   //              11   // Keyboard h and H
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_I), MP_ROM_INT(HID_KEY_I)},   //              12   // Keyboard i and I
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_J), MP_ROM_INT(HID_KEY_J)},   //              13   // Keyboard j and J
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_K), MP_ROM_INT(HID_KEY_K)},   //              14   // Keyboard k and K
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_L), MP_ROM_INT(HID_KEY_L)},   //              15   // Keyboard l and L
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_M), MP_ROM_INT(HID_KEY_M)},   //              16   // Keyboard m and M
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_N), MP_ROM_INT(HID_KEY_N)},   //              17   // Keyboard n and N
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_O), MP_ROM_INT(HID_KEY_O)},   //              18   // Keyboard o and O
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_P), MP_ROM_INT(HID_KEY_P)},   //              19   // Keyboard p and p
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_Q), MP_ROM_INT(HID_KEY_Q)},   //              20   // Keyboard q and Q
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_R), MP_ROM_INT(HID_KEY_R)},   //              21   // Keyboard r and R
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_S), MP_ROM_INT(HID_KEY_S)},   //              22   // Keyboard s and S
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_T), MP_ROM_INT(HID_KEY_T)},   //              23   // Keyboard t and T
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_U), MP_ROM_INT(HID_KEY_U)},   //              24   // Keyboard u and U
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_V), MP_ROM_INT(HID_KEY_V)},   //              25   // Keyboard v and V
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_W), MP_ROM_INT(HID_KEY_W)},   //              26   // Keyboard w and W
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_X), MP_ROM_INT(HID_KEY_X)},   //              27   // Keyboard x and X
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_Y), MP_ROM_INT(HID_KEY_Y)},   //              28   // Keyboard y and Y
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_Z), MP_ROM_INT(HID_KEY_Z)},   //              29   // Keyboard z and Z
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_1), MP_ROM_INT(HID_KEY_1)},   //              30   // Keyboard 1 and !
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_2), MP_ROM_INT(HID_KEY_2)},   //              31   // Keyboard 2 and @
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_3), MP_ROM_INT(HID_KEY_3)},   //              32   // Keyboard 3 and #
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_4), MP_ROM_INT(HID_KEY_4)},   //              33   // Keyboard 4 and %
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_5), MP_ROM_INT(HID_KEY_5)},   //              34   // Keyboard 5 and %
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_6), MP_ROM_INT(HID_KEY_6)},   //              35   // Keyboard 6 and ^
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_7), MP_ROM_INT(HID_KEY_7)},   //              36   // Keyboard 7 and &
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_8), MP_ROM_INT(HID_KEY_8)},   //              37   // Keyboard 8 and *
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_9), MP_ROM_INT(HID_KEY_9)},   //              38   // Keyboard 9 and (
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_0), MP_ROM_INT(HID_KEY_0)},   //              39   // Keyboard 0 and )
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_RETURN), MP_ROM_INT(HID_KEY_RETURN)},   //         40   // Keyboard Return (ENTER)
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_ESCAPE), MP_ROM_INT(HID_KEY_ESCAPE)},   //         41   // Keyboard ESCAPE
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_DELTE), MP_ROM_INT(HID_KEY_DELETE)},   //         42   // Keyboard DELETE (Backspace)
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_TAB), MP_ROM_INT(HID_KEY_TAB)},   //            43   // Keyboard Tab
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_SPACE), MP_ROM_INT(HID_KEY_SPACEBAR)},   //       44   // Keyboard Spacebar
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_MINUS), MP_ROM_INT(HID_KEY_MINUS)},   //          45   // Keyboard - and (underscore)
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_EQUAL), MP_ROM_INT(HID_KEY_EQUAL)},   //          46   // Keyboard = and +
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_LEFT_BRKT), MP_ROM_INT(HID_KEY_LEFT_BRKT)},   //      47   // Keyboard [ and {
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_RIGHT_BRKT), MP_ROM_INT(HID_KEY_RIGHT_BRKT)},   //     48   // Keyboard ] and }
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_BACK_SLASH), MP_ROM_INT(HID_KEY_BACK_SLASH)},   //     49   // Keyboard \ and |
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_SEMI_COLON), MP_ROM_INT(HID_KEY_SEMI_COLON)},   //     51   // Keyboard ; and :
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_SGL_QUOTE), MP_ROM_INT(HID_KEY_SGL_QUOTE)},   //      52   // Keyboard ' and "
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_GRV_ACCENT), MP_ROM_INT(HID_KEY_GRV_ACCENT)},   //     53   // Keyboard Grave Accent and Tilde
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_COMMA), MP_ROM_INT(HID_KEY_COMMA)},   //          54   // Keyboard , and <
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_DOT), MP_ROM_INT(HID_KEY_DOT)},   //            55   // Keyboard . and >
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_FWD_SLASH), MP_ROM_INT(HID_KEY_FWD_SLASH)},   //      56   // Keyboard / and ?
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_CAPS_LOCK), MP_ROM_INT(HID_KEY_CAPS_LOCK)},   //      57   // Keyboard Caps Lock
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F1), MP_ROM_INT(HID_KEY_F1)},   //             58   // Keyboard F1
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F2), MP_ROM_INT(HID_KEY_F2)},   //             59   // Keyboard F2
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F3), MP_ROM_INT(HID_KEY_F3)},   //             60   // Keyboard F3
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F4), MP_ROM_INT(HID_KEY_F4)},   //             61   // Keyboard F4
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F5), MP_ROM_INT(HID_KEY_F5)},   //             62   // Keyboard F5
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F6), MP_ROM_INT(HID_KEY_F6)},   //             63   // Keyboard F6
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F7), MP_ROM_INT(HID_KEY_F7)},   //             64   // Keyboard F7
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F8), MP_ROM_INT(HID_KEY_F8)},   //             65   // Keyboard F8
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F9), MP_ROM_INT(HID_KEY_F9)},   //             66   // Keyboard F9
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F10), MP_ROM_INT(HID_KEY_F10)},   //            67   // Keyboard F10
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F11), MP_ROM_INT(HID_KEY_F11)},   //            68   // Keyboard F11
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_F12), MP_ROM_INT(HID_KEY_F12)},   //            69   // Keyboard F12
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_PRNT_SCREEN), MP_ROM_INT(HID_KEY_PRNT_SCREEN)},   //    70   // Keyboard Print Screen
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_SCROLL_LOCK), MP_ROM_INT(HID_KEY_SCROLL_LOCK)},   //    71   // Keyboard Scroll Lock
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_PAUSE), MP_ROM_INT(HID_KEY_PAUSE)},   //          72   // Keyboard Pause
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_INSERT), MP_ROM_INT(HID_KEY_INSERT)},   //         73   // Keyboard Insert
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_HOME), MP_ROM_INT(HID_KEY_HOME)},   //           74   // Keyboard Home
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_PAGE_UP), MP_ROM_INT(HID_KEY_PAGE_UP)},   //        75   // Keyboard PageUp
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_DELETE_FWD), MP_ROM_INT(HID_KEY_DELETE_FWD)},   //     76   // Keyboard Delete Forward
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_END), MP_ROM_INT(HID_KEY_END)},   //            77   // Keyboard End
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_PAGE_DOWN), MP_ROM_INT(HID_KEY_PAGE_DOWN)},   //      78   // Keyboard PageDown
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_RIGHT_ARROW), MP_ROM_INT(HID_KEY_RIGHT_ARROW)},   //    79   // Keyboard RightArrow
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_LEFT_ARROW), MP_ROM_INT(HID_KEY_LEFT_ARROW)},   //     80   // Keyboard LeftArrow
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_DOWN_ARROW), MP_ROM_INT(HID_KEY_DOWN_ARROW)},   //     81   // Keyboard DownArrow
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_UP_ARROW), MP_ROM_INT(HID_KEY_UP_ARROW)},   //       82   // Keyboard UpArrow
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_NUM_LOCK), MP_ROM_INT(HID_KEY_NUM_LOCK)},   //       83   // Keypad Num Lock and Clear
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_DIVIDE), MP_ROM_INT(HID_KEY_DIVIDE)},   //         84   // Keypad /
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_MULTIPLY), MP_ROM_INT(HID_KEY_MULTIPLY)},   //       85   // Keypad *
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_SUBTRACT), MP_ROM_INT(HID_KEY_SUBTRACT)},   //       86   // Keypad -
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_ADD), MP_ROM_INT(HID_KEY_ADD)},   //            87   // Keypad +
    { MP_ROM_QSTR(MP_QSTR_HID_KEY_ENTER), MP_ROM_INT(HID_KEY_ENTER)},   //          88   // Keypad ENTER
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_1), MP_ROM_INT(HID_KEYPAD_1)},   //           89   // Keypad 1 and End
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_2), MP_ROM_INT(HID_KEYPAD_2)},   //           90   // Keypad 2 and Down Arrow
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_3), MP_ROM_INT(HID_KEYPAD_3)},   //           91   // Keypad 3 and PageDn
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_4), MP_ROM_INT(HID_KEYPAD_4)},   //           92   // Keypad 4 and Lfet Arrow
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_5), MP_ROM_INT(HID_KEYPAD_5)},   //           93   // Keypad 5
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_6), MP_ROM_INT(HID_KEYPAD_6)},   //           94   // Keypad 6 and Right Arrow
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_7), MP_ROM_INT(HID_KEYPAD_7)},   //           95   // Keypad 7 and Home
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_8), MP_ROM_INT(HID_KEYPAD_8)},   //           96   // Keypad 8 and Up Arrow
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_9), MP_ROM_INT(HID_KEYPAD_9)},   //           97   // Keypad 9 and PageUp
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_0), MP_ROM_INT(HID_KEYPAD_0)},   //           98   // Keypad 0 and Insert
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_DOT), MP_ROM_INT(HID_KEYPAD_DOT)},   //         99   // Keypad . and Delete
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_MUTE), MP_ROM_INT(HID_KEY_MUTE)},   //           127  // Keyboard Mute
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_VOLUME_UP), MP_ROM_INT(HID_KEY_VOLUME_UP)},   //      128  // Keyboard Volume up
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_VOLUME_DOWN), MP_ROM_INT(HID_KEY_VOLUME_DOWN)},   //    129  // Keyboard Volume down
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_LEFT_CTRL), MP_ROM_INT(HID_KEY_LEFT_CTRL)},   //      224  // Keyboard LeftContorl
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_LEFT_SHFIT), MP_ROM_INT(HID_KEY_LEFT_SHIFT)},   //     225  // Keyboard LeftShift
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_LEFT_ALT), MP_ROM_INT(HID_KEY_LEFT_ALT)},   //       226  // Keyboard LeftAlt
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_LEFT_GUI), MP_ROM_INT(HID_KEY_LEFT_GUI)},   //       227  // Keyboard LeftGUI
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_RIGHT_CTRL), MP_ROM_INT(HID_KEY_RIGHT_CTRL)},   //     228  // Keyboard LeftContorl
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_RIGHT_SHIFT), MP_ROM_INT(HID_KEY_RIGHT_SHIFT)},   //    229  // Keyboard LeftShift
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_RIGHT_ALT), MP_ROM_INT(HID_KEY_RIGHT_ALT)},   //      230  // Keyboard LeftAlt
    { MP_ROM_QSTR(MP_QSTR_HID_KEYPAD_RIGHT_GUI), MP_ROM_INT(HID_KEY_RIGHT_GUI)},   //      231  // Keyboard RightGUI

    { MP_ROM_QSTR(MP_QSTR_HID_MOUSE_LEFT), MP_ROM_INT(HID_MOUSE_LEFT)},   //       
    { MP_ROM_QSTR(MP_QSTR_HID_MOUSE_MIDDLE), MP_ROM_INT(HID_MOUSE_MIDDLE)},   //      
    { MP_ROM_QSTR(MP_QSTR_HID_MOUSE_RIGHT), MP_ROM_INT(HID_MOUSE_RIGHT)},   //      

        // HID Consumer Usage IDs (subset of the codes available in the USB HID Usage Tables spec)
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_POWER), MP_ROM_INT(HID_CONSUMER_POWER)},         //          48  // Power
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_RESET), MP_ROM_INT(HID_CONSUMER_RESET)},         //          49  // Reset
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_SLEEP), MP_ROM_INT(HID_CONSUMER_SLEEP)},         //          50  // Sleep

    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_MENU), MP_ROM_INT(HID_CONSUMER_MENU)},          //           64  // Menu
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_SELECTION), MP_ROM_INT(HID_CONSUMER_SELECTION)},     //      128 // Selection
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_ASSIGN_SEL), MP_ROM_INT(HID_CONSUMER_ASSIGN_SEL)},    //     129 // Assign Selection
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_MODE_STEP), MP_ROM_INT(HID_CONSUMER_MODE_STEP)},     //      130 // Mode Step
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_RECALL_LAST), MP_ROM_INT(HID_CONSUMER_RECALL_LAST)},   //    131 // Recall Last
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_QUIT), MP_ROM_INT(HID_CONSUMER_QUIT)},          //           148 // Quit
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_HELP), MP_ROM_INT(HID_CONSUMER_HELP)},          //           149 // Help
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_CHANNEL_UP), MP_ROM_INT(HID_CONSUMER_CHANNEL_UP)},    //     156 // Channel Increment
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_CHANNEL_DOWN), MP_ROM_INT(HID_CONSUMER_CHANNEL_DOWN)},  //   157 // Channel Decrement

    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_PLAY), MP_ROM_INT(HID_CONSUMER_PLAY)},          //           176 // Play
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_PAUSE), MP_ROM_INT(HID_CONSUMER_PAUSE)},         //          177 // Pause
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_RECORD), MP_ROM_INT(HID_CONSUMER_RECORD)},        //         178 // Record
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_FAST_FORWARD), MP_ROM_INT(HID_CONSUMER_FAST_FORWARD)},  //   179 // Fast Forward
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_REWIND), MP_ROM_INT(HID_CONSUMER_REWIND)},        //         180 // Rewind
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_SCAN_NEXT_TRK), MP_ROM_INT(HID_CONSUMER_SCAN_NEXT_TRK)}, //  181 // Scan Next Track
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_SCAN_PREV_TRK), MP_ROM_INT(HID_CONSUMER_SCAN_PREV_TRK)}, //  182 // Scan Previous Track
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_STOP), MP_ROM_INT(HID_CONSUMER_STOP)},          //           183 // Stop
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_EJECT), MP_ROM_INT(HID_CONSUMER_EJECT)},         //          184 // Eject
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_RANDOM_PLAY), MP_ROM_INT(HID_CONSUMER_RANDOM_PLAY)},   //    185 // Random Play
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_SELECT_DISC), MP_ROM_INT(HID_CONSUMER_SELECT_DISC)},   //    186 // Select Disk
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_ENTER_DISC), MP_ROM_INT(HID_CONSUMER_ENTER_DISC)},    //     187 // Enter Disc
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_REPEAT), MP_ROM_INT(HID_CONSUMER_REPEAT)},        //         188 // Repeat
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_STOP_EJECT), MP_ROM_INT(HID_CONSUMER_STOP_EJECT)},    //     204 // Stop/Eject
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_PLAY_PAUSE), MP_ROM_INT(HID_CONSUMER_PLAY_PAUSE)},    //     205 // Play/Pause
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_PLAY_SKIP), MP_ROM_INT(HID_CONSUMER_PLAY_SKIP)},     //      206 // Play/Skip

    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_VOLUME),  MP_ROM_INT(HID_CONSUMER_VOLUME)},   //         224 // Volume
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_BALANCE), MP_ROM_INT(HID_CONSUMER_BALANCE)},   //        225 // Balance
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_MUTE), MP_ROM_INT(HID_CONSUMER_MUTE)},      //           226 // Mute
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_BASS), MP_ROM_INT(HID_CONSUMER_BASS)},      //     227 // Bass
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_VOLUME_UP), MP_ROM_INT(HID_CONSUMER_VOLUME_UP)},         //   233 // Volume Increment
    { MP_ROM_QSTR(MP_QSTR_HID_CONSUMER_VOLUME_DOWN), MP_ROM_INT(HID_CONSUMER_VOLUME_DOWN)},  //  234 // Volume Decrement  
};
STATIC MP_DEFINE_CONST_DICT(ble_locals_dict, ble_locals_table);

const mp_obj_module_t mp_module_ble_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&ble_locals_dict,
};

STATIC const mp_rom_map_elem_t bluetooth_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_bluetooth) },
    { MP_ROM_QSTR(MP_QSTR_ble), MP_ROM_PTR(&mp_module_ble_module) },
};
STATIC MP_DEFINE_CONST_DICT(bluetooth_module_globals_dict, bluetooth_globals_table);

const mp_obj_module_t mp_module_bluetooth = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&bluetooth_module_globals_dict
};