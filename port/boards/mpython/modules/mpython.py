# labplus mPython library
# MIT license; Copyright (c) 2018 labplus
# V1.0 Zhang KaiHua(apple_eat@126.com)

# mpython buildin periphers drivers

# history:
# V1.1 add oled draw function,add buzz.freq().  by tangliufeng
# V1.2 add servo/ui class,by tangliufeng

from machine import I2C, PWM, Pin, ADC, TouchPad
from ssd1106 import SSD1106_I2C
import esp, math, time, network
import ustruct, array
from neopixel import NeoPixel
# from esp import dht_readinto
from time import sleep_ms, sleep_us, sleep
import framebuf 
import calibrate_img
from micropython import schedule,const
import NVS

i2c = I2C(0, scl=Pin(Pin.P19), sda=Pin(Pin.P20), freq=400000)

if '_print' not in dir(): _print = print

def print(_t, *args, sep=' ', end='\n'):
    _s = str(_t)[0:1]
    if u'\u4e00' <= _s <= u'\u9fff':
        _print(' ' + str(_t), *args, sep=sep, end=end)
    else:
        _print(_t, *args, sep=sep, end=end)

# my_wifi = wifi()
#多次尝试连接wifi
def try_connect_wifi(_wifi, _ssid, _pass, _times):
    if _times < 1: return False
    try:
        print("Try Connect WiFi ... {} Times".format(_times) )
        _wifi.connectWiFi(_ssid, _pass)
        if _wifi.sta.isconnected(): return True
        else:
            time.sleep(5)
            return try_connect_wifi(_wifi, _ssid, _pass, _times-1)
    except:
        time.sleep(5)
        return try_connect_wifi(_wifi, _ssid, _pass, _times-1)

class Font(object):
    def __init__(self, font_address=0x400000):
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
        # if uni not in range(self.first_char, self.last_char):
        #     return None
        if (uni < self.first_char or uni > self.last_char):
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

    def DispChar(self, s, x, y, mode=TextMode.normal, auto_return=False):
            row = 0
            str_width = 0
            if self.f is None:
                return
            for c in s:
                data = self.f.GetCharacterData(c)
                if data is None:
                    if auto_return is True:
                        x = x + self.f.width
                    else:
                        x = x + self.width
                    continue
                width, bytes_per_line = ustruct.unpack('HH', data[:4])
                # print('character [%d]: width = %d, bytes_per_line = %d' % (ord(c)
                # , width, bytes_per_line))
                if auto_return is True:
                    if x > self.width - width:
                        str_width += self.width - x
                        x = 0
                        row += 1
                        y += self.f.height
                        if y > (self.height - self.f.height)+0:
                            y, row = 0, 0
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
                                    c = self.buffer[page * (self.width if auto_return is True else 128) + px] & bit
                                    if c != 0:
                                        c = 0
                                    else:
                                        c = 1
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
                str_width += width + 1
            return (str_width-1,(x-1, y))

    def DispChar_font(self, font, s, x, y, invert=False):
        """
        custom font display.Ref by , https://github.com/peterhinch/micropython-font-to-py
        :param font:  use font_to_py.py script convert to `py` from `ttf` or `otf`.
        """
        screen_width = self.width
        screen_height = self.height
        text_row = x
        text_col = y
        text_length = 0
        if font.hmap():
            font_map = framebuf.MONO_HMSB if font.reverse() else framebuf.MONO_HLSB
        else:
            raise ValueError('Font must be horizontally mapped.')
        for c in s:
            glyph, char_height, char_width = font.get_ch(c)
            buf = bytearray(glyph)
            if invert:
                for i, v in enumerate(buf):
                    buf[i] = 0xFF & ~ v
            fbc = framebuf.FrameBuffer(buf, char_width, char_height, font_map)
            if text_row + char_width > screen_width - 1:
                text_length += screen_width-text_row
                text_row = 0
                text_col += char_height
            if text_col + char_height > screen_height + 2:
                text_col = 0

            super().blit(fbc, text_row, text_col)
            text_row = text_row + char_width+1
            text_length += char_width+1
        return (text_length-1, (text_row-1, text_col))

# display
if 60 in i2c.scan():
    oled = OLED()
    display = oled
else:
    pass

