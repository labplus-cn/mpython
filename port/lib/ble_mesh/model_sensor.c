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
#include "model_sensor.h"
// #include "state_binding.h"
// #include "transition.h"

static const char *tag = "model_sensor";

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

static struct bt_mesh_model_pub gen_onoff_srv_pub_root;
static struct bt_mesh_model_pub gen_onoff_cli_pub_root;
static struct bt_mesh_model_pub gen_level_srv_pub_root;
static struct bt_mesh_model_pub gen_level_cli_pub_root;
static struct bt_mesh_model_pub gen_def_trans_time_srv_pub;
static struct bt_mesh_model_pub gen_def_trans_time_cli_pub;
static struct bt_mesh_model_pub gen_power_onoff_srv_pub;
static struct bt_mesh_model_pub gen_power_onoff_cli_pub;
static struct bt_mesh_model_pub light_ctl_srv_pub;
static struct bt_mesh_model_pub light_ctl_cli_pub;
static struct bt_mesh_model_pub vnd_pub;


static struct os_mbuf *bt_mesh_pub_msg_health_pub;
static struct os_mbuf *bt_mesh_pub_msg_gen_onoff_srv_pub_root;
static struct os_mbuf *bt_mesh_pub_msg_gen_onoff_cli_pub_root;
static struct os_mbuf *bt_mesh_pub_msg_gen_level_srv_pub_root;
static struct os_mbuf *bt_mesh_pub_msg_gen_level_cli_pub_root;
static struct os_mbuf *bt_mesh_pub_msg_gen_def_trans_time_srv_pub;
static struct os_mbuf *bt_mesh_pub_msg_gen_def_trans_time_cli_pub;
static struct os_mbuf *bt_mesh_pub_msg_gen_power_onoff_srv_pub;
static struct os_mbuf *bt_mesh_pub_msg_gen_power_onoff_cli_pub;
static struct os_mbuf *bt_mesh_pub_msg_light_ctl_srv_pub;
static struct os_mbuf *bt_mesh_pub_msg_light_ctl_cli_pub;
static struct os_mbuf *bt_mesh_pub_msg_vnd_pub;


void init_pub(void)
{
	bt_mesh_pub_msg_health_pub			= NET_BUF_SIMPLE(1 + 3 + 0);
	bt_mesh_pub_msg_gen_onoff_srv_pub_root		= NET_BUF_SIMPLE(2 + 3);
	bt_mesh_pub_msg_gen_onoff_cli_pub_root		= NET_BUF_SIMPLE(2 + 4);
	bt_mesh_pub_msg_gen_level_srv_pub_root		= NET_BUF_SIMPLE(2 + 5);
	bt_mesh_pub_msg_gen_level_cli_pub_root		= NET_BUF_SIMPLE(2 + 7);
	bt_mesh_pub_msg_light_ctl_srv_pub		= NET_BUF_SIMPLE(2 + 9);
	bt_mesh_pub_msg_light_ctl_cli_pub		= NET_BUF_SIMPLE(2 + 9);
	bt_mesh_pub_msg_vnd_pub				= NET_BUF_SIMPLE(3 + 6);

	health_pub.msg				= bt_mesh_pub_msg_health_pub;
	gen_onoff_srv_pub_root.msg		= bt_mesh_pub_msg_gen_onoff_srv_pub_root;
	gen_onoff_cli_pub_root.msg		= bt_mesh_pub_msg_gen_onoff_cli_pub_root;
	gen_level_srv_pub_root.msg		= bt_mesh_pub_msg_gen_level_srv_pub_root;
	gen_level_cli_pub_root.msg		= bt_mesh_pub_msg_gen_level_cli_pub_root;
	light_ctl_srv_pub.msg			= bt_mesh_pub_msg_light_ctl_srv_pub;
	light_ctl_cli_pub.msg			= bt_mesh_pub_msg_light_ctl_cli_pub;
	vnd_pub.msg				= bt_mesh_pub_msg_vnd_pub;
}

/* Definitions of models user data (Start) */
struct generic_onoff_state gen_onoff_srv_root_user_data;

struct generic_level_state gen_level_srv_root_user_data;

struct light_ctl_state light_ctl_srv_user_data;

struct vendor_state vnd_user_data;

/* Definitions of models user data (End) */

static struct bt_mesh_elem elements[];

/* message handlers (Start) */
/* Generic OnOff srv message handlers */
static void gen_onoff_status_srv(struct bt_mesh_model *model,
                             struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-onoff on_off STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 3 + 4);
	struct generic_onoff_state *state = model->user_data; //on_off state store in model->user_data->on_off

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_GEN_ONOFF_STATUS);
	net_buf_simple_add_u8(msg, state->onoff);

	// if (state->transition->counter) {
	// 	calculate_rt(state->transition);
	// 	net_buf_simple_add_u8(msg, state->target_onoff);
	// 	net_buf_simple_add_u8(msg, state->transition->rt);
	// }

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send GEN_ONOFF_SRV Status response\n");
	}

	os_mbuf_free_chain(msg);
}

