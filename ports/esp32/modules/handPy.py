# handPy driver for MicroPython on ESP32
# MIT license; Copyright (c) 2018 zh.kaihua@gmail.com

from machine import I2C, PWM, Pin
from ssd1106 import SSD1106_I2C
import esp
import ustruct

i2c = I2C(scl = Pin(22), sda = Pin(23), freq = 400000)

class Font(object):
    def __init__(self, font_address = 0x300000):
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

class Display(SSD1106_I2C):
    """ 128x64 oled display """
    
    def __init__(self):
        super().__init__(128, 64, i2c)
        self.f = Font()
        if self.f == None:
          print('font init failed')
        else:
          print('font init success:%s' % self.f.header)

    def DispChar(self, s, x, y, c):
        for c in s:
            data = self.f.GetCharacterData(c)
            if data == None:
              x = x + self.width
              continue
            width, bytes_per_line =  ustruct.unpack('HH', data[:4])
            print('character [%d]: width = %d, bytes_per_line = %d' % (ord(c), width, bytes_per_line))
            for h in range(0, self.f.height):
                w = 0
                i = 0
                while w < width:
                    mask = data[4 + h * bytes_per_line + i]
                    if (width - w) >= 8:
                        n = 8
                    else:
                        n = width - w
                    for p in range(0, n):
                        if (mask& 0x80) != 0:
                            super().pixel(x + w + p, y + h, 1)
                        else:
                            super().pixel(x + w + p, y + h, 0)
                        mask = mask << 1
                    w = w + 8
                    i = i + 1
            x = x + width

    
display = Display()
buzz = PWM(Pin(5), 500, 0)

    







