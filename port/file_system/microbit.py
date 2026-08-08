# The MIT License (MIT)

# Copyright (c) 2019, labplus@Tangliufeng

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# 掌控板兼容Microbit库,已实现功能有以下:
# - MicrBit Module 基础函数
# - MicroBitDispl
# - 内置Image图片和构建类

import os,sys,time,_thread,esp32,framebuf,machine,gc
from framebuf import FrameBuffer
from machine import UART, ADC, Pin
from mpython import oled, MPythonPin, PinMode, button_a, button_b, accelerometer

pendolino = [0x0, 0x0, 0x0, 0x0, 0x0, 0x8, 0x8, 0x8, 0x0, 0x8, 0xa, 0x4a, 0x40, 0x0, 0x0, 0xa, 0x5f, 0xea, 0x5f, 0xea, 0xe, 0xd9, 0x2e, 0xd3, 0x6e, 0x19, 0x32, 0x44, 0x89, 0x33, 0xc, 0x92, 0x4c, 0x92, 0x4d, 0x8, 0x8, 0x0, 0x0, 0x0, 0x4, 0x88, 0x8, 0x8, 0x4, 0x8, 0x4, 0x84, 0x84, 0x88, 0x0, 0xa, 0x44, 0x8a, 0x40, 0x0, 0x4, 0x8e, 0xc4, 0x80, 0x0, 0x0, 0x0, 0x4, 0x88, 0x0, 0x0, 0xe, 0xc0, 0x0, 0x0, 0x0, 0x0, 0x8, 0x0, 0x1, 0x22, 0x44, 0x88, 0x10, 0xc, 0x92, 0x52, 0x52, 0x4c, 0x4, 0x8c, 0x84, 0x84, 0x8e, 0x1c, 0x82, 0x4c, 0x90, 0x1e, 0x1e, 0xc2, 0x44, 0x92, 0x4c, 0x6, 0xca, 0x52, 0x5f, 0xe2, 0x1f, 0xf0, 0x1e, 0xc1, 0x3e, 0x2, 0x44, 0x8e, 0xd1, 0x2e, 0x1f, 0xe2, 0x44, 0x88, 0x10, 0xe, 0xd1, 0x2e, 0xd1, 0x2e, 0xe, 0xd1, 0x2e, 0xc4, 0x88, 0x0, 0x8, 0x0, 0x8, 0x0, 0x0, 0x4, 0x80, 0x4, 0x88, 0x2, 0x44, 0x88, 0x4, 0x82, 0x0, 0xe, 0xc0, 0xe, 0xc0, 0x8, 0x4, 0x82, 0x44, 0x88, 0xe, 0xd1, 0x26, 0xc0, 0x4, 0xe, 0xd1, 0x35, 0xb3, 0x6c, 0xc, 0x92, 0x5e, 0xd2, 0x52, 0x1c, 0x92, 0x5c, 0x92, 0x5c, 0xe, 0xd0, 0x10, 0x10, 0xe, 0x1c, 0x92, 0x52, 0x52, 0x5c, 0x1e, 0xd0, 0x1c, 0x90, 0x1e, 0x1e, 0xd0, 0x1c, 0x90, 0x10, 0xe, 0xd0, 0x13, 0x71, 0x2e, 0x12, 0x52, 0x5e, 0xd2, 0x52, 0x1c, 0x88, 0x8, 0x8, 0x1c, 0x1f, 0xe2, 0x42, 0x52, 0x4c, 0x12, 0x54, 0x98, 0x14, 0x92, 0x10, 0x10, 0x10, 0x10, 0x1e, 0x11, 0x3b, 0x75, 0xb1, 0x31, 0x11, 0x39, 0x35, 0xb3, 0x71, 0xc, 0x92, 0x52, 0x52, 0x4c, 0x1c, 0x92, 0x5c, 0x90, 0x10, 0xc, 0x92, 0x52, 0x4c, 0x86, 0x1c, 0x92, 0x5c, 0x92, 0x51, 0xe, 0xd0, 0xc, 0x82, 0x5c, 0x1f, 0xe4, 0x84, 0x84, 0x84, 0x12, 0x52, 0x52, 0x52, 0x4c, 0x11, 0x31, 0x31, 0x2a, 0x44, 0x11, 0x31, 0x35, 0xbb, 0x71, 0x12, 0x52, 0x4c, 0x92, 0x52, 0x11, 0x2a, 0x44, 0x84, 0x84, 0x1e, 0xc4, 0x88, 0x10, 0x1e, 0xe, 0xc8, 0x8, 0x8, 0xe, 0x10, 0x8, 0x4, 0x82, 0x41, 0xe, 0xc2, 0x42, 0x42, 0x4e, 0x4, 0x8a, 0x40, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1f, 0x8, 0x4, 0x80, 0x0, 0x0, 0x0, 0xe, 0xd2, 0x52, 0x4f, 0x10, 0x10, 0x1c, 0x92, 0x5c, 0x0, 0xe, 0xd0, 0x10, 0xe, 0x2, 0x42, 0x4e, 0xd2, 0x4e, 0xc, 0x92, 0x5c, 0x90, 0xe, 0x6, 0xc8, 0x1c, 0x88, 0x8, 0xe, 0xd2, 0x4e, 0xc2, 0x4c, 0x10, 0x10, 0x1c, 0x92, 0x52, 0x8, 0x0, 0x8, 0x8, 0x8, 0x2, 0x40, 0x2, 0x42, 0x4c, 0x10, 0x14, 0x98, 0x14, 0x92, 0x8, 0x8, 0x8, 0x8, 0x6, 0x0, 0x1b, 0x75, 0xb1, 0x31, 0x0, 0x1c, 0x92, 0x52, 0x52, 0x0, 0xc, 0x92, 0x52, 0x4c, 0x0, 0x1c, 0x92, 0x5c, 0x90, 0x0, 0xe, 0xd2, 0x4e, 0xc2, 0x0, 0xe, 0xd0, 0x10, 0x10, 0x0, 0x6, 0xc8, 0x4, 0x98, 0x8, 0x8, 0xe, 0xc8, 0x7, 0x0, 0x12, 0x52, 0x52, 0x4f, 0x0, 0x11, 0x31, 0x2a, 0x44, 0x0, 0x11, 0x31, 0x35, 0xbb, 0x0, 0x12, 0x4c, 0x8c, 0x92, 0x0, 0x11, 0x2a, 0x44, 0x98, 0x0, 0x1e, 0xc4, 0x88, 0x1e, 0x6, 0xc4, 0x8c, 0x84, 0x86, 0x8, 0x8, 0x8, 0x8, 0x8, 0x18, 0x8, 0xc, 0x88, 0x18, 0x0, 0x0, 0xc, 0x83, 0x60]
pendolino = bytearray(pendolino)

