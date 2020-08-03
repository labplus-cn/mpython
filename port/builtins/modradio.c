#include <stdlib.h>
#include <string.h>

#include "py/obj.h"
#include "py/objstr.h"
#include "py/runtime.h"
#include "mphalport.h"

#include "freertos/FreeRTOS.h"
#include "freertos/semphr.h"
#include "freertos/timers.h"

// esp-idf componants
#include "esp_system.h"
#include "nvs_flash.h"
#include "tcpip_adapter.h"
#include "esp_wifi.h"
#include "esp_now.h"
#include "esp_log.h"

#define RADIO_CHANNEL_DEFAULT  10
#define RADIO_QUEUE_SIZE_DEFUALT 5

static const uint8_t broadcast_mac[ESP_NOW_ETH_ALEN] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF};
static bool radio_inited = false;
extern mp_obj_t esp_initialize();
extern bool wifi_started;

typedef struct {
    uint8_t mac_address[ESP_NOW_ETH_ALEN];
    uint8_t *data;
    uint8_t data_len;
}radio_recv_event_t;

static QueueHandle_t radio_recv_queue = NULL;
static uint8_t radio_channel = RADIO_CHANNEL_DEFAULT;

static void radio_recv_cb(const uint8_t *mac_addr, const uint8_t *data, int len) {
    radio_recv_event_t evt;
    memcpy(evt.mac_address, mac_addr, ESP_NOW_ETH_ALEN);
    evt.data = malloc(len);
    if (evt.data != NULL) {
        memcpy(evt.data, data, len);
        evt.data_len = len;
        if (xQueueSend(radio_recv_queue, &evt, 0) == pdFALSE) {
            free(evt.data);
        }
    }
}

void radio_enable(void) {
    if(!radio_inited) {
        esp_initialize();
        if(!wifi_started) {
            wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
            ESP_ERROR_CHECK(esp_wifi_init(&cfg));
            ESP_ERROR_CHECK(esp_wifi_set_storage(WIFI_STORAGE_RAM));
            ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
            ESP_ERROR_CHECK(esp_wifi_start());
            wifi_started = true;
        }
        ESP_ERROR_CHECK(esp_wifi_set_promiscuous(true));
        ESP_ERROR_CHECK(esp_wifi_set_channel(radio_channel, 0));
        
        // espnow init
        radio_recv_queue = xQueueCreate(RADIO_QUEUE_SIZE_DEFUALT, sizeof(radio_recv_event_t));
        if (radio_recv_queue == NULL) {
            mp_raise_ValueError(MP_ERROR_TEXT("radio on failed"));
        }
        ESP_ERROR_CHECK(esp_now_init());
        ESP_ERROR_CHECK(esp_now_register_recv_cb(radio_recv_cb));
        ESP_ERROR_CHECK(esp_now_set_pmk((uint8_t *)"mpython-2019"));

        // add broadcast peer
        esp_now_peer_info_t *peer = malloc(sizeof(esp_now_peer_info_t));
        if( peer == NULL) {
            mp_raise_ValueError(MP_ERROR_TEXT("radio on failed"));
            esp_now_deinit();
        }
        memset(peer, 0, sizeof(esp_now_peer_info_t));
        peer->channel = radio_channel;
        wifi_mode_t mode;
        esp_wifi_get_mode(&mode);
        peer->ifidx = (mode == WIFI_MODE_STA) ? ESP_IF_WIFI_STA:ESP_IF_WIFI_AP;
        peer->encrypt = false;
        memcpy(peer->peer_addr, broadcast_mac, ESP_NOW_ETH_ALEN);
        ESP_ERROR_CHECK(esp_now_add_peer(peer));
        free(peer);

        radio_inited = true;
    }
}

void radio_disable(void) {
    if(radio_inited) {
        if (radio_recv_queue != NULL) {
            vQueueDelete(radio_recv_queue);
        }
        esp_now_deinit();
        esp_wifi_set_promiscuous(false);
        radio_inited = false;
    }
}

static mp_obj_t radio_send(mp_obj_t msg) {
    if (radio_inited) {
        size_t len;
        const char *data = mp_obj_str_get_data(msg, &len);
        if (esp_now_send(broadcast_mac, (const uint8_t *)data, len) == ESP_OK) {
            return mp_const_true;
        }
    }
    return mp_const_false;
}
MP_DEFINE_CONST_FUN_OBJ_1(radio_send_obj, radio_send);

static mp_obj_t radio_send_bytes(mp_obj_t msg) {
    if (radio_inited) {
        mp_buffer_info_t bufinfo;
        mp_get_buffer_raise(msg, &bufinfo, MP_BUFFER_READ);
        if (esp_now_send(broadcast_mac, (const uint8_t *)bufinfo.buf, bufinfo.len) == ESP_OK) {
            return mp_const_true;
        }
    }
    return mp_const_false;
}
MP_DEFINE_CONST_FUN_OBJ_1(radio_send_bytes_obj, radio_send_bytes);


