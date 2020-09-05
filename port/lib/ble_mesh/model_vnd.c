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
#include "model_vnd.h"

static const char *tag = "model_vnd";

struct bt_mesh_model_pub vnd_pub;
struct os_mbuf *bt_mesh_pub_msg_vnd_pub;

/* Definitions of models user data (Start) */
struct vendor_state vnd_user_data;
/* Definitions of models user data (End) */

/* message handlers (Start) */
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

	// now = k_uptime_get();
	// if (state->last_tid == tid &&
	//     state->last_src_addr == ctx->addr &&
	//     state->last_dst_addr == ctx->recv_dst &&
	//     (now - state->last_msg_timestamp <= K_SECONDS(6))) {
	// 	return;
	// }

	state->last_tid = tid;
	state->last_src_addr = ctx->addr;
	state->last_dst_addr = ctx->recv_dst;
	// state->last_msg_timestamp = now;
	state->current = current;

	ESP_LOGI(tag, "Vendor model message = %04x\n", state->current);
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
	// ESP_LOGI(tag, "response = %08lx\n", net_buf_simple_pull_le32(buf));
}

/* Mapping of message handlers for Vendor (0x4321) */
static const struct bt_mesh_model_op vnd_ops[] = {
	{ BT_MESH_MODEL_OP_3(0x01, CID_RUNTIME), 0, vnd_get },
	{ BT_MESH_MODEL_OP_3(0x02, CID_RUNTIME), 3, vnd_set },
	{ BT_MESH_MODEL_OP_3(0x03, CID_RUNTIME), 3, vnd_set_unack },
	{ BT_MESH_MODEL_OP_3(0x04, CID_RUNTIME), 6, vnd_status },
	BT_MESH_MODEL_OP_END,
};

struct bt_mesh_model vnd_models[1] = {
	BT_MESH_MODEL_VND(CID_RUNTIME, 0x4321, vnd_ops, &vnd_pub, &vnd_user_data),
};