# microbit引脚映射
def pin_esp2bit(pin):
    pins_remap_esp32 = (33, 32, 35, 34, 39, 0, 16, 17, 26, 25, 36, 2, -1, 18, 19, 21, 5, -1, -1, 22, 23, -1, -1, 27, 14, 12,
                        13, 15, 4)
    if pin == None:
        return None
    else:
        return pins_remap_esp32[pin]

# 芯片温度
def temperature():
    return int((esp32.raw_temperature()-32)/1.8)

# sound sensor
_sound = ADC(Pin(36))
_sound.atten(_sound.ATTN_11DB)

# light sensor
_light = ADC(Pin(39))
_light.atten(_light.ATTN_11DB)

# 声音
def sound():
    return _sound.read()

# 光线
def light():
    return _light.read()

# 复位
def reset():
    machine.reset()

# 毫秒延时
def sleep(n):
    time.sleep_ms(n)

# 运行时间ms
def running_time():
    return  time.ticks_ms()


class MicroBitUART(UART):

    def __init__(self):
        super().__init__(1)
        self.redirect = False

    def init(self, *arg, **kws):
        try:
            tx = kws["tx"]
            rx = kws["rx"]
        except KeyError:
            pass
        else:
            kws['tx'] = pin_esp2bit(tx.id)
            kws['rx'] = pin_esp2bit(rx.id)
            self.redirect = True
        super().init(*arg, **kws)

    def any(self):
        if not self.redirect: super().init(115200, tx=1, rx=3)
        return super().any()

    def read(self,*arg):
        if not self.redirect: super().init(115200, tx=1, rx=3)
        return super().read(*arg)

    def readall(self):
        if not self.redirect: super().init(115200, tx=1, rx=3)
        return super().read()

    def readinto(self,*arg):
        if not self.redirect: super().init(115200, tx=1, rx=3)
        return super().readinto(*arg)

    def readline(self):
        if not self.redirect: super().init(115200, tx=1, rx=3)
        return super().readline()

    def write(self,*arg):
        if not self.redirect: super().init(115200, tx=1, rx=3)
        return super().write(*arg)
    

