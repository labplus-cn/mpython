#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "py/mperrno.h"
#include "py/mphal.h"
#include "py/runtime.h"
#include "extmod/machine_i2c.h"
#include "esp_log.h"
#include "mfrc522.h"

#define MFRC522_ADDR (47) 
#define MAX_LEN (16)
// static const char *TAG = "RFID";
static mp_obj_base_t *i2c_obj = NULL;
//原扇区A密码，16个扇区，每个扇区密码6Byte
static uint8_t sectorKeyA[16][6] = {
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF },
		{ 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF }, };

STATIC mp_obj_t mfrc522_init(mp_obj_t i2c) {
    if(!i2c_obj)
        i2c_obj = (mp_obj_base_t *)MP_OBJ_TO_PTR(i2c);
    RFID_init();
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mfrc522_init_obj, mfrc522_init);

STATIC mp_obj_t mfrc522_find_card(void) {
    unsigned char str[MAX_LEN];

	if (RFID_findCard(PICC_REQIDL, str) == MI_OK)
	{
        return MP_OBJ_NEW_SMALL_INT(str[0] + (((uint16_t)str[1]) << 8));   
	}

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mfrc522_find_card_obj, mfrc522_find_card);

STATIC mp_obj_t mfrc522_anticoll(void) {
    unsigned char str[MAX_LEN];
    // uint8_t serNum[5];       // 4字节卡序列号，第5字节为校验字节

	if (RFID_anticoll(str) == MI_OK)
	{
        mp_obj_t serNum[5] = {
            serNum[0] = mp_obj_new_int(str[0]),
            serNum[1] = mp_obj_new_int(str[1]),
            serNum[2] = mp_obj_new_int(str[2]),
            serNum[3] = mp_obj_new_int(str[3]),
            serNum[4] = mp_obj_new_int(str[4]),
        };
        return mp_obj_new_tuple(5, serNum);   
	}
    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mfrc522_anticoll_obj, mfrc522_anticoll);

STATIC mp_obj_t mfrc522_select_tag(mp_obj_t serialNum) {
    // unsigned char str[MAX_LEN];
    uint8_t serNum[5];       // 4字节卡序列号，第5字节为校验字节
    mp_obj_t *elem;\
    uint16_t size;

    mp_obj_get_array_fixed_n(serialNum, 5, &elem);
    serNum[0] = mp_obj_get_int(elem[0]);
    serNum[1] = mp_obj_get_int(elem[1]);
    serNum[2] = mp_obj_get_int(elem[2]);
    serNum[3] = mp_obj_get_int(elem[3]);
    serNum[4] = mp_obj_get_int(elem[4]);

    size = RFID_selectTag(serNum);
	if (size > 0)
        return MP_OBJ_NEW_SMALL_INT(size);   

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mfrc522_select_tag_obj, mfrc522_select_tag);

