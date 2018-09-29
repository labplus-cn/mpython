# digital_out_high.py
# 引脚输出高电平,点亮一个灯

from machine import Pin

led_pin = Pin(16, Pin.OUT)
led_pin.value(1)
