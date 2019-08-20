# 滑杆控制马达转速 
from mpython_classroom_kit import *
from mpython import *

while True:
    # 读取滑杆电阻值
    slider_value= slider_res.read()
    # 将电阻值映射至(-100,100)
    speed = numberMap(slider_value,0,4095,-100,100)
    print("speed: %d" %speed)
    # 设置马达转速
    set_motor(speed)
