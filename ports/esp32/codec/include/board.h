/*
 * board.h
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#ifndef _BOARD_H_
#define _BOARD_H_

#ifdef __cplusplus
extern "C" {
#endif

/* Press button related */
#define GPIO_SEL_REC                GPIO_SEL_36    //SENSOR_VP
#define GPIO_SEL_MODE               GPIO_SEL_39    //SENSOR_VN
#define GPIO_REC                    GPIO_NUM_36
#define GPIO_MODE                   GPIO_NUM_39 

#define I2S_NUM         (0)

#ifdef __cplusplus
}
#endif

#endif
