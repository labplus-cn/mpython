# RGB LED
#  掌控板内置RGB LED点阵控制

from machine import Pin
from neopixel import NeoPixel
import time

pixels = Pin(15, Pin.OUT)
np = NeoPixel(pixels, 25)

while True:
  color = ((32, 0, 0), (0, 32, 0), (0, 0, 32),(32, 32, 32))
  
  for i in range(0, 25):
    np[i] = color[color_index]
  np.write()
  color_index = color_index + 1
  color_index = color_index % 4
  
  time.sleep_ms(1000)