/* Generic OnOff Server message handlers */
static void gen_onoff_get_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "#mesh-onoff GET\n");

	gen_onoff_status_srv(model, ctx);
}

static void gen_onoff_set_unack_srv(struct bt_mesh_model *model,struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	struct generic_onoff_state *state = model->user_data;

    state->on_off = net_buf_simple_pull_u8(buf);
	ESP_LOGI(tag, "#mesh-onoff SET-UNACK: on_off=%d\n", state->on_off);
}

static void gen_onoff_set_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	struct generic_onoff_state *state = model->user_data;
    state->on_off = net_buf_simple_pull_u8(buf);
	ESP_LOGI(tag, "#mesh-onoff SET: on_off=%d\n", state->on_off);

    gen_onoff_status_srv(model, ctx); //ACK
}

/* Generic OnOff Client message handlers */
static void gen_onoff_status_cli(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "Acknownledgement from GEN_ONOFF_SRV\n");
	ESP_LOGI(tag, "Present OnOff = %02x\n", net_buf_simple_pull_u8(buf));

	if (buf->om_len == 2) {
		ESP_LOGI(tag, "Target OnOff = %02x\n", net_buf_simple_pull_u8(buf));
		ESP_LOGI(tag, "Remaining Time = %02x\n", net_buf_simple_pull_u8(buf));
	}
}

void gen_onoff_publish(struct bt_mesh_model *model)
{
	int err;
	struct os_mbuf *msg = model->pub->msg;
	struct generic_onoff_state *state = model->user_data;

	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		return;
	}

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_GEN_ONOFF_SET_UNACK);
	net_buf_simple_add_u8(msg, state->onoff);

	err = bt_mesh_model_publish(model);
	if (err) {
		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
	}
}

/* Generic Level Server message handlers */
static void gen_level_status_srv(struct bt_mesh_model *model,
                             struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-level STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 3 + 4);
	struct generic_level_state *state = model->user_data; //on_off state store in model->user_data->on_off

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_GEN_LEVEL_STATUS);
	net_buf_simple_add_le16(msg, state->level);

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send GEN_ONOFF_SRV Status response\n");
	}

	os_mbuf_free_chain(msg);
}
static void gen_level_get_srv(struct bt_mesh_model *model,  struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
    ESP_LOGI(tag, "#mesh-level GET\n");

    gen_level_status(model, ctx);
}

static void gen_level_set_unack_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	struct generic_level_state *state = model->user_data; //on_off state store in model->user_data->on_off

    state->level = (int16_t) net_buf_simple_pull_le16(buf);
    ESP_LOGI(tag, "#mesh-level SET-UNACK: level=%d\n", state->level);
}

static void gen_level_set_srv(struct bt_mesh_model *model,  struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	struct generic_level_state *state = model->user_data; //on_off state store in model->user_data->on_off

    state->level = (int16_t) net_buf_simple_pull_le16(buf);
    ESP_LOGI(tag, "#mesh-level SET-ACK: level=%d\n", state->level);
	gen_level_status_srv(model, ctx);
}

/* Generic Level Client message handlers */
static void gen_level_status_cli(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "Acknownledgement from GEN_LEVEL_SRV\n");
	ESP_LOGI(tag, "Present Level = %04x\n", net_buf_simple_pull_le16(buf));

	if (buf->om_len == 3) {
		ESP_LOGI(tag, "Target Level = %04x\n", net_buf_simple_pull_le16(buf));
		ESP_LOGI(tag, "Remaining Time = %02x\n", net_buf_simple_pull_u8(buf));
	}
}

void gen_level_publish(struct bt_mesh_model *model)
{
	int err;
	struct os_mbuf *msg = model->pub->msg;
	struct generic_level_state *state = model->user_data;

	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		return;
	}

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_GEN_LEVEL_SET_UNACK);
	net_buf_simple_add_le16(msg, state->level);


	err = bt_mesh_model_publish(model);
	if (err) {
		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
	}
}

/* Vendor Model message handlers*/
static void vnd_get(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	struct os_mbuf *msg = NET_BUF_SIMPLE(3 + 6 + 4);
	struct vendor_state *state = model->user_data;

	/* This is dummy response for demo purpose */
	state->response = 0xA578FEB3;

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_3(0x04, CID_RUNTIME));
	net_buf_simple_add_le16(msg, state->current);
	net_buf_simple_add_le32(msg, state->response);

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send VENDOR Status response\n");
	}

	os_mbuf_free_chain(msg);
}

