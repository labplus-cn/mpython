#include "freertos/FreeRTOS.h"
#include "oled.h"
#include "../../../extmod/font_petme128_8x8.h"
#include "startup.h"

static uint8_t oled_vram[OLED_WIDTH*OLED_HEIGHT/8];

esp_err_t write_cmd(uint8_t cmd) {
    uint8_t temp[2];
    temp[0] = 0x80;         // Co=1, D/C#=0
    temp[1] = cmd;
    return i2c_writeto(SH1106_I2C_ADDRESS, temp, sizeof(temp));
}

esp_err_t write_data(uint8_t * buff, size_t size) {
    if (size == 0) {
        return ESP_OK;
    }

    uint8_t temp[2];
    temp[0] = SH1106_I2C_ADDRESS << 1;
    temp[1] = 0x40;     // Co=0, D/C#=1
    i2c_cmd_handle_t handler = i2c_cmd_link_create();
    i2c_master_start(handler);
    i2c_master_write(handler, temp, sizeof(temp), ACK_CHECK_EN);
    i2c_master_write(handler, buff, size, ACK_CHECK_EN);
    i2c_master_stop(handler);
    esp_err_t ret = i2c_master_cmd_begin(I2C_MASTER_NUM, handler, 500/portTICK_RATE_MS);
    i2c_cmd_link_delete(handler);
    return ret;
}

const uint8_t oled_init_cmd[] = {
    SET_DISP_OFF,               // display off
	SET_DISP_CLK_DIV, 0x80,     // timing and driving scheme
	SET_MUX_RATIO, 0x3f,        // 0xa8
	SET_DISP_OFFSET, 0x00,      // 0xd3
	SET_DISP_START_LINE | 0x00, // start line
	SET_CHARGE_PUMP,  0x10,     // 0x10 if external_vcc else 0x14,
	SET_MEM_ADDR, 0x00,         // address setting
	SET_SEG_REMAP | 0x01,       // column addr 127 mapped to SEG0
	SET_COM_OUT_DIR | 0x08,     // scan from COM[N] to COM0
	SET_COM_PIN_CFG, 0x12,
	SET_CONTRACT_CTRL, 0xcf,
	SET_PRECHARGE, 0x22,        // 0x22 if self.external_vcc else 0xf1,
	SET_VCOM_DESEL, 0x40,       // 0.83*Vcc
	SET_ENTIRE_ON,              // output follows RAM contents
	SET_NORM_INV,       
	SET_DISP_ON                 // on
};

bool oled_init() {
    i2c_master_init();
    for (int i = 0; i < sizeof(oled_init_cmd); i++) {
        if (write_cmd(oled_init_cmd[i]) != ESP_OK) {
            return false;
        }
    }
    return true;
}

void oled_deinit() 
{
    i2c_master_deinit();
}

void oled_drawPixel(int16_t x, int16_t y, int16_t color) {
  if ((x < 0) || (x >= OLED_WIDTH) || (y < 0) || (y >= OLED_HEIGHT))
    return;
    // x is which column
    switch (color) 
    {
      case WHITE:   oled_vram[x+ (y/8)*OLED_WIDTH] |=  (1 << (y&7)); break;
      case BLACK:   oled_vram[x+ (y/8)*OLED_WIDTH] &= ~(1 << (y&7)); break; 
      case INVERSE: oled_vram[x+ (y/8)*OLED_WIDTH] ^=  (1 << (y&7)); break; 
    }
}

void oled_clear()
{
    for (int i = 0; i < sizeof(oled_vram); i++) {
        oled_vram[i] = 0;
    }
}

void oled_drawImg(const uint8_t * img) 
{
    for (int i = 0; i < sizeof(oled_vram); i++) {
        oled_vram[i] = img[i];
    }
}
const uint8_t * ani_startup[25] = {
    img_00001, img_00002, img_00003, img_00004, img_00005,
    img_00006, img_00007, img_00008, img_00009, img_00010,
    img_00011, img_00012, img_00013, img_00014, img_00015,
    img_00016, img_00017, img_00018, img_00019, img_00020,
    img_00021, img_00022, img_00023, img_00024, img_00030,
};

void oled_drawAnimation(const uint8_t **pImgs, int len, int frameRate)
{
    int i = 0;
    for (; i < len; i++) {
        oled_drawImg(pImgs[i]);
        oled_show();
        vTaskDelay(1000/frameRate /portTICK_RATE_MS);
    } 
    // for (i = len -1; i >= 0; i--) {
    //     oled_drawImg(pImgs[i]);
    //     oled_show();
    //     vTaskDelay(1000/frameRate /portTICK_RATE_MS);
    // } 
}

void oled_print(const char * str, int x0, int y0)
{
    while(*str) {
        char c = *str++;
        if ( c < 32 || c > 127) {
            if (c == '\n') {
                y0 += 8;
                x0 = 0;
                continue;
            } else {
                c = 32;
            }
        }
        // auto new line,when reach the right sidle
        if (x0 >= OLED_WIDTH) {
            y0 += 8;
            x0 = 0;
        }
        // get char data
        const uint8_t *chr_data = &font_petme128_8x8[(c - 32) * 8];
        // loop over char data
        for (int j = 0; j < 8; j++, x0++) {
            if (0 <= x0 && x0 < OLED_WIDTH) { // clip x
                uint8_t vline_data = chr_data[j]; // each byte is a column of 8 pixels, LSB at top
                for (int y = y0; vline_data; vline_data >>= 1, y++) { // scan over vertical column
                    if (vline_data & 1) { // only draw if pixel set
                        if (0 <= y && y < OLED_HEIGHT) { // clip y
                            oled_drawPixel(x0, y, 1);
                        }
                    }
                }
            }
        }

    }
}

void oled_show() {
    for (uint8_t i = 0; i < OLED_HEIGHT/8; i++) {
        write_cmd(SET_PAGE_ADDR1 | i);
        write_cmd(SET_COL_ADDR_L | 0);
        write_cmd(SET_COL_ADDR_H | 0);
        write_data((oled_vram + i*OLED_WIDTH), OLED_WIDTH);
        //vTaskDelay(10 / portTICK_RATE_MS);
    }
}
