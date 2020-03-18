#include "modmotion.h"
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/runtime.h"
#include "extmod/machine_i2c.h"
#include "esp_log.h"

#include "inv_mpu.h"
#include "inv_mpu_dmp_motion_driver.h"
#include "invensense.h"
// #include "invensense_adv.h"
#include "eMPL_outputs.h"
#include "mltypes.h"
#include "mpu.h"
#include "log.h"
#include "packet.h"
#include "accel_auto_cal.h"
#include "compass_vec_cal.h"
#include "fast_no_motion.h"
#include "fusion_9axis.h"
#include "gyro_tc.h"
#include "heading_from_gyro.h"
#include "mag_disturb.h"
#include "motion_no_motion.h"
#include "no_gyro_fusion.h"
#include "quaternion_supervisor.h"
#include "mag_disturb.h"
#include "results_holder.h"

static const char *TAG = "MPU6050";
#define MPU6050_ADDR 104 
#define MPU6050 1
#define get_tick_count(x) *x=mp_hal_ticks_ms()

/* Private typedef -----------------------------------------------------------*/
/* Data read from MPL. */
#define PRINT_ACCEL     (0x01)
#define PRINT_GYRO      (0x02)
#define PRINT_QUAT      (0x04)
#define PRINT_COMPASS   (0x08)
#define PRINT_EULER     (0x10)
#define PRINT_ROT_MAT   (0x20)
#define PRINT_HEADING   (0x40)
#define PRINT_PEDO      (0x80)
#define PRINT_LINEAR_ACCEL (0x100)
#define PRINT_GRAVITY_VECTOR (0x200)

volatile uint32_t hal_timestamp = 0;
#define ACCEL_ON        (0x01)
#define GYRO_ON         (0x02)
#define COMPASS_ON      (0x04)

#define MOTION          (0)
#define NO_MOTION       (1)

/* Starting sampling rate. */
#define DEFAULT_MPU_HZ  (20)

#define FLASH_SIZE      (512)
#define FLASH_MEM_START ((void*)0x1800)

#define PEDO_READ_MS    (1000)
#define TEMP_READ_MS    (500)
#define COMPASS_READ_MS (100)

mp_obj_base_t *i2c_obj = NULL;
struct int_param_s int_param;
unsigned char new_temp = 0;

struct rx_s {
    unsigned char header[3];
    unsigned char cmd;
};
struct hal_s {
    unsigned char lp_accel_mode;
    unsigned char sensors;
    unsigned char dmp_on;
    unsigned char wait_for_tap;
    volatile unsigned char new_gyro;
    unsigned char motion_int_mode;
    unsigned long no_dmp_hz;
    unsigned long next_pedo_ms;
    unsigned long next_temp_ms;
    unsigned long next_compass_ms;
    unsigned int report;
    unsigned short dmp_features;
    struct rx_s rx;
};
static struct hal_s hal = {0};

volatile unsigned char rx_new;

unsigned char *mpl_key = (unsigned char*)"eMPL 5.1";

/* Platform-specific information. Kinda like a boardfile. */
struct platform_data_s {
    signed char orientation[9];
};

/* The sensors can be mounted onto the board in any orientation. The mounting
 * matrix seen below tells the MPL how to rotate the raw data from the
 * driver(s).
 * TODO: The following matrices refer to the configuration on internal test
 * boards at Invensense. If needed, please modify the matrices to match the
 * chip-to-body matrix for your particular set up.
 */
static struct platform_data_s gyro_pdata = {
    .orientation = { 1, 0, 0,
                     0, 1, 0,
                     0, 0, 1}
};

#if defined MPU9150 || defined MPU9250
static struct platform_data_s compass_pdata = {
    .orientation = { 0, 1, 0,
                     1, 0, 0,
                     0, 0, -1}
};
#define COMPASS_ENABLED 1
#elif defined AK8975_SECONDARY
static struct platform_data_s compass_pdata = {
    .orientation = {-1, 0, 0,
                     0, 1, 0,
                     0, 0,-1}
};
#define COMPASS_ENABLED 1
#elif defined AK8963_SECONDARY
static struct platform_data_s compass_pdata = {
    .orientation = {-1, 0, 0,
                     0,-1, 0,
                     0, 0, 1}
};
#define COMPASS_ENABLED 1
#endif