static void vnd_set_unack(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	u8_t tid;
	int current;
	s64_t now;
	struct vendor_state *state = model->user_data;

	current = net_buf_simple_pull_le16(buf);
	tid = net_buf_simple_pull_u8(buf);

	now = k_uptime_get();
	if (state->last_tid == tid &&
	    state->last_src_addr == ctx->addr &&
	    state->last_dst_addr == ctx->recv_dst &&
	    (now - state->last_msg_timestamp <= K_SECONDS(6))) {
		return;
	}

	state->last_tid = tid;
	state->last_src_addr = ctx->addr;
	state->last_dst_addr = ctx->recv_dst;
	state->last_msg_timestamp = now;
	state->current = current;

	ESP_LOGI(tag, "Vendor model message = %04x\n", state->current);

	if (state->current == STATE_ON) {
		/* LED2 On */
		hal_gpio_write(led_device[1], 0);
	} else {
		/* LED2 Off */
		hal_gpio_write(led_device[1], 1);
	}
}

static void vnd_set(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	vnd_set_unack(model, ctx, buf);
	vnd_get(model, ctx, buf);
}

static void vnd_status(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "Acknownledgement from Vendor\n");
	ESP_LOGI(tag, "cmd = %04x\n", net_buf_simple_pull_le16(buf));
	ESP_LOGI(tag, "response = %08lx\n", net_buf_simple_pull_le32(buf));
}

// /* Light CTL Server message handlers */
// static void light_ctl_get(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 9 + 4);
// 	struct light_ctl_state *state = model->user_data;

// 	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_LIGHT_CTL_STATUS);
// 	net_buf_simple_add_le16(msg, state->lightness);
// 	net_buf_simple_add_le16(msg, state->temp);

// 	if (state->transition->counter) {
// 		calculate_rt(state->transition);
// 		net_buf_simple_add_le16(msg, state->target_lightness);
// 		net_buf_simple_add_le16(msg, state->target_temp);
// 		net_buf_simple_add_u8(msg, state->transition->rt);
// 	}

// 	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
// 		ESP_LOGI(tag, "Unable to send LightCTL Status response\n");
// 	}

// 	os_mbuf_free_chain(msg);
// }

// void light_ctl_publish(struct bt_mesh_model *model)
// {
// 	int err;
// 	struct os_mbuf *msg = model->pub->msg;
// 	struct light_ctl_state *state = model->user_data;

// 	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
// 		return;
// 	}

// 	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_LIGHT_CTL_STATUS);

// 	/* Here, as per Model specification, status should be
// 	 * made up of lightness & temperature values only
// 	 */
// 	net_buf_simple_add_le16(msg, state->lightness);
// 	net_buf_simple_add_le16(msg, state->temp);

// 	if (state->transition->counter) {
// 		calculate_rt(state->transition);
// 		net_buf_simple_add_le16(msg, state->target_lightness);
// 		net_buf_simple_add_le16(msg, state->target_temp);
// 		net_buf_simple_add_u8(msg, state->transition->rt);
// 	}

// 	err = bt_mesh_model_publish(model);
// 	if (err) {
// 		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
// 	}
// }

// static void light_ctl_set_unack(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	u8_t tid, tt, delay;
// 	s16_t delta_uv;
// 	u16_t lightness, temp;
// 	s64_t now;
// 	struct light_ctl_state *state = model->user_data;

// 	lightness = net_buf_simple_pull_le16(buf);
// 	temp = net_buf_simple_pull_le16(buf);
// 	delta_uv = (s16_t) net_buf_simple_pull_le16(buf);
// 	tid = net_buf_simple_pull_u8(buf);

// 	if (temp < TEMP_MIN || temp > TEMP_MAX) {
// 		return;
// 	}


// 	state->last_tid = tid;
// 	state->last_src_addr = ctx->addr;
// 	state->last_dst_addr = ctx->recv_dst;
// 	state->last_msg_timestamp = now;
// 	state->target_lightness = lightness;

// 	if (temp < state->temp_range_min) {
// 		temp = state->temp_range_min;
// 	} else if (temp > state->temp_range_max) {
// 		temp = state->temp_range_max;
// 	}

// 	state->target_temp = temp;
// 	state->target_delta_uv = delta_uv;

// 	if (state->target_lightness != state->lightness ||
// 	    state->target_temp != state->temp ||
// 	    state->target_delta_uv != state->delta_uv) {
// 		light_ctl_tt_values(state, tt, delay);
// 	} else {
// 		light_ctl_publish(model);
// 		return;
// 	}

// 	/* For Instantaneous Transition */
// 	if (state->transition->counter == 0) {
// 		state->lightness = state->target_lightness;
// 		state->temp = state->target_temp;
// 		state->delta_uv = state->target_delta_uv;
// 	}

