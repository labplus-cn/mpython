#ifndef MICROPY_INCLUDED_ESP32_MODMOTION_H
#define MICROPY_INCLUDED_ESP32_MODMOTION_H

#include "py/obj.h"

int esp32_i2c_write(unsigned char slave_addr, unsigned char reg_addr, unsigned char length, unsigned char *data);
int esp32_i2c_read(unsigned char slave_addr, unsigned char reg_addr, unsigned char length, unsigned char *data);


#endif // MICROPY_INCLUDED_ESP32_MODMOTION_H