class MOTION(object):
    def __init__(self):
        self.i2c = i2c
        addr = self.i2c.scan()
        if 38 in addr:
            MOTION.chip = 1  # MSA300
            MOTION.IIC_ADDR = 38
        elif 107 in addr:
            MOTION.chip = 2  # QMI8658
            MOTION.IIC_ADDR = 107
        else:
            raise OSError("MOTION init error")
        if(MOTION.chip == 1):
            pass
        elif(MOTION.chip == 2):
            MOTION._writeReg(0x60, 0x01) # soft reset regist value.
            time.sleep_ms(20)
            MOTION._writeReg(0x02, 0x60) # Enabe reg address auto increment auto
            MOTION._writeReg(0x08, 0x03) # Enable accel and gyro
            MOTION._writeReg(0x03, 0x1c) # accel range:4g ODR 128HZ
            MOTION._writeReg(0x04, 0x40) # gyro ODR 8000HZ, FS 256dps
            MOTION._writeReg(0x06, 0x55) # Enable accel and gyro Low-Pass Filter
        # print('Motion init finished!')

    # @staticmethod
    def _readReg(reg, nbytes=1):
        return i2c.readfrom_mem(MOTION.IIC_ADDR, reg, nbytes)

    # @staticmethod
    def _writeReg(reg, value):
        i2c.writeto_mem(MOTION.IIC_ADDR, reg, value.to_bytes(1, 'little'))

    def get_fw_version(self):
        if(self.chip==1):
            pass
        elif(self.chip==2):
            MOTION._writeReg(0x0a, 0x10) # send ctrl9R read FW cmd
            while True:
                if (MOTION._readReg(0x2F, 1)[0] & 0X01) == 0X01:
                    break
            buf = MOTION._readReg(0X49, 3)
            # print(buf[0])
            # print(buf[1])
            # print(buf[2])
        
    class Accelerometer():
        """MSA300"""
        # Range and resolustion
        RANGE_2G = const(0)
        RANGE_4G = const(1)
        RANGE_8G = const(2)
        RANGE_16G = const(3)
        RES_14_BIT = const(0) 
        RES_12_BIT = const(1)
        RES_10_BIT = const(2)
        # Event
        TILT_LEFT = const(0)
        TILT_RIGHT = const(1)
        TILT_UP = const(2)
        TILT_DOWN = const(3)
        FACE_UP = const(4)
        FACE_DOWN = const(5)
        SINGLE_CLICK = const(6)
        DOUBLE_CLICK = const(7)
        FREEFALL = const(8)

        """QMI8658C"""
        # Range and resolustion
        # QMI8658C_RANGE_2G = const(0x00)
        # QMI8658C_RANGE_4G = const(0x10)
        # QMI8658C_RANGE_8G = const(0x20)
        # QMI8658C_RANGE_16G = const(0x40)

        def __init__(self):
            if(MOTION.chip==1):
                self.set_resolution(MOTION.Accelerometer.RES_10_BIT)
                self.set_range(MOTION.Accelerometer.RANGE_2G)
                MOTION._writeReg(0x12, 0x03)               # polarity of y,z axis,
                MOTION._writeReg(0x11, 0)                  # set power mode = normal
                # interrupt
                MOTION._writeReg(0x16, 0x70)      # int enabled: Orient | S_TAP | D_TAP 
                MOTION._writeReg(0x17, 0x08)      # int enabled: Freefall
                MOTION._writeReg(0x19, 0x71)      # int1 map to: Orient, S_TAP, D_TAP, Freefall
                MOTION._writeReg(0x20, 0x02)      # int1 active level = 0, output = OD
                MOTION._writeReg(0x21, 0x0C)      # int tempoary latched 25ms
                # freefall:
                #   single mode: |acc_x| < Threshold && |acc_y| < Threshold && |acc_z| < Threshold, at least time > Duration
                #   sum mode: |acc_x| + |acc_y| + |acc_z| < Threshold, at least time > Duration
                MOTION._writeReg(0x22, 20)    # Freefall Duration:(n+1)*2ms, range from 2ms to 512ms
                MOTION._writeReg(0x23, 48)    # Freefall Threshold: n*7.81mg
                MOTION._writeReg(0x24, 0x01)  # Freefall mode = 0-singlemode;hysteresis = n*125mg
                # tap:
                MOTION._writeReg(0x2A, 0x06)  # Tap duration:quit = 30ms, shock=50ms, time window for secent shock=500ms
                MOTION._writeReg(0x2B, 0x0A)  # Tap threshold = 10*[62.5mg@2G | 125mg@4G | 250mg@8G | 500mg@16g]
                # Orient
                MOTION._writeReg(0x2C, 0x18)  # Orient hysteresis= 1*62.5mg; 
                                            #        block mode = 10 z_axis blocking or slope in any axis > 0.2g;
                                            #        orient mode = 00-symetrical
                MOTION._writeReg(0x2D, 8)     # Z-axis block
                # int pin irq register
                self.int = Pin(37, Pin.IN)
                self.int.irq(trigger=Pin.IRQ_FALLING, handler=self.irq)
                # event handler 
                self.event_tilt_up = None
                self.event_tilt_down = None
                self.event_tilt_left = None
                self.event_tilt_right = None
                self.event_face_up = None
                self.event_face_down = None
                self.event_single_click = None
                self.event_double_click = None
                self.event_freefall = None
            elif(MOTION.chip==2):
                # 设置偏移值
                self.x_offset = 0
                self.y_offset = 0
                self.z_offset = 0
                self.get_nvs_offset()
                try:
                    id =  MOTION._readReg(0x0, 2)
                except:
                    pass
                self.set_range(MOTION.Accelerometer.RANGE_2G) #设置默认分辨率+-2g
                self.int = Pin(37, Pin.IN)
                self.int.irq(trigger=Pin.IRQ_FALLING, handler=self.irq)
                # event handler 
                self.wom = None
            

        def irq(self, arg):
            if(MOTION.chip==1):
                reg_int = MOTION._readReg(0x09)[0]
                reg_orent = MOTION._readReg(0x0C)[0]
                # orient_int
                if (reg_int & 0x40):
                    if ((reg_orent & 0x30) == 0x00 and self.event_tilt_left is not None):
                        schedule(self.event_tilt_left, self.TILT_LEFT)
                    if ((reg_orent & 0x30) == 0x10 and self.event_tilt_right is not None):
                        schedule(self.event_tilt_right, self.TILT_RIGHT)
                    if ((reg_orent & 0x30) == 0x20 and self.event_tilt_up is not None):
                        schedule(self.event_tilt_up, self.TILT_UP)
                    if ((reg_orent & 0x30) == 0x30 and self.event_tilt_down is not None):
                        schedule(self.event_tilt_down, self.TILT_DOWN)
                    if ((reg_orent & 0x40) == 0x00 and self.event_face_up):
                        schedule(self.event_face_up, self.FACE_UP)
                    if ((reg_orent & 0x40) == 0x40 and self.event_face_down):
                        schedule(self.event_face_down, self.FACE_DOWN)
                # single tap
                if (reg_int & 0x20):
                    if (self.event_single_click is not None):
                        schedule(self.event_single_click, self.SINGLE_CLICK)
                # double tap
                if (reg_int & 0x10):
                    if (self.event_double_click is not None):
                        schedule(self.event_double_click, self.DOUBLE_CLICK)
                # freefall
                if (reg_int & 0x01):
                    if (self.event_freefall is not None):
                        schedule(self.event_freefall, self.FREEFALL)
                # print("acc sensor interrupt, because 0x%2x, orient = 0x%2x" % (reg_int, reg_orent))
            elif(MOTION.chip==2):  
                flag = MOTION._readReg(0x2F, 1)[0]
                if (flag & 0x04) == 0x04:
                    print('wom int trigged.')

        def wom_config(self):
            if(MOTION.chip==1):
                pass
            elif(MOTION.chip==2):
                MOTION._writeReg(0x60, 0x01) # soft reset regist value.
                time.sleep_ms(20)
                MOTION._writeReg(0x08, 0x0) # disable all sensor
                MOTION._writeReg(0x03, 0x1c) # accel range:4g ODR 128HZ
                MOTION._writeReg(0x0B, 0xfF) # CAL_L WoM Threshold(1mg/LSB resolution)
                MOTION._writeReg(0x0C, 0x8F) # CAL_H WoM (INT1 blank time 0x1f)
                MOTION._writeReg(0x0A, 0x08)
                while True:
                    if (MOTION._readReg(0x2F, 1)[0] & 0X01) == 0X01:
                        break
                MOTION._writeReg(0x08, 0x01) # enable accel

        def set_resolution(self, resolution):# set data output rate
            if(MOTION.chip==1):
                format = MOTION._readReg(0x0f, 1)
                format = format[0] & ~0xC
                format |= (resolution << 2)
                MOTION._writeReg(0x0f, format)
            elif(MOTION.chip==2):
                self.odr = resolution
                format = MOTION._readReg(0x03, 1)
                format = format[0] & 0xf0
                format |= (resolution & 0x0f)
                MOTION._writeReg(0x03, format)
                
        def set_range(self, range):
            if(MOTION.chip==1):
                self.range = range
                format = MOTION._readReg(0x0f, 1)
                format = format[0] & ~0x3
                format |= range
                MOTION._writeReg(0x0f, format)
            elif(MOTION.chip==2):
                if(range==3):
                    range = 64 #0x40
                else:
                    range = range << 4
                self.FS = 2*(2**(range >> 4))
                format = MOTION._readReg(0x03, 1)
                format = format[0] & 0x8F
                format |= range
                MOTION._writeReg(0x03, format)

        def set_offset(self, x=None, y=None, z=None):
            if(MOTION.chip==1):
                for i in (x, y, z):
                    if i is not None:
                        if i < -1 or i > 1:
                            raise ValueError("out of range,only offset 1 gravity")
                if x is not None:
                    MOTION._writeReg(0x39, int(round(x/0.0039)))
                elif y is not None:
                    MOTION._writeReg(0x38, int(round(y/0.0039)))
                elif z is not None:
                    MOTION._writeReg(0x3A, int(round(z/0.0039)))
            elif(MOTION.chip==2):
                for i in (x, y, z):
                    if i is not None:
                        if i < -16 or i > 16:
                            raise ValueError("超出调整范围!!!")
                if x is not None:
                    self.x_offset = x
                    self.set_nvs_offset("x", x)
                if y is not None:
                    self.y_offset = y
                    self.set_nvs_offset("y", y)
                if z is not None:
                    self.z_offset = z
                    self.set_nvs_offset("z", z)
                
        def get_x(self):
            if(MOTION.chip==1):
                retry = 0
                if (retry < 5):
                    try:
                        buf = MOTION._readReg(0x02, 2)
                        x = ustruct.unpack('h', buf)[0]
                        return x / 4 / 4096 * 2**self.range
                    except:
                        retry = retry + 1
                else:
                    raise Exception("i2c read/write error!")
            elif(MOTION.chip==2):
                buf = MOTION._readReg(0x35, 2)
                x = ustruct.unpack('<h', buf)[0]
                return (x * self.FS) / 32768 + self.x_offset

        def get_y(self):
            if(MOTION.chip==1):
                retry = 0
                if (retry < 5):
                    try:
                        buf = MOTION._readReg(0x04, 2)
                        y = ustruct.unpack('h', buf)[0]
                        return y / 4 / 4096 * 2**self.range
                    except:
                        retry = retry + 1
                else:
                    raise Exception("i2c read/write error!")
            elif(MOTION.chip==2):
                buf = MOTION._readReg(0x37, 2)
                y = ustruct.unpack('<h', buf)[0]
                return (y * self.FS) / 32768  + self.y_offset

        def get_z(self):
            if(MOTION.chip==1):
                retry = 0
                if (retry < 5):
                    try:
                        buf = MOTION._readReg(0x06, 2)
                        z = ustruct.unpack('h', buf)[0]
                        return z / 4 / 4096 * 2**self.range
                    except:
                        retry = retry + 1
                else:
                    raise Exception("i2c read/write error!")
            elif(MOTION.chip==2):
                buf = MOTION._readReg(0x39, 2)
                z = ustruct.unpack('<h', buf)[0]
                return (z * self.FS) / 32768 + self.z_offset
                # return -(z * self.FS) / 32768
     
        def roll_pitch_angle(self):
            x, y, z = self.get_x(), self.get_y(), -self.get_z()
            # vector normalize
            mag = math.sqrt(x ** 2 + y ** 2+z ** 2)
            x /= mag
            y /= mag
            z /= mag
            roll = math.degrees(-math.asin(y))
            pitch = math.degrees(math.atan2(x, z))

            return roll, pitch
        
        def get_nvs_offset(self):
            try:
                tmp = NVS("offset_a")
                self.x_offset = round(tmp.get_i32("x")/1e5, 5)
                self.y_offset = round(tmp.get_i32("y")/1e5, 5)
                self.z_offset = round(tmp.get_i32("z")/1e5, 5)
            except OSError as e:
                # print('Accelerometer get_nvs_offset:',e)
                # self.x_offset = 0
                # self.y_offset = 0
                # self.z_offset = 0
                self.set_offset(0,0,0)
        
        def set_nvs_offset(self, key, value):
            try:
                nvs = NVS("offset_a")
                nvs.set_i32(key, int(value*1e5))
                nvs.commit()
            except OSError as e:
                print('Gyroscope set_nvs_offset error:',e)

    class Gyroscope():
        # gyro full scale
        RANGE_16_DPS =  const(0x00)
        RANGE_32_DPS =  const(0x10)
        RANGE_64_DPS =  const(0x20)
        RANGE_128_DPS =  const(0x30)
        RANGE_256_DPS =  const(0x40)
        RANGE_512_DPS =  const(0x50)
        RANGE_1024_DPS = const(0x60)
        RANGE_2048_DPS = const(0x70)

        def __init__(self):
            if(MOTION.chip==1):
                pass
            elif(MOTION.chip==2):
                # 设置偏移值
                self.x_offset = 0
                self.y_offset = 0
                self.z_offset = 0
                self.get_nvs_offset()
                self.set_range(MOTION.Gyroscope.RANGE_256_DPS)

        def set_range(self, range):
            if(MOTION.chip==1):
                pass
            elif(MOTION.chip==2):
                self.FS = 16*(2**(range >> 4))        
                format = MOTION._readReg(0x04, 1)
                format = format[0] & 0x8F
                format |= range
                MOTION._writeReg(0x04, format)

        def set_ODR(self, odr):  # set data output rate
            if(MOTION.chip==1):
                pass
            elif(MOTION.chip==2):
                self.odr = odr
                format = MOTION._readReg(0x04, 1)
                format = format[0] & 0xF0
                format |= odr
                MOTION._writeReg(0x04, format)

        def get_x(self):
            if(MOTION.chip==1):
                pass
            elif(MOTION.chip==2):
                buf = MOTION._readReg(0x3b, 2)
                x = ustruct.unpack('<h', buf)[0]
                return (x * self.FS) / 32768 + self.x_offset

        def get_y(self):
            if(MOTION.chip==1):
                pass
            elif(MOTION.chip==2):
                buf = MOTION._readReg(0x3d, 2)
                y = ustruct.unpack('<h', buf)[0]
                return (y * self.FS) / 32768 + self.y_offset

        def get_z(self):
            if(MOTION.chip==1):
                pass
            elif(MOTION.chip==2):
                buf = MOTION._readReg(0x3f, 2)
                z = ustruct.unpack('<h', buf)[0]
                return (z * self.FS) / 32768 + self.z_offset
        
        def set_offset(self, x=None, y=None, z=None):
            if(MOTION.chip==1):
                pass
            elif(MOTION.chip==2):
                for i in (x, y, z):
                    if i is not None:
                        if i < -4096 or i > 4096:
                            raise ValueError("超出调整范围!!!")
                if x is not None:
                    self.x_offset = x
                    self.set_nvs_offset("x", x)
                if y is not None:
                    self.y_offset = y
                    self.set_nvs_offset("y", y)
                if z is not None:
                    self.z_offset = z
                    self.set_nvs_offset("z", z)

        def get_nvs_offset(self):
            if(MOTION.chip==1):
                pass
            elif(MOTION.chip==2):
                try:
                    tmp = NVS("offset_g")
                    self.x_offset = round(tmp.get_i32("x")/1e5, 5)
                    self.y_offset = round(tmp.get_i32("y")/1e5, 5)
                    self.z_offset = round(tmp.get_i32("z")/1e5, 5)
                except OSError as e:
                    # print('Gyroscope get_nvs_offset:',e)
                    self.set_offset(0,0,0)
                    # self.x_offset = 0
                    # self.y_offset = 0
                    # self.z_offset = 0

        def set_nvs_offset(self, key, value):
            try:
                nvs = NVS("offset_g")
                nvs.set_i32(key, int(value*1e5))
                nvs.commit()
            except OSError as e:
                print('Gyroscope set_nvs_offset error:',e)

    
