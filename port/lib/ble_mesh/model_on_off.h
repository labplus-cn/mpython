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

#ifndef _MODEL_ON_OFF_H_
#define _MODEL_ON_OFF_H_

struct generic_onoff_state {
	u8_t onoff;
	u8_t target_onoff;

	u8_t last_tid;
	u16_t last_src_addr;
	u16_t last_dst_addr;
};

extern struct generic_onoff_state gen_onoff_srv_root_user_data;
extern struct bt_mesh_model_pub gen_onoff_srv_pub_root;
extern struct bt_mesh_model_pub gen_onoff_cli_pub_root; 
extern struct os_mbuf *bt_mesh_pub_msg_gen_onoff_srv_pub_root;
extern struct os_mbuf *bt_mesh_pub_msg_gen_onoff_cli_pub_root;

extern const struct bt_mesh_model_op gen_onoff_srv_op[];
extern const struct bt_mesh_model_op gen_onoff_cli_op[];

void gen_onoff_publish(struct bt_mesh_model *model);
#endif // end _MODEL_ON_OFF_H_