#ifdef COMPASS_ENABLED
void send_status_compass() {
	long data[3] = { 0 };
	int8_t accuracy = { 0 };
	unsigned long timestamp;
	inv_get_compass_set(data, &accuracy, (inv_time_t*) &timestamp);
	MPL_LOGI("Compass: %7.4f %7.4f %7.4f ",
			data[0]/65536.f, data[1]/65536.f, data[2]/65536.f);
	MPL_LOGI("Accuracy= %d\r\n", accuracy);

}
#endif

/* Handle sensor on/off combinations. */
static void setup_gyro(void)
{
    unsigned char mask = 0, lp_accel_was_on = 0;
    if (hal.sensors & ACCEL_ON)
        mask |= INV_XYZ_ACCEL;
    if (hal.sensors & GYRO_ON) {
        mask |= INV_XYZ_GYRO;
        lp_accel_was_on |= hal.lp_accel_mode;
    }
#ifdef COMPASS_ENABLED
    if (hal.sensors & COMPASS_ON) {
        mask |= INV_XYZ_COMPASS;
        lp_accel_was_on |= hal.lp_accel_mode;
    }
#endif
    /* If you need a power transition, this function should be called with a
     * mask of the sensors still enabled. The driver turns off any sensors
     * excluded from this mask.
     */
    mpu_set_sensors(mask);
    mpu_configure_fifo(mask);
    if (lp_accel_was_on) {
        unsigned short rate;
        hal.lp_accel_mode = 0;
        /* Switching out of LP accel, notify MPL of new accel sampling rate. */
        mpu_get_sample_rate(&rate);
        inv_set_accel_sample_rate(1000000L / rate);
    }
}

static void tap_cb(unsigned char direction, unsigned char count)
{
    switch (direction) {
    case TAP_X_UP:
        MPL_LOGI("Tap X+ ");
        break;
    case TAP_X_DOWN:
        MPL_LOGI("Tap X- ");
        break;
    case TAP_Y_UP:
        MPL_LOGI("Tap Y+ ");
        break;
    case TAP_Y_DOWN:
        MPL_LOGI("Tap Y- ");
        break;
    case TAP_Z_UP:
        MPL_LOGI("Tap Z+ ");
        break;
    case TAP_Z_DOWN:
        MPL_LOGI("Tap Z- ");
        break;
    default:
        return;
    }
    MPL_LOGI("x%d\n", count);
    return;
}

static void android_orient_cb(unsigned char orientation)
{
	switch (orientation) {
	case ANDROID_ORIENT_PORTRAIT:
        MPL_LOGI("Portrait\n");
        break;
	case ANDROID_ORIENT_LANDSCAPE:
        MPL_LOGI("Landscape\n");
        break;
	case ANDROID_ORIENT_REVERSE_PORTRAIT:
        MPL_LOGI("Reverse Portrait\n");
        break;
	case ANDROID_ORIENT_REVERSE_LANDSCAPE:
        MPL_LOGI("Reverse Landscape\n");
        break;
	default:
		return;
	}
}