// 	state->transition->just_started = true;
// 	light_ctl_publish(model);
// 	light_ctl_handler(state);
// }

// static void light_ctl_set(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	u8_t tid, tt, delay;
// 	s16_t delta_uv;
// 	u16_t lightness, temp;
// 	s64_t now;
// 	struct light_ctl_state *state = model->user_data;

// 	lightness = net_buf_simple_pull_le16(buf);
// 	temp = net_buf_simple_pull_le16(buf);
// 	delta_uv = (s16_t) net_buf_simple_pull_le16(buf);
// 	tid = net_buf_simple_pull_u8(buf);

// 	if (temp < TEMP_MIN || temp > TEMP_MAX) {
// 		return;
// 	}

// 	now = k_uptime_get();
// 	if (state->last_tid == tid &&
// 	    state->last_src_addr == ctx->addr &&
// 	    state->last_dst_addr == ctx->recv_dst &&
// 	    (now - state->last_msg_timestamp <= K_SECONDS(6))) {
// 		light_ctl_get(model, ctx, buf);
// 		return;
// 	}

// 	switch (buf->om_len) {
// 	case 0x00:	/* No optional fields are available */
// 		tt = default_tt;
// 		delay = 0;
// 		break;
// 	case 0x02:	/* Optional fields are available */
// 		tt = net_buf_simple_pull_u8(buf);
// 		if ((tt & 0x3F) == 0x3F) {
// 			return;
// 		}

// 		delay = net_buf_simple_pull_u8(buf);
// 		break;
// 	default:
// 		return;
// 	}

// 	*ptr_counter = 0;
// 	os_callout_stop(ptr_timer);

// 	state->last_tid = tid;
// 	state->last_src_addr = ctx->addr;
// 	state->last_dst_addr = ctx->recv_dst;
// 	state->last_msg_timestamp = now;
// 	state->target_lightness = lightness;

// 	if (temp < state->temp_range_min) {
// 		temp = state->temp_range_min;
// 	} else if (temp > state->temp_range_max) {
// 		temp = state->temp_range_max;
// 	}

// 	state->target_temp = temp;
// 	state->target_delta_uv = delta_uv;

// 	if (state->target_lightness != state->lightness ||
// 	    state->target_temp != state->temp ||
// 	    state->target_delta_uv != state->delta_uv) {
// 		light_ctl_tt_values(state, tt, delay);
// 	} else {
// 		light_ctl_get(model, ctx, buf);
// 		light_ctl_publish(model);
// 		return;
// 	}

// 	/* For Instantaneous Transition */
// 	if (state->transition->counter == 0) {
// 		state->lightness = state->target_lightness;
// 		state->temp = state->target_temp;
// 		state->delta_uv = state->target_delta_uv;
// 	}

// 	state->transition->just_started = true;
// 	light_ctl_get(model, ctx, buf);
// 	light_ctl_publish(model);
// 	light_ctl_handler(state);
// }

// static void light_ctl_temp_range_get(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 5 + 4);
// 	struct light_ctl_state *state = model->user_data;

// 	state->status_code = RANGE_SUCCESSFULLY_UPDATED;

// 	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_LIGHT_CTL_TEMP_RANGE_STATUS);
// 	net_buf_simple_add_u8(msg, state->status_code);
// 	net_buf_simple_add_le16(msg, state->temp_range_min);
// 	net_buf_simple_add_le16(msg, state->temp_range_max);

// 	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
// 		ESP_LOGI(tag, "Unable to send LightCTL Temp Range Status response\n");
// 	}

// 	os_mbuf_free_chain(msg);
// }

// static void light_ctl_default_get(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 6 + 4);
// 	struct light_ctl_state *state = model->user_data;

// 	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_LIGHT_CTL_DEFAULT_STATUS);
// 	net_buf_simple_add_le16(msg, state->lightness_def);
// 	net_buf_simple_add_le16(msg, state->temp_def);
// 	net_buf_simple_add_le16(msg, state->delta_uv_def);

// 	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
// 		ESP_LOGI(tag, "Unable to send LightCTL Default Status response\n");
// 	}

// 	os_mbuf_free_chain(msg);
// }

// /* Light CTL Setup Server message handlers */

// static void light_ctl_default_publish(struct bt_mesh_model *model)
// {
// 	int err;
// 	struct os_mbuf *msg = model->pub->msg;
// 	struct light_ctl_state *state = model->user_data;

// 	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
// 		return;
// 	}

// 	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_LIGHT_CTL_DEFAULT_STATUS);
// 	net_buf_simple_add_le16(msg, state->lightness_def);
// 	net_buf_simple_add_le16(msg, state->temp_def);
// 	net_buf_simple_add_le16(msg, state->delta_uv_def);