class Matrix(FrameBuffer):

    def __init__(self):
        self.buffer = bytearray(5)
        super().__init__(self.buffer, 5, 5, framebuf.MONO_VLSB)
        self.grid = 12
        self._pixel_o = (37, 5)

    def draw_pixel(self,x,y,c):
            pixel = (self._pixel_o[0]+x*self.grid, self._pixel_o[1]+y*self.grid)
            oled.fill_rect(pixel[0],pixel[1],int(self.grid/2),int(self.grid/2),c)

    def draw_matrix(self,buf):
        temp=bytearray(5)
        for i in range(5):
            temp[i]=(buf[i]<<3)&0xff
            for j in range(5):
                if temp[i] << j & 0x80:
                    self.draw_pixel(i, 4-j, 1)
                else:
                    self.draw_pixel(i,4-j,0)

    def get_char(self,char):
        buf = bytearray(5)
        buf_v = bytearray(5)
        index = 5*(ord(char)-32)
        temp = pendolino[index:index+5]
        for i in range(5):
            buf[i] = (temp[i] << 3) & 0xff
        for i in range(5):
            for j in range(5):
                buf_v[4-i] |= ((buf[j] >> (3+i) & 0x01) << j) & 0xff
        return buf_v
       
    def text(self,text):
        self.buffer_text= []
        text=str(text)
        self.text_length=len(text)
        for i in range(self.text_length):
            temp=self.get_char(text[i])
            temp_list=list(temp)
            self.buffer_text.extend(temp_list)
            self.buffer_text.append(0)
        self.buffer[:]=bytearray(self.buffer_text[0:5])[:]

    def left_shift(self, step):
        for i in range(step):
            self.buffer_text.append(self.buffer_text[0])
            self.buffer_text.pop(0)
        self.buffer[:]=bytearray(self.buffer_text[0:5])[:]
        self.show()

    def show(self):
        self.draw_matrix(self.buffer)
        oled.show()
      
class MicroBitImage():

    def __init__(self,*arg):
        self.buffer = bytearray()
        if len(arg)==1:
            if type(arg[0]) == str:
                self.buffer = self.str2bytes(arg[0])
                self._str = arg[0]
            else:
                raise TypeError("The argument must be a string" )
        else:
            self._weight =arg[0]
            self._height =arg[1]
            self.buffer = bytearray(arg[2])
            self._str = self.bytes2str(*arg)

    def __repr__(self):
        return 'Image({!r})'.format(self._str)

    def str2bytes(self,string):
        if string.find(":") ==-1:
            list_=string.split()
        else:
            list_ = string.split(":")
        self._height = len(list_)
        self._weight = len(list_[0])
        buf=bytearray()
        for raw in range(self._height):
            for col in range(self._weight):
                if int(list_[raw][col]):
                    buf.append(1)
                else:
                    buf.append(0)
        return buf

    def bytes2str(self,width,height,buf):
        list_=[""]*height
        for  h in range(height):
            for  w in range(width):
                if buf[h*height+w]:
                    list_[h]+="9"
                else:
                    list_[h]+="0"
        return ":".join(list_)

    def width(self):
        return self._weight

    def height(self):
        return self._height