static inline void run_self_test(void)
{
    int result;
    long gyro[3], accel[3];

#if defined (MPU6500) || defined (MPU9250)
    result = mpu_run_6500_self_test(gyro, accel, 0);
#elif defined (MPU6050) || defined (MPU9150)
    result = mpu_run_self_test(gyro, accel);
#endif
    if (result == 0x7) {
	MPL_LOGI("Passed!\n");
        MPL_LOGI("accel: %7.4f %7.4f %7.4f\n",
                    accel[0]/65536.f,
                    accel[1]/65536.f,
                    accel[2]/65536.f);
        MPL_LOGI("gyro: %7.4f %7.4f %7.4f\n",
                    gyro[0]/65536.f,
                    gyro[1]/65536.f,
                    gyro[2]/65536.f);
        /* Test passed. We can trust the gyro data here, so now we need to update calibrated data*/

#ifdef USE_CAL_HW_REGISTERS
        /*
         * This portion of the code uses the HW offset registers that are in the MPUxxxx devices
         * instead of pushing the cal data to the MPL software library
         */
        unsigned char i = 0;

        for(i = 0; i<3; i++) {
        	gyro[i] = (long)(gyro[i] * 32.8f); //convert to +-1000dps
        	accel[i] *= 2048.f; //convert to +-16G
        	accel[i] = accel[i] >> 16;
        	gyro[i] = (long)(gyro[i] >> 16);
        }

        mpu_set_gyro_bias_reg(gyro);

#if defined (MPU6500) || defined (MPU9250)
        mpu_set_accel_bias_6500_reg(accel);
#elif defined (MPU6050) || defined (MPU9150)
        mpu_set_accel_bias_6050_reg(accel);
#endif
#else
        /* Push the calibrated data to the MPL library.
         *
         * MPL expects biases in hardware units << 16, but self test returns
		 * biases in g's << 16.
		 */
    	unsigned short accel_sens;
    	float gyro_sens;

		mpu_get_accel_sens(&accel_sens);
		accel[0] *= accel_sens;
		accel[1] *= accel_sens;
		accel[2] *= accel_sens;
		inv_set_accel_bias(accel, 3);
		mpu_get_gyro_sens(&gyro_sens);
		gyro[0] = (long) (gyro[0] * gyro_sens);
		gyro[1] = (long) (gyro[1] * gyro_sens);
		gyro[2] = (long) (gyro[2] * gyro_sens);
		inv_set_gyro_bias(gyro, 3);
#endif
    }
    else {
            if (!(result & 0x1))
                MPL_LOGE("Gyro failed.\n");
            if (!(result & 0x2))
                MPL_LOGE("Accel failed.\n");
            if (!(result & 0x4))
                MPL_LOGE("Compass failed.\n");
     }

}

/* Every time new gyro data is available, this function is called in an
 * ISR context. In this example, it sets a flag protecting the FIFO read
 * function.
 * 中断响应回调函数
 */
void gyro_data_ready_cb(void)
{
    hal.new_gyro = 1;    //置位一个标志，通知应用可读FIFO
}

STATIC void mpu6050_read_fifo(void)
{
    unsigned long sensor_timestamp;
    int new_data = 0;
    long quat[4];
    unsigned long timestamp;

    get_tick_count(&timestamp);

    /* Temperature data doesn't need to be read with every gyro sample.
    * Let's make them timer-based like the compass reads.
    */
    if (timestamp > hal.next_temp_ms) {
        hal.next_temp_ms = timestamp + TEMP_READ_MS;
        new_temp = 1;
    }

    if (hal.new_gyro && hal.dmp_on) {
        short gyro[3], accel_short[3], sensors;
        unsigned char more;
        long accel[3], temperature;
        sensors = (INV_XYZ_ACCEL | INV_XYZ_GYRO | INV_WXYZ_QUAT);
        /* This function gets new data from the FIFO when the DMP is in
            * use. The FIFO can contain any combination of gyro, accel,
            * quaternion, and gesture data. The sensors parameter tells the
            * caller which data fields were actually populated with new data.
            * For example, if sensors == (INV_XYZ_GYRO | INV_WXYZ_QUAT), then
            * the FIFO isn't being filled with accel data.
            * The driver parses the gesture data to determine if a gesture
            * event has occurred; on an event, the application will be notified
            * via a callback (assuming that a callback function was properly
            * registered). The more parameter is non-zero if there are
            * leftover packets in the FIFO.
            */
        dmp_read_fifo(gyro, accel_short, quat, &sensor_timestamp, &sensors, &more);
        // if (!more)
        //     hal.new_gyro = 0;
        if (sensors & INV_XYZ_GYRO) {
            /* Push the new data to the MPL. */
            inv_build_gyro(gyro, sensor_timestamp);
            new_data = 1;

            if (new_temp) {
                new_temp = 0;
                /* Temperature only used for gyro temp comp. */
                mpu_get_temperature(&temperature, &sensor_timestamp);
                inv_build_temp(temperature, sensor_timestamp);
            }
        }
        if (sensors & INV_XYZ_ACCEL) {
            accel[0] = (long)accel_short[0];
            accel[1] = (long)accel_short[1];
            accel[2] = (long)accel_short[2];
            inv_build_accel(accel, 0, sensor_timestamp);
            new_data = 1;
        }
        if (sensors & INV_WXYZ_QUAT) {
            inv_build_quat(quat, 0, sensor_timestamp);
            new_data = 1;
        }
    } 
    if (new_data) {
        inv_store_gaming_quaternion(quat, timestamp);
        inv_execute_on_data();
    }
}