motion = MOTION()
accelerometer = motion.Accelerometer()
gyroscope = motion.Gyroscope()

class Magnetic(object):
    """ MMC5983MA driver """
    """ MMC5603NJ driver 20211028替换"""
    def __init__(self):
        self.addr = 48
        self.i2c = i2c
        self._judge_id()
        time.sleep_ms(5)
        if (self.product_ID==48):
            pass  # MMC5983MA
        elif (self.product_ID==16):
            pass  # MMC5603NJ
        else:
            raise OSError("Magnetic init error")
        """ MMC5983MA driver """
        # 传量器裸数据，乘0.25后转化为mGS
        self.raw_x = 0.0
        self.raw_y = 0.0
        self.raw_z = 0.0
        # 校准后的偏移量, 基于裸数据
        self.cali_offset_x = 0.0 
        self.cali_offset_y = 0.0
        self.cali_offset_z = 0.0
        # 去皮偏移量，类似电子秤去皮功能，基于裸数据。
        self.peeling_x = 0.0
        self.peeling_y = 0.0
        self.peeling_z = 0.0
        self.is_peeling = 0
        if (self.chip==1):
            self.i2c.writeto(self.addr, b'\x09\x20\xbd\x00', True)
        """ MMC5603NJ driver """
        if (self.chip==2):
            self._writeReg(0x1C, 0x80)#软件复位
            time.sleep_ms(100)
            self._writeReg(0x1A, 255)
            self._writeReg(0x1B, 0b10100001)
            # self._writeReg(0x1C, 0b00000011)
            self._writeReg(0x1C, 0b00000000)
            self._writeReg(0x1D, 0b10010000)
            time.sleep_ms(100)

    def _readReg(self, reg, nbytes=1):
        return i2c.readfrom_mem(self.addr, reg, nbytes)

    def _writeReg(self, reg, value):
        i2c.writeto_mem(self.addr, reg, value.to_bytes(1, 'little')) 

    def _set_offset(self):
        if(self.chip == 1):
            self.i2c.writeto(self.addr, b'\x09\x08', True)  #set
            self.i2c.writeto(self.addr, b'\x09\x01', True)
            while True:
                self.i2c.writeto(self.addr, b'\x08', False)
                buf = self.i2c.readfrom(self.addr, 1)
                status = ustruct.unpack('B', buf)[0]
                if(status & 0x01):
                    break
            self.i2c.writeto(self.addr, b'\x00', False)
            buf = self.i2c.readfrom(self.addr, 6)
            data = ustruct.unpack('>3H', buf)

            self.i2c.writeto(self.addr, b'\x09\x10', True)  #reset

            self.i2c.writeto(self.addr, b'\x09\x01', True)
            while True:
                self.i2c.writeto(self.addr, b'\x08', False)
                buf = self.i2c.readfrom(self.addr, 1)
                status = ustruct.unpack('B', buf)[0]
                if(status & 0x01):
                    break
            self.i2c.writeto(self.addr, b'\x00', False)
            buf = self.i2c.readfrom(self.addr, 6)
            data1 = ustruct.unpack('>3H', buf)

            self.x_offset = (data[0] + data1[0])/2
            self.y_offset = (data[1] + data1[1])/2
            self.z_offset = (data[2] + data1[2])/2
        elif(self.chip == 2):
            pass
    
    def _get_raw(self):
        if (self.chip == 1):
            retry = 0
            if (retry < 5):
                try:
                    self.i2c.writeto(self.addr, b'\x09\x08', True)  #set

                    self.i2c.writeto(self.addr, b'\x09\x01', True)
                    while True:
                        self.i2c.writeto(self.addr, b'\x08', False)
                        buf = self.i2c.readfrom(self.addr, 1)
                        status = ustruct.unpack('B', buf)[0]
                        if(status & 0x01):
                            break
                    self.i2c.writeto(self.addr, b'\x00', False)
                    buf = self.i2c.readfrom(self.addr, 6)
                    data = ustruct.unpack('>3H', buf)

                    self.i2c.writeto(self.addr, b'\x09\x10', True)  #reset

                    self.i2c.writeto(self.addr, b'\x09\x01', True)
                    while True:
                        self.i2c.writeto(self.addr, b'\x08', False)
                        buf = self.i2c.readfrom(self.addr, 1)
                        status = ustruct.unpack('B', buf)[0]
                        if(status & 0x01):
                            break
                    self.i2c.writeto(self.addr, b'\x00', False)
                    buf = self.i2c.readfrom(self.addr, 6)
                    data1 = ustruct.unpack('>3H', buf)

                    self.raw_x = -((data[0] - data1[0])/2)
                    self.raw_y = -((data[1] - data1[1])/2)
                    self.raw_z = -((data[2] - data1[2])/2)
                    # print(str(self.raw_x) + "   " + str(self.raw_y) + "  " + str(self.raw_z))
                except:
                    retry = retry + 1
            else:
                raise Exception("i2c read/write error!")     
        elif(self.chip == 2):
            retry = 0
            if (retry < 5):
                try:
                    _raw_x = 0.0
                    _raw_y = 0.0
                    _raw_z = 0.0

                    # self.i2c.writeto(self.addr, b'\x1B\x08', True)  #set
                    # self.i2c.writeto(self.addr, b'\x1B\x01', True)
                    
                    # while True:
                    #     buf = self._readReg(0x18, 1)
                    #     status = buf[0]
                    #     if(status & 0x40):
                    #         break

                    # _buf = self._readReg(0x00, 9)

                    self.i2c.writeto(self.addr, b'\x1B\x08', True)  #set
                    # self.i2c.writeto(self.addr, b'\x1B\x80', True)
                    self.i2c.writeto(self.addr, b'\x1B\x01', True)
                    
                    while True:
                        sleep_ms(25)
                        buf = self._readReg(0x18, 1)
                        status = buf[0]
                        if(status & 0x40):
                            break

                    buf = self._readReg(0x00, 9)

                    _raw_x = (buf[0] << 12) | (buf[1] << 4) | (buf[6] >> 4)
                    _raw_y = (buf[2] << 12) | (buf[3] << 4) | (buf[7] >> 4)
                    _raw_z = (buf[4] << 12) | (buf[5] << 4) | (buf[8] >> 4)

                    self.raw_x = _raw_x
                    self.raw_y = _raw_y
                    self.raw_z = _raw_z
                except:
                    retry = retry + 1
            else:
                raise Exception("i2c read/write error!")

    def peeling(self):
        '''
        去除磁场环境
        '''
        self._get_raw()
        self.peeling_x = self.raw_x
        self.peeling_y = self.raw_y
        self.peeling_z = self.raw_z
        self.is_peeling = 1

    def clear_peeling(self):
        self.peeling_x = 0.0
        self.peeling_y = 0.0
        self.peeling_z = 0.0
        self.is_peeling = 0

    def get_x(self):
        if (self.chip == 1):
            self._get_raw()
            return self.raw_x * 0.25
        if (self.chip == 2):
            self._get_raw()
            if(self.cali_offset_x):
                return -0.0625 * (self.raw_x - self.cali_offset_x)
            else:
                return -0.0625 * (self.raw_x - 524288)
            # return -(self.raw_x - 524288)/16384

    def get_y(self):
        if (self.chip == 1):
            self._get_raw()
            return self.raw_y * 0.25
        if (self.chip == 2):
            self._get_raw()
            if(self.cali_offset_y):
                return -0.0625 * (self.raw_y - self.cali_offset_y)
            else:
                return -0.0625 * (self.raw_y - 524288)
            # return -(self.raw_y - 524288)/16384

    def get_z(self):
        if (self.chip == 1):
            self._get_raw()
            return self.raw_z * 0.25 
        if (self.chip == 2):
            self._get_raw()
            if(self.cali_offset_z):
                return 0.0625 * (self.raw_z - self.cali_offset_z)
            else:
                return 0.0625 * (self.raw_z - 524288)
            # return (self.raw_z - 524288)/16384

    def get_field_strength(self):
        if(self.chip==1):
            self._get_raw()
            if self.is_peeling == 1:
                return (math.sqrt((self.raw_x - self.peeling_x)*(self.raw_x - self.peeling_x) + (self.raw_y - self.peeling_y)*(self.raw_y - self.peeling_y) + (self.raw_z - self.peeling_z)*(self.raw_z - self.peeling_z)))*0.25
            return (math.sqrt(self.raw_x * self.raw_x + self.raw_y * self.raw_y + self.raw_z * self.raw_z))*0.25
        elif(self.chip==2):
            self._get_raw()
            if self.is_peeling == 1:
                return (math.sqrt(math.pow(self.raw_x - self.peeling_x, 2) + pow(self.raw_y - self.peeling_y, 2) + pow(self.raw_z - self.peeling_z , 2)))*0.0625
            return (math.sqrt(math.pow(self.get_x(), 2) + pow(self.get_y(), 2) + pow(self.get_z(), 2)))

    def calibrate(self):
        oled.fill(0)
        oled.DispChar("步骤1:", 0,0,1)
        oled.DispChar("如图",0,26,1)
        oled.DispChar("转几周",0,43,1)
        oled.bitmap(64,0,calibrate_img.rotate,64,64,1)
        oled.show()
        self._get_raw()
        min_x = max_x = self.raw_x
        min_y = max_y = self.raw_y
        min_z = max_z = self.raw_z
        ticks_start = time.ticks_ms()
        while (time.ticks_diff(time.ticks_ms(), ticks_start) < 15000) :
            self._get_raw()
            min_x = min(self.raw_x, min_x)
            min_y = min(self.raw_y, min_y)
            max_x = max(self.raw_x, max_x)
            max_y = max(self.raw_y, max_y)
            time.sleep_ms(100)
        self.cali_offset_x = (max_x + min_x) / 2
        self.cali_offset_y = (max_y + min_y) / 2
        print('cali_offset_x: ' + str(self.cali_offset_x) + '  cali_offset_y: ' + str(self.cali_offset_y))
        oled.fill(0)
        oled.DispChar("步骤2:", 85,0,1)
        oled.DispChar("如图",85,26,1)
        oled.DispChar("转几周",85,43,1)
        oled.bitmap(0,0,calibrate_img.rotate1,64,64,1)
        oled.show()
        ticks_start = time.ticks_ms()
        while (time.ticks_diff(time.ticks_ms(), ticks_start) < 15000) :
            self._get_raw()
            min_z = min(self.raw_z, min_z)
            max_z = max(self.raw_z, max_z)
            time.sleep_ms(100)
        self.cali_offset_z = (max_z + min_z) / 2
  
        print('cali_offset_z: ' + str(self.cali_offset_z))

        oled.fill(0)
        oled.DispChar("校准完成", 40,24,1)
        oled.show()
        oled.fill(0)

    def get_heading(self):
        if(self.chip==1):
            self._get_raw()
            temp_x = self.raw_x - self.cali_offset_x
            temp_y = self.raw_y - self.cali_offset_y
            # temp_z = self.raw_z - self.cali_offset_z
            heading = math.atan2(temp_y, -temp_x) * (180 / 3.14159265) + 180 + 3
            return heading
        else:
            if(self.cali_offset_x):
                self._get_raw()
                temp_x = -(self.raw_x - self.cali_offset_x)
                temp_y = -(self.raw_y - self.cali_offset_y)
                heading = math.atan2(temp_y, -temp_x) * (180 / 3.14159265) + 180 + 3
            else:
                heading = math.atan2(self.get_y(), -self.get_x()) * (180 / 3.14159265) + 180 + 3
            return heading
        
    def _get_temperature(self):
        if(self.chip==1):
            retry = 0
            if (retry < 5):
                try:
                    self.i2c.writeto(self.addr, b'\x09\x02', True)
                    while True:
                        self.i2c.writeto(self.addr, b'\x08', False)
                        buf = self.i2c.readfrom(self.addr, 1)
                        status = ustruct.unpack('B', buf)[0]
                        if(status & 0x02):
                            break
                    self.i2c.writeto(self.addr, b'\x07', False)
                    buf = self.i2c.readfrom(self.addr, 1)
                    temp = (ustruct.unpack('B', buf)[0])*0.8 -75
                    # print(data)
                    return temp
                except:
                    retry = retry + 1
            else:
                raise Exception("i2c read/write error!")   
        elif(self.chip == 2):
            pass

    def _get_id(self):
        if (self.chip==1):
            retry = 0
            if (retry < 5):
                try:
                    self.i2c.writeto(self.addr, bytearray([0x2f]), False)
                    buf = self.i2c.readfrom(self.addr, 1, True)
                    print(buf)
                    id = ustruct.unpack('B', buf)[0]
                    return id
                except:
                    retry = retry + 1
            else:
                raise Exception("i2c read/write error!")
        elif (self.chip==2):
            retry = 0
            if (retry < 5):
                try:
                    self.i2c.writeto(self.addr, bytearray([0x39]), False)
                    buf = self.i2c.readfrom(self.addr, 1, True)
                    id = ustruct.unpack('B', buf)[0]
                    return id
                except:
                    retry = retry + 1
            else:
                raise Exception("i2c read/write error!")

    def _judge_id(self):
        """
        判断product_ID
        """
        retry = 0
        if (retry < 5):
            try:
                self.i2c.writeto(self.addr, bytearray([0x39]), False)
                buf = self.i2c.readfrom(self.addr, 1, True)
                id = ustruct.unpack('B', buf)[0]
                if(id == 16):
                    self.chip = 2
                    self.product_ID = 16
                else:
                    self.chip = 1
                    self.product_ID = 48
            except:
                retry = retry + 1
        else:
            raise Exception("i2c read/write error!") 

