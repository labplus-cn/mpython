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
#include "mesh/mesh.h"

// #include "storage.h"

#include "ble_mesh.h"
#include "device.h"
#include "model_vnd.h"
#include "model_on_off.h"
#include "model_level.h"
#include "model_light.h"
#include "model_sensor.h"

static const char *tag = "device";

static struct bt_mesh_cfg_srv cfg_srv = {
	.relay = BT_MESH_RELAY_ENABLED,
	.beacon = BT_MESH_BEACON_ENABLED,

#if defined(CONFIG_BT_MESH_FRIEND)
	.frnd = BT_MESH_FRIEND_ENABLED,
#else
	.frnd = BT_MESH_FRIEND_NOT_SUPPORTED,
#endif

#if defined(CONFIG_BT_MESH_GATT_PROXY)
	.gatt_proxy = BT_MESH_GATT_PROXY_ENABLED,
#else
	.gatt_proxy = BT_MESH_GATT_PROXY_NOT_SUPPORTED,
#endif

	.default_ttl = 7,

	/* 2 transmissions with 20ms interval */
	.net_transmit = BT_MESH_TRANSMIT(2, 20),

	/* 3 transmissions with 20ms interval */
	.relay_retransmit = BT_MESH_TRANSMIT(3, 20),
};

static struct bt_mesh_health_srv health_srv = {
};

static struct bt_mesh_model_pub health_pub;
static struct os_mbuf *bt_mesh_pub_msg_health_pub;

void init_pub(void)
{
	bt_mesh_pub_msg_health_pub					= NET_BUF_SIMPLE(1 + 3 + 0);
	bt_mesh_pub_msg_gen_onoff_srv_pub_root		= NET_BUF_SIMPLE(2 + 1);
	// bt_mesh_pub_msg_gen_onoff_cli_pub_root		= NET_BUF_SIMPLE(2 + 1);
	bt_mesh_pub_msg_gen_level_srv_pub_root		= NET_BUF_SIMPLE(2 + 2);
	// bt_mesh_pub_msg_gen_level_cli_pub_root		= NET_BUF_SIMPLE(2 + 2);

	bt_mesh_pub_msg_light_lightness_srv_pub		= NET_BUF_SIMPLE(2 + 2);
	// bt_mesh_pub_msg_light_lightness_cli_pub		= NET_BUF_SIMPLE(2 + 2);	
	bt_mesh_pub_msg_light_ctl_srv_pub			= NET_BUF_SIMPLE(2 + 2);
	// bt_mesh_pub_msg_light_ctl_cli_pub			= NET_BUF_SIMPLE(2 + 2);
	bt_mesh_pub_msg_light_hsl_srv_pub			= NET_BUF_SIMPLE(2 + 6);
	// bt_mesh_pub_msg_light_hsl_cli_pub			= NET_BUF_SIMPLE(2 + 6);
	bt_mesh_pub_msg_sensor_srv_pub              = NET_BUF_SIMPLE(2 + 20);
    // bt_mesh_pub_msg_sensor_cli_pub              = NET_BUF_SIMPLE(2 + 2);
	// bt_mesh_pub_msg_sensor_setup_srv_pub              = NET_BUF_SIMPLE(2 + 2);

	bt_mesh_pub_msg_vnd_pub						= NET_BUF_SIMPLE(3 + 6);

	health_pub.msg					= bt_mesh_pub_msg_health_pub;
	gen_onoff_srv_pub_root.msg		= bt_mesh_pub_msg_gen_onoff_srv_pub_root;
	gen_onoff_cli_pub_root.msg		= bt_mesh_pub_msg_gen_onoff_srv_pub_root;
	gen_level_srv_pub_root.msg		= bt_mesh_pub_msg_gen_level_srv_pub_root;
	gen_level_cli_pub_root.msg		= bt_mesh_pub_msg_gen_level_srv_pub_root;

	light_lightness_srv_pub.msg		= bt_mesh_pub_msg_light_lightness_srv_pub;
	light_lightness_cli_pub.msg		= bt_mesh_pub_msg_light_lightness_srv_pub;
	light_ctl_srv_pub.msg			= bt_mesh_pub_msg_light_ctl_srv_pub;
	light_ctl_cli_pub.msg			= bt_mesh_pub_msg_light_ctl_srv_pub;
	light_hsl_srv_pub.msg			= bt_mesh_pub_msg_light_hsl_srv_pub;
	light_hsl_cli_pub.msg			= bt_mesh_pub_msg_light_hsl_srv_pub;
	sensor_srv_pub.msg              = bt_mesh_pub_msg_sensor_srv_pub;
	sensor_cli_pub.msg              = bt_mesh_pub_msg_sensor_srv_pub;
	// sensor_setup_srv_pub.msg        = bt_mesh_pub_msg_sensor_setup_srv_pub;

	vnd_pub.msg						= bt_mesh_pub_msg_vnd_pub;
}

