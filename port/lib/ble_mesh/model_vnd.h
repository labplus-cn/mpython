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

#ifndef _MODEL_VND_H_
#define _MODEL_VND_H_

#define CID_RUNTIME 0x05C3

#define STATE_OFF	0x00
#define STATE_ON	0x01
#define STATE_DEFAULT	0x01
#define STATE_RESTORE	0x02

struct vendor_state {
	int current;
	u32_t response;
	u8_t last_tid;
	u16_t last_src_addr;
	u16_t last_dst_addr;
	u8_t len;
	u8_t data[16];
};


extern struct vendor_state vnd_user_data;
extern struct bt_mesh_model_pub vnd_pub_srv;
extern struct bt_mesh_model_pub vnd_pub_cli;
extern struct os_mbuf *bt_mesh_pub_msg_vnd_pub;
// extern struct os_mbuf *bt_mesh_pub_msg_vnd_pub_cli;
extern struct bt_mesh_model vnd_models[2];

void vnd_publish(struct bt_mesh_model *model);

#endif //_MODEL_VND_H_
