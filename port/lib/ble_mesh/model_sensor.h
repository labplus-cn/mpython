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

#ifndef _MODEL_SENSOR_H_
#define _MODEL_SENSOR_H_

struct sensor_descriptor_state {
	u16_t propertyID; //measured sensor intensity
	u16_t tolerance1;
	u16_t tolerance2;
	u16_t period;
	u16_t update_interval;
};

struct sensor_setup_state {
	u16_t sensor_linear; //measured sensor intensity
	u16_t sensor_temp;
	u16_t sensor_hue;
	u16_t sensor_saturation;
	u16_t sensor_actual;

	u8_t last_tid;
};

extern struct sensor_state sensor_user_data;
extern struct sensor_setup_state sensor_setup_user_data;

extern struct bt_mesh_model_pub sensor_srv_pub;
extern struct bt_mesh_model_pub sensor_cli_pub;
extern struct bt_mesh_model_pub sensor_setup_srv_pub;

extern struct os_mbuf *bt_mesh_pub_msg_sensor_srv_pub;
extern struct os_mbuf *bt_mesh_pub_msg_sensor_cli_pub;
extern struct os_mbuf *bt_mesh_pub_msg_sensor_setup_srv_pub;

extern const struct bt_mesh_model_op sensor_srv_op[];
extern const struct bt_mesh_model_op sensor_cli_op[];
extern const struct bt_mesh_model_op sensor_setup_srv_op[];

void sensor_publish(struct bt_mesh_model *model);
// void sensor_publish(struct bt_mesh_model *model);
// void sensor_publish(struct bt_mesh_model *model);

// void sensor_ctl_temp_publish(struct bt_mesh_model *model);

#endif // _MODEL_sensor_H_
