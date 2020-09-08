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
#include "model_on_off.h"
// #include "state_binding.h"
// #include "transition.h"

static const char *tag = "model_onoff";

struct bt_mesh_model_pub gen_onoff_srv_pub_root;
struct bt_mesh_model_pub gen_onoff_cli_pub_root;

struct os_mbuf *bt_mesh_pub_msg_gen_onoff_srv_pub_root;
struct os_mbuf *bt_mesh_pub_msg_gen_onoff_cli_pub_root;

/* Definitions of models user data (Start) */
struct generic_onoff_state gen_onoff_user_data;
/* Definitions of models user data (End) */

/* message handlers (Start) */
/* Generic OnOff srv message handlers */
static void gen_onoff_status_srv(struct bt_mesh_model *model,
                             struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-onoff on_off STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(2 + 1 + 4);
	struct generic_onoff_state *state = model->user_data; //on_off state store in model->user_data->on_off

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_GEN_ONOFF_STATUS);
	net_buf_simple_add_u8(msg, state->onoff);

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

    state->onoff = net_buf_simple_pull_u8(buf);
	ESP_LOGI(tag, "#mesh-onoff SET-UNACK: on_off=%d\n", state->onoff);
}

static void gen_onoff_set_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	struct generic_onoff_state *state = model->user_data;
    state->onoff = net_buf_simple_pull_u8(buf);
	ESP_LOGI(tag, "#mesh-onoff SET: on_off=%d\n", state->onoff);

    gen_onoff_status_srv(model, ctx); //ACK
}

/* Generic OnOff Client message handlers */
static void gen_onoff_status_cli(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "Acknownledgement from GEN_ONOFF_SRV\n");
	ESP_LOGI(tag, "Present OnOff = %02x\n", net_buf_simple_pull_u8(buf));
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

/* Mapping of message handlers for Generic OnOff Server (0x1000) */
const struct bt_mesh_model_op gen_onoff_srv_op[] = {
	{ BT_MESH_MODEL_OP_2(0x82, 0x01), 0, gen_onoff_get_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x02), 1, gen_onoff_set_srv },
	{ BT_MESH_MODEL_OP_2(0x82, 0x03), 1, gen_onoff_set_unack_srv },
	BT_MESH_MODEL_OP_END,
};

/* Mapping of message handlers for Generic OnOff Client (0x1001) */
const struct bt_mesh_model_op gen_onoff_cli_op[] = {
	{ BT_MESH_MODEL_OP_2(0x82, 0x04), 1, gen_onoff_status_cli },
	BT_MESH_MODEL_OP_END,
};