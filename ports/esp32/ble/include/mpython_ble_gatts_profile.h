/**
 * 
 */

#ifndef __MPYTHON_BLE_GATTS_PROFILE_H
#define __MPYTHON_BLE_GATTS_PROFILE_H

#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_bt_defs.h"
#include "esp_gap_ble_api.h"
#include "esp_gatts_api.h"
#include "esp_gatt_defs.h"
#include "esp_bt_main.h"
#include "esp_bt_device.h"

extern const uint16_t character_declaration_uuid;
extern const uint16_t primary_service_uuid;
extern const uint16_t include_service_uuid;
extern const uint16_t character_declaration_uuid;
extern const uint16_t character_client_config_uuid;

///the propoty definition
extern const uint8_t char_prop_notify;
extern const uint8_t char_prop_read;
extern const uint8_t char_prop_write_nr;
extern const uint8_t char_prop_read_write;
extern const uint8_t char_prop_read_notify;
extern const uint8_t char_prop_read_write_notify;

#define PRIMARY_SERVICE_UUID16(_perm_, _uuid_) {\
    .attr_control.auto_rsp = ESP_GATT_AUTO_RSP,\
    .att_desc.uuid_length = ESP_UUID_LEN_16,\
    .att_desc.uuid_p = (uint8_t *)&primary_service_uuid,\
    .att_desc.perm = (_perm_),\
    .att_desc.max_length = 2,\
    .att_desc.length = sizeof((_uuid_)),\
    .att_desc.value = (uint8_t *)&(_uuid_) }

#define CHAR_DECLARATION_READ() {\
    .attr_control.auto_rsp = ESP_GATT_AUTO_RSP,\
    .att_desc.uuid_length = ESP_UUID_LEN_16,\
    .att_desc.uuid_p = (uint8_t *)&character_declaration_uuid,\
    .att_desc.perm = ESP_GATT_PERM_READ,\
    .att_desc.max_length = 1,\
    .att_desc.length = 1,\
    .att_desc.value = (uint8_t *)&(char_prop_read) }

#define CHAR_DECLARATION_READ_NOTIFY() {\
    .attr_control.auto_rsp = ESP_GATT_AUTO_RSP,\
    .att_desc.uuid_length = ESP_UUID_LEN_16,\
    .att_desc.uuid_p = (uint8_t *)&character_declaration_uuid,\
    .att_desc.perm = ESP_GATT_PERM_READ,\
    .att_desc.max_length = 1,\
    .att_desc.length = 1,\
    .att_desc.value = (uint8_t *)&(char_prop_read_notify) }

#define CHAR_DECLARATION_WRITE() {\
    .attr_control.auto_rsp = ESP_GATT_AUTO_RSP,\
    .att_desc.uuid_length = ESP_UUID_LEN_16,\
    .att_desc.uuid_p = (uint8_t *)&character_declaration_uuid,\
    .att_desc.perm = ESP_GATT_PERM_READ,\
    .att_desc.max_length = 1,\
    .att_desc.length = 1,\
    .att_desc.value = (uint8_t *)&(char_prop_write_nr) }

#define CHAR_DECLARATION_READ_WRITE() {\
    .attr_control.auto_rsp = ESP_GATT_AUTO_RSP,\
    .att_desc.uuid_length = ESP_UUID_LEN_16,\
    .att_desc.uuid_p = (uint8_t *)&character_declaration_uuid,\
    .att_desc.perm = ESP_GATT_PERM_READ,\
    .att_desc.max_length = 1,\
    .att_desc.length = 1,\
    .att_desc.value = (uint8_t *)&(char_prop_read_write) }

#define CHAR_DECLARATION_READ_WRITE_NOTIFY() {\
    .attr_control.auto_rsp = ESP_GATT_AUTO_RSP,\
    .att_desc.uuid_length = ESP_UUID_LEN_16,\
    .att_desc.uuid_p = (uint8_t *)&character_declaration_uuid,\
    .att_desc.perm = ESP_GATT_PERM_READ,\
    .att_desc.max_length = 1,\
    .att_desc.length = 1,\
    .att_desc.value = (uint8_t *)&(char_prop_read_write_notify) }

#define CHAR_DESCRIPTOR_CCCD(_cccd_flag_) {\
    .attr_control.auto_rsp = ESP_GATT_AUTO_RSP,\
    .att_desc.uuid_length = ESP_UUID_LEN_16,\
    .att_desc.uuid_p = (uint8_t *)&character_client_config_uuid,\
    .att_desc.perm = ESP_GATT_PERM_READ | ESP_GATT_PERM_WRITE,\
    .att_desc.max_length = 2,\
    .att_desc.length = sizeof((_cccd_flag_)),\
    .att_desc.value = (uint8_t *)&(_cccd_flag_) }


#define APP_ID_START    0
#define BOARD_SERVICE_APP_ID  APP_ID_START + 0
#define HIDD_SERVICE_APP_ID   APP_ID_START + 1

void gatts_event_handler(esp_gatts_cb_event_t event, esp_gatt_if_t gatts_if, esp_ble_gatts_cb_param_t *param);

extern bool is_ble_connected;
#endif


