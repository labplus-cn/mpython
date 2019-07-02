/**
 * 
 */

#ifndef __MPYTHON_BLE_SERVICE_HIDD_H__
#define __MPYTHON_BLE_SERVICE_HIDD_H__
#include "esp_gatts_api.h"
#include "esp_gatt_defs.h"
#include "esp_gap_ble_api.h"
#include "mpython_ble_gatts_profile.h"
#include "mpython_ble_service_hidd_usages.h"



// HID keyboard input report length
#define HID_KEYBOARD_IN_RPT_LEN     8

// HID LED output report length
#define HID_LED_OUT_RPT_LEN         1

// HID mouse input report length
#define HID_MOUSE_IN_RPT_LEN        4

// HID consumer control input report length
#define HID_CC_IN_RPT_LEN           2


void esp_hidd_send_consumer_value(consumer_cmd_t key_cmd, bool key_pressed);
void esp_hidd_send_keyboard_value(key_mask_t special_key_mask, uint8_t *keyboard_cmd, uint8_t num_key);
void esp_hidd_send_mouse_value(mouse_cmd_t mouse_button, int8_t mickeys_x, int8_t mickeys_y);
void gatts_service_hidd_handler(esp_gatts_cb_event_t event, esp_gatt_if_t gatts_if, esp_ble_gatts_cb_param_t *param);
#endif  ///__HID_DEVICE_LE_PRF__