// 	err = bt_mesh_model_publish(model);
// 	if (err) {
// 		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
// 	}
// }

// static bool light_ctl_default_setunack(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	u16_t lightness, temp;
// 	s16_t delta_uv;
// 	struct light_ctl_state *state = model->user_data;

// 	lightness = net_buf_simple_pull_le16(buf);
// 	temp = net_buf_simple_pull_le16(buf);
// 	delta_uv = (s16_t) net_buf_simple_pull_le16(buf);

// 	/* Here, Model specification is silent about tid implementation */

// 	if (temp < TEMP_MIN || temp > TEMP_MAX) {
// 		return false;
// 	}

// 	if (temp < state->temp_range_min) {
// 		temp = state->temp_range_min;
// 	} else if (temp > state->temp_range_max) {
// 		temp = state->temp_range_max;
// 	}

// 	if (state->lightness_def != lightness || state->temp_def != temp ||
// 	    state->delta_uv_def != delta_uv) {
// 		state->lightness_def = lightness;
// 		state->temp_def = temp;
// 		state->delta_uv_def = delta_uv;

// 		save_on_flash(LIGHTNESS_TEMP_DEF_STATE);
// 	}

// 	return true;
// }

// static void light_ctl_default_set_unack(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	if (light_ctl_default_setunack(model, ctx, buf) == true) {
// 		light_ctl_default_publish(model);
// 	}
// }

// static void light_ctl_default_set(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	if (light_ctl_default_setunack(model, ctx, buf) == true) {
// 		light_ctl_default_get(model, ctx, buf);
// 		light_ctl_default_publish(model);
// 	}
// }

// static void light_ctl_temp_range_publish(struct bt_mesh_model *model)
// {
// 	int err;
// 	struct os_mbuf *msg = model->pub->msg;
// 	struct light_ctl_state *state = model->user_data;

// 	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
// 		return;
// 	}

// 	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_LIGHT_CTL_TEMP_RANGE_STATUS);
// 	net_buf_simple_add_u8(msg, state->status_code);
// 	net_buf_simple_add_le16(msg, state->temp_range_min);
// 	net_buf_simple_add_le16(msg, state->temp_range_max);

// 	err = bt_mesh_model_publish(model);
// 	if (err) {
// 		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
// 	}
// }

// static bool light_ctl_temp_range_setunack(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	u16_t min, max;
// 	struct light_ctl_state *state = model->user_data;

// 	min = net_buf_simple_pull_le16(buf);
// 	max = net_buf_simple_pull_le16(buf);

// 	/* Here, Model specification is silent about tid implementation */

// 	/* This is as per 6.1.3.1 in Mesh Model Specification */
// 	if (min < TEMP_MIN || min > TEMP_MAX ||
// 	    max < TEMP_MIN || max > TEMP_MAX) {
// 		return false;
// 	}

// 	if (min <= max) {
// 		state->status_code = RANGE_SUCCESSFULLY_UPDATED;

// 		if (state->temp_range_min != min ||
// 		    state->temp_range_max != max) {

// 			state->temp_range_min = min;
// 			state->temp_range_max = max;

// 			save_on_flash(TEMPERATURE_RANGE);
// 		}
// 	} else {
// 		/* The provided value for Range Max cannot be set */
// 		state->status_code = CANNOT_SET_RANGE_MAX;
// 		return false;
// 	}

// 	return true;
// }

// static void light_ctl_temp_range_set_unack(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	if (light_ctl_temp_range_setunack(model, ctx, buf) == true) {
// 		light_ctl_temp_range_publish(model);
// 	}
// }

// static void light_ctl_temp_range_set(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	if (light_ctl_temp_range_setunack(model, ctx, buf) == true) {
// 		light_ctl_temp_range_get(model, ctx, buf);
// 		light_ctl_temp_range_publish(model);
// 	}
// }

// /* Light CTL Client message handlers */
// static void light_ctl_status(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	ESP_LOGI(tag, "Acknownledgement from LIGHT_CTL_SRV\n");
// 	ESP_LOGI(tag, "Present CTL Lightness = %04x\n", net_buf_simple_pull_le16(buf));
// 	ESP_LOGI(tag, "Present CTL Temperature = %04x\n",
// 	       net_buf_simple_pull_le16(buf));

// 	if (buf->om_len == 5) {
// 		ESP_LOGI(tag, "Target CTL Lightness = %04x\n",
// 		       net_buf_simple_pull_le16(buf));
// 		ESP_LOGI(tag, "Target CTL Temperature = %04x\n",
// 		       net_buf_simple_pull_le16(buf));
// 		ESP_LOGI(tag, "Remaining Time = %02x\n", net_buf_simple_pull_u8(buf));
// 	}
// }