int esp32_i2c_write(unsigned char slave_addr, unsigned char reg_addr, unsigned char len, unsigned char *data)
{
    mp_machine_i2c_p_t *i2c_p = (mp_machine_i2c_p_t*)i2c_obj->type->protocol;
    uint8_t temp[len+1];
    temp[0] = (uint8_t)reg_addr;
    for(int i = 0; i < len; i++)
        temp[i+1] = data[i];
    // int ret = i2c_p->writeto(i2c_obj, MPU6050_ADDR,  (const uint8_t *)temp, length+1, true);
    // if (ret < 0) {
    //     mp_raise_OSError(-ret);
    // }
    // return 0;
    mp_machine_i2c_buf_t buf = {.len = len+1, .buf = (uint8_t*)temp};
    bool stop = true;
    unsigned int flags = stop ? MP_MACHINE_I2C_FLAG_STOP : 0;
    int ret = i2c_p->transfer((mp_obj_base_t *)i2c_obj, MPU6050_ADDR, 1, &buf, flags);
    if (ret < 0) {
        mp_raise_OSError(-ret);
    }
    return 0;
}

int esp32_i2c_read(unsigned char slave_addr, unsigned char reg_addr, unsigned char len, unsigned char *dest)
{
    mp_machine_i2c_p_t *i2c_p = (mp_machine_i2c_p_t*)i2c_obj->type->protocol;


    uint8_t _reg_addr = reg_addr;
    // int ret = i2c_p->writeto(i2c_obj, MPU6050_ADDR,  (const uint8_t *)&_reg_addr, 1, false);
    // if (ret < 0) {
    //     mp_raise_OSError(-ret);
    // }
    mp_machine_i2c_buf_t buf = {.len = 1, .buf = (uint8_t*)&_reg_addr};
    bool stop = false;
    unsigned int flags = stop ? MP_MACHINE_I2C_FLAG_STOP : 0;
    int ret = i2c_p->transfer((mp_obj_base_t *)i2c_obj, MPU6050_ADDR, 1, &buf, flags);
    if (ret < 0) {
        mp_raise_OSError(-ret);
    }

    // ret = i2c_p->readfrom(i2c_obj, MPU6050_ADDR, (uint8_t*)data, length, true);
    // if (ret < 0) {
    //     mp_raise_OSError(-ret);
    // }

    // return 0;

    buf.len = len;
    buf.buf = dest;
    stop = true;
    flags = MP_MACHINE_I2C_FLAG_READ | (stop ? MP_MACHINE_I2C_FLAG_STOP : 0);
    ret = i2c_p->transfer((mp_obj_base_t *)i2c_obj, MPU6050_ADDR, 1, &buf, flags);
    if (ret < 0) {
        mp_raise_OSError(-ret);
    }

    return 0;
}

