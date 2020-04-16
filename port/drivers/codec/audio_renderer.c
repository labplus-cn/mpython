/*
 * audio_renderer.c
 * renderer使用：
 *  1 初始化I2S
 *      相关参数配置，安装驱动
 *      如果配置成内置ADC DAC需设置ADC DAC模式，否则要配置引脚
 *      初始化完成后，最好，清除DMA缓存，并关闭I2S，避免产生噪音。
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#include <stdbool.h>
#include <string.h>

#include "freertos/FreeRTOS.h"

#include "esp_log.h"
#include "driver/gpio.h"
#include "driver/i2s.h"
#include "audio_player.h"
#include "audio_renderer.h"
#include "http_client.h"
#include "mpconfigboard.h"
#define TAG "renderer"

#define I2S_USE_NUM I2S_NUM_0
// #define USE_I2S_FORMAT        I2S_CHANNEL_FMT_ONLY_RIGHT //(I2S_CHANNEL_FMT_RIGHT_LEFT)
// //I2S channel number
// #define USE_I2S_CHANNEL_NUM   ((USE_I2S_FORMAT < I2S_CHANNEL_FMT_ONLY_RIGHT) ? (2) : (1))

renderer_config_t *renderer_instance = NULL;
// static QueueHandle_t i2s_event_queue;
extern HTTP_HEAD_VAL http_head[6];

static void init_i2s(renderer_config_t *config)
{     
    i2s_mode_t mode = I2S_MODE_MASTER;

    if (config->mode == I2S_MODE_TX)
    {
        mode = mode | I2S_MODE_TX;
        #if MICROPY_BUILDIN_DAC 
        mode = mode | I2S_MODE_DAC_BUILT_IN;
        // ESP_LOGE(TAG, "I2S MODE IS DAC BUILT IN");
        #endif
    }
    if (config->mode == I2S_MODE_RX)
    {
        mode = mode | I2S_MODE_RX;
        #if MICROPY_BUILDIN_ADC
        mode = mode | I2S_MODE_ADC_BUILT_IN;
        // ESP_LOGE(TAG, "I2S MODE IS ADC BUILT IN");
        #endif
    }

    /*
     * Allocate just enough to decode AAC+, which has huge frame sizes.
     *
     * Memory consumption formula:
     * (bits_per_sample / 8) * num_chan * dma_buf_count * dma_buf_len
     *
     * 16 bit: 32 * 256 = 8192 bytes
     * 32 bit: 32 * 256 = 16384 bytes
     */
    i2s_config_t i2s_config = {
        .mode = mode,                                 // I2S_MODE_MASTER | I2S_MODE_TX | I2S_MODE_DAC_BUILT_IN,
        .sample_rate = config->sample_rate,           //16000 default
        .bits_per_sample = config->bit_depth,         //16bit default
        .channel_format = config->channel_format,   
        #if MICROPY_BUILDIN_DAC || MICROPY_BUILDIN_ADC
        .communication_format = I2S_COMM_FORMAT_I2S_MSB,
        #else          
        .communication_format = I2S_COMM_FORMAT_I2S,
        #endif
        .dma_buf_count = 16,                           //16 32 number of buffers, 128 max.
        .dma_buf_len = 64,                          //128 64 size of each buffer
        .use_apll = config->use_apll,
        .intr_alloc_flags =0 // ESP_INTR_FLAG_LEVEL1 // Interrupt level 1 ESP_INTR_FLAG_LEVEL0?
    };


    // i2s_driver_uninstall(I2S_USE_NUM);
    i2s_driver_install(I2S_USE_NUM, &i2s_config, 0, NULL);
    // ESP_LOGE(TAG, "4 i2s driver intalled, RAM left: %d", esp_get_free_heap_size());

    if(config->mode == I2S_MODE_TX) 
    {
        #if MICROPY_BUILDIN_DAC
        i2s_set_dac_mode(I2S_DAC_CHANNEL_BOTH_EN);
        #else
        i2s_set_clk(I2S_USE_NUM, config->sample_rate, config->bit_depth, config->i2s_channal_nums);
        #endif
        i2s_zero_dma_buffer(0);
    }
    else if(config->mode == I2S_MODE_RX)
    {
        #if MICROPY_BUILDIN_ADC
        i2s_set_adc_mode(ADC_UNIT_1, ADC1_CHANNEL_2); //renderer_instance->adc1_channel );
        #endif
    }

    #if !MICROPY_BUILDIN_DAC || !MICROPY_BUILDIN_ADC
    i2s_pin_config_t i2s_pin_cfg;
    i2s_pin_cfg.bck_io_num = GPIO_NUM_18; //5;
    i2s_pin_cfg.ws_io_num = GPIO_NUM_5; //25;
    i2s_pin_cfg.data_out_num = GPIO_NUM_32; //26;
    i2s_pin_cfg.data_in_num = GPIO_NUM_35; //35;
    i2s_set_pin(I2S_USE_NUM, &i2s_pin_cfg);
    // i2s_mclk_gpio_select(config->i2s_num, GPIO_NUM_0);
    PIN_FUNC_SELECT(PERIPHS_IO_MUX_GPIO0_U, FUNC_GPIO0_CLK_OUT1);
    WRITE_PERI_REG(PIN_CTRL, 0xFFF0);
    #endif

    // i2s_stop(I2S_USE_NUM);
    // ESP_LOGE(TAG, "1.1 Create after i2s driver install: RAM left 1 %d", esp_get_free_heap_size());
}

