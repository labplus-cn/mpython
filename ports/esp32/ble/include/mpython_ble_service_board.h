/**
 * 
 */

#ifndef __MPYTHON_BLE_SERVICE_BOARD_H__
#define __MPYTHON_BLE_SERVICE_BOARD_H__

#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_bt_defs.h"
#include "esp_gap_ble_api.h"
#include "esp_gatts_api.h"
#include "esp_gatt_defs.h"
#include "esp_bt_main.h"
#include "esp_bt_device.h"

typedef void (*board_service_write_cb_t)(uint8_t *value, uint8_t len);

void board_service_register_output_callback(board_service_write_cb_t callback);

void board_service_send_notify(uint8_t *value, uint16_t len);

void board_service_input_update(uint8_t *value, uint16_t len);

void gatts_service_board_handler(esp_gatts_cb_event_t event, esp_gatt_if_t gatts_if, esp_ble_gatts_cb_param_t *param);
#endif