/*
STATIC int mp_machine_i2c_readfrom(mp_obj_base_t *self, uint16_t addr, uint8_t *dest, size_t len, bool stop) {
    mp_machine_i2c_p_t *i2c_p = (mp_machine_i2c_p_t*)self->type->protocol;
    mp_machine_i2c_buf_t buf = {.len = len, .buf = dest};
    unsigned int flags = MP_MACHINE_I2C_FLAG_READ | (stop ? MP_MACHINE_I2C_FLAG_STOP : 0);
    return i2c_p->transfer(self, addr, 1, &buf, flags);
}

STATIC int mp_machine_i2c_writeto(mp_obj_base_t *self, uint16_t addr, const uint8_t *src, size_t len, bool stop) {
    mp_machine_i2c_p_t *i2c_p = (mp_machine_i2c_p_t*)self->type->protocol;
    mp_machine_i2c_buf_t buf = {.len = len, .buf = (uint8_t*)src};
    unsigned int flags = stop ? MP_MACHINE_I2C_FLAG_STOP : 0;
    return i2c_p->transfer(self, addr, 1, &buf, flags);
} */

STATIC mp_obj_t mpu6050_init(mp_obj_t i2c) {
    inv_error_t result;

    unsigned char accel_fsr;
    unsigned short gyro_rate, gyro_fsr;
    unsigned long timestamp;
    struct int_param_s int_param;

    i2c_obj = MP_OBJ_TO_PTR(i2c);

    hal.sensors |= ACCEL_ON;
    setup_gyro();
    hal.new_gyro = 1;  //无中为引脚，人为置位标志，可读FIFO
    hal.lp_accel_mode = 0;
    hal.report = PRINT_QUAT | PRINT_ACCEL;

    /* 1 mpu_init()底层驱𩅏初始化 */
    result = mpu_init(&int_param);
    if (result) {
        ESP_LOGE(TAG, "Could not initialize gyro.\n");
    }

    /* 2 inv_init_mpl() mllite库初始化 */
    result = inv_init_mpl();
    if (result) {
        ESP_LOGE(TAG, "Could not initialize MPL.\n");
    }

    /* 3 inv_enable_eMPL_outputs() 使能eMPL_hal层面的输出 */
    /* If you need to estimate your heading before the compass is calibrated,
     * enable this algorithm. It becomes useless after a good figure-eight is
     * detected, so we'll just leave it out to save memory.
     * inv_enable_heading_from_gyro();
     */

    /* Allows use of the MPL APIs in read_from_mpl. */
    inv_enable_eMPL_outputs();

  /* 3 inv_start_mpl() 启动mllite层 */
  result = inv_start_mpl();
  if (result == INV_ERROR_NOT_AUTHORIZED) {
      while (1) {
          ESP_LOGE(TAG, "Not authorized.\n");
      }
  }
  if (result) {
      ESP_LOGE(TAG, "Could not start the MPL.\n");
  }

  /* 4 硬件配置 */
    /* Get/set hardware configuration. Start gyro. */
    /* Wake up all sensors. */
#ifdef COMPASS_ENABLED
    mpu_set_sensors(INV_XYZ_GYRO | INV_XYZ_ACCEL | INV_XYZ_COMPASS);
#else
    mpu_set_sensors(INV_XYZ_GYRO | INV_XYZ_ACCEL);
#endif
    /* Push both gyro and accel data into the FIFO. */
    mpu_configure_fifo(INV_XYZ_GYRO | INV_XYZ_ACCEL);
    mpu_set_sample_rate(DEFAULT_MPU_HZ);
#ifdef COMPASS_ENABLED
    /* The compass sampling rate can be less than the gyro/accel sampling rate.
     * Use this function for proper power management.
     */
    mpu_set_compass_sample_rate(1000 / COMPASS_READ_MS);
#endif
    /* Read back configuration in case it was set improperly. */
    mpu_get_sample_rate(&gyro_rate);
    mpu_get_gyro_fsr(&gyro_fsr);
    mpu_get_accel_fsr(&accel_fsr);
#ifdef COMPASS_ENABLED
    mpu_get_compass_fsr(&compass_fsr);
#endif
    /* Sync driver configuration with MPL. */
    /* Sample rate expected in microseconds. */
    inv_set_gyro_sample_rate(1000000L / gyro_rate);
    inv_set_accel_sample_rate(1000000L / gyro_rate);
#ifdef COMPASS_ENABLED
    /* The compass rate is independent of the gyro and accel rates. As long as
     * inv_set_compass_sample_rate is called with the correct value, the 9-axis
     * fusion algorithm's compass correction gain will work properly.
     */
    inv_set_compass_sample_rate(COMPASS_READ_MS * 1000L);
#endif
    /* Set chip-to-body orientation matrix.
     * Set hardware units to dps/g's/degrees scaling factor.
     */
    inv_set_gyro_orientation_and_scale(
            inv_orientation_matrix_to_scalar(gyro_pdata.orientation),
            (long)gyro_fsr<<15);
    inv_set_accel_orientation_and_scale(
            inv_orientation_matrix_to_scalar(gyro_pdata.orientation),
            (long)accel_fsr<<15);
#ifdef COMPASS_ENABLED
    inv_set_compass_orientation_and_scale(
            inv_orientation_matrix_to_scalar(compass_pdata.orientation),
            (long)compass_fsr<<15);
#endif
    /* Initialize HAL state variables. */
#ifdef COMPASS_ENABLED
    hal.sensors = ACCEL_ON | GYRO_ON | COMPASS_ON;
#else
    hal.sensors = ACCEL_ON | GYRO_ON;
#endif
    hal.dmp_on = 0;
    hal.report = 0;
    hal.rx.cmd = 0;
    hal.next_pedo_ms = 0;
    hal.next_compass_ms = 0;
    hal.next_temp_ms = 0;

  /* Compass reads are handled by scheduler. */
    get_tick_count(&timestamp);

     /* 5 配置DMP */
    dmp_load_motion_driver_firmware();
    dmp_set_orientation(
        inv_orientation_matrix_to_scalar(gyro_pdata.orientation));
    dmp_register_tap_cb(tap_cb);
    dmp_register_android_orient_cb(android_orient_cb);
    /*
     * Known Bug -
     * DMP when enabled will sample sensor data at 200Hz and output to FIFO at the rate
     * specified in the dmp_set_fifo_rate API. The DMP will then sent an interrupt once
     * a sample has been put into the FIFO. Therefore if the dmp_set_fifo_rate is at 25Hz
     * there will be a 25Hz interrupt from the MPU device.
     *
     * There is a known issue in which if you do not enable DMP_FEATURE_TAP
     * then the interrupts will be at 200Hz even if fifo rate
     * is set at a different rate. To avoid this issue include the DMP_FEATURE_TAP
     *
     * DMP sensor fusion works only with gyro at +-2000dps and accel +-2G
     */
    hal.dmp_features = DMP_FEATURE_6X_LP_QUAT | DMP_FEATURE_TAP |
        DMP_FEATURE_ANDROID_ORIENT | DMP_FEATURE_SEND_RAW_ACCEL | DMP_FEATURE_SEND_CAL_GYRO |
        DMP_FEATURE_GYRO_CAL;
    dmp_enable_feature(hal.dmp_features);
    dmp_set_fifo_rate(DEFAULT_MPU_HZ);
    run_self_test();
    mpu_set_dmp_state(1); //使能DMP
    hal.dmp_on = 1;

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mpu6050_init_obj, mpu6050_init);

