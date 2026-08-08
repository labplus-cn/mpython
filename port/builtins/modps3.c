#include <stdint.h>
#include <string.h>
#include "py/runtime.h"
#include "py/obj.h"
#include "esp_bt.h"
#include "esp_bt_main.h"
#include "esp_bt_device.h"
#include "drivers/ps3/ps3/include/ps3.h"

static ps3_t current_ps3_data;
static bool is_connected = false;
static bool is_initialized = false;

static void my_ps3_event_callback(ps3_t ps3, ps3_event_t event) {
    current_ps3_data = ps3;
}

static void my_ps3_connection_callback(uint8_t connected) {
    is_connected = connected;
}

STATIC mp_obj_t ps3_init(size_t n_args, const mp_obj_t *args) {
    if (is_initialized) {
        return mp_const_none;
    }

    // Convert MAC string if provided
    if (n_args > 0) {
        const char *mac_str = mp_obj_str_get_str(args[0]);
        uint8_t mac[6];
        if (sscanf(mac_str, "%hhx:%hhx:%hhx:%hhx:%hhx:%hhx", &mac[0], &mac[1], &mac[2], &mac[3], &mac[4], &mac[5]) == 6) {
            ps3SetBluetoothMacAddress(mac);
        } else {
            mp_raise_ValueError(MP_ERROR_TEXT("invalid MAC address format"));
        }
    }

    // Initialize Bluetooth Controller if not already initialized
    if (esp_bt_controller_get_status() == ESP_BT_CONTROLLER_STATUS_IDLE) {
        esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
        if (esp_bt_controller_init(&bt_cfg) != ESP_OK) {
            mp_raise_msg(&mp_type_RuntimeError, MP_ERROR_TEXT("Bluetooth controller init failed"));
        }
    }
    if (esp_bt_controller_get_status() != ESP_BT_CONTROLLER_STATUS_ENABLED) {
        #if defined(CONFIG_BTDM_CTRL_MODE_BR_EDR_ONLY) || defined(CONFIG_BTDM_CONTROLLER_MODE_BR_EDR_ONLY)
        if (esp_bt_controller_enable(ESP_BT_MODE_CLASSIC_BT) != ESP_OK) {
        #else
        if (esp_bt_controller_enable(ESP_BT_MODE_BTDM) != ESP_OK) {
        #endif
            mp_raise_msg(&mp_type_RuntimeError, MP_ERROR_TEXT("Bluetooth controller enable failed"));
        }
    }

    // Initialize Bluedroid host if not already initialized
    if (esp_bluedroid_get_status() == ESP_BLUEDROID_STATUS_UNINITIALIZED) {
        if (esp_bluedroid_init() != ESP_OK) {
            mp_raise_msg(&mp_type_RuntimeError, MP_ERROR_TEXT("Bluedroid init failed"));
        }
    }
    if (esp_bluedroid_get_status() != ESP_BLUEDROID_STATUS_ENABLED) { 
        if (esp_bluedroid_enable() != ESP_OK) {
            mp_raise_msg(&mp_type_RuntimeError, MP_ERROR_TEXT("Bluedroid enable failed"));
        }
    }

    // Setup callbacks and initialize PS3 L2CAP services
    ps3SetEventCallback(my_ps3_event_callback);
    ps3SetConnectionCallback(my_ps3_connection_callback);
    ps3Init();

    is_initialized = true;
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(ps3_init_obj, 0, 1, ps3_init);

STATIC mp_obj_t ps3_deinit(void) {
    if (is_initialized) {
        ps3Deinit();
        is_initialized = false;
        is_connected = false;
        memset(&current_ps3_data, 0, sizeof(ps3_t));
    }
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(ps3_deinit_obj, ps3_deinit);

STATIC mp_obj_t ps3_is_connected(void) {
    return mp_obj_new_bool(is_connected);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(ps3_is_connected_obj, ps3_is_connected);

STATIC mp_obj_t ps3_get_button(mp_obj_t button_obj) {
    const char *name = mp_obj_str_get_str(button_obj);
    bool pressed = false;

    if (strcmp(name, "select") == 0) pressed = current_ps3_data.button.select;
    else if (strcmp(name, "l3") == 0) pressed = current_ps3_data.button.l3;
    else if (strcmp(name, "r3") == 0) pressed = current_ps3_data.button.r3;
    else if (strcmp(name, "start") == 0) pressed = current_ps3_data.button.start;
    else if (strcmp(name, "up") == 0) pressed = current_ps3_data.button.up;
    else if (strcmp(name, "right") == 0) pressed = current_ps3_data.button.right;
    else if (strcmp(name, "down") == 0) pressed = current_ps3_data.button.down;
    else if (strcmp(name, "left") == 0) pressed = current_ps3_data.button.left;
    else if (strcmp(name, "l2") == 0) pressed = current_ps3_data.button.l2;
    else if (strcmp(name, "r2") == 0) pressed = current_ps3_data.button.r2;
    else if (strcmp(name, "l1") == 0) pressed = current_ps3_data.button.l1;
    else if (strcmp(name, "r1") == 0) pressed = current_ps3_data.button.r1;
    else if (strcmp(name, "triangle") == 0) pressed = current_ps3_data.button.triangle;
    else if (strcmp(name, "circle") == 0) pressed = current_ps3_data.button.circle;
    else if (strcmp(name, "cross") == 0) pressed = current_ps3_data.button.cross;
    else if (strcmp(name, "square") == 0) pressed = current_ps3_data.button.square;
    else if (strcmp(name, "ps") == 0) pressed = current_ps3_data.button.ps;
    else {
        mp_raise_ValueError(MP_ERROR_TEXT("unknown button name"));
    }

    return mp_obj_new_bool(pressed);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(ps3_get_button_obj, ps3_get_button);

STATIC mp_obj_t ps3_get_analog(mp_obj_t analog_obj) {
    const char *name = mp_obj_str_get_str(analog_obj);
    int value = 0;

    if (strcmp(name, "lx") == 0) value = current_ps3_data.analog.stick.lx;
    else if (strcmp(name, "ly") == 0) value = current_ps3_data.analog.stick.ly;
    else if (strcmp(name, "rx") == 0) value = current_ps3_data.analog.stick.rx;
    else if (strcmp(name, "ry") == 0) value = current_ps3_data.analog.stick.ry;
    else if (strcmp(name, "up") == 0) value = current_ps3_data.analog.button.up;
    else if (strcmp(name, "right") == 0) value = current_ps3_data.analog.button.right;
    else if (strcmp(name, "down") == 0) value = current_ps3_data.analog.button.down;
    else if (strcmp(name, "left") == 0) value = current_ps3_data.analog.button.left;
    else if (strcmp(name, "l2") == 0) value = current_ps3_data.analog.button.l2;
    else if (strcmp(name, "r2") == 0) value = current_ps3_data.analog.button.r2;
    else if (strcmp(name, "l1") == 0) value = current_ps3_data.analog.button.l1;
    else if (strcmp(name, "r1") == 0) value = current_ps3_data.analog.button.r1;
    else if (strcmp(name, "triangle") == 0) value = current_ps3_data.analog.button.triangle;
    else if (strcmp(name, "circle") == 0) value = current_ps3_data.analog.button.circle;
    else if (strcmp(name, "cross") == 0) value = current_ps3_data.analog.button.cross;
    else if (strcmp(name, "square") == 0) value = current_ps3_data.analog.button.square;
    else {
        mp_raise_ValueError(MP_ERROR_TEXT("unknown analog axis name"));
    }

    return mp_obj_new_int(value);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(ps3_get_analog_obj, ps3_get_analog);

STATIC mp_obj_t ps3_set_led(mp_obj_t player_obj) {
    int player = mp_obj_get_int(player_obj);
    if (player < 1 || player > 4) {
        mp_raise_ValueError(MP_ERROR_TEXT("player LED must be between 1 and 4"));
    }
    ps3SetLed(player);
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_1(ps3_set_led_obj, ps3_set_led);

STATIC mp_obj_t ps3_set_rumble(mp_obj_t intensity_obj, mp_obj_t duration_obj) {
    int intensity = mp_obj_get_int(intensity_obj);
    int duration = mp_obj_get_int(duration_obj);

    if (intensity < 0 || intensity > 100) {
        mp_raise_ValueError(MP_ERROR_TEXT("rumble intensity must be between 0 and 100"));
    }
    
    // Map intensity and duration as done in Arduino library
    uint8_t raw_intensity = (intensity * 255) / 100;
    uint8_t raw_duration = 255;
    if (duration >= 0) {
        raw_duration = (duration * 254) / 5000;
        if (raw_duration > 254) raw_duration = 254;
    }

    ps3_cmd_t cmd = {0};
    cmd.rumble_right_intensity = raw_intensity;
    cmd.rumble_left_intensity = raw_intensity;
    cmd.rumble_right_duration = raw_duration;
    cmd.rumble_left_duration = raw_duration;

    ps3Cmd(cmd);

    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_2(ps3_set_rumble_obj, ps3_set_rumble);

STATIC const mp_rom_map_elem_t ps3_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_ps3) },
    { MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&ps3_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&ps3_deinit_obj) },
    { MP_ROM_QSTR(MP_QSTR_is_connected), MP_ROM_PTR(&ps3_is_connected_obj) },
    { MP_ROM_QSTR(MP_QSTR_get_button), MP_ROM_PTR(&ps3_get_button_obj) },
    { MP_ROM_QSTR(MP_QSTR_get_analog), MP_ROM_PTR(&ps3_get_analog_obj) },
    { MP_ROM_QSTR(MP_QSTR_set_led), MP_ROM_PTR(&ps3_set_led_obj) },
    { MP_ROM_QSTR(MP_QSTR_set_rumble), MP_ROM_PTR(&ps3_set_rumble_obj) },
};
STATIC MP_DEFINE_CONST_DICT(ps3_module_globals, ps3_module_globals_table);

const mp_obj_module_t mp_module_ps3 = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t*)&ps3_module_globals,
};
