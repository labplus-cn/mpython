/**
 * 
 */

#ifndef MPYTHON_BLE_GAP_PROFILE_H
#define MPYTHON_BLE_GAP_PROFILE_H

#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_bt_defs.h"
#include "esp_gap_ble_api.h"
#include "esp_gatts_api.h"
#include "esp_gatt_defs.h"
#include "esp_bt_main.h"
#include "esp_bt_device.h"
#include "driver/gpio.h"

void mpython_ble_peripheral_init(const char *name);

void gap_event_handler(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param);

esp_err_t mpython_ble_gap_set_adv_data(void);

esp_err_t mpython_ble_gap_start_advertising(void);

esp_err_t mpython_ble_gap_stop_advertising(void);

#endif