STATIC mp_obj_t mpu6050_accel() {
    long data[9];
    int8_t accuracy;
    unsigned long timestamp;

    mpu6050_read_fifo();
    if (inv_get_sensor_type_accel(data, &accuracy, (inv_time_t*)&timestamp))
    {
      // ESP_LOGE(TAG, "%ld, %ld, %ld", data[0], data[1], data[2]); 
        mp_obj_t tuple[3] = {
            tuple[0] = mp_obj_new_int(data[0]),
            tuple[1] = mp_obj_new_int(data[1]),
            tuple[2] = mp_obj_new_int(data[2]),
        };
        return mp_obj_new_tuple(3, tuple);
    }
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mpu6050_accel_obj, mpu6050_accel);

STATIC mp_obj_t mpu6050_gyro() {
    long data[9];
    int8_t accuracy;
    unsigned long timestamp;

    mpu6050_read_fifo();
    if (inv_get_sensor_type_gyro(data, &accuracy, (inv_time_t*)&timestamp))
    {
         mp_obj_t tuple[3] = {
            tuple[0] = mp_obj_new_int(data[0]),
            tuple[1] = mp_obj_new_int(data[1]),
            tuple[2] = mp_obj_new_int(data[2]),
        };
        return mp_obj_new_tuple(3, tuple);       
    }
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mpu6050_gyro_obj, mpu6050_gyro);

