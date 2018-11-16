from mpython import *

s=Servo(0)

for i in range(181):
    s.write_angle(i)
    sleep_ms(20)