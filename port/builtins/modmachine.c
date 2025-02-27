#include <stdint.h>
#include <stdio.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#if MICROPY_ESP_IDF_4
#include "esp32/rom/rtc.h"
#include "esp32/clk.h"
#include "esp_sleep.h"
#else
#include "rom/ets_sys.h"
#include "rom/rtc.h"
#include "esp_clk.h"
#endif
#include "esp_pm.h"
#include "driver/touch_pad.h"

#include "py/obj.h"
#include "py/runtime.h"
#include "lib/utils/pyexec.h"
#include "extmod/machine_mem.h"
#include "extmod/machine_signal.h"
#include "extmod/machine_pulse.h"
#include "extmod/machine_i2c.h"
#include "extmod/machine_spi.h"
#include "modmachine.h"
#include "machine_rtc.h"


#if MICROPY_PY_MACHINE

typedef enum {
    MP_PWRON_RESET = 1,
    MP_HARD_RESET,
    MP_WDT_RESET,
    MP_DEEPSLEEP_RESET,
    MP_SOFT_RESET
} reset_reason_t;

STATIC mp_obj_t machine_freq(size_t n_args, const mp_obj_t *args) {
    if (n_args == 0) {
        // get
        return mp_obj_new_int(esp_clk_cpu_freq());
    } else {
        // set
        mp_int_t freq = mp_obj_get_int(args[0]) / 1000000;
        if (freq != 20 && freq != 40 && freq != 80 && freq != 160 && freq != 240) {
            mp_raise_ValueError(MP_ERROR_TEXT("frequency must be 20MHz, 40MHz, 80Mhz, 160MHz or 240MHz"));
        }
        esp_pm_config_esp32_t pm;
        pm.max_freq_mhz = freq;
        pm.min_freq_mhz = freq;
        pm.light_sleep_enable = false;
        esp_err_t ret = esp_pm_configure(&pm);
        if (ret != ESP_OK) {
            mp_raise_ValueError(NULL);
        }
        while (esp_clk_cpu_freq() != freq * 1000000) {
            vTaskDelay(1);
        }
        return mp_const_none;
    }
}
STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(machine_freq_obj, 0, 1, machine_freq);

STATIC mp_obj_t machine_sleep_helper(wake_type_t wake_type, size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {

    enum {ARG_sleep_ms};
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_sleep_ms, MP_ARG_INT, { .u_int = 0 } },
    };

    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);


    mp_int_t expiry = args[ARG_sleep_ms].u_int;

    if (expiry != 0) {
        esp_sleep_enable_timer_wakeup(((uint64_t)expiry) * 1000);
    }

    if (machine_rtc_config.ext0_pin != -1 && (machine_rtc_config.ext0_wake_types & wake_type)) {
        esp_sleep_enable_ext0_wakeup(machine_rtc_config.ext0_pin, machine_rtc_config.ext0_level ? 1 : 0);
    }

    if (machine_rtc_config.ext1_pins != 0) {
        esp_sleep_enable_ext1_wakeup(
            machine_rtc_config.ext1_pins,
            machine_rtc_config.ext1_level ? ESP_EXT1_WAKEUP_ANY_HIGH : ESP_EXT1_WAKEUP_ALL_LOW);
    }

    if (machine_rtc_config.wake_on_touch) {
        if (esp_sleep_enable_touchpad_wakeup() != ESP_OK) {
            mp_raise_msg(&mp_type_RuntimeError, MP_ERROR_TEXT("esp_sleep_enable_touchpad_wakeup() failed"));
        }
    }

    switch (wake_type) {
        case MACHINE_WAKE_SLEEP:
            esp_light_sleep_start();
            break;
        case MACHINE_WAKE_DEEPSLEEP:
            esp_deep_sleep_start();
            break;
    }
    return mp_const_none;
}

STATIC mp_obj_t machine_lightsleep(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    return machine_sleep_helper(MACHINE_WAKE_SLEEP, n_args, pos_args, kw_args);
};
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(machine_lightsleep_obj, 0, machine_lightsleep);

STATIC mp_obj_t machine_deepsleep(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    return machine_sleep_helper(MACHINE_WAKE_DEEPSLEEP, n_args, pos_args, kw_args);
};
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(machine_deepsleep_obj, 0,  machine_deepsleep);

STATIC mp_obj_t machine_reset_cause(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    switch (esp_reset_reason()) {
        case ESP_RST_POWERON:
        case ESP_RST_BROWNOUT:
            return MP_OBJ_NEW_SMALL_INT(MP_PWRON_RESET);
            break;

        case ESP_RST_INT_WDT:
        case ESP_RST_TASK_WDT:
        case ESP_RST_WDT:
            return MP_OBJ_NEW_SMALL_INT(MP_WDT_RESET);
            break;

        case ESP_RST_DEEPSLEEP:
            return MP_OBJ_NEW_SMALL_INT(MP_DEEPSLEEP_RESET);
            break;

        case ESP_RST_SW:
        case ESP_RST_PANIC:
        case ESP_RST_EXT: // Comment in ESP-IDF: "For ESP32, ESP_RST_EXT is never returned"
            return MP_OBJ_NEW_SMALL_INT(MP_HARD_RESET);
            break;

        case ESP_RST_SDIO:
        case ESP_RST_UNKNOWN:
        default:
            return MP_OBJ_NEW_SMALL_INT(0);
            break;
    }
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(machine_reset_cause_obj, 0,  machine_reset_cause);

STATIC mp_obj_t machine_wake_reason(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    return MP_OBJ_NEW_SMALL_INT(esp_sleep_get_wakeup_cause());
}
STATIC MP_DEFINE_CONST_FUN_OBJ_KW(machine_wake_reason_obj, 0,  machine_wake_reason);

STATIC mp_obj_t machine_reset(void) {
    esp_restart();
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(machine_reset_obj, machine_reset);

STATIC mp_obj_t machine_soft_reset(void) {
    pyexec_system_exit = PYEXEC_FORCED_EXIT;
    mp_raise_type(&mp_type_SystemExit);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(machine_soft_reset_obj, machine_soft_reset);

STATIC mp_obj_t machine_unique_id(void) {
    uint8_t chipid[6];
    esp_efuse_mac_get_default(chipid);
    return mp_obj_new_bytes(chipid, 6);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(machine_unique_id_obj, machine_unique_id);

STATIC mp_obj_t machine_unique_id_custom(void) {
    esp_err_t ret = ESP_OK;
    uint8_t custom_mac[6];
    uint8_t custom_error_mac[8] = { 0xff, 0xff, 0xff, 0xff, 0xff, 0xff };
    ret = esp_efuse_mac_get_custom(custom_mac);
    if (ret != ESP_OK) {
        // ESP_LOGE("Get base MAC address from BLK3 of EFUSE error (%s)", esp_err_to_name(ret));
        return mp_obj_new_bytes(custom_error_mac, 6);
    }
    else {
        return mp_obj_new_bytes(custom_mac, 6);
        // ESP_LOGI(TAG, "custom_mac===");
    }
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(machine_unique_id_custom_obj, machine_unique_id_custom);


STATIC mp_obj_t machine_idle(void) {
    taskYIELD();
    return mp_const_none;
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(machine_idle_obj, machine_idle);

STATIC mp_obj_t machine_disable_irq(void) {
    uint32_t state = MICROPY_BEGIN_ATOMIC_SECTION();
    return mp_obj_new_int(state);
}
MP_DEFINE_CONST_FUN_OBJ_0(machine_disable_irq_obj, machine_disable_irq);

STATIC mp_obj_t machine_enable_irq(mp_obj_t state_in) {
    uint32_t state = mp_obj_get_int(state_in);
    MICROPY_END_ATOMIC_SECTION(state);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(machine_enable_irq_obj, machine_enable_irq);

STATIC const mp_rom_map_elem_t machine_module_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_umachine) },

    { MP_ROM_QSTR(MP_QSTR_mem8), MP_ROM_PTR(&machine_mem8_obj) },
    { MP_ROM_QSTR(MP_QSTR_mem16), MP_ROM_PTR(&machine_mem16_obj) },
    { MP_ROM_QSTR(MP_QSTR_mem32), MP_ROM_PTR(&machine_mem32_obj) },

    { MP_ROM_QSTR(MP_QSTR_freq), MP_ROM_PTR(&machine_freq_obj) },
    { MP_ROM_QSTR(MP_QSTR_reset), MP_ROM_PTR(&machine_reset_obj) },
    { MP_ROM_QSTR(MP_QSTR_soft_reset), MP_ROM_PTR(&machine_soft_reset_obj) },
    { MP_ROM_QSTR(MP_QSTR_unique_id), MP_ROM_PTR(&machine_unique_id_obj) },
    { MP_ROM_QSTR(MP_QSTR_unique_id_custom), MP_ROM_PTR(&machine_unique_id_custom_obj) },
    { MP_ROM_QSTR(MP_QSTR_sleep), MP_ROM_PTR(&machine_lightsleep_obj) },
    { MP_ROM_QSTR(MP_QSTR_lightsleep), MP_ROM_PTR(&machine_lightsleep_obj) },
    { MP_ROM_QSTR(MP_QSTR_deepsleep), MP_ROM_PTR(&machine_deepsleep_obj) },
    { MP_ROM_QSTR(MP_QSTR_idle), MP_ROM_PTR(&machine_idle_obj) },

    { MP_ROM_QSTR(MP_QSTR_disable_irq), MP_ROM_PTR(&machine_disable_irq_obj) },
    { MP_ROM_QSTR(MP_QSTR_enable_irq), MP_ROM_PTR(&machine_enable_irq_obj) },

    { MP_ROM_QSTR(MP_QSTR_time_pulse_us), MP_ROM_PTR(&machine_time_pulse_us_obj) },

    { MP_ROM_QSTR(MP_QSTR_Timer), MP_ROM_PTR(&machine_timer_type) },
    { MP_ROM_QSTR(MP_QSTR_WDT), MP_ROM_PTR(&machine_wdt_type) },
    #if MICROPY_HW_ENABLE_SDCARD
    { MP_ROM_QSTR(MP_QSTR_SDCard), MP_ROM_PTR(&machine_sdcard_type) },
    #endif

    // wake abilities
    { MP_ROM_QSTR(MP_QSTR_SLEEP), MP_ROM_INT(MACHINE_WAKE_SLEEP) },
    { MP_ROM_QSTR(MP_QSTR_DEEPSLEEP), MP_ROM_INT(MACHINE_WAKE_DEEPSLEEP) },
    { MP_ROM_QSTR(MP_QSTR_Pin), MP_ROM_PTR(&machine_pin_type) },
    { MP_ROM_QSTR(MP_QSTR_Signal), MP_ROM_PTR(&machine_signal_type) },
    { MP_ROM_QSTR(MP_QSTR_TouchPad), MP_ROM_PTR(&machine_touchpad_type) },
    { MP_ROM_QSTR(MP_QSTR_ADC), MP_ROM_PTR(&machine_adc_type) },
    { MP_ROM_QSTR(MP_QSTR_DAC), MP_ROM_PTR(&machine_dac_type) },
    { MP_ROM_QSTR(MP_QSTR_I2C), MP_ROM_PTR(&machine_i2c_type) },
    { MP_ROM_QSTR(MP_QSTR_PWM), MP_ROM_PTR(&machine_pwm_type) },
    { MP_ROM_QSTR(MP_QSTR_RTC), MP_ROM_PTR(&machine_rtc_type) },
    { MP_ROM_QSTR(MP_QSTR_SPI), MP_ROM_PTR(&mp_machine_soft_spi_type) },
    { MP_ROM_QSTR(MP_QSTR_UART), MP_ROM_PTR(&machine_uart_type) },

    // Reset reasons
    { MP_ROM_QSTR(MP_QSTR_reset_cause), MP_ROM_PTR(&machine_reset_cause_obj) },
    { MP_ROM_QSTR(MP_QSTR_HARD_RESET), MP_ROM_INT(MP_HARD_RESET) },
    { MP_ROM_QSTR(MP_QSTR_PWRON_RESET), MP_ROM_INT(MP_PWRON_RESET) },
    { MP_ROM_QSTR(MP_QSTR_WDT_RESET), MP_ROM_INT(MP_WDT_RESET) },
    { MP_ROM_QSTR(MP_QSTR_DEEPSLEEP_RESET), MP_ROM_INT(MP_DEEPSLEEP_RESET) },
    { MP_ROM_QSTR(MP_QSTR_SOFT_RESET), MP_ROM_INT(MP_SOFT_RESET) },

    // Wake reasons
    { MP_ROM_QSTR(MP_QSTR_wake_reason), MP_ROM_PTR(&machine_wake_reason_obj) },
    { MP_ROM_QSTR(MP_QSTR_PIN_WAKE), MP_ROM_INT(ESP_SLEEP_WAKEUP_EXT0) },
    { MP_ROM_QSTR(MP_QSTR_EXT0_WAKE), MP_ROM_INT(ESP_SLEEP_WAKEUP_EXT0) },
    { MP_ROM_QSTR(MP_QSTR_EXT1_WAKE), MP_ROM_INT(ESP_SLEEP_WAKEUP_EXT1) },
    { MP_ROM_QSTR(MP_QSTR_TIMER_WAKE), MP_ROM_INT(ESP_SLEEP_WAKEUP_TIMER) },
    { MP_ROM_QSTR(MP_QSTR_TOUCHPAD_WAKE), MP_ROM_INT(ESP_SLEEP_WAKEUP_TOUCHPAD) },
    { MP_ROM_QSTR(MP_QSTR_ULP_WAKE), MP_ROM_INT(ESP_SLEEP_WAKEUP_ULP) },
};

STATIC MP_DEFINE_CONST_DICT(machine_module_globals, machine_module_globals_table);

const mp_obj_module_t mp_module_machine = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&machine_module_globals,
};

#endif // MICROPY_PY_MACHINE