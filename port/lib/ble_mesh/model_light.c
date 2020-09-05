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
#include "model_light.h"

static const char *tag = "model_light";

struct bt_mesh_model_pub light_lightness_srv_pub;
struct bt_mesh_model_pub light_lightness_cli_pub;
struct bt_mesh_model_pub light_ctl_srv_pub;
struct bt_mesh_model_pub light_ctl_cli_pub;
struct bt_mesh_model_pub light_hsl_srv_pub;
struct bt_mesh_model_pub light_hsl_cli_pub;

struct os_mbuf *bt_mesh_pub_msg_light_lightness_srv_pub;
struct os_mbuf *bt_mesh_pub_msg_light_lightness_cli_pub;
struct os_mbuf *bt_mesh_pub_msg_light_ctl_srv_pub;
struct os_mbuf *bt_mesh_pub_msg_light_ctl_cli_pub;
struct os_mbuf *bt_mesh_pub_msg_light_hsl_srv_pub;
struct os_mbuf *bt_mesh_pub_msg_light_hsl_cli_pub;

/* Definitions of models user data (Start) */
struct light_state light_user_data;
/* Definitions of models user data (End) */

/* message handlers (Start) */
/* Light Lightness Server message handlers */
static void light_lightness_status_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-lightness STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 2 + 4);
	struct light_state *data = model->user_data; //on_off state store in model->user_data->on_off

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x4E));
	net_buf_simple_add_le16(msg, data->light_linear);

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send GEN_ONOFF_SRV Status response\n");
	}

	os_mbuf_free_chain(msg);
}

static void light_lightness_get_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "#mesh-lightness GET\n");

	light_lightness_status_srv(model, ctx);
}

static void light_lightness_set_unack_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
    light_user_data.light_linear = (uint16_t)net_buf_simple_pull_le16(buf);
	ESP_LOGI(tag, "#mesh-lightness SET-UNACK: lightness=%d\n", light_user_data.light_linear);
}

static void light_lightness_set_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	light_user_data.light_linear = (uint16_t)net_buf_simple_pull_le16(buf);
	ESP_LOGI(tag, "#mesh-lightness SET: light=%d\n", light_user_data.light_linear);

    light_lightness_status_srv(model, ctx); //ACK
}

void light_lightness_publish(struct bt_mesh_model *model)
{
	int err;
	struct os_mbuf *msg = model->pub->msg;
	struct light_state *data = model->user_data;

	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		return;
	}

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x4D));
	net_buf_simple_add_le16(msg, data->light_linear);

	err = bt_mesh_model_publish(model);
	if (err) {
		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
	}
}

static void light_lightness_status_cli(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "Acknownledgement from LIGHT_LIGHTNESS_SRV\n");
	ESP_LOGI(tag, "Present lightness = %02x\n", net_buf_simple_pull_le16(buf));
}
//----------------------
static void light_ctl_temp_status_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-light-temp STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 2 + 4);
	struct light_state *data = model->user_data; 

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x66));
	net_buf_simple_add_le16(msg, data->light_temp);

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send GEN_ONOFF_SRV Status response\n");
	}

	os_mbuf_free_chain(msg);
}

static void light_ctl_temp_get_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "#mesh-light-temp GET\n");

	light_ctl_temp_status_srv(model, ctx);
}

static void light_ctl_temp_set_unack_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
    light_user_data.light_temp = (uint16_t)net_buf_simple_pull_le16(buf);
	ESP_LOGI(tag, "#mesh-light-temp SET-UNACK: temp=%d\n", light_user_data.light_temp);
}

static void light_ctl_temp_set_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	light_user_data.light_temp = (uint16_t)net_buf_simple_pull_le16(buf);
	ESP_LOGI(tag, "#mesh-lightness SET: light=%d\n", light_user_data.light_temp);

    light_ctl_temp_status_srv(model, ctx); //ACK
}

void light_ctl_publish(struct bt_mesh_model *model)
{
	int err;
	struct os_mbuf *msg = model->pub->msg;
	struct light_state *data = model->user_data;

	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		return;
	}

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x65));
	net_buf_simple_add_le16(msg, data->light_temp);

	err = bt_mesh_model_publish(model);
	if (err) {
		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
	}
}

static void light_ctl_temp_status_cli(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "Acknownledgement from LIGHT_CTL_SRV\n");
	ESP_LOGI(tag, "Present temp = %02x\n", net_buf_simple_pull_le16(buf));
}