// static void light_ctl_temp_range_status(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	ESP_LOGI(tag, "Acknownledgement from LIGHT_CTL_SRV (Temperature Range)\n");
// 	ESP_LOGI(tag, "Status Code = %02x\n", net_buf_simple_pull_u8(buf));
// 	ESP_LOGI(tag, "Range Min = %04x\n", net_buf_simple_pull_le16(buf));
// 	ESP_LOGI(tag, "Range Max = %04x\n", net_buf_simple_pull_le16(buf));
// }

// static void light_ctl_temp_status(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	ESP_LOGI(tag, "Acknownledgement from LIGHT_CTL_TEMP_SRV\n");
// 	ESP_LOGI(tag, "Present CTL Temperature = %04x\n",
// 	       net_buf_simple_pull_le16(buf));
// 	ESP_LOGI(tag, "Present CTL Delta UV = %04x\n",
// 	       net_buf_simple_pull_le16(buf));

// 	if (buf->om_len == 5) {
// 		ESP_LOGI(tag, "Target CTL Temperature = %04x\n",
// 		       net_buf_simple_pull_le16(buf));
// 		ESP_LOGI(tag, "Target CTL Delta UV = %04x\n",
// 		       net_buf_simple_pull_le16(buf));
// 		ESP_LOGI(tag, "Remaining Time = %02x\n", net_buf_simple_pull_u8(buf));
// 	}
// }

// static void light_ctl_default_status(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	ESP_LOGI(tag, "Acknownledgement from LIGHT_CTL_SRV (Default)\n");
// 	ESP_LOGI(tag, "Lightness = %04x\n", net_buf_simple_pull_le16(buf));
// 	ESP_LOGI(tag, "Temperature = %04x\n", net_buf_simple_pull_le16(buf));
// 	ESP_LOGI(tag, "Delta UV = %04x\n", net_buf_simple_pull_le16(buf));
// }

// /* Light CTL Temp. Server message handlers */
// static void light_ctl_temp_get(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 9 + 4);
// 	struct light_ctl_state *state = model->user_data;

// 	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_LIGHT_CTL_TEMP_STATUS);
// 	net_buf_simple_add_le16(msg, state->temp);
// 	net_buf_simple_add_le16(msg, state->delta_uv);

// 	if (state->transition->counter) {
// 		calculate_rt(state->transition);
// 		net_buf_simple_add_le16(msg, state->target_temp);
// 		net_buf_simple_add_le16(msg, state->target_delta_uv);
// 		net_buf_simple_add_u8(msg, state->transition->rt);
// 	}

// 	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
// 		ESP_LOGI(tag, "Unable to send LightCTL Temp. Status response\n");
// 	}

// 	os_mbuf_free_chain(msg);
// }

// void light_ctl_temp_publish(struct bt_mesh_model *model)
// {
// 	int err;
// 	struct os_mbuf *msg = model->pub->msg;
// 	struct light_ctl_state *state = model->user_data;

// 	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
// 		return;
// 	}

// 	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_LIGHT_CTL_TEMP_STATUS);
// 	net_buf_simple_add_le16(msg, state->temp);
// 	net_buf_simple_add_le16(msg, state->delta_uv);

// 	if (state->transition->counter) {
// 		calculate_rt(state->transition);
// 		net_buf_simple_add_le16(msg, state->target_temp);
// 		net_buf_simple_add_le16(msg, state->target_delta_uv);
// 		net_buf_simple_add_u8(msg, state->transition->rt);
// 	}

// 	err = bt_mesh_model_publish(model);
// 	if (err) {
// 		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
// 	}
// }

// static void light_ctl_temp_set_unack(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	u8_t tid, tt, delay;
// 	s16_t delta_uv;
// 	u16_t temp;
// 	s64_t now;
// 	struct light_ctl_state *state = model->user_data;

// 	temp = net_buf_simple_pull_le16(buf);
// 	delta_uv = (s16_t) net_buf_simple_pull_le16(buf);
// 	tid = net_buf_simple_pull_u8(buf);

// 	if (temp < TEMP_MIN || temp > TEMP_MAX) {
// 		return;
// 	}

// 	now = k_uptime_get();
// 	if (state->last_tid == tid &&
// 	    state->last_src_addr == ctx->addr &&
// 	    state->last_dst_addr == ctx->recv_dst &&
// 	    (now - state->last_msg_timestamp <= K_SECONDS(6))) {
// 		return;
// 	}

// 	switch (buf->om_len) {
// 	case 0x00:	/* No optional fields are available */
// 		tt = default_tt;
// 		delay = 0;
// 		break;
// 	case 0x02:	/* Optional fields are available */
// 		tt = net_buf_simple_pull_u8(buf);
// 		if ((tt & 0x3F) == 0x3F) {
// 			return;
// 		}

