from mpython import *
import time

def testdrawline():
    for i in range(0,64):
        display.line(0,0,i*2,63,1)
        display.show()
    for i in range(0,32):
        display.line(0,0,127,i*2,1)
        display.show()
    time.sleep_ms(250)
    display.fill(0)
    display.show()
    for i in range(0,32):
        display.line(0,63,i*4,0,1)
        display.show()
    for i in range(0,16):
        display.line(0,63,127,(64-4*i)-1,1)
        display.show()
    time.sleep_ms(250)
    display.fill(0)
    display.show()
    for i in range(1,32):
        display.rect(2*i,2*i,(128-4*i)-1,(64-2*i)-1,1)
        display.show()

testdrawline()