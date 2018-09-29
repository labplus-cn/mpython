# bink_pwm.py
# 利用模拟输出(pwm)实现灯亮灭

from machine import Pin, PWM
import time

# led引脚初始化，频率为1HZ，每秒闪烁一次
led_pin = PWM(Pin(16), freq = 1, duty = 512)

