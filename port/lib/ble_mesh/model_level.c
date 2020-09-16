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
#include "model_level.h"
#include "py/runtime.h"
#include "py/obj.h"

static const char *tag = "model_level";
extern mp_obj_t callbacks[6];

struct bt_mesh_model_pub gen_level_srv_pub_root;
struct bt_mesh_model_pub gen_level_cli_pub_root;

struct os_mbuf *bt_mesh_pub_msg_gen_level_srv_pub_root;
struct os_mbuf *bt_mesh_pub_msg_gen_level_cli_pub_root;

/* Definitions of models user data (Start) */
struct generic_level_state gen_level_user_data;
/* Definitions of models user data (End) */

/* message handlers (Start) */
/* Generic Level Server message handlers */
static void gen_level_status_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx)
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

    gen_level_status_srv(model, ctx);
}

static void gen_level_set_unack_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	struct generic_level_state *state = model->user_data; //on_off state store in model->user_data->on_off

    state->level = (int16_t) net_buf_simple_pull_le16(buf);
    ESP_LOGI(tag, "#mesh-level SET-UNACK: level=%d\n", state->level);

	if(callbacks[1]){
		mp_sched_schedule(callbacks[1], mp_obj_new_int(state->level));
	}
}

static void gen_level_set_srv(struct bt_mesh_model *model,  struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	struct generic_level_state *state = model->user_data; //on_off state store in model->user_data->on_off

    state->level = (int16_t) net_buf_simple_pull_le16(buf);
    ESP_LOGI(tag, "#mesh-level SET-ACK: level=%d\n", state->level);
	gen_level_status_srv(model, ctx);

	if(callbacks[1]){
		mp_sched_schedule(callbacks[1], mp_obj_new_int(state->level));
	}
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

/* Mapping of message handlers for Generic Levl Server (0x1002) */
const struct bt_mesh_model_op gen_level_srv_op[] = {
	{ BT_MESH_MODEL_OP_2(0x82, 0x05), 0, gen_level_get_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x06), 2, gen_level_set_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x07), 2, gen_level_set_unack_srv },
	BT_MESH_MODEL_OP_END,
};

/* Mapping of message handlers for Generic Level Client (0x1003) */
const struct bt_mesh_model_op gen_level_cli_op[] = {
	{ BT_MESH_MODEL_OP_2(0x82, 0x08), 2, gen_level_status_cli },
	BT_MESH_MODEL_OP_END,
};