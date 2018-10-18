from mpython import *
from time import sleep_ms

x = 0
vx = 1
while True:
    x += vx
    display.fill(0)
    display.pixel(x,10,1)
    display.pixel(x,9,1)
    display.pixel(x,11,1)
    
    display.pixel(x+1,10,1)
    display.pixel(x-1,10,1)
    
    if x > 128:
        x = 0
    display.show()
    sleep_ms(10)
    