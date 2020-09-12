/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

/* Bluetooth: Mesh Generic OnOff, Generic Level, Lighting & Vendor Models
 *
 * Copyright (c) 2018 Vikrant More
 *
 * SPDX-License-Identifier: Apache-2.0
 */
#include "esp_log.h"
// #include "common.h"
#include "ble_mesh.h"
#include "device.h"
#include "config/config.h"

static const char *tag = "ble_mesh";

#define OOB_AUTH_ENABLE 1
#ifdef OOB_AUTH_ENABLE

static int output_number(bt_mesh_output_action_t action, u32_t number)
{
	ESP_LOGI(tag, "OOB Number: %u\n", number);
	return 0;
}

static int output_string(const char *str)
{
	ESP_LOGI(tag, "OOB String: %s\n", str);
	return 0;
}

#endif

static void prov_complete(u16_t net_idx, u16_t addr)
{
	ESP_LOGI(tag, "Local node provisioned, primary address 0x%04x\n", addr);
}

static void prov_reset(void)
{
	bt_mesh_prov_enable(BT_MESH_PROV_ADV | BT_MESH_PROV_GATT);
}

static u8_t dev_uuid[16] = MYNEWT_VAL(BLE_MESH_DEV_UUID);

static const struct bt_mesh_prov prov = { //use for provisioning.
	.uuid = dev_uuid,
#ifdef OOB_AUTH_ENABLE
	.output_size = 6,
	.output_actions = BT_MESH_DISPLAY_NUMBER | BT_MESH_DISPLAY_STRING,
	.output_number = output_number,
	.output_string = output_string,
#endif
	.complete = prov_complete,
	.reset = prov_reset,
};

void blemesh_on_reset(int reason)
{
	ESP_LOGI(tag, "Resetting state; reason=%d\n", reason);
}

void blemesh_on_sync(void)
{
	int err;
	ble_addr_t addr;
	ESP_LOGI(tag, "Bluetooth initialized. RAM left: %d\n", esp_get_free_heap_size());

	/* Use NRPA */
	err = ble_hs_id_gen_rnd(1, &addr);
	assert(err == 0);
	err = ble_hs_id_set_rnd(addr.val);
	assert(err == 0);

	err = bt_mesh_init(addr.type, &prov, &comp);
	if (err) {
		ESP_LOGI(tag, "ble_hs_set_rnd  %d  %d \n", addr.val[0], addr.val[1]);
		return;
	}

	if (IS_ENABLED(CONFIG_SETTINGS)) {
		// settings_load();
		bt_mesh_settings_init();
	}

	if (bt_mesh_is_provisioned()) {
		ESP_LOGE(tag, "Mesh network restored from flash\n");
	}

	bt_mesh_prov_enable(BT_MESH_PROV_GATT | BT_MESH_PROV_ADV);

	ESP_LOGI(tag, "Mesh initialized. RAM left: %d\n", esp_get_free_heap_size());

	// bt_initialized();
}
