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
#ifndef __SYS_CONFIG_H_
#define __SYS_CONFIG_H_

/**
 * @addtogroup SysConfig Configuration of Apache Mynewt System
 * @{
 */

#include <os/queue.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Load configuration from registered persistence sources. Handlers for
 * configuration subtrees registered earlier will be called for encountered
 * values.
 *
 * @return 0 on success, non-zero on failure.
 */
int conf_load(void);

/**
 * Write a single configuration value to persisted storage (if it has
 * changed value).
 *
 * @param name Name/key of the configuration item.
 * @param var Value of the configuration item.
 *
 * @return 0 on success, non-zero on failure.
 */
int conf_save_one(const char *name, char *var);

void bt_mesh_settings_init(void);
int bt_mesh_settings_deinit(void);
#ifdef __cplusplus
}
#endif
#endif /* __SYS_CONFIG_H_ */