# Acceleration.py
# 利用加速度传感器控制灯亮灭

from labplus import *
import time

led = Pin(16, Pin.OUT) # led引脚初始化
acc = MMA8653() # 定义一个加速度传感器实例
ledState = False

while True:
  # 检测加速度传感器变化
  acc_x1 = acc.getX()
  acc_y1 = acc.getY()
  acc_z1 = acc.getZ()
  time.sleep_ms(500)
  acc_x2 = acc.getX()
  acc_y2 = acc.getY()
  acc_z2 = acc.getZ() 
  # 变化值超过一定量，改变led状态
  if abs(acc_x1 - acc_x2) > 0.5 or abs(acc_y1 - acc_y2) > 0.5 or abs(acc_z1 - acc_z2) > 0.5:
    ledState = not ledState
    
  if ledState:
    led.value(1)
  else :
    led.value(0)