STATIC mp_obj_t mpu6050_compass() {
    mpu6050_read_fifo();

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mpu6050_compass_obj, mpu6050_compass);

STATIC mp_obj_t mpu6050_quat() {
    long data[9];
    int8_t accuracy;
    unsigned long timestamp;
    // float float_data[3] = {0};

    mpu6050_read_fifo();

    if (inv_get_sensor_type_quat(data, &accuracy, (inv_time_t*)&timestamp)) {
        // ESP_LOGE(TAG, "%ld, %ld, %ld, %ld", data[0], data[1], data[2], data[3]);
        mp_obj_t tuple[4] = {
            tuple[0] = mp_obj_new_int(data[0]),
            tuple[1] = mp_obj_new_int(data[1]),
            tuple[2] = mp_obj_new_int(data[2]),
            tuple[3] = mp_obj_new_int(data[3]),
        };
        return mp_obj_new_tuple(4, tuple);
    }
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mpu6050_quat_obj, mpu6050_quat);

STATIC mp_obj_t mpu6050_euler() {
    long data[9];
    int8_t accuracy;
    unsigned long timestamp;

    mpu6050_read_fifo();
    if (inv_get_sensor_type_euler(data, &accuracy, (inv_time_t*)&timestamp))
    {
         mp_obj_t tuple[3] = {
            tuple[0] = mp_obj_new_int(data[0]),
            tuple[1] = mp_obj_new_int(data[1]),
            tuple[2] = mp_obj_new_int(data[2]),
        };
        return mp_obj_new_tuple(3, tuple);         
    }
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mpu6050_euler_obj, mpu6050_euler);

STATIC mp_obj_t mpu6050_rot_mat() {
    long data[9];
    int8_t accuracy;
    unsigned long timestamp;

    mpu6050_read_fifo();
    if (inv_get_sensor_type_rot_mat(data, &accuracy, (inv_time_t*)&timestamp))
    {
         mp_obj_t tuple[3] = {
            tuple[0] = mp_obj_new_int(data[0]),
            tuple[1] = mp_obj_new_int(data[1]),
            tuple[2] = mp_obj_new_int(data[2]),
        };
        return mp_obj_new_tuple(3, tuple);          
    }
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mpu6050_rot_mat_obj, mpu6050_rot_mat);

STATIC mp_obj_t mpu6050_heading() {
    long data[9];
    int8_t accuracy;
    unsigned long timestamp;

    mpu6050_read_fifo();
    if (inv_get_sensor_type_heading(data, &accuracy, (inv_time_t*)&timestamp))
    {
        return mp_obj_new_int(data[0]);
    }
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mpu6050_heading_obj, mpu6050_heading);

STATIC const mp_map_elem_t mpython_mpu6050_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_mpu6050)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_init), (mp_obj_t)&mpu6050_init_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_accel), (mp_obj_t)&mpu6050_accel_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_gyro), (mp_obj_t)&mpu6050_gyro_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_compass), (mp_obj_t)&mpu6050_compass_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_quat), (mp_obj_t)&mpu6050_quat_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_euler), (mp_obj_t)&mpu6050_euler_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_rot_mat), (mp_obj_t)&mpu6050_rot_mat_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_heading), (mp_obj_t)&mpu6050_heading_obj},
};

STATIC MP_DEFINE_CONST_DICT(mpython_mpu6050_locals_dict, mpython_mpu6050_locals_dict_table);

const mp_obj_module_t mp_module_motion = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mpython_mpu6050_locals_dict,
};