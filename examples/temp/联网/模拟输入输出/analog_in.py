# analog_in.py
# 利用板载光线传感器模拟光线采样值，实现灯亮度调节

from machine import Pin, PWM, ADC
import time
# 光线传感器引脚初始化
light = ADC(Pin(39))
# led引脚初始化，频率为1HZ，每秒闪烁一次
led_pin = PWM(Pin(16), freq = 1023, duty = 0)

while True:
  lightVal = light.read()//4
  print(lightVal)
  led_pin.duty(lightVal)
  time.sleep_ms(500)



