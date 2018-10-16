# mPython drivers for MicroPython
# MIT license; Copyright (c) 2018 ZhangKaiHua
# v1.0

from machine import I2C, PWM, Pin, ADC
from ssd1106 import SSD1106_I2C
import esp
import ustruct
from neopixel import NeoPixel

i2c = I2C(scl=Pin(22,mode=Pin.OUT ,pull=None), sda=Pin(23,mode=Pin.OUT ,pull=None), freq=400000)

class Font(object):
    def __init__(self, font_address=0x300000):
        self.font_address = font_address
        buffer = bytearray(18)
        esp.flash_read(self.font_address, buffer)
        self.header, \
        self.height, \
        self.width, \
        self.baseline, \
        self.x_height, \
        self.Y_height, \
        self.first_char,\
        self.last_char = ustruct.unpack('4sHHHHHHH', buffer)
        self.first_char_info_address = self.font_address + 18
    def GetCharacterData(self, c):
        uni = ord(c)
        if uni not in range(self.first_char, self.last_char):
          return None
        char_info_address = self.first_char_info_address + (uni - self.first_char) * 6
        buffer = bytearray(6)
        esp.flash_read(char_info_address, buffer)
        ptr_char_data, len = ustruct.unpack('IH', buffer)   
        if (ptr_char_data) == 0 or (len == 0):
          return None
        buffer = bytearray(len)
        esp.flash_read(ptr_char_data + self.font_address, buffer)
        return buffer

class Accelerometer():
    """  """
    def __init__(self):
        self.addr = 38
        self.i2c = i2c
        self.i2c.writeto(self.addr, b'\x0F\x08')    # set resolution = 10bit
        self.i2c.writeto(self.addr, b'\x11\x00')    # set power mode = normal
    
    def get_x(self):
        self.i2c.writeto(self.addr, b'\x02', False)
        buf = self.i2c.readfrom(self.addr, 2)
        x = ustruct.unpack('h', buf)[0]
        return x / 4 / 4096
        
    def get_y(self):
        self.i2c.writeto(self.addr, b'\x04', False)
        buf = self.i2c.readfrom(self.addr, 2)
        y = ustruct.unpack('h', buf)[0]
        return y / 4 / 4096
    def get_z(self):
        self.i2c.writeto(self.addr, b'\x06', False)
        buf = self.i2c.readfrom(self.addr, 2)
        z = ustruct.unpack('h', buf)[0]
        return z / 4 / 4096
        
        
        

class TextMode():
  normal = 1
  rev = 2
  trans = 3
  xor = 4
  
class Display(SSD1106_I2C):
    """ 128x64 oled display """
    def __init__(self):
        super().__init__(128, 64, i2c)
        self.f = Font()
        if self.f == None:
            raise Exception('font load failed')

    def DispChar(self, s, x, y, mode = TextMode.normal):
        if self.f == None:
            return
        for c in s:
            data = self.f.GetCharacterData(c)
            if data == None:
              x = x + self.width
              continue
            width, bytes_per_line =  ustruct.unpack('HH', data[:4])
            # print('character [%d]: width = %d, bytes_per_line = %d' % (ord(c), width, bytes_per_line))
            for h in range(0, self.f.height):
                w = 0
                i = 0
                while w < width:
                    mask = data[4 + h * bytes_per_line + i]
                    if (width - w) >= 8:
                        n = 8
                    else:
                        n = width - w
                    py = y + h
                    page = py >> 3
                    bit = 0x80 >> (py % 8)
                    for p in range(0, n):
                        px = x + w + p
                        c = 0
                        if (mask & 0x80) != 0:
                            if mode == TextMode.normal or mode == TextMode.trans:
                              c = 1
                            if mode == TextMode.rev:
                              c = 0
                            if mode == TextMode.xor:                               
                              c = self.buffer[page * 128 + px] & bit
                              if c != 0:
                                c = 0
                              else:
                                c = 1
                              print("px = %d, py = %d, c = %d" % (px, py, c))
                            super().pixel(px, py, c)
                        else:
                            if mode == TextMode.normal:
                                c = 0
                                super().pixel(px, py, c)
                            if mode == TextMode.rev:
                                c = 1
                                super().pixel(px, py, c)
                        mask = mask << 1
                    w = w + 8
                    i = i + 1
            x = x + width + 1


class Buzz(object):
    def __init__(self, pin = 16):
        self.pin = pin
        self.io = Pin(self.pin) 
        self.io.value(1)
        self.isOn = False
        
    def on(self, freq = 500):
        if self.isOn == False:
          self.pwm = PWM(self.io, freq, 512)
          self.isOn = True
        
    def off(self):
        if self.isOn == True:
          self.pwm.deinit()
          self.io.init(self.pin, Pin.OUT)
          self.io.value(1)
          self.isOn = False
            
# buzz
buzz = Buzz()

# display
display = Display()

# 3 axis accelerometer
accelerometer = Accelerometer()

# 3 rgb leds
rgb = NeoPixel(Pin(17, Pin.OUT), 3, 3, 1)
rgb.write()

# light sensor
light = ADC(Pin(39))

# sound sensor
sound = ADC(Pin(36))

# buttons
button_a = Pin(0, Pin.IN, Pin.PULL_UP)
button_b = Pin(2, Pin.IN, Pin.PULL_UP)

    







