# light.py
# 采集板载光线传感器值，实现板载RGB LED亮度调节

from machine import Pin, PWM, ADC
import time
from neopixel import NeoPixel

# 光线传感器引脚初始化
light = ADC(Pin(39))
# 板载RGB LED初始化
pixels = Pin(15, Pin.OUT)
np = NeoPixel(pixels, 25)

# 循环采集光线值，控制灯亮度
while True:
  lightVal = light.read()//8 #把采到的光线值缩放到0-255范围
  print(lightVal)
  
  for i in range(0, 25):
    np[i] = (0,lightVal,0)
  np.write()

  time.sleep_ms(500)