# Magnetic
if 48 in i2c.scan():
    magnetic = Magnetic()

class BME280(object):
    def __init__(self):
        self.addr = 119
        # The “ctrl_hum” register sets the humidity data acquisition options of the device
        # 0x01 = [2:0]oversampling ×1
        i2c.writeto(self.addr, b'\xF2\x01')
        # The “ctrl_meas” register sets the pressure and temperature data acquisition options of the device.
        # The register needs to be written after changing “ctrl_hum” for the changes to become effective.
        # 0x27 = [7:5]Pressure oversampling ×1 | [4:2]Temperature oversampling ×4 | [1:0]Normal mode
        i2c.writeto(self.addr, b'\xF4\x27')
        # The “config” register sets the rate, filter and interface options of the device. Writes to the “config”
        # register in normal mode may be ignored. In sleep mode writes are not ignored.
        i2c.writeto(self.addr, b'\xF5\x00')

        i2c.writeto(self.addr, b'\x88', False)
        bytes = i2c.readfrom(self.addr, 6)
        self.dig_T = ustruct.unpack('Hhh', bytes)

        i2c.writeto(self.addr, b'\x8E', False)
        bytes = i2c.readfrom(self.addr, 18)
        self.dig_P = ustruct.unpack('Hhhhhhhhh', bytes)

        i2c.writeto(self.addr, b'\xA1', False)
        self.dig_H = array.array('h', [0, 0, 0, 0, 0, 0])
        self.dig_H[0] = i2c.readfrom(self.addr, 1)[0]
        i2c.writeto(self.addr, b'\xE1', False)
        buff = i2c.readfrom(self.addr, 7)
        self.dig_H[1] = ustruct.unpack('h', buff[0:2])[0]
        self.dig_H[2] = buff[2]
        self.dig_H[3] = (buff[3] << 4) | (buff[4] & 0x0F)
        self.dig_H[4] = (buff[5] << 4) | (buff[4] >> 4 & 0x0F)
        self.dig_H[5] = buff[6]

    def temperature(self):
        retry = 0
        if (retry < 5):
            try:
                i2c.writeto(self.addr, b'\xFA', False)
                buff = i2c.readfrom(self.addr, 3)
                T = (((buff[0] << 8) | buff[1]) << 4) | (buff[2] >> 4 & 0x0F)
                c1 = (T / 16384.0 - self.dig_T[0] / 1024.0) * self.dig_T[1]
                c2 = ((T / 131072.0 - self.dig_T[0] / 8192.0) * (T / 131072.0 - self.dig_T[0] / 8192.0)) * self.dig_T[2]
                self.tFine = c1 + c2
                return self.tFine / 5120.0
            except:
                retry = retry + 1
        else:
            raise Exception("i2c read/write error!")

    def pressure(self):
        retry = 0
        if (retry < 5):
            try:
                self.temperature()
                i2c.writeto(self.addr, b'\xF7', False)
                buff = i2c.readfrom(self.addr, 3)
                P = (((buff[0] << 8) | buff[1]) << 4) | (buff[2] >> 4 & 0x0F)
                c1 = self.tFine / 2.0 - 64000.0
                c2 = c1 * c1 * self.dig_P[5] / 32768.0
                c2 = c2 + c1 * self.dig_P[4] * 2.0
                c2 = c2 / 4.0 + self.dig_P[3] * 65536.0
                c1 = (self.dig_P[2] * c1 * c1 / 524288.0 + self.dig_P[1] * c1) / 524288.0
                c1 = (1.0 + c1 / 32768.0) * self.dig_P[0]
                if c1 == 0.0:
                    return 0
                p = 1048576.0 - P
                p = (p - c2 / 4096.0) * 6250.0 / c1
                c1 = self.dig_P[8] * p * p / 2147483648.0
                c2 = p * self.dig_P[7] / 32768.0
                p = p + (c1 + c2 + self.dig_P[6]) / 16.0
                return p
            except:
                retry = retry + 1
        else:
            raise Exception("i2c read/write error!")

    def humidity(self):
        retry = 0
        if (retry < 5):
            try:
                self.temperature()
                i2c.writeto(self.addr, b'\xFD', False)
                buff = i2c.readfrom(self.addr, 2)
                H = buff[0] << 8 | buff[1]
                h = self.tFine - 76800.0
                h = (H - (self.dig_H[3] * 64.0 + self.dig_H[4] / 16384.0 * h)) * \
                    (self.dig_H[1] / 65536.0 * (1.0 + self.dig_H[5] / 67108864.0 * h * \
                    (1.0 + self.dig_H[2] / 67108864.0 * h)))
                h = h * (1.0 - self.dig_H[0] * h / 524288.0)
                if h > 100.0:
                    return 100.0
                elif h < 0.0:
                    return 0.0
                else:
                    return h
            except:
                retry = retry + 1
        else:
            raise Exception("i2c read/write error!")

