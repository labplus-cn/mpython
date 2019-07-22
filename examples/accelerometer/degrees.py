# 通过y轴加速度求y轴与水平面倾斜角度

from mpython import*
from math import acos,degrees

while True:
    y=accelerometer.get_y()
    if y<=1 and y>=-1:
        rad_y=acos(y)
        deg_y=90-degrees(rad_y)
        oled.DispChar('%.2f°' %deg_y,50,25)
        oled.show()
        oled.fill(0)
        

