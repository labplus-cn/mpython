from servo import Servo
import time

s=Servo(0)

for i in range(181):
    s.write_angle(i)
    time.sleep_ms(100)