//------------------------
static void light_hsl_status_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-light-hsl STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 6 + 4);
	struct light_state *data = model->user_data; 

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x78));
	net_buf_simple_add_le16(msg, data->light_linear);
	net_buf_simple_add_le16(msg, data->light_hue);
	net_buf_simple_add_le16(msg, data->light_saturation);

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send GEN_ONOFF_SRV Status response\n");
	}

	os_mbuf_free_chain(msg);
}

static void light_hsl_get_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "#mesh-hsl GET\n");

	light_hsl_status_srv(model, ctx);
}

static void light_hsl_set_unack_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
    light_user_data.light_linear = (uint16_t)net_buf_simple_pull_le16(buf);
	light_user_data.light_hue = (uint16_t)net_buf_simple_pull_le16(buf);
	light_user_data.light_saturation = (uint16_t)net_buf_simple_pull_le16(buf);
	ESP_LOGI(tag, "#mesh-hsl SET-UNACK: light_linear=%d hue=%d saturation=%d\n", light_user_data.light_linear,
					light_user_data.light_hue, light_user_data.light_saturation);
}

static void light_hsl_set_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
    light_user_data.light_linear = (uint16_t)net_buf_simple_pull_le16(buf);
	light_user_data.light_hue = (uint16_t)net_buf_simple_pull_le16(buf);
	light_user_data.light_saturation = (uint16_t)net_buf_simple_pull_le16(buf);
	ESP_LOGI(tag, "#mesh-hsl SET: light_linear=%d hue=%d saturation=%d\n", light_user_data.light_linear,
					light_user_data.light_hue, light_user_data.light_saturation);

    light_hsl_status_srv(model, ctx); //ACK
}

void light_hsl_publish(struct bt_mesh_model *model)
{
	int err;
	struct os_mbuf *msg = model->pub->msg;
	struct light_state *data = model->user_data;

	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		return;
	}

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_2(0x82, 0x77));
	net_buf_simple_add_le16(msg, data->light_linear);
	net_buf_simple_add_le16(msg, data->light_hue);
	net_buf_simple_add_le16(msg, data->light_saturation);

	err = bt_mesh_model_publish(model);
	if (err) {
		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
	}
}

static void light_hsl_status_cli(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "Acknownledgement from LIGHT_CTL_SRV\n");
	ESP_LOGI(tag, "Present linear = %02x hue = %02x saturation = %02x\n", net_buf_simple_pull_le16(buf),
	net_buf_simple_pull_le16(buf), net_buf_simple_pull_le16(buf));
}
//-----------------------------
/* Mapping of message handlers for Light Lightness Server (0x1300) */
const struct bt_mesh_model_op light_lightness_srv_op[] = {
	{ BT_MESH_MODEL_OP_2(0x82, 0x4B), 0, light_lightness_get_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x4C), 2, light_lightness_set_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x4D), 2, light_lightness_set_unack_srv },
	BT_MESH_MODEL_OP_END,
};

/* Mapping of message handlers for Light Lightness Client (0x1302) */
const struct bt_mesh_model_op light_lightness_cli_op[] = {
	{ BT_MESH_MODEL_OP_2(0x82, 0x4E), 2, light_lightness_status_cli },
	BT_MESH_MODEL_OP_END,
};

/* Mapping of message handlers for Light CTL Server (0x1303) */
const struct bt_mesh_model_op light_ctl_srv_op[] = {
	{ BT_MESH_MODEL_OP_2(0x82, 0x61), 0,  light_ctl_temp_get_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x64), 2, light_ctl_temp_set_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x65), 2, light_ctl_temp_set_unack_srv },
	BT_MESH_MODEL_OP_END,
};

/* Mapping of message handlers for Light CTL Client (0x1305) */
const struct bt_mesh_model_op light_ctl_cli_op[] = {
	{ BT_MESH_MODEL_OP_2(0x82, 0x66), 2, light_ctl_temp_status_cli },
	BT_MESH_MODEL_OP_END,
};

/* Mapping of message handlers for Light CTL Server (0x1303) */
const struct bt_mesh_model_op light_hsl_srv_op[] = {
	{ BT_MESH_MODEL_OP_2(0x82, 0x6D), 0,  light_hsl_get_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x76), 6,  light_hsl_set_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x77), 6,  light_hsl_set_unack_srv },
	BT_MESH_MODEL_OP_END,
};

/* Mapping of message handlers for Light CTL Client (0x1305) */
const struct bt_mesh_model_op light_hsl_cli_op[] = {
	{ BT_MESH_MODEL_OP_2(0x82, 0x78), 6, light_hsl_status_cli },
	BT_MESH_MODEL_OP_END,
};