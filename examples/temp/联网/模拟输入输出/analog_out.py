# analog_out.py
# 利用模拟输出(pwm)实现灯亮度调节

from machine import Pin, PWM
import time

# led引脚初始化，频率为1HZ，每秒闪烁一次
led_pin = PWM(Pin(16), freq = 1023, duty = 0)

while True:
  for i in range(0,1024):
    led_pin.duty(i)
    time.sleep_ms(10)


