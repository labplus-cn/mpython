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
#include "py/obj.h"
#include "py/objstr.h"
#include "py/runtime.h"
#include "mphalport.h"
#include "esp_log.h"
#include "mesh/mesh.h"

#include "ble_mesh.h"
#include "model_vnd.h"

static const char *tag = "model_vnd";
extern mp_obj_t callbacks[6];

struct bt_mesh_model_pub vnd_pub_srv;
struct bt_mesh_model_pub vnd_pub_cli;
struct os_mbuf *bt_mesh_pub_msg_vnd_pub;
// struct os_mbuf *bt_mesh_pub_msg_vnd_pub_cli;

/* Definitions of models user data (Start) */
struct vendor_state vnd_user_data;
/* Definitions of models user data (End) */

/* message handlers (Start) */
/* Vendor Model message handlers*/
static void vnd_status_srv(struct bt_mesh_model *model,
                             struct bt_mesh_msg_ctx *ctx)
{
	ESP_LOGI(tag, "#mesh-vnd STATUS\n");

	struct os_mbuf *msg = NET_BUF_SIMPLE(3 + 17 + 4);
	struct vendor_state *state = model->user_data; //on_off state store in model->user_data->on_off

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_3(0x04, CID_RUNTIME));
	net_buf_simple_add_u8(msg, state->len);
	for(int i = 0; i < state->len; i++)
		net_buf_simple_add_u8(msg, state->data[i]);

	if (bt_mesh_model_send(model, ctx, msg, NULL, NULL)) {
		ESP_LOGI(tag, "Unable to send GEN_ONOFF_SRV Status response\n");
	}

	os_mbuf_free_chain(msg);
}

static void vnd_get_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	ESP_LOGI(tag, "#mesh-vnd GET\n");

	vnd_status_srv(model, ctx);
}

static void vnd_set_unack_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	struct vendor_state *state = model->user_data;

	state->len = net_buf_simple_pull_u8(buf);
	for(int i = 0; i < state->len; i++)
		state->data[i] = net_buf_simple_pull_u8(buf);

    vstr_t vstr;
    vstr_init_len(&vstr, state->len);
	for(int i = 0; i < state->len; i++)
		vstr.buf[i] = state->data[i];
	if(callbacks[5]){
		mp_sched_schedule(callbacks[5], mp_obj_new_str_from_vstr(&mp_type_bytes, &vstr));
	}
}

static void vnd_set_srv(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	struct vendor_state *state = model->user_data;

	state->len = net_buf_simple_pull_u8(buf);
	for(int i = 0; i < state->len; i++)
		state->data[i] = net_buf_simple_pull_u8(buf);
	ESP_LOGI(tag, "#mesh-vnd SET-UNACK: state->data[0]=%d\n", state->data[0]);

	vnd_status_srv(model, ctx);

    vstr_t vstr;
    vstr_init_len(&vstr, state->len);
	for(int i = 0; i < state->len; i++)
		vstr.buf[i] = state->data[i];
	if(callbacks[5]){
		mp_sched_schedule(callbacks[5], mp_obj_new_str_from_vstr(&mp_type_bytes, &vstr));
	}
}

static void vnd_status_cli(struct bt_mesh_model *model, struct bt_mesh_msg_ctx *ctx, struct os_mbuf *buf)
{
	// ESP_LOGI(tag, "Acknownledgement from Vendor\n");
	// ESP_LOGI(tag, "cmd = %04x\n", net_buf_simple_pull_le16(buf));
	// ESP_LOGI(tag, "response = %08lx\n", net_buf_simple_pull_le32(buf));
}

void vnd_publish(struct bt_mesh_model *model)
{
	int err;
	struct os_mbuf *msg = model->pub->msg;
	struct vendor_state *state = model->user_data;

	if (model->pub->addr == BT_MESH_ADDR_UNASSIGNED) {
		return;
	}

	bt_mesh_model_msg_init(msg, BT_MESH_MODEL_OP_3(0x03, CID_RUNTIME));
	net_buf_simple_add_u8(msg, state->len);
	for(int i = 0; i < state->len; i++)
		net_buf_simple_add_u8(msg, state->data[i]);

	err = bt_mesh_model_publish(model);
	if (err) {
		ESP_LOGI(tag, "bt_mesh_model_publish err %d\n", err);
	}
}

/* Mapping of message handlers for Vendor (0x4321) */
static const struct bt_mesh_model_op vnd_srv_ops[] = {
	{ BT_MESH_MODEL_OP_3(0x01, CID_RUNTIME), 0, vnd_get_srv },
	{ BT_MESH_MODEL_OP_3(0x02, CID_RUNTIME), 3, vnd_set_srv },
	{ BT_MESH_MODEL_OP_3(0x03, CID_RUNTIME), 3, vnd_set_unack_srv },
	BT_MESH_MODEL_OP_END,
};

static const struct bt_mesh_model_op vnd_cli_ops[] = {
	{ BT_MESH_MODEL_OP_3(0x04, CID_RUNTIME), 6, vnd_status_cli },
	BT_MESH_MODEL_OP_END,
};

struct bt_mesh_model vnd_models[2] = {
	BT_MESH_MODEL_VND(CID_RUNTIME, 0x4321, vnd_srv_ops, &vnd_pub_srv, &vnd_user_data),
	BT_MESH_MODEL_VND(CID_RUNTIME, 0x4320, vnd_cli_ops, &vnd_pub_cli, &vnd_user_data),
};




