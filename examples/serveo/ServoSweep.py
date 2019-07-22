from mpython import *

s=Servo(0)

while True:
    for i in range(0,180,1):
        s.write_angle(i)
        sleep_ms(50)
    for i in range(180,0,-1):
        s.write_angle(i)
        sleep_ms(50)