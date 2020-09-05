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

#ifndef _MODEL_LIGHT_H_
#define _MODEL_LIGHT_H_

struct light_state {
	u16_t light_linear; //measured light intensity
	u16_t light_temp;
	u16_t light_hue;
	u16_t light_saturation;
	u16_t light_actual;

	u8_t last_tid;
};

extern struct light_state light_user_data;

extern struct bt_mesh_model_pub light_lightness_srv_pub;
extern struct bt_mesh_model_pub light_lightness_cli_pub;
extern struct bt_mesh_model_pub light_ctl_srv_pub;
extern struct bt_mesh_model_pub light_ctl_cli_pub;
extern struct bt_mesh_model_pub light_hsl_srv_pub;
extern struct bt_mesh_model_pub light_hsl_cli_pub;

extern struct os_mbuf *bt_mesh_pub_msg_light_lightness_srv_pub;
extern struct os_mbuf *bt_mesh_pub_msg_light_lightness_cli_pub;
extern struct os_mbuf *bt_mesh_pub_msg_light_ctl_srv_pub;
extern struct os_mbuf *bt_mesh_pub_msg_light_ctl_cli_pub;
extern struct os_mbuf *bt_mesh_pub_msg_light_hsl_srv_pub;
extern struct os_mbuf *bt_mesh_pub_msg_light_hsl_cli_pub;

extern const struct bt_mesh_model_op light_lightness_srv_op[];
extern const struct bt_mesh_model_op light_lightness_cli_op[];
extern const struct bt_mesh_model_op light_ctl_srv_op[];
extern const struct bt_mesh_model_op light_ctl_cli_op[];
extern const struct bt_mesh_model_op light_hsl_srv_op[];
extern const struct bt_mesh_model_op light_hsl_cli_op[];

void light_lightness_publish(struct bt_mesh_model *model);
void light_ctl_publish(struct bt_mesh_model *model);
void light_hsl_publish(struct bt_mesh_model *model);

// void light_ctl_temp_publish(struct bt_mesh_model *model);

#endif // _MODEL_LIGHT_H_
