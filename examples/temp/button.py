
from machine import Pin
from handPy import *

# buttons
BTNA = Pin(0, mode=Pin.OPEN_DRAIN,pull=Pin.PULL_UP,value=1)
BTNB = Pin(2, mode=Pin.OPEN_DRAIN,pull=Pin.PULL_UP,value=1)


while True:
  
  if BTNA.value() == 0 and  BTNB.value() == 0 :
    rgb[0] = (32,0,0)
    rgb[1] = (0,32,0)
    rgb[2] = (0,0,32)
    rgb.write()
  if BTNA.value() == 0 and  BTNB.value() == 1 :
    rgb[0] = (32,32,32)
    rgb[1] = (0,0,0)
    rgb[2] = (0,0,0)
    rgb.write()
  if BTNA.value() == 1 and  BTNB.value() == 0 :
    rgb[0] = (0,0,0)
    rgb[1] = (0,0,0)
    rgb[2] = (32,32,32)
    rgb.write()
  else:
    rgb.fill((0,0,0))
    rgb.write()
    
    


 
 





