class Image(MicroBitImage):

    HEART = MicroBitImage(5, 5, [
        0, 1, 0, 1, 0,
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1,
        0, 1, 1, 1, 0,
        0, 0, 1, 0, 0
    ])
    HEART_SMALL = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 1, 0, 1, 0,
        0, 1, 1, 1, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 0, 0
    ])
    HAPPY = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 1, 0, 1, 0,
        0, 0, 0, 0, 0,
        1, 0, 0, 0, 1,
        0, 1, 1, 1, 0
    ])

    SMILE = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 1, 0, 1, 0,
        0, 0, 0, 0, 0,
        1, 0, 0, 0, 1,
        0, 1, 1, 1, 0
    ])
    SAD = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 1, 0, 1, 0,
        0, 0, 0, 0, 0,
        0, 1, 1, 1, 0,
        1, 0, 0, 0, 1
    ])

    CONFUSED = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 1, 0, 1, 0,
        0, 0, 0, 0, 0,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1
    ])

    ANGRY = MicroBitImage(5, 5, [
        1, 0, 0, 0, 1,
        0, 1, 0, 1, 0,
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        1, 0, 1, 0, 1
    ])

    ASLEEP = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        1, 1, 0, 1, 1,
        0, 0, 0, 0, 0,
        0, 1, 1, 1, 0,
        0, 0, 0, 0, 0
    ])

    SURPRISED = MicroBitImage(5, 5, [
        0, 1, 0, 1, 0,
        0, 0, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 1, 0, 1, 0,
        0, 0, 1, 0, 0
    ])

    SILLY = MicroBitImage(5, 5, [
        1, 0, 0, 0, 1,
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 0, 1, 0, 1,
        0, 0, 1, 1, 1
    ])
    FABULOUS = MicroBitImage(5, 5, [
        1, 1, 1, 1, 1,
        1, 1, 0, 1, 1,
        0, 0, 0, 0, 0,
        0, 1, 0, 1, 0,
        0, 1, 1, 1, 0
    ])

    MEH = MicroBitImage(5, 5, [
        0, 1, 0, 1, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 1, 0,
        0, 0, 1, 0, 0,
        0, 1, 0, 0, 0
    ])

    YES = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 1,
        0, 0, 0, 1, 0,
        1, 0, 1, 0, 0,
        0, 1, 0, 0, 0
    ])

    NO = MicroBitImage(5, 5, [
        1, 0, 0, 0, 1,
        0, 1, 0, 1, 0,
        0, 0, 1, 0, 0,
        0, 1, 0, 1, 0,
        1, 0, 0, 0, 1
    ])

    CLOCK12 = MicroBitImage(5, 5, [
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0
    ])

    CLOCK1 = MicroBitImage(5, 5, [
        0, 0, 0, 1, 0,
        0, 0, 0, 1, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0
    ])

    CLOCK2 = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 0, 0, 1, 1,
        0, 0, 1, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0
    ])

    CLOCK3 = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 1, 1, 1,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0
    ])

    CLOCK4 = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 1, 1,
        0, 0, 0, 0, 0
    ])

    CLOCK5 = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 1, 0,
        0, 0, 0, 1, 0
    ])

    CLOCK6 = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0
    ])

    CLOCK7 = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 1, 0, 0, 0,
        0, 1, 0, 0, 0
    ])

    CLOCK8 = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 1, 0, 0,
        1, 1, 0, 0, 0,
        0, 0, 0, 0, 0
    ])

    CLOCK9 = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
        1, 1, 1, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0
    ])

    CLOCK10 = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        1, 1, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0
    ])

    CLOCK11 = MicroBitImage(5, 5, [
        0, 1, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0
    ])

    ARROW_N = MicroBitImage(5, 5, [
        0, 0, 1, 0, 0,
        0, 1, 1, 1, 0,
        1, 0, 1, 0, 1,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0
    ])

    ARROW_NE = MicroBitImage(5, 5, [
        0, 0, 1, 1, 1,
        0, 0, 0, 1, 1,
        0, 0, 1, 0, 1,
        0, 1, 0, 0, 0,
        1, 0, 0, 0, 0
    ])

    ARROW_E = MicroBitImage(5, 5, [
        0, 0, 1, 0, 0,
        0, 0, 0, 1, 0,
        1, 1, 1, 1, 1,
        0, 0, 0, 1, 0,
        0, 0, 1, 0, 0
    ])

    ARROW_SE = MicroBitImage(5, 5, [
        1, 0, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 0, 1, 0, 1,
        0, 0, 0, 1, 1,
        0, 0, 1, 1, 1
    ])

    ARROW_S = MicroBitImage(5, 5, [
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        1, 0, 1, 0, 1,
        0, 1, 1, 1, 0,
        0, 0, 1, 0, 0
    ])

    ARROW_SW = MicroBitImage(5, 5, [
        0, 0, 0, 0, 1,
        0, 0, 0, 1, 0,
        1, 0, 1, 0, 0,
        1, 1, 0, 0, 0,
        1, 1, 1, 0, 0
    ])
    ARROW_W = MicroBitImage(5, 5, [
        0, 0, 1, 0, 0,
        0, 1, 0, 0, 0,
        1, 1, 1, 1, 1,
        0, 1, 0, 0, 0,
        0, 0, 1, 0, 0
    ])
    ARROW_NW = MicroBitImage(5, 5, [
        1, 1, 1, 0, 0,
        1, 1, 0, 0, 0,
        1, 0, 1, 0, 0,
        0, 0, 0, 1, 0,
        0, 0, 0, 0, 1
    ])
    TRIANGLE = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 1, 0, 1, 0,
        1, 1, 1, 1, 1,
        0, 0, 0, 0, 0
    ])
    TRIANGLE_LEFT = MicroBitImage(5, 5, [
        1, 0, 0, 0, 0,
        1, 1, 0, 0, 0,
        1, 0, 1, 0, 0,
        1, 0, 0, 1, 0,
        1, 1, 1, 1, 1
    ])
    CHESSBOARD = MicroBitImage(5, 5, [
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1,
        0, 1, 0, 1, 0,
        1, 0, 1, 0, 1,
        0, 1, 0, 1, 0
    ])
    DIAMOND_SMALL = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 1, 0, 1, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 0, 0
    ])
    SQUARE = MicroBitImage(5, 5, [
        1, 1, 1, 1, 1,
        1, 0, 0, 0, 1,
        1, 0, 0, 0, 1,
        1, 0, 0, 0, 1,
        1, 1, 1, 1, 1
    ])
    SQUARE_SMALL = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 1, 1, 1, 0,
        0, 1, 0, 1, 0,
        0, 1, 1, 1, 0,
        0, 0, 0, 0, 0
    ])
    RABBIT = MicroBitImage(5, 5, [
        1, 0, 1, 0, 0,
        1, 0, 1, 0, 0,
        1, 1, 1, 1, 0,
        1, 1, 0, 1, 0,
        1, 1, 1, 1, 0
    ])
    COW = MicroBitImage(5, 5, [
        1, 0, 0, 0, 1,
        1, 0, 0, 0, 1,
        1, 1, 1, 1, 1,
        0, 1, 1, 1, 0,
        0, 0, 1, 0, 0
    ])
    CROTCHET = MicroBitImage(5, 5, [
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        1, 1, 1, 0, 0,
        1, 1, 1, 0, 0
    ])

    QUAVER = MicroBitImage(5, 5, [
        0, 0, 1, 0, 0,
        0, 0, 1, 1, 0,
        0, 0, 1, 0, 1,
        1, 1, 1, 0, 0,
        1, 1, 1, 0, 0
    ])

    QUAVERS = MicroBitImage(5, 5, [
        0, 1, 1, 1, 1,
        0, 1, 0, 0, 1,
        0, 1, 0, 0, 1,
        1, 1, 0, 1, 1,
        1, 1, 0, 1, 1
    ])
    PITCHFORK = MicroBitImage(5, 5, [
        1, 0, 1, 0, 1,
        1, 0, 1, 0, 1,
        1, 1, 1, 1, 1,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0
    ])
    XMAS = MicroBitImage(5, 5, [
        0, 0, 1, 0, 0,
        0, 1, 1, 1, 0,
        0, 0, 1, 0, 0,
        0, 1, 1, 1, 0,
        1, 1, 1, 1, 1
    ])
    PACMAN = MicroBitImage(5, 5, [
        0, 1, 1, 1, 1,
        1, 1, 0, 1, 0,
        1, 1, 1, 0, 0,
        1, 1, 1, 1, 0,
        0, 1, 1, 1, 1
    ])
    TARGET = MicroBitImage(5, 5, [
        0, 0, 1, 0, 0,
        0, 1, 1, 1, 0,
        1, 1, 0, 1, 1,
        0, 1, 1, 1, 0,
        0, 0, 1, 0, 0
    ])
    TSHIRT = MicroBitImage(5, 5, [
        1, 1, 0, 1, 1,
        1, 1, 1, 1, 1,
        0, 1, 1, 1, 0,
        0, 1, 1, 1, 0,
        0, 1, 1, 1, 0
    ])
    ROLLERSKATE = MicroBitImage(5, 5, [
        0, 0, 0, 1, 1,
        0, 0, 0, 1, 1,
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1,
        0, 1, 0, 1, 0
    ])
    DUCK = MicroBitImage(5, 5, [
        0, 1, 1, 0, 0,
        1, 1, 1, 0, 0,
        0, 1, 1, 1, 1,
        0, 1, 1, 1, 0,
        0, 0, 0, 0, 0
    ])
    HOUSE = MicroBitImage(5, 5, [
        0, 0, 1, 0, 0,
        0, 1, 1, 1, 0,
        1, 1, 1, 1, 1,
        0, 1, 1, 1, 0,
        0, 1, 0, 1, 0
    ])
    TORTOISE = MicroBitImage(5, 5, [
        0, 0, 0, 0, 0,
        0, 1, 1, 1, 0,
        1, 1, 1, 1, 1,
        0, 1, 0, 1, 0,
        0, 0, 0, 0, 0
    ])
    BUTTERFLY = MicroBitImage(5, 5, [
        1, 1, 0, 1, 1,
        1, 1, 1, 1, 1,
        0, 0, 1, 0, 0,
        1, 1, 1, 1, 1,
        1, 1, 0, 1, 1
    ])
    STICKFIGURE = MicroBitImage(5, 5, [
        0, 0, 1, 0, 0,
        1, 1, 1, 1, 1,
        0, 0, 1, 0, 0,
        0, 1, 0, 1, 0,
        1, 0, 0, 0, 1
    ])
    GHOST = MicroBitImage(5, 5, [
        1, 1, 1, 1, 1,
        1, 0, 1, 0, 1,
        1, 1, 1, 1, 1,
        1, 1, 1, 1, 1,
        1, 0, 1, 0, 1
    ])
    SWORD = MicroBitImage(5, 5, [
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 1, 0, 0,
        0, 1, 1, 1, 0,
        0, 0, 1, 0, 0
    ])
    GIRAFFE = MicroBitImage(5, 5, [
        1, 1, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 1, 1, 1, 0,
        0, 1, 0, 1, 0
    ])
    SKULL = MicroBitImage(5, 5, [
        0, 1, 1, 1, 0,
        1, 0, 1, 0, 1,
        1, 1, 1, 1, 1,
        0, 1, 1, 1, 0,
        0, 1, 1, 1, 0
    ])
    UMBRELLA = MicroBitImage(5, 5, [
        0, 1, 1, 1, 0,
        1, 1, 1, 1, 1,
        0, 0, 1, 0, 0,
        1, 0, 1, 0, 0,
        0, 1, 1, 0, 0
    ])
    SNAKE = MicroBitImage(5, 5, [
        1, 1, 0, 0, 0,
        1, 1, 0, 1, 1,
        0, 1, 0, 1, 0,
        0, 1, 1, 1, 0,
        0, 0, 0, 0, 0
    ])