struct bt_mesh_model root_models[] = {
	BT_MESH_MODEL_CFG_SRV(&cfg_srv),
	BT_MESH_MODEL_HEALTH_SRV(&health_srv, &health_pub),

	BT_MESH_MODEL(BT_MESH_MODEL_ID_GEN_ONOFF_SRV, gen_onoff_srv_op, &gen_onoff_srv_pub_root, &gen_onoff_user_data), //参数：类型 操作集 消息发布结构 用户数据
	BT_MESH_MODEL(BT_MESH_MODEL_ID_GEN_ONOFF_CLI, gen_onoff_cli_op, &gen_onoff_cli_pub_root, &gen_onoff_user_data),
	BT_MESH_MODEL(BT_MESH_MODEL_ID_GEN_LEVEL_SRV, gen_level_srv_op, &gen_level_srv_pub_root, &gen_level_user_data),
	BT_MESH_MODEL(BT_MESH_MODEL_ID_GEN_LEVEL_CLI, gen_level_cli_op, &gen_level_cli_pub_root, &gen_level_user_data),

	BT_MESH_MODEL(BT_MESH_MODEL_ID_LIGHT_LIGHTNESS_SRV, light_lightness_srv_op, &light_lightness_srv_pub, &light_user_data),
	BT_MESH_MODEL(BT_MESH_MODEL_ID_LIGHT_LIGHTNESS_CLI, light_lightness_cli_op, &light_lightness_cli_pub, &light_user_data),
	BT_MESH_MODEL(BT_MESH_MODEL_ID_LIGHT_CTL_SRV, light_ctl_srv_op, &light_ctl_srv_pub, &light_user_data),
	BT_MESH_MODEL(BT_MESH_MODEL_ID_LIGHT_CTL_CLI, light_ctl_cli_op, &light_ctl_cli_pub, &light_user_data),
	BT_MESH_MODEL(BT_MESH_MODEL_ID_LIGHT_HSL_SRV, light_hsl_srv_op, &light_hsl_srv_pub, &light_user_data),
	BT_MESH_MODEL(BT_MESH_MODEL_ID_LIGHT_HSL_CLI, light_hsl_cli_op, &light_hsl_cli_pub, &light_user_data),
	BT_MESH_MODEL(BT_MESH_MODEL_ID_SENSOR_SRV, sensor_srv_op, &sensor_srv_pub, &sensor_user_data),
	BT_MESH_MODEL(BT_MESH_MODEL_ID_SENSOR_CLI, sensor_cli_op, &sensor_cli_pub, &light_user_data),
	// BT_MESH_MODEL(BT_MESH_MODEL_ID_SENSOR_SETUP_SRV, sensor_setup_srv_op, &sensor_setup_srv_pub, &sensor_setup_user_data),
};

static struct bt_mesh_elem elements[] = {
	BT_MESH_ELEM(0, root_models, vnd_models),
};

/* node 组合结构 */
const struct bt_mesh_comp comp = {
	.cid = CID_RUNTIME,
	.elem = elements,
	.elem_count = ARRAY_SIZE(elements),
};

