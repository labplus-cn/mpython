#define MICROPY_HW_BOARD_NAME "mpython-classroom-kit"
#define MICROPY_HW_MCU_NAME "ESP32"

#define MICROPY_BUILDIN_ADC                 (0)
#define MICROPY_BUILDIN_DAC                 (0)

extern const struct _mp_obj_module_t mp_module_motion;
extern const struct _mp_obj_module_t mp_module_rgbLED5x5;

#define MPYTHON_PORT_ROOT_POINTER \
        struct _MP3DecInfo  *mp3DecInfo; \
        struct _FrameHeader  *fh; \
        struct _SideInfo  *si; \
        struct _ScaleFactorInfo  *sfi; \
        struct _HuffmanInfo  *hi; \
        struct _DequantInfo  *di; \
        struct _IMDCTInfo  *mi; \
        struct _SubbandInfo  *sbi; \
        unsigned char *mp3DecReadBuf; \
        short *mp3DecOutBuf; \

#define BOARD_PORT_BUILTIN_MODULES \
        { MP_OBJ_NEW_QSTR(MP_QSTR_motion_mpu6050), (mp_obj_t)&mp_module_motion }, \
        { MP_ROM_QSTR(MP_QSTR_rgbLED5x5), MP_ROM_PTR(&mp_module_rgbLED5x5) }, \
    
        