
from machine import *

def callback(p):
  
  print('pin change',p)

p0=Pin(33,mode=Pin.IN,pull=Pin.PULL_UP)
p1=Pin(32,mode=Pin.IN,pull=Pin.PULL_UP)


p0.irq(trigger=Pin.IRQ_FALLING, handler=callback)
p1.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=callback)