# bm280
# if 119 in i2c.scan():
#     bme280 = BME280()

class PinMode(object):
    IN = 1
    OUT = 2
    PWM = 3
    ANALOG = 4
    OUT_DRAIN = 5


pins_remap_esp32 = (33, 32, 35, 34, 39, 0, 16, 17, 26, 25, 36, 2, -1, 18, 19, 21, 5, -1, -1, 22, 23, -1, -1, 27, 14, 12,
                    13, 15, 4)


class MPythonPin():
    def __init__(self, pin, mode=PinMode.IN, pull=None):
        if mode not in [PinMode.IN, PinMode.OUT, PinMode.PWM, PinMode.ANALOG, PinMode.OUT_DRAIN]:
            raise TypeError("mode must be 'IN, OUT, PWM, ANALOG,OUT_DRAIN'")
        if pin == 4:
            raise TypeError("P4 is used for light sensor")
        if pin == 10:
            raise TypeError("P10 is used for sound sensor")
        try:
            self.id = pins_remap_esp32[pin]
        except IndexError:
            raise IndexError("Out of Pin range")
        if mode == PinMode.IN:
            # if pin in [3]:
            #     raise TypeError('IN not supported on P%d' % pin)
            self.Pin = Pin(self.id, Pin.IN, pull)
        if mode == PinMode.OUT:
            if pin in [2, 3]:
                raise TypeError('OUT not supported on P%d' % pin)
            self.Pin = Pin(self.id, Pin.OUT, pull)
        if mode == PinMode.OUT_DRAIN:
            if pin in [2, 3]:
                raise TypeError('OUT_DRAIN not supported on P%d' % pin)
            self.Pin = Pin(self.id, Pin.OPEN_DRAIN, pull)
        if mode == PinMode.PWM:
            if pin not in [0, 1, 5, 6, 7, 8, 9, 11, 13, 14, 15, 16, 19, 20, 23, 24, 25, 26, 27, 28]:
                raise TypeError('PWM not supported on P%d' % pin)
            self.pwm = PWM(Pin(self.id), duty=0)
        if mode == PinMode.ANALOG:
            if pin not in [0, 1, 2, 3, 4, 10]:
                raise TypeError('ANALOG not supported on P%d' % pin)
            self.adc = ADC(Pin(self.id))
            self.adc.atten(ADC.ATTN_11DB)
        self.mode = mode

    def irq(self, handler=None, trigger=Pin.IRQ_RISING):
        if not self.mode == PinMode.IN:
            raise TypeError('the pin is not in IN mode')
        return self.Pin.irq(handler, trigger)

    def read_digital(self):
        if not self.mode == PinMode.IN:
            raise TypeError('the pin is not in IN mode')
        return self.Pin.value()

    def write_digital(self, value):
        if self.mode not in [PinMode.OUT, PinMode.OUT_DRAIN]:
            raise TypeError('the pin is not in OUT or OUT_DRAIN mode')
        self.Pin.value(value)

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