STATIC mp_obj_t radio_receive(mp_uint_t n_args, const mp_obj_t * args) {
    bool with_address = false;
    if (n_args == 1) {
        with_address = mp_obj_is_true(args[0]);
    }

    if (radio_inited) {
        radio_recv_event_t evt;
        if (xQueueReceive(radio_recv_queue, &evt, 0)) {
            mp_obj_t msg[2];
            msg[0] = mp_obj_new_str_copy(&mp_type_str, evt.data, evt.data_len);
            free(evt.data);

            if (with_address) {
                vstr_t vstr;
                vstr_init(&vstr, 0);
                vstr_printf(&vstr, "%02X%02X%02X%02X%02X%02X", MAC2STR(evt.mac_address));   
                msg[1] = mp_obj_new_str_from_vstr(&mp_type_str, &vstr);    
                return mp_obj_new_tuple(2, msg);         
            } else {
                return msg[0];
            }
        }
    }
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(radio_receive_obj, 0, 1, radio_receive);


STATIC mp_obj_t radio_receive_bytes(mp_uint_t n_args, const mp_obj_t * args) {
    bool with_address = false;
    if (n_args == 1) {
        with_address = mp_obj_is_true(args[0]);
    }

    if (radio_inited) {
        radio_recv_event_t evt;
        if (xQueueReceive(radio_recv_queue, &evt, 0)) {
            mp_obj_t msg[2];
            msg[0] = mp_obj_new_str_copy(&mp_type_bytes, evt.data, evt.data_len);
            free(evt.data);
            if (with_address) { 
                msg[1] = mp_obj_new_str_copy(&mp_type_bytes, evt.mac_address, ESP_NOW_ETH_ALEN);    
                return mp_obj_new_tuple(2, msg);         
            } else {
                return msg[0];
            }
        }
    }
    return mp_const_none;}
MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN(radio_receive_bytes_obj, 0, 1, radio_receive_bytes);



STATIC mp_obj_t radio_config(mp_uint_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    (void)pos_args;     // unused;
    if (n_args != 0) {
        mp_raise_TypeError(MP_ERROR_TEXT("arguments must be keywords"));
    }

    qstr arg_name = MP_QSTR_;
    if (kw_args->used) {
        for (size_t i = 0; i < kw_args->alloc; i++) {
            if (MP_MAP_SLOT_IS_FILLED(kw_args, i)) {
                mp_int_t value = mp_obj_get_int_truncated(kw_args->table[i].value);
                arg_name = mp_obj_str_get_qstr(kw_args->table[i].key);
                switch(arg_name) {
                    case MP_QSTR_channel:
                        if (!(0 <= value && value <= 14)) 
                            goto value_error;
                        radio_channel = value;
                        esp_wifi_set_channel(radio_channel, 0);
                        break;
                    // 其他参数未使用,保持和micro:bit兼容
                    case MP_QSTR_length:
                    case MP_QSTR_queue:
                    case MP_QSTR_power:
                    case MP_QSTR_data_rate:
                    case MP_QSTR_address:
                    case MP_QSTR_group:
                        break;
                    default:
                        nlr_raise(mp_obj_new_exception_msg_varg(&mp_type_ValueError, MP_ERROR_TEXT("unknown argument %q"), arg_name));
                        break;
                }
            }
        }
    }
    return mp_const_none;

value_error:
    nlr_raise(mp_obj_new_exception_msg_varg(&mp_type_ValueError, MP_ERROR_TEXT("value out of range for argument '%q'"), arg_name));
}
MP_DEFINE_CONST_FUN_OBJ_KW(radio_config_obj, 0, radio_config);

STATIC mp_obj_t radio_init(void) {
    radio_channel = RADIO_CHANNEL_DEFAULT;
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(radio___init___obj, radio_init); 

STATIC mp_obj_t radio_on(void) {
    radio_enable();
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(radio_on_obj, radio_on);

STATIC mp_obj_t radio_off(void) {
    radio_disable();
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(radio_off_obj, radio_off);

STATIC const mp_map_elem_t radio_module_locals_dict_table[] = {
    { MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_radio) },
    { MP_OBJ_NEW_QSTR(MP_QSTR___init__), (mp_obj_t)&radio___init___obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_send), (mp_obj_t)&radio_send_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_send_bytes), (mp_obj_t)&radio_send_bytes_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_receive), (mp_obj_t)&radio_receive_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_receive_bytes), (mp_obj_t)&radio_receive_bytes_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_config), (mp_obj_t)&radio_config_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_on), (mp_obj_t)&radio_on_obj },
    { MP_OBJ_NEW_QSTR(MP_QSTR_off), (mp_obj_t)&radio_off_obj}
};

STATIC MP_DEFINE_CONST_DICT(radio_module_locals_dict, radio_module_locals_dict_table);

const mp_obj_module_t mp_module_radio = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&radio_module_locals_dict
};