class MicroBitDisplay():

    def __init__(self):
        self.matrix = Matrix()
        self.ison = True
        _thread.start_new_thread(self._loop, ())
        self.lock=_thread.allocate_lock()
        self.clear()

    def get_pixel(self, x, y):
        temp = (self.matrix.buffer[x] << 3) & 0xff
        if temp << 4-y & 0x80:
            return True
        else:
            return False

    def set_pixel(self, x, y, value):
        self.matrix.pixel(x,y,value)
        self.matrix.show()

    def clear(self):
        self.matrix.fill(0)
        self.matrix.show()

    def hline(self, *arg ,**kws):
        self.matrix.hline(*arg ,**kws)
        self.matrix.show()

    def vline(self, *arg ,**kws):
        self.matrix.vline(*arg ,**kws)
        self.matrix.show()

    def show(self, value,delay = 150,*,wait = True,loop = False,clear = False):
        if type(value) == MicroBitImage:
            img=value
            for h in range(5):
                for w in range(5):
                    if img.buffer[h*5+w]:
                        self.matrix.pixel(w,h,1)
                    else:
                        self.matrix.pixel(w,h,0)
            self.matrix.show()
        else:
            self.scroll(value,delay,wait=wait,loop=loop)
            if clear:
                self.clear()

    def scroll(self, value, delay=150, *, wait=True, loop=False, monospace=False):
        self._wait =wait
        self._value = value
        self._delay = delay
        while loop:
            self._text(value,delay)
        if self._wait and (not loop):
            self._text(value,delay)
        

    def _text(self,value,delay):
        self.matrix.text(value)
        self.matrix.show()
        time.sleep_ms(delay)
        if self.matrix.text_length >1:
            for i in range(len(self.matrix.buffer_text)-5):
                self.matrix.left_shift(1)
                time.sleep_ms(delay)
            

    def _loop(self):
        self._wait =True
        while True:
            if not self._wait:
                self._text(self._value,self._delay)
                self._wait= True

    def on(self):
        oled.poweron()
        self.ison = True

    def off(self):
        oled.poweroff()
        self.ison = False

    def is_on(self):
        return self.ison