class wifi:
    def __init__(self):
        self.sta = network.WLAN(network.STA_IF)
        self.ap = network.WLAN(network.AP_IF)

    def connectWiFi(self, ssid, passwd, timeout=10):
        if self.sta.isconnected():
            self.sta.disconnect()
        self.sta.active(True)
        list = self.sta.scan()
        for i, wifi_info in enumerate(list):
            try:
                if wifi_info[0].decode() == ssid:
                    self.sta.connect(ssid, passwd)
                    wifi_dbm = wifi_info[3]
                    break
            except UnicodeError:
                self.sta.connect(ssid, passwd)
                wifi_dbm = '?'
                break
            if i == len(list) - 1:
                raise OSError("SSID invalid / failed to scan this wifi")
        start = time.time()
        print("Connection WiFi", end="")
        while (self.sta.ifconfig()[0] == '0.0.0.0'):
            if time.ticks_diff(time.time(), start) > timeout:
                print("")
                raise OSError("Timeout!,check your wifi password and keep your network unblocked")
            print(".", end="")
            time.sleep_ms(500)
        print("")
        print('WiFi(%s,%sdBm) Connection Successful, Config:%s' % (ssid, str(wifi_dbm), str(self.sta.ifconfig())))

    def disconnectWiFi(self):
        if self.sta.isconnected():
            self.sta.disconnect()
        self.sta.active(False)
        print('disconnect WiFi...')

    def enable_APWiFi(self, essid, password=b'',channel=10):
        self.ap.active(True)
        if password:
            authmode=4
        else:
            authmode=0
        self.ap.config(essid=essid,password=password,authmode=authmode, channel=channel)

    def disable_APWiFi(self):
        self.ap.active(False)
        print('disable AP WiFi...')


