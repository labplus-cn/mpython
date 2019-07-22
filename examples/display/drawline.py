from mpython import *
import time

def testdrawline():
    for i in range(0,64):
        oled.line(0,0,i*2,63,1)
        oled.show()
    for i in range(0,32):
        oled.line(0,0,127,i*2,1)
        oled.show()
    time.sleep_ms(250)
    oled.fill(0)
    oled.show()
    for i in range(0,32):
        oled.line(0,63,i*4,0,1)
        oled.show()
    for i in range(0,16):
        oled.line(0,63,127,(64-4*i)-1,1)
        oled.show()
    time.sleep_ms(250)
    oled.fill(0)
    oled.show()
    for i in range(1,32):
        oled.rect(2*i,2*i,(128-4*i)-1,(64-2*i)-1,1)
        oled.show()

testdrawline()