// 		delay = net_buf_simple_pull_u8(buf);
// 		break;
// 	default:
// 		return;
// 	}

// 	*ptr_counter = 0;
// 	os_callout_stop(ptr_timer);

// 	state->last_tid = tid;
// 	state->last_src_addr = ctx->addr;
// 	state->last_dst_addr = ctx->recv_dst;
// 	state->last_msg_timestamp = now;

// 	if (temp < state->temp_range_min) {
// 		temp = state->temp_range_min;
// 	} else if (temp > state->temp_range_max) {
// 		temp = state->temp_range_max;
// 	}

// 	state->target_temp = temp;
// 	state->target_delta_uv = delta_uv;

// 	if (state->target_temp != state->temp ||
// 	    state->target_delta_uv != state->delta_uv) {
// 		light_ctl_temp_tt_values(state, tt, delay);
// 	} else {
// 		light_ctl_temp_publish(model);
// 		return;
// 	}

// 	/* For Instantaneous Transition */
// 	if (state->transition->counter == 0) {
// 		state->temp = state->target_temp;
// 		state->delta_uv = state->target_delta_uv;
// 	}

// 	state->transition->just_started = true;
// 	light_ctl_temp_publish(model);
// 	light_ctl_temp_handler(state);
// }

// static void light_ctl_temp_set(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
// {
// 	u8_t tid, tt, delay;
// 	s16_t delta_uv;
// 	u16_t temp;
// 	s64_t now;
// 	struct light_ctl_state *state = model->user_data;

// 	temp = net_buf_simple_pull_le16(buf);
// 	delta_uv = (s16_t) net_buf_simple_pull_le16(buf);
// 	tid = net_buf_simple_pull_u8(buf);

// 	if (temp < TEMP_MIN || temp > TEMP_MAX) {
// 		return;
// 	}

// 	now = k_uptime_get();
// 	if (state->last_tid == tid &&
// 	    state->last_src_addr == ctx->addr &&
// 	    state->last_dst_addr == ctx->recv_dst &&
// 	    (now - state->last_msg_timestamp <= K_SECONDS(6))) {
// 		light_ctl_temp_get(model, ctx, buf);
// 		return;
// 	}

// 	switch (buf->om_len) {
// 	case 0x00:	/* No optional fields are available */
// 		tt = default_tt;
// 		delay = 0;
// 		break;
// 	case 0x02:	/* Optional fields are available */
// 		tt = net_buf_simple_pull_u8(buf);
// 		if ((tt & 0x3F) == 0x3F) {
// 			return;
// 		}

// 		delay = net_buf_simple_pull_u8(buf);
// 		break;
// 	default:
// 		return;
// 	}

// 	*ptr_counter = 0;
// 	os_callout_stop(ptr_timer);

// 	state->last_tid = tid;
// 	state->last_src_addr = ctx->addr;
// 	state->last_dst_addr = ctx->recv_dst;
// 	state->last_msg_timestamp = now;

// 	if (temp < state->temp_range_min) {
// 		temp = state->temp_range_min;
// 	} else if (temp > state->temp_range_max) {
// 		temp = state->temp_range_max;
// 	}

// 	state->target_temp = temp;
// 	state->target_delta_uv = delta_uv;

// 	if (state->target_temp != state->temp ||
// 	    state->target_delta_uv != state->delta_uv) {
// 		light_ctl_temp_tt_values(state, tt, delay);
// 	} else {
// 		light_ctl_temp_get(model, ctx, buf);
// 		light_ctl_temp_publish(model);
// 		return;
// 	}

// 	/* For Instantaneous Transition */
// 	if (state->transition->counter == 0) {
// 		state->temp = state->target_temp;
// 		state->delta_uv = state->target_delta_uv;
// 	}

// 	state->transition->just_started = true;
// 	light_ctl_temp_get(model, ctx, buf);
// 	light_ctl_temp_publish(model);
// 	light_ctl_temp_handler(state);
// }

/* message handlers (End) */

// /* Mapping of message handlers for Generic OnOff Server (0x1000) */
// static const struct bt_mesh_model_op gen_onoff_srv_op[] = {
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x01), 0, gen_onoff_get_srv },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x02), 2, gen_onoff_set_srv },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x03), 2, gen_onoff_set_unack_srv },
// 	BT_MESH_MODEL_OP_END,
// };

// /* Mapping of message handlers for Generic OnOff Client (0x1001) */
// static const struct bt_mesh_model_op gen_onoff_cli_op[] = {
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x04), 1, gen_onoff_status_cli },
// 	BT_MESH_MODEL_OP_END,
// };