STATIC mp_obj_t mfrc522_auth(mp_obj_t serialNum, mp_obj_t block) {
    uint8_t serNum[5];       // 4字节卡序列号，第5字节为校验字节
    mp_obj_t *elem;
    int _block = mp_obj_get_int(block);

    mp_obj_get_array_fixed_n(serialNum, 5, &elem);
    serNum[0] = mp_obj_get_int(elem[0]);
    serNum[1] = mp_obj_get_int(elem[1]);
    serNum[2] = mp_obj_get_int(elem[2]);
    serNum[3] = mp_obj_get_int(elem[3]);
    serNum[4] = mp_obj_get_int(elem[4]);

    if (RFID_auth(PICC_AUTHENT1A, _block, sectorKeyA[_block / 4], serNum) == MI_OK) //卡认证
        return MP_OBJ_NEW_SMALL_INT(1);   

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(mfrc522_auth_obj, mfrc522_auth);

/* 以下所有操作须先完成寻卡及卡密验证工作先*/
STATIC mp_obj_t mfrc522_read_block(mp_obj_t block) {
    int _block = mp_obj_get_int(block);
    vstr_t vstr;
    vstr_init_len(&vstr, 16);
    if (RFID_readBlock(_block, (uint8_t*)vstr.buf) == MI_OK)
        return mp_obj_new_str_from_vstr(&mp_type_bytes, &vstr);

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mfrc522_read_block_obj, mfrc522_read_block);

STATIC mp_obj_t mfrc522_write_block(mp_obj_t block, mp_obj_t buf_in) {
    int _block = mp_obj_get_int(block);
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(buf_in, &bufinfo, MP_BUFFER_READ);
    if (RFID_writeBlock(_block, bufinfo.buf) == MI_OK)
        return MP_OBJ_NEW_SMALL_INT(1);

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(mfrc522_write_block_obj, mfrc522_write_block);

STATIC mp_obj_t mfrc522_increment(mp_obj_t block, mp_obj_t value) {
    int _block = mp_obj_get_int(block);
    int32_t pvalue = mp_obj_get_int(value);

    if (RFID_IncDecCardBlock(PICC_INCREMENT, _block, pvalue) == MI_OK)
        return MP_OBJ_NEW_SMALL_INT(1);

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(mfrc522_increment_obj, mfrc522_increment);

STATIC mp_obj_t mfrc522_decrement(mp_obj_t block, mp_obj_t value) {
    int _block = mp_obj_get_int(block);
    int32_t pvalue = mp_obj_get_int(value);

    if (RFID_IncDecCardBlock(PICC_DECREMENT, _block, pvalue) == MI_OK)
        return MP_OBJ_NEW_SMALL_INT(1);

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_2(mfrc522_decrement_obj, mfrc522_decrement);

STATIC mp_obj_t mfrc522_set_purse(mp_obj_t block) {
    uint8_t _block = (uint8_t)mp_obj_get_int(block);
    uint8_t data1[16] = { 0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 
                          _block, ~_block, _block, ~_block };
    if (RFID_writeBlock(_block, data1) == MI_OK)
        return MP_OBJ_NEW_SMALL_INT(1);

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mfrc522_set_purse_obj, mfrc522_set_purse);

STATIC mp_obj_t mfrc522_balance(mp_obj_t block) {
    int _block = mp_obj_get_int(block);
    uint8_t buff[4];

    if (RFID_readBlock(_block, buff) == MI_OK)
        return mp_obj_new_int(buff[0] + (((int32_t)buff[1]) << 8) + (((int32_t)buff[2]) << 16) + (((int32_t)buff[3]) << 24));

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_1(mfrc522_balance_obj, mfrc522_balance);

STATIC mp_obj_t mfrc522_halt(void) {
    if (RFID_halt() == MI_OK)
        return MP_OBJ_NEW_SMALL_INT(1);

    return mp_const_none;
}
MP_DEFINE_CONST_FUN_OBJ_0(mfrc522_halt_obj, mfrc522_halt);

STATIC const mp_map_elem_t mpython_rfid_locals_dict_table[] = {
    {MP_OBJ_NEW_QSTR(MP_QSTR___name__), MP_OBJ_NEW_QSTR(MP_QSTR_rfid)},
    {MP_OBJ_NEW_QSTR(MP_QSTR_init), (mp_obj_t)&mfrc522_init_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_find_card), (mp_obj_t)&mfrc522_find_card_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_anticoll), (mp_obj_t)&mfrc522_anticoll_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_select_tag), (mp_obj_t)&mfrc522_select_tag_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_auth), (mp_obj_t)&mfrc522_auth_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_read_block), (mp_obj_t)&mfrc522_read_block_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_write_block), (mp_obj_t)&mfrc522_write_block_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_increment), (mp_obj_t)&mfrc522_increment_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_decrement), (mp_obj_t)&mfrc522_decrement_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_set_purse), (mp_obj_t)&mfrc522_set_purse_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_balance), (mp_obj_t)&mfrc522_balance_obj},
    {MP_OBJ_NEW_QSTR(MP_QSTR_halt), (mp_obj_t)&mfrc522_halt_obj},
};

STATIC MP_DEFINE_CONST_DICT(mpython_rfid_locals_dict, mpython_rfid_locals_dict_table);

const mp_obj_module_t mp_module_rfid = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&mpython_rfid_locals_dict,
};

void writeReg(uint8_t reg_addr, uint8_t val)
{
    mp_machine_i2c_p_t *i2c_p = (mp_machine_i2c_p_t*)i2c_obj->type->protocol;
    uint8_t temp[2];
    temp[0] = (uint8_t)reg_addr;
    temp[1] = val;

    mp_machine_i2c_buf_t buf = {.len = 2, .buf = temp};
    bool stop = true;
    unsigned int flags = stop ? MP_MACHINE_I2C_FLAG_STOP : 0;
    int ret = i2c_p->transfer((mp_obj_base_t *)i2c_obj, MFRC522_ADDR, 1, &buf, flags);
    if (ret < 0) {
        mp_raise_OSError(-ret);
    }
}

uint8_t readReg(uint8_t reg_addr)
{
	uint8_t buff; 
    mp_machine_i2c_p_t *i2c_p = (mp_machine_i2c_p_t*)i2c_obj->type->protocol;

    uint8_t _reg_addr = reg_addr;
    mp_machine_i2c_buf_t buf = {.len = 1, .buf = (uint8_t*)&_reg_addr};
    bool stop = false;
    unsigned int flags = stop ? MP_MACHINE_I2C_FLAG_STOP : 0;
    int ret = i2c_p->transfer((mp_obj_base_t *)i2c_obj, MFRC522_ADDR, 1, &buf, flags);
    if (ret < 0) {
        mp_raise_OSError(-ret);
    }

    buf.len = 1;
    buf.buf = &buff;
    stop = true;
    flags = MP_MACHINE_I2C_FLAG_READ | (stop ? MP_MACHINE_I2C_FLAG_STOP : 0);
    ret = i2c_p->transfer((mp_obj_base_t *)i2c_obj, MFRC522_ADDR, 1, &buf, flags);
    if (ret < 0) {
        mp_raise_OSError(-ret);
    }

  return(buff);
}