class MicroBitPin:
    IN = 1
    OUT = 2
    PWM = 3
    ANALOG = 4

    def __init__(self, id):
        self.id = id
        self.current_mode = None
        self.mpython_pin = None

    def __change_pin_mode(self, pinmode):
        if self.current_mode is not pinmode:
            self.mpython_pin = MPythonPin(self.id, mode=pinmode)
            if pinmode == MicroBitPin.ANALOG:
                self.mpython_pin.adc.width(ADC.WIDTH_10BIT)
            self.current_mode = pinmode

    def read_digital(self):
        self.__change_pin_mode(MicroBitPin.IN)
        return self.mpython_pin.read_digital()

    def write_digital(self, value):
        self.__change_pin_mode(MicroBitPin.OUT)
        self.mpython_pin.write_digital(value)

    def read_analog(self):
        self.__change_pin_mode(MicroBitPin.ANALOG)
        return self.mpython_pin.read_analog()

    def write_analog(self, value):
        self.__change_pin_mode(MicroBitPin.PWM)
        self.mpython_pin.write_analog(value)

    def set_analog_period(period):
        #TODO
        pass

    def set_analog_period_microseconds(period):
        #TODO
        pass

uart = MicroBitUART()
display=MicroBitDisplay()
# Pin
pin0 = MicroBitPin(0)
pin1 = MicroBitPin(1)
pin2 = MicroBitPin(2)
pin3 = MicroBitPin(3)
pin4 = MicroBitPin(4)
pin5 = MicroBitPin(5)
pin6 = MicroBitPin(6)
pin7 = MicroBitPin(7)
pin8 = MicroBitPin(8)
pin9 = MicroBitPin(9)
pin10 = MicroBitPin(10)
pin11 = MicroBitPin(11)

pin13 = MicroBitPin(13)
pin14 = MicroBitPin(14)
pin15 = MicroBitPin(15)
pin16 = MicroBitPin(16)

pin19 = MicroBitPin(19)
pin20 = MicroBitPin(20)

def accelerometer_get_gestures():
    return (accelerometer.get_x(), accelerometer.get_y(), accelerometer.get_z())

accelerometer.get_gestures = accelerometer_get_gestures

try:
    from mpython import magnetic
except ImportError as e:
    pass
else:
    compass = magnetic
    compass.heading = magnetic.get_heading

gc.collect()