// /* Mapping of message handlers for Generic Levl Server (0x1002) */
// static const struct bt_mesh_model_op gen_level_srv_op[] = {
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x05), 0, gen_level_get_srv },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x06), 3, gen_level_set_srv },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x07), 3, gen_level_set_unack_srv },
//     { BT_MESH_MODEL_OP_2(0x82, 0x08), 3, gen_level_status_srv },
// 	BT_MESH_MODEL_OP_END,
// };

// /* Mapping of message handlers for Generic Level Client (0x1003) */
// static const struct bt_mesh_model_op gen_level_cli_op[] = {
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x08), 2, gen_level_status_cli },
// 	BT_MESH_MODEL_OP_END,
// };


// /* Mapping of message handlers for Light CTL Server (0x1303) */
// static const struct bt_mesh_model_op light_ctl_srv_op[] = {
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x5D), 0, light_ctl_get },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x5E), 7, light_ctl_set },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x5F), 7, light_ctl_set_unack },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x62), 0, light_ctl_temp_range_get },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x67), 0, light_ctl_default_get },
// 	BT_MESH_MODEL_OP_END,
// };

// /* Mapping of message handlers for Light CTL Setup Server (0x1304) */
// static const struct bt_mesh_model_op light_ctl_setup_srv_op[] = {
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x69), 6, light_ctl_default_set },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x6A), 6, light_ctl_default_set_unack },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x6B), 4, light_ctl_temp_range_set },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x6C), 4, light_ctl_temp_range_set_unack },
// 	BT_MESH_MODEL_OP_END,
// };

// /* Mapping of message handlers for Light CTL Client (0x1305) */
// static const struct bt_mesh_model_op light_ctl_cli_op[] = {
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x60), 4, light_ctl_status },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x63), 5, light_ctl_temp_range_status },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x66), 4, light_ctl_temp_status },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x68), 6, light_ctl_default_status },
// 	BT_MESH_MODEL_OP_END,
// };

// /* Mapping of message handlers for Light CTL Temp. Server (0x1306) */
// static const struct bt_mesh_model_op light_ctl_temp_srv_op[] = {
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x61), 0, light_ctl_temp_get },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x64), 5, light_ctl_temp_set },
// 	{ BT_MESH_MODEL_OP_2(0x82, 0x65), 5, light_ctl_temp_set_unack },
// 	BT_MESH_MODEL_OP_END,
// };

// /* Mapping of message handlers for Vendor (0x4321) */
// static const struct bt_mesh_model_op vnd_ops[] = {
// 	{ BT_MESH_MODEL_OP_3(0x01, CID_RUNTIME), 0, vnd_get },
// 	{ BT_MESH_MODEL_OP_3(0x02, CID_RUNTIME), 3, vnd_set },
// 	{ BT_MESH_MODEL_OP_3(0x03, CID_RUNTIME), 3, vnd_set_unack },
// 	{ BT_MESH_MODEL_OP_3(0x04, CID_RUNTIME), 6, vnd_status },
// 	BT_MESH_MODEL_OP_END,
// };

struct bt_mesh_model root_models[] = {
	BT_MESH_MODEL_CFG_SRV(&cfg_srv),
	BT_MESH_MODEL_HEALTH_SRV(&health_srv, &health_pub),

	BT_MESH_MODEL(BT_MESH_MODEL_ID_GEN_ONOFF_SRV, gen_onoff_srv_op, &gen_onoff_srv_pub_root, &gen_onoff_srv_root_user_data), //参数：类型 操作集 消息发布结构 用户数据
	BT_MESH_MODEL(BT_MESH_MODEL_ID_GEN_ONOFF_CLI, gen_onoff_cli_op, &gen_onoff_cli_pub_root, NULL),

	BT_MESH_MODEL(BT_MESH_MODEL_ID_GEN_LEVEL_SRV, gen_level_srv_op, &gen_level_srv_pub_root, &gen_level_srv_root_user_data),
	BT_MESH_MODEL(BT_MESH_MODEL_ID_GEN_LEVEL_CLI, gen_level_cli_op, &gen_level_cli_pub_root, NULL),

	// BT_MESH_MODEL(BT_MESH_MODEL_ID_LIGHT_CTL_SRV, light_ctl_srv_op, &light_ctl_srv_pub, &light_ctl_srv_user_data),
	// BT_MESH_MODEL(BT_MESH_MODEL_ID_LIGHT_CTL_SETUP_SRV, light_ctl_setup_srv_op, &light_ctl_srv_pub, &light_ctl_srv_user_data),
	// BT_MESH_MODEL(BT_MESH_MODEL_ID_LIGHT_CTL_CLI,  light_ctl_cli_op, &light_ctl_cli_pub, NULL),
};

struct bt_mesh_model vnd_models[] = {
	BT_MESH_MODEL_VND(CID_RUNTIME, 0x4321, vnd_ops,
			  &vnd_pub, &vnd_user_data),
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