# 3 rgb leds
rgb = NeoPixel(Pin(17, Pin.OUT), 3, 3, 1, brightness=0.3)
rgb.write()

# light sensor
light = ADC(Pin(39))
light.atten(light.ATTN_11DB)

# sound sensor
sound = ADC(Pin(36))
sound.atten(sound.ATTN_11DB)

# buttons
class Button:
    def __init__(self, pin_num, reverse=False):
        self.__reverse = reverse
        (self.__press_level, self.__release_level) = (0, 1) if not self.__reverse else (1, 0)
        self.__pin = Pin(pin_num, Pin.IN, pull=Pin.PULL_UP)
        self.__pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.__irq_handler)
        # self.__user_irq = None
        self.event_pressed = None
        self.event_released = None
        self.__pressed_count = 0
        self.__was_pressed = False
        # print("level: pressed is {}, released is {}." .format(self.__press_level, self.__release_level))
    

    def __irq_handler(self, pin):
        irq_falling = True if pin.value() == self.__press_level else False
        # debounce
        time.sleep_ms(10)
        if self.__pin.value() == (self.__press_level if irq_falling else self.__release_level):
            # new event handler
            # pressed event
            if irq_falling:
                if self.event_pressed is not None:
                    schedule(self.event_pressed, self.__pin)
                # key status
                self.__was_pressed = True
                if (self.__pressed_count < 100):
                    self.__pressed_count = self.__pressed_count + 1
            # release event
            else:
                if self.event_released is not None:
                    schedule(self.event_released, self.__pin)

                
    def is_pressed(self):
        if self.__pin.value() == self.__press_level:
            return True
        else:
            return False

    def was_pressed(self):
        r = self.__was_pressed
        self.__was_pressed = False
        return r

    def get_presses(self):
        r = self.__pressed_count
        self.__pressed_count = 0
        return r

    def value(self):
        return self.__pin.value()

    def irq(self, *args, **kws):
        self.__pin.irq(*args, **kws)



