# labplus mPython library
# MIT license; Copyright (c) 2018 labplus
# V1.0 Zhang KaiHua(apple_eat@126.com)

# mpython buildin periphers drivers

from machine import I2C, PWM, Pin, ADC, TouchPad
from ssd1106 import SSD1106_I2C
import esp
import ustruct
from neopixel import NeoPixel
from time import sleep_ms, sleep_us

pins_remap_esp32 = [33, 32, 35, 34, 39, 0, 16, 17, 26, 25, 
                    36,  2, -1, 18, 19, 21, 5, -1, -1, 22,
                    23,  -1, -1,
                    27, 14, 12, 13, 15, 4]

i2c = I2C(scl=Pin(22), sda=Pin(23), freq=400000)


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
        char_info_address = self.first_char_info_address + \
            (uni - self.first_char) * 6
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


class OLED(SSD1106_I2C):
    """ 128x64 oled display """
    def __init__(self):
        super().__init__(128, 64, i2c)
        self.f = Font()
        if self.f is None:
            raise Exception('font load failed')

    def DispChar(self, s, x, y, mode=TextMode.normal):
        if self.f is None:
            return
        for c in s:
            data = self.f.GetCharacterData(c)
            if data is None:
                x = x + self.width
                continue
            width, bytes_per_line = ustruct.unpack('HH', data[:4])
            # print('character [%d]: width = %d, bytes_per_line = %d' % (ord(c)
            # , width, bytes_per_line))
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
                            if mode == TextMode.normal or \
                               mode == TextMode.trans:
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
    
    def __init__(self, pin=6):
        self.id = pins_remap_esp32[pin]
        self.io = Pin(self.id) 
        self.io.value(1)
        self.isOn = False

    def on(self, freq=500):
        if self.isOn is False:
            self.pwm = PWM(self.io, freq, 512)
            self.isOn = True

    def off(self):
        if self.isOn:
            self.pwm.deinit()
            self.io.init(self.id, Pin.OUT)
            self.io.value(1)
            self.isOn = False


class PinMode(object):
    IN = 1
    OUT = 2
    PWM = 3
    ANALOG = 4


class MPythonPin(Pin):
    def __init__(self, pin, mode=PinMode.IN):
        if mode not in [PinMode.IN, PinMode.OUT, PinMode.PWM, PinMode.ANALOG]:
            raise TypeError("mode must be 'IN, OUT, PWM, ANALOG'")
        if pin == 3:
            raise TypeError("pin3 is used for resistance sensor")
        if pin == 4:
            raise TypeError("pin4 is used for light sensor")
        if pin == 10:
            raise TypeError("pin10 is used for sound sensor")
        self.id = pins_remap_esp32[pin]
        if mode == PinMode.IN:
            super().__init__(self.id, Pin.IN, Pin.PULL_UP)
        if mode == PinMode.OUT:
            if pin == 2:
                raise TypeError('pin2 only can be set "IN, ANALOG"')
            super().__init__(self.id, Pin.OUT)
        if mode == PinMode.PWM:
            if pin == 2:
                raise TypeError('pin2 only can be set "IN, ANALOG"')
            self.pwm = PWM(Pin(self.id), duty=0)
        if mode == PinMode.ANALOG:
            if pin not in [0, 1, 2, 3, 4, 10]:
                raise TypeError('the pin can~t be set as analog')
            self.adc = ADC(Pin(self.id))
            self.adc.atten(ADC.ATTN_11DB)
        self.mode = mode
        
    def read_digital(self):
        if not self.mode == PinMode.IN:
            raise TypeError('the pin is not in IN mode')
        return super().value()
        
    def write_digital(self, value):
        if not self.mode == PinMode.OUT:
            raise TypeError('the pin is not in OUT mode')
        super().value(value)
        
    def read_analog(self):
        if not self.mode == PinMode.ANALOG:
            raise TypeError('the pin is not in ANALOG mode')
        return self.adc.read()
        
    def write_analog(self, duty, freq=1000):
        if not self.mode == PinMode.PWM:
            raise TypeError('the pin is not in PWM mode')        
        self.pwm.freq(freq)
        self.pwm.duty(duty)
'''
# to be test
class LightSensor(ADC):
    
    def __init__(self):
        super().__init__(Pin(pins_remap_esp32[4]))
        # super().atten(ADC.ATTN_11DB)
    
    def value(self):
        # lux * k * Rc = N * 3.9/ 4096
        # k = 0.0011mA/Lux
        # lux = N * 3.9/ 4096 / Rc / k
        return super().read() * 1.1 / 4095 / 6.81 / 0.011
    
'''

# buzz
buzz = Buzz()

# display
oled = OLED()
display = oled

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

# touchpad
touchPad_P = TouchPad(Pin(27))
touchPad_Y = TouchPad(Pin(14))
touchPad_T = TouchPad(Pin(12))
touchPad_H = TouchPad(Pin(13))
touchPad_O = TouchPad(Pin(15))
touchPad_N = TouchPad(Pin(4))