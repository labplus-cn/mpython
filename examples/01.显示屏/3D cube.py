# 3D CUBE MicroPython version with ESP32 and ssd1306 OLED 

from machine import Pin, I2C
from micropython import const
from time import sleep_ms
from math import sin, cos
from mpython import *


X = const(64)
Y = const(32)

f = [[0.0 for _ in range(3)] for _ in range(8)]
cube = ((-20,-20, 20), (20,-20, 20), (20,20, 20), (-20,20, 20),
        (-20,-20,-20), (20,-20,-20), (20,20,-20), (-20,20,-20))




while True:

        for i in range(8):
            r  = angle * 0.0174532  # 1 degree
            x1 = cube[i][2] * sin(r) + cube[i][0] * cos(r)  # rotate Y
            ya = cube[i][1]
            z1 = cube[i][2] * cos(r) - cube[i][0] * sin(r)
            x2 = x1
            y2 = ya * cos(r) - z1 * sin(r)  # rotate X
            z2 = ya * sin(r) + z1 * cos(r)
            x3 = x2 * cos(r) - y2 * sin(r)  # rotate Z
            y3 = x2 * sin(r) + y2 * cos(r)
            z3 = z2
            x3 = x3 + X
            y3 = y3 + Y
            f[i][0] = x3  # store new values
            f[i][1] = y3
            f[i][2] = z3
        display.fill(0)  # clear
        display.line(int(f[0][0]), int(f[0][1]), int(f[1][0]), int(f[1][1]), 1)
        display.line(int(f[1][0]), int(f[1][1]), int(f[2][0]), int(f[2][1]), 1)
        display.line(int(f[2][0]), int(f[2][1]), int(f[3][0]), int(f[3][1]), 1)
        display.line(int(f[3][0]), int(f[3][1]), int(f[0][0]), int(f[0][1]), 1)
        display.line(int(f[4][0]), int(f[4][1]), int(f[5][0]), int(f[5][1]), 1)
        display.line(int(f[5][0]), int(f[5][1]), int(f[6][0]), int(f[6][1]), 1)
        display.line(int(f[6][0]), int(f[6][1]), int(f[7][0]), int(f[7][1]), 1)
        display.line(int(f[7][0]), int(f[7][1]), int(f[4][0]), int(f[4][1]), 1)
        display.line(int(f[0][0]), int(f[0][1]), int(f[4][0]), int(f[4][1]), 1)
        display.line(int(f[1][0]), int(f[1][1]), int(f[5][0]), int(f[5][1]), 1)
        display.line(int(f[2][0]), int(f[2][1]), int(f[6][0]), int(f[6][1]), 1)
        display.line(int(f[3][0]), int(f[3][1]), int(f[7][0]), int(f[7][1]), 1)
        display.line(int(f[1][0]), int(f[1][1]), int(f[3][0]), int(f[3][1]), 1)  # cross
        display.line(int(f[0][0]), int(f[0][1]), int(f[2][0]), int(f[2][1]), 1)  # cross
        display.DispChar('3D CUBE', 0, 0)
        display.show()  # display
        sleep_ms(1)