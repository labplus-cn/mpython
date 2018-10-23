# servo.py
# 利用pwm实现舵机控制

from machine import Pin, PWM
import time

# 舵机引脚初始化，频率为50HZ，
servo = PWM(Pin(16), freq = 50, duty = 0)

# 循环实现舵机0-180转动
while True:
    for i in range(25,128): #占空比duty值范围25-128，对应0-180度
        servo.duty(i)
        time.sleep_ms(100)



