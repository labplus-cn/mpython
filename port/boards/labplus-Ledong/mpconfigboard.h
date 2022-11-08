#define MICROPY_HW_BOARD_NAME "labplus-Ledong"
// #define MICROPY_HW_BOARD_NAME "InnovaBit-Core"
#define MICROPY_HW_MCU_NAME "ESP32"

#define MICROPY_BUILDIN_ADC                 (0)
#define MICROPY_BUILDIN_DAC                 (0)

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

