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

/* Bluetooth: Mesh Generic OnOff, Generic Level, sensoring & Vendor Models
 *
 * Copyright (c) 2018 Vikrant More
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include "esp_log.h"
#include "mesh/mesh.h"

// #include "storage.h"

#include "ble_mesh.h"
#include "model_sensor.h"

static const char *tag = "model_sensor";

struct bt_mesh_model_pub sensor_srv_pub;
struct bt_mesh_model_pub sensor_cli_pub;
struct bt_mesh_model_pub sensor_setup_srv_pub;

struct os_mbuf *bt_mesh_pub_msg_sensor_srv_pub;
struct os_mbuf *bt_mesh_pub_msg_sensor_cli_pub;
struct os_mbuf *bt_mesh_pub_msg_sensor_setup_srv_pub;

/* Definitions of models user data (Start) */
struct sensor_state sensor_user_data;
struct sensor_setup_state sensor_setup_user_data;
/* Definitions of models user data (End) */

/* message handlers (Start) */
/* sensor  sensor_descriptor message handlers */
static void sensor_descriptor_status_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-sensorness STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 2 + 4);
	struct sensor_state *data = model->user_data; //on_off state store in model->user_data->on_off

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x4E));
	net_buf_simple_add_le16(msg, data->sensor_linear);

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send GEN_ONOFF_SRV Status response\n");
	}

	os_mbuf_free_chain(msg);
}

static void sensor_descriptor_get_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "#mesh-sensorness GET\n");

	sensor_descriptor_status_srv(model, ctx);
}

void sensor_descriptor_publish(struct bt_mesh_model *model)
{
	int err;
	struct os_mbuf *msg = model->pub->msg;
	struct sensor_state *data = model->user_data;

	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		return;
	}

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x4D));
	net_buf_simple_add_le16(msg, data->sensor_linear);

	err = bt_mesh_model_publish(model);
	if (err) {
		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
	}
}

static void sensor_descriptor_status_cli(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "Acknownledgement from sensor_sensorNESS_SRV\n");
	ESP_LOGI(tag, "Present sensorness = %02x\n", net_buf_simple_pull_le16(buf));
}
//----------------------
static void sensor_status_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-sensorness STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 2 + 4);
	struct sensor_state *data = model->user_data; //on_off state store in model->user_data->on_off

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x4E));
	net_buf_simple_add_le16(msg, data->sensor_linear);

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send GEN_ONOFF_SRV Status response\n");
	}

	os_mbuf_free_chain(msg);
}

static void sensor_get_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "#mesh-sensorness GET\n");

	sensor_status_srv(model, ctx);
}

void sensor_publish(struct bt_mesh_model *model)
{
	int err;
	struct os_mbuf *msg = model->pub->msg;
	struct sensor_state *data = model->user_data;

	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		return;
	}

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x4D));
	net_buf_simple_add_le16(msg, data->sensor_linear);

	err = bt_mesh_model_publish(model);
	if (err) {
		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
	}
}

static void sensor_status_cli(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "Acknownledgement from sensor_sensorNESS_SRV\n");
	ESP_LOGI(tag, "Present sensorness = %02x\n", net_buf_simple_pull_le16(buf));
}
//----------------------
static void sensor_colum_status_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-sensorness STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 2 + 4);
	struct sensor_state *data = model->user_data; //on_off state store in model->user_data->on_off

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x4E));
	net_buf_simple_add_le16(msg, data->sensor_linear);

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send GEN_ONOFF_SRV Status response\n");
	}

	os_mbuf_free_chain(msg);
}

static void sensor_colum_get_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "#mesh-sensorness GET\n");

	sensor_colum_status_srv(model, ctx);
}

void sensor_colum_publish(struct bt_mesh_model *model)
{
	int err;
	struct os_mbuf *msg = model->pub->msg;
	struct sensor_state *data = model->user_data;

	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		return;
	}

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x4D));
	net_buf_simple_add_le16(msg, data->sensor_linear);

	err = bt_mesh_model_publish(model);
	if (err) {
		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
	}
}

static void sensor_colum_status_cli(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "Acknownledgement from sensor_sensorNESS_SRV\n");
	ESP_LOGI(tag, "Present sensorness = %02x\n", net_buf_simple_pull_le16(buf));
}
//----------------------
static void sensor_series_status_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-sensorness STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 2 + 4);
	struct sensor_state *data = model->user_data; //on_off state store in model->user_data->on_off

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x4E));
	net_buf_simple_add_le16(msg, data->sensor_linear);

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send GEN_ONOFF_SRV Status response\n");
	}

	os_mbuf_free_chain(msg);
}

static void sensor_series_get_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "#mesh-sensorness GET\n");

	sensor_series_status_srv(model, ctx);
}

void sensor_series_publish(struct bt_mesh_model *model)
{
	int err;
	struct os_mbuf *msg = model->pub->msg;
	struct sensor_state *data = model->user_data;

	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		return;
	}

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x4D));
	net_buf_simple_add_le16(msg, data->sensor_linear);

	err = bt_mesh_model_publish(model);
	if (err) {
		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
	}
}

static void sensor_series_status_cli(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "Acknownledgement from sensor_sensorNESS_SRV\n");
	ESP_LOGI(tag, "Present sensorness = %02x\n", net_buf_simple_pull_le16(buf));
}

//----------------------
static void sensor_cadence_status_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-light-hsl STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 6 + 4);
	struct sensor_state *data = model->user_data; 

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x78));
	net_buf_simple_add_le16(msg, data->sensor_linear);
	net_buf_simple_add_le16(msg, data->sensor_hue);
	net_buf_simple_add_le16(msg, data->sensor_saturation);

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send GEN_ONOFF_SRV Status response\n");
	}

	os_mbuf_free_chain(msg);
}

static void sensor_cadence_get_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "#mesh-hsl GET\n");

	sensor_cadence_status_srv(model, ctx);
}

static void sensor_cadence_set_unack_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
    sensor_user_data.sensor_linear = (uint16_t)net_buf_simple_pull_le16(buf);
	sensor_user_data.sensor_hue = (uint16_t)net_buf_simple_pull_le16(buf);
	sensor_user_data.sensor_saturation = (uint16_t)net_buf_simple_pull_le16(buf);
	ESP_LOGI(tag, "#mesh-hsl SET-UNACK: light_linear=%d hue=%d saturation=%d\n", sensor_user_data.sensor_linear,
					sensor_user_data.sensor_hue, sensor_user_data.sensor_saturation);
}

static void sensor_cadence_set_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
    sensor_user_data.sensor_linear = (uint16_t)net_buf_simple_pull_le16(buf);
	sensor_user_data.sensor_hue = (uint16_t)net_buf_simple_pull_le16(buf);
	sensor_user_data.sensor_saturation = (uint16_t)net_buf_simple_pull_le16(buf);
	ESP_LOGI(tag, "#mesh-hsl SET: light_linear=%d hue=%d saturation=%d\n", sensor_user_data.sensor_linear,
					sensor_user_data.sensor_hue, sensor_user_data.sensor_saturation);

    sensor_cadence_status_srv(model, ctx); //ACK
}

void sensor_cadence_publish(struct bt_mesh_model *model)
{
	int err;
	struct os_mbuf *msg = model->pub->msg;
	struct sensor_state *data = model->user_data;

	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		return;
	}

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x77));
	net_buf_simple_add_le16(msg, data->sensor_linear);
	net_buf_simple_add_le16(msg, data->sensor_hue);
	net_buf_simple_add_le16(msg, data->sensor_saturation);

	err = bt_mesh_model_publish(model);
	if (err) {
		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
	}
}

//----------------------
static void sensor_setting_status_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-light-hsl STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 6 + 4);
	struct sensor_state *data = model->user_data; 

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x78));
	net_buf_simple_add_le16(msg, data->sensor_linear);
	net_buf_simple_add_le16(msg, data->sensor_hue);
	net_buf_simple_add_le16(msg, data->sensor_saturation);

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send GEN_ONOFF_SRV Status response\n");
	}

	os_mbuf_free_chain(msg);
}

static void sensor_settings_get_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "#mesh-hsl GET\n");

	sensor_setting_status_srv(model, ctx);
}

static void sensor_setting_get_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "#mesh-hsl GET\n");

	sensor_setting_status_srv(model, ctx);
}

static void sensor_setting_set_unack_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
    sensor_user_data.sensor_linear = (uint16_t)net_buf_simple_pull_le16(buf);
	sensor_user_data.sensor_hue = (uint16_t)net_buf_simple_pull_le16(buf);
	sensor_user_data.sensor_saturation = (uint16_t)net_buf_simple_pull_le16(buf);
	ESP_LOGI(tag, "#mesh-hsl SET-UNACK: light_linear=%d hue=%d saturation=%d\n", sensor_user_data.sensor_linear,
					sensor_user_data.sensor_hue, sensor_user_data.sensor_saturation);
}

static void sensor_setting_set_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
    sensor_user_data.sensor_linear = (uint16_t)net_buf_simple_pull_le16(buf);
	sensor_user_data.sensor_hue = (uint16_t)net_buf_simple_pull_le16(buf);
	sensor_user_data.sensor_saturation = (uint16_t)net_buf_simple_pull_le16(buf);
	ESP_LOGI(tag, "#mesh-hsl SET-UNACK: light_linear=%d hue=%d saturation=%d\n", sensor_user_data.sensor_linear,
					sensor_user_data.sensor_hue, sensor_user_data.sensor_saturation);

    sensor_setting_status_srv(model, ctx); //ACK
}

void sensor_setting_publish(struct bt_mesh_model *model)
{
	int err;
	struct os_mbuf *msg = model->pub->msg;
	struct sensor_state *data = model->user_data;

	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		return;
	}

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x77));
	net_buf_simple_add_le16(msg, data->sensor_linear);
	net_buf_simple_add_le16(msg, data->sensor_hue);
	net_buf_simple_add_le16(msg, data->sensor_saturation);

	err = bt_mesh_model_publish(model);
	if (err) {
		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
	}
}

/* Mapping of message handlers for sensor sensorness Server (0x1300) */
const struct bt_mesh_model_op sensor_srv_op[] = {
	{ BT_MESH_MODEL_OP_2(0x82, 0x30), 8, sensor_descriptor_get_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x31), 2, sensor_get_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x32), 2, sensor_colum_get_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x33), 2, sensor_series_get_srv },
	BT_MESH_MODEL_OP_END,
};

/* Mapping of message handlers for sensor Lightness Client (0x1302) */
const struct bt_mesh_model_op sensor_cli_op[] = {
	{ BT_MESH_MODEL_OP_1(0x51), 8, sensor_descriptor_status_cli },
	{ BT_MESH_MODEL_OP_1(0x52), 2, sensor_status_cli },
	{ BT_MESH_MODEL_OP_1(0x53), 2, sensor_colum_status_cli },
	{ BT_MESH_MODEL_OP_1(0x54), 2, sensor_series_status_cli },
	BT_MESH_MODEL_OP_END,
};

/* Mapping of message handlers for sensor sensorness Server (0x1300) */
const struct bt_mesh_model_op sensor_setup_srv_op[] = {
	{ BT_MESH_MODEL_OP_2(0x82, 0x34), 0, sensor_cadence_get_srv },
	{ BT_MESH_MODEL_OP_1(0x55),       2, sensor_cadence_set_srv },
	{ BT_MESH_MODEL_OP_1(0x56),       2, sensor_cadence_set_unack_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x35), 0, sensor_settings_get_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x36), 0, sensor_setting_get_srv },
	{ BT_MESH_MODEL_OP_1(0x59),       2, sensor_setting_set_srv },
	{ BT_MESH_MODEL_OP_1(0x5A),       2, sensor_setting_set_unack_srv },
	BT_MESH_MODEL_OP_END,
};