class Touch:

    def __init__(self, pin):
        self.__touch_pad = TouchPad(pin)
        self.__touch_pad.irq(self.__irq_handler)
        self.event_pressed = None
        self.event_released = None
        self.__pressed_count = 0
        self.__was_pressed = False
        self.__value = 0

    def __irq_handler(self, value):
        # when pressed
        if value == 1:
            if self.event_pressed is not None:
                self.event_pressed(value)
            self.__was_pressed = True
            self.__value = 1
            if (self.__pressed_count < 100):
                self.__pressed_count = self.__pressed_count + 1
        # when released
        else:
            self.__value = 0
            if self.event_released is not None:
                self.event_released(value)
            
    def config(self, threshold):
        self.__touch_pad.config(threshold)

    def is_pressed(self):
        if self.__value:
            return True
        else:
            return False

    def was_pressed(self):
        r = self.__was_pressed
        self.__was_pressed = False
        return r

    def get_presses(self):
        r = self.__pressed_count
        self.__pressed_count = 0
        return r

    def read(self):
        return self.__touch_pad.read()


# button_a = Pin(0, Pin.IN, Pin.PULL_UP)
# button_b = Pin(2, Pin.IN, Pin.PULL_UP)
button_a = Button(0)
button_b = Button(2)


# touchpad
touchpad_p = touchPad_P = Touch(Pin(27))
touchpad_y = touchPad_Y = Touch(Pin(14))
touchpad_t = touchPad_T = Touch(Pin(12))
touchpad_h = touchPad_H = Touch(Pin(13))
touchpad_o = touchPad_O = Touch(Pin(15))
touchpad_n = touchPad_N = Touch(Pin(4))

from gui import *


def numberMap(inputNum, bMin, bMax, cMin, cMax):
    outputNum = 0
    outputNum = ((cMax - cMin) / (bMax - bMin)) * (inputNum - bMin) + cMin
    return outputNum