void renderer_zero_dma_buffer()
{
    if(renderer_instance != NULL)
    {
        i2s_zero_dma_buffer(I2S_USE_NUM);
    }
}

renderer_config_t *renderer_get()
{
    return renderer_instance;
}

/* init renderer sink */
void renderer_init(renderer_config_t *config)
{
    /* Create renderer. */
    if (renderer_instance == NULL)
        renderer_instance = calloc(1, sizeof(renderer_config_t));

    renderer_instance->bit_depth  = config->bit_depth;
    renderer_instance->sample_rate = config->sample_rate;
    renderer_instance->mode = config->mode; 
    renderer_instance->use_apll = config->use_apll; 
    renderer_instance->channel_format = config->channel_format;
    renderer_instance->i2s_channal_nums = (renderer_instance->channel_format < I2S_CHANNEL_FMT_ONLY_RIGHT) ? (2) : (1);
    renderer_instance->adc1_channel = config->adc1_channel;

    // ESP_LOGE(TAG, "init I2S mode %d, %d bit, %d Hz", renderer_instance->mode, renderer_instance->bit_depth, renderer_instance->sample_rate);
    init_i2s(config);
}

void renderer_start()
{
    if(renderer_instance != NULL)
    {
        i2s_start(I2S_USE_NUM);
        // buffer might contain noise
        i2s_zero_dma_buffer(I2S_USE_NUM);
    }
}

void renderer_stop()
{
    if(renderer_instance != NULL)
    {
        i2s_stop(I2S_USE_NUM);
        i2s_zero_dma_buffer(I2S_USE_NUM);
    }
}

void renderer_deinit()
{
    if(renderer_instance != NULL)
    {
        i2s_stop(I2S_USE_NUM);
        i2s_driver_uninstall(I2S_USE_NUM);
        free(renderer_instance);
        renderer_instance = NULL;
    }
}

void renderer_adc_enable()
{
    if(renderer_instance != NULL)
    {
        i2s_adc_enable(I2S_USE_NUM);
    }
}

void renderer_adc_disable()
{
    if(renderer_instance != NULL)
    {
        i2s_adc_disable(I2S_USE_NUM);
    }
}

void renderer_set_clk(uint32_t rate, i2s_bits_per_sample_t bits, i2s_channel_t ch)
{
    if(renderer_instance != NULL)
    {
        i2s_set_clk(I2S_USE_NUM, rate, bits, ch);
    }
}

void renderer_read_raw(uint8_t *buff, uint32_t len)
{
    size_t bytes_read;
    i2s_read(I2S_USE_NUM, (void *)buff, len, &bytes_read, portMAX_DELAY);
}

void renderer_write(const void *src, size_t size, size_t *bytes_written, TickType_t ticks_to_wait)
{
    i2s_write(I2S_USE_NUM, src, size, bytes_written, ticks_to_wait);
}

void i2s_adc_data_scale(uint8_t * d_buff, uint8_t* s_buff, uint32_t len)
{
    // uint32_t j = 0;
    // uint32_t dac_value;
    for (uint16_t j = 0; j < len; j++) 
        d_buff[j] = s_buff[j];

    // if(renderer_instance->bit_depth == I2S_BITS_PER_SAMPLE_16BIT) 
    // { 
    //     // memcpy(d_buff, s_buff, len);
    //     for (int i = 0; i < len; i += 2) {
    //         // adc_val = ((((uint16_t) (s_buff[i + 1] & 0xf) << 8) | ((s_buff[i + 0]))));
    //         // adc_val = (adc_val - 2048 - 300) << 4; 
    //         // d_buff[j++] = adc_val & 0xff;
    //         // d_buff[j++] = (adc_val >> 8) & 0xff;
    //         dac_value = ((((uint16_t) (s_buff[i + 1] & 0xf) << 8) | ((s_buff[i + 0]))));
    //         d_buff[j++] = 0;
    //         d_buff[j++] = dac_value * 256 / 4096; 
    //         // printf("%02x", s_buff[i]);
    //         // printf("%02x", (uint8_t)(adc_val * 256 / 4096));
    //         // printf("%d\n", (dac_value - 2048 - 300) << 2);
    //     }
    // }
}

void i2s_adc_data_scale1(uint16_t * d_buff, uint8_t* s_buff, uint32_t len)
{
    uint32_t j = 0;
    uint16_t adc_val;

    if(renderer_instance->bit_depth == I2S_BITS_PER_SAMPLE_16BIT) 
    {
        // memcpy(d_buff, s_buff, len);
        for (int i = 0; i < len; i += 2) {
            adc_val = ((((uint16_t) (s_buff[i + 1] & 0xf) << 8) | ((s_buff[i + 0]))));
            // adc_val = (adc_val - 2048 - 300) << 2; 
            d_buff[j++] = adc_val;
            // printf("%d", adc_val);
        }
        // printf("\r\n");
    }
}