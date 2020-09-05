#include <stdlib.h>
#include <string.h>

#include "py/obj.h"
#include "py/objstr.h"
#include "py/runtime.h"
#include "mphalport.h"

#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/timers.h"
#include "freertos/FreeRTOSConfig.h"
// esp-idf componants
#include "esp_system.h"
#include "esp_log.h"
/* BLE */
#include "esp_nimble_hci.h"
#include "nimble/nimble_port.h"
#include "nimble/nimble_port_freertos.h"
#include "host/ble_hs.h"
#include "host/util/util.h"
#include "services/gap/ble_svc_gap.h"
#include "services/gatt/ble_svc_gatt.h"
#include "extmod/nimble/modbluetooth_nimble.h"
#include "mesh/mesh.h"
#include "ble_mesh.h"

static const char *tag = "NimBLE_MESH";

uint8_t gen_on_off_state;
int16_t gen_level_state;

extern volatile int mp_bluetooth_nimble_ble_state;

void ble_store_config_init(void);

extern void mp_bluetooth_deinit(void);

static mp_obj_t init() {
    mp_bluetooth_deinit(); // Clean up if necessary.

    ble_hs_cfg.reset_cb = blemesh_on_reset;
    ble_hs_cfg.sync_cb = blemesh_on_sync;
    // ble_hs_cfg.gatts_register_cb = gatts_register_cb;
    ble_hs_cfg.store_status_cb = ble_store_util_status_rr;

    // MP_STATE_PORT(bluetooth_nimble_root_pointers) = m_new0(mp_bluetooth_nimble_root_pointers_t, 1);
    // mp_bluetooth_gatts_db_create(&MP_STATE_PORT(bluetooth_nimble_root_pointers)->gatts_db);

    mp_bluetooth_nimble_ble_state = MP_BLUETOOTH_NIMBLE_BLE_STATE_STARTING;

    mp_bluetooth_nimble_port_preinit(); //esp_nimble_hci_and_controller_init()
    nimble_port_init();
    mp_bluetooth_nimble_port_postinit(); //do nothing.

    // By default, just register the default gap/gatt service.
    ble_svc_gap_init();
    ble_svc_gatt_init();
    bt_mesh_register_gatt();

    init_pub();

    /* XXX Need to have template for store */
    ble_store_config_init();

    mp_bluetooth_nimble_port_start();

    // Wait for sync callback
    while (mp_bluetooth_nimble_ble_state != MP_BLUETOOTH_NIMBLE_BLE_STATE_ACTIVE) {
        MICROPY_EVENT_POLL_HOOK
    }

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(init_obj, init);

static mp_obj_t get_on_off(){
    return MP_OBJ_NEW_SMALL_INT(gen_on_off_state);
}
MP_DEFINE_CONST_FUN_OBJ_0(get_on_off_obj, get_on_off);

static mp_obj_t get_level(){
    return MP_OBJ_NEW_SMALL_INT(gen_level_state);
}
MP_DEFINE_CONST_FUN_OBJ_0(get_level_obj, get_level);

static mp_obj_t set_on_off(mp_obj_t on_off){
    gen_on_off_state = mp_obj_get_int(on_off);
    // gen_onoff_publish(gen_on_off_state);
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(set_on_off_obj, set_on_off);

static mp_obj_t set_level(mp_obj_t level){
    gen_level_state = mp_obj_get_int(level);
    
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(set_level_obj, set_level);

STATIC const mp_map_elem_t ble_mesh_module_locals_dict_table[] = {
    { MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_ble_mesh) },
    // { MP_OBJ_NEW_QSTR(MP_QSTR___init__), (mp_obj_t)&radio___init___obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_init), (mp_obj_t)&init_obj},
    // { MP_ROM_QSTR(MP_QSTR_MODELS_GEN), MP_ROM_INT(MODELS_GEN) },
    // { MP_ROM_QSTR(MP_QSTR_MODELS_LIGHT), MP_ROM_INT(MODELS_LIGHT) },
    // { MP_ROM_QSTR(MP_QSTR_MODELS_SENSOR), MP_ROM_INT(MODELS_SENSOR) },
    { MP_OBJ_NEW_QSTR(MP_QSTR_get_on_off), (mp_obj_t)&get_on_off_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_get_level), (mp_obj_t)&get_level_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_set_on_off), (mp_obj_t)&set_on_off_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_set_level), (mp_obj_t)&set_level_obj },
    // { MP_ROM_QSTR(MP_QSTR_MODELS_SENSOR), MP_ROM_INT(MODELS_SENSOR) },
    // { MP_ROM_QSTR(MP_QSTR_MODELS_SENSOR), MP_ROM_INT(MODELS_SENSOR) },
};

STATIC MP_DEFINE_CONST_DICT(ble_mesh_module_locals_dict, ble_mesh_module_locals_dict_table);

const mp_obj_module_t mp_module_ble_mesh = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&ble_mesh_module_locals_dict
};