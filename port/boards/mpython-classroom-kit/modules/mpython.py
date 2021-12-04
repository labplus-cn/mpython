# labplus mPython library
# MIT license; Copyright (c) 2018 labplus
# V1.0 Zhang KaiHua(apple_eat@126.com)

# mpython buildin periphers drivers

# history:
# V1.1 add oled draw function,add buzz.freq().  by tangliufeng
# V1.2 add servo/ui class,by tangliufeng

from machine import I2C, PWM, Pin, ADC, TouchPad, UART
from ssd1106 import SSD1106_I2C
import esp, math, time, network,audio
import ustruct, array, ujson
from neopixel import NeoPixel
from esp import dht_readinto
from time import sleep_ms, sleep_us, sleep
from framebuf import FrameBuffer
import motion_mpu6050
from apu_kit import APU

i2c = I2C(0, scl=Pin(Pin.P19), sda=Pin(Pin.P20), freq=400000)

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

class Motion():

    class Accelerometer():
        """Accelerometer mpu6050的加速度传感器
        """

        def get_x(self):
            return  motion_mpu6050.accel()[1]/65536

        def get_y(self):
            return - motion_mpu6050.accel()[0]/65536

        def get_z(self):
            return motion_mpu6050.accel()[2]/65536
        
        @property
        def x(self):
            return self.get_x()
        @property
        def y(self):
            return self.get_y()
        @property
        def z(self):
            return self.get_z()

    class Gyroscope():
        """Gyroscope mpu6050的角速度传感器
        """

        def get_x(self):
            return motion_mpu6050.gyro()[1]/65536

        def get_y(self):
            return - motion_mpu6050.gyro()[0]/65536

        def get_z(self):
            return motion_mpu6050.gyro()[2]/65536
        @property
        def x(self):
            return self.get_x()
        @property
        def y(self):
            return self.get_y()
        @property
        def z(self):
            return self.get_z()

    def __init__(self):
        motion_mpu6050.init(i2c)
        while not motion_mpu6050.accel():
            pass

    # output following: Pitch: -180 to 180 Roll: -90 to 90 Yaw: -180 to 180
    def get_euler(self):
        n =  list([i/65536 for i in motion_mpu6050.euler()])
        n[0] = (-(n[0]+180) if n[0]<0 else -(n[0]-180))
        n[1] = -n[1]
        return tuple(n)
        
    # output w x y z
    def get_quat(self):
        return tuple([i/math.pow(2, 30) for i in motion_mpu6050.quat()])

    # 加速度传感器
    accelerometer = Accelerometer()

    # 角速度传感器
    gyroscope = Gyroscope()

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
        try:
            self.id = pins_remap_esp32[pin]
        except IndexError:
            raise IndexError("Out of Pin range")
        if mode == PinMode.IN:
            if pin in [3]:
                raise TypeError('IN not supported on P%d' % pin)
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

class sound():

    @staticmethod
    def init():
        audio.recorder_init(i2c)
        audio.set_volume(0)

    @staticmethod
    def deinit():
        audio.recorder_deinit()

    @staticmethod
    def read():
        loudness = audio.loudness()
        if loudness:
            return loudness

# touchpad
class BS8112A(object):
   """  """

   def __init__(self, i2c):
      self.addr = 80
      # config
      self._i2c = i2c
      self.config = [0xB0, 0x00, 0x00, 0x83, 0xf3, 0x98, 0x0f, 0x0f,
                     0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x00]
      checksum = 0
      for i in range(1, 19):
         checksum += self.config[i]
      checksum &= 0xff
      self.config[18] = checksum
      # print(self.config[18])
      retry = 0
      if (retry < 5):
         try:
            self._i2c.writeto(self.addr, bytearray(self.config), True)
            return
         except:
               retry = retry + 1
      else:
         raise Exception("bs8112a i2c read/write error!")

       # i2c.writeto(self.addr, b'\xB0', False)
       # time.sleep_ms(10)
       # print(i2c.readfrom(self.addr, 17, True))

   # key map:
   # value       bit7 bit6 bit5 bit4 bit3 bit2 bit1 bit0
   # bs8112a key Key8 Key7 Key6 Key5 Key4 Key3 Key2 Key1
   # mpython key       N    O    H    T    Y    P
   def key_value(self):
      retry = 0
      if (retry < 5):
         try:
            self._i2c.writeto(self.addr, b'\x08', False)
            time.sleep_ms(10)
            value = self._i2c.readfrom(self.addr, 1, True)
            time.sleep_ms(10)
            return value
         except:
               retry = retry + 1
      else:
         raise Exception("bs8112a i2c read/write error!")

bs8112a = BS8112A(i2c)
class Touthpad():
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        key = bs8112a.key_value()
        if key != None:
            if (key[0] & self.pin) != 0:
                return 0
            else:
                return 1023
        return 1023

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


# 202108018 更换SHT20 SPL06传感器
class WEATHER(object):
    def __init__(self):
        self.i2c = i2c
        addr = self.i2c.scan()
        if 118 in addr:
            WEATHER.chip = 1  # SPL06-001
            WEATHER.IIC_ADDR = 118
        elif 119 in addr:
            WEATHER.chip = 2  # BME280
            WEATHER.IIC_ADDR = 119
        else:
            raise OSError("WEATHER init error")
        if(WEATHER.chip == 1):
            # SPL06
            WEATHER._writeReg(0x06, 0x01) # 压力配置寄存器
            WEATHER._writeReg(0x07, 0x80) # 温度配置寄存器
            WEATHER._writeReg(0x08, 0x07) # 设置连续的压力和温度测量
            WEATHER._writeReg(0x09, 0x00) 
            sleep_ms(50)
            try:
                id = WEATHER._readReg(0x0D)
                if(id[0]!=0x10):
                    print('SPL06 ID error:',id)
            except OSError as e:
                print(e)
            # SHT20
            self.sht20 = SHT20() 
        elif(WEATHER.chip == 2):
            self.bme280 = BME280()

    def _readReg(reg, nbytes=1):
        return i2c.readfrom_mem(WEATHER.IIC_ADDR, reg, nbytes)

    def _writeReg(reg, value):
        i2c.writeto_mem(WEATHER.IIC_ADDR, reg, value.to_bytes(1, 'little'))

    def get_traw(self):
        tmp_MSB = WEATHER._readReg(0x03)
        tmp_LSB = WEATHER._readReg(0x04)
        tmp_XLSB = WEATHER._readReg(0x05)

        tmp = (tmp_MSB[0] << 16) | (tmp_LSB[0] << 8) | tmp_XLSB[0]
        if(tmp & (1 << 23)):
            tmp= -((tmp ^ 0xffffff) +1)

        return tmp

    def get_temperature_scale_factor(self):
        tmp_Byte = WEATHER._readReg(0x07)
        tmp_Byte = tmp_Byte[0] & 0B111 

        if(tmp_Byte == 0B000):
            k = 524288.0
        elif(tmp_Byte == 0B001):
            k = 1572864.0
        elif(tmp_Byte == 0B010):
            k = 3670016.0
        elif(tmp_Byte == 0B011):
            k = 7864320.0
        elif(tmp_Byte == 0B100):
            k = 253952.0
        elif(tmp_Byte == 0B101):
            k = 516096.0
        elif(tmp_Byte == 0B110):
            k = 1040384.0
        elif(tmp_Byte == 0B111):
            k = 2088960.0 

        return k

    def get_pressure_scale_factor(self):
        tmp_Byte = WEATHER._readReg(0x06)
        tmp_Byte = tmp_Byte[0] & 0B111 

        if(tmp_Byte == 0B000):
            k = 524288.0
        elif(tmp_Byte == 0B001):
            k = 1572864.0
        elif(tmp_Byte == 0B010):
            k = 3670016.0
        elif(tmp_Byte == 0B011):
            k = 7864320.0
        elif(tmp_Byte == 0B100):
            k = 253952.0
        elif(tmp_Byte == 0B101):
            k = 516096.0
        elif(tmp_Byte == 0B110):
            k = 1040384.0
        elif(tmp_Byte == 0B111):
            k = 2088960.0

        return k

    def get_praw(self):
        tmp_MSB = WEATHER._readReg(0x00)
        tmp_LSB = WEATHER._readReg(0x01)
        tmp_XLSB = WEATHER._readReg(0x02)

        tmp = ((tmp_MSB[0] << 16) | (tmp_LSB[0] << 8) | tmp_XLSB[0] )& 0x00ffffff

        if(tmp & (1 << 23)):
            tmp= -((tmp ^ 0xffffff) +1)

        return tmp

    def get_c0(self):
        tmp_MSB = WEATHER._readReg(0x10)
        tmp_LSB = WEATHER._readReg(0x11)

        tmp_LSB = tmp_LSB[0] >> 4
        tmp = tmp_MSB[0] << 4 | tmp_LSB

        if (tmp & (1 << 11)):
            tmp= -((tmp ^ 0xfff) +1)
            
        return tmp
    
    def get_c1(self):
        tmp_MSB = WEATHER._readReg(0x11)
        tmp_LSB = WEATHER._readReg(0x12)

        tmp = ((tmp_MSB[0] & 0xF) << 8) | tmp_LSB[0]

        if (tmp & (1 << 11)):
            tmp= -((tmp ^ 0xfff) +1)

        return tmp
    
    def get_c00(self):
        tmp_MSB = WEATHER._readReg(0x13)
        tmp_LSB = WEATHER._readReg(0x14)
        tmp_XLSB = WEATHER._readReg(0x15)

        tmp = ((tmp_MSB[0] << 12) | (tmp_LSB[0] << 4) | (tmp_XLSB[0] >> 4))

        if(tmp & (1 << 19)):
            tmp = -((tmp ^ 0xfffff) +1)
        
        return tmp

    def get_c10(self):
        tmp_MSB = WEATHER._readReg(0x15)
        tmp_LSB = WEATHER._readReg(0x16)
        tmp_XLSB = WEATHER._readReg(0x17)

        tmp_MSB = tmp_MSB[0] & 0x0F

        tmp = (tmp_MSB << 16) | (tmp_LSB[0]  << 8) | tmp_XLSB[0]

        if(tmp & (1 << 19)):
            tmp= -((tmp ^ 0xFFFFF) +1)

        return tmp

    def get_c01(self):
        tmp_MSB = WEATHER._readReg(0x18)
        tmp_LSB = WEATHER._readReg(0x19)

        tmp = (tmp_MSB[0] << 8) | tmp_LSB[0]

        if(tmp & (1 << 15)):
            tmp= -((tmp ^ 0xFFFF) +1)

        return tmp

    def get_c11(self):
        tmp_MSB = WEATHER._readReg(0x1A)
        tmp_LSB = WEATHER._readReg(0x1B)

        tmp = (tmp_MSB[0] << 8) | tmp_LSB[0]

        if(tmp & (1 << 15)):
            tmp= -((tmp ^ 0xFFFF) +1)

        return tmp

    def get_c20(self):
        tmp_MSB = WEATHER._readReg(0x1C)
        tmp_LSB = WEATHER._readReg(0x1D)

        tmp = (tmp_MSB[0] << 8) | tmp_LSB[0]
        
        if(tmp & (1 << 15)):
            tmp= -((tmp ^ 0xFFFF) +1)

        return tmp

    def get_c21(self):
        tmp_MSB = WEATHER._readReg(0x1E)
        tmp_LSB = WEATHER._readReg(0x1F)
        tmp = (tmp_MSB[0] << 8) | tmp_LSB[0]
        
        if(tmp & (1 << 15)):
            tmp= -((tmp ^ 0xFFFF) +1)

        return tmp

    def get_c30(self):
        tmp_MSB = WEATHER._readReg(0x20)
        tmp_LSB = WEATHER._readReg(0x21)

        tmp = (tmp_MSB[0] << 8) | tmp_LSB[0]
        
        if(tmp & (1 << 15)):
            tmp= -((tmp ^ 0xFFFF) +1)

        return tmp
    
    def get_temperature(self):
        """
        获取温度
        :return: 温度,单位摄氏度
        """
        c0 = self.get_c0()
        c1 = self.get_c1()
        traw = self.get_traw()
        t_scale = self.get_temperature_scale_factor()

        traw_sc = traw / t_scale
        temp_c = ((c0) * 0.5) + ((c1) * traw_sc)
        temp_f = (temp_c * 9/5) + 32

        return temp_c

    def pressure(self):
        """
        获取气压
        :return: 气压,单位Pa
        """
        if(WEATHER.chip == 1):
            traw = self.get_traw()
            t_scale = self.get_temperature_scale_factor()
            traw_sc = traw / t_scale

            praw = self.get_praw()
            p_scale = self.get_pressure_scale_factor()
            praw_sc = praw / p_scale

            pcomp = self.get_c00()+ praw_sc*(self.get_c10()+ praw_sc*(self.get_c20()+ praw_sc*self.get_c30())) + traw_sc*self.get_c01() + traw_sc*praw_sc*(self.get_c11()+praw_sc*self.get_c21())
        # print("pcomp", "{:.2f}".format(pcomp))
        elif(WEATHER.chip == 2):
            pcomp = self.bme280.pressure()
       
        return pcomp

    def temperature(self):
        """
        获取温度
        :return: 温度,单位摄氏度
        """
        if(WEATHER.chip == 1):
            return self.sht20.temperature()
        elif(WEATHER.chip == 2):
            return self.bme280.temperature()
    
    def humidity(self):
        """
        获取湿度
        :return: 湿度,单位%
        """
        if(WEATHER.chip == 1):
            return self.sht20.humidity()
        elif(WEATHER.chip == 2):
            return self.bme280.humidity()


class SHT20(object):
    """
    温湿度模块SHT20控制类
    :param i2c: I2C实例对象,默认i2c=i2c.
    """

    def __init__(self, i2c=i2c):
        self.i2c = i2c

    def temperature(self):
        """
        获取温度

        :return: 温度,单位摄氏度
        """
        self.i2c.writeto(0x40, b'\xf3')
        sleep_ms(70)
        t = i2c.readfrom(0x40, 2)
        return -46.86 + 175.72 * (t[0] * 256 + t[1]) / 65535

    def humidity(self):
        """
        获取湿度

        :return: 湿度,单位%
        """
        self.i2c.writeto(0x40, b'\xf5')
        sleep_ms(25)
        t = i2c.readfrom(0x40, 2)
        return -6 + 125 * (t[0] * 256 + t[1]) / 65535


from gui import *

def numberMap(inputNum, bMin, bMax, cMin, cMax):
    outputNum = 0
    outputNum = ((cMax - cMin) / (bMax - bMin)) * (inputNum - bMin) + cMin
    return outputNum

""" devices on-board
"""
# display
oled = OLED()
# display = oled

# 3 axis accelerometer
motion = Motion()
accelerometer = motion.accelerometer
gyroscope = motion.gyroscope

#气象传感器
#SHT20 SPL06 bme280
weather = WEATHER()

# rgb matrix
rgb = NeoPixel(Pin(25, Pin.OUT), 25, 3, 1)
rgb.write()

# light sensor
light = ADC(Pin(39))
light.atten(light.ATTN_11DB)

# human infrared
pir = Pin(21, mode=Pin.IN, pull=None)

# slide POT
slider_res = ADC(Pin(34))
slider_res.atten(slider_res.ATTN_11DB)

# touch pad
touchpad_p = touchPad_P = Touthpad(2)
touchpad_y = touchPad_Y = Touthpad(4)
touchpad_t = touchPad_T = Touthpad(8)
touchpad_h = touchPad_H = Touthpad(16)
touchpad_o = touchPad_O = Touthpad(32)
touchpad_n = touchPad_N = Touthpad(64)

# buttons
# button_a = Pin(19, Pin.IN, Pin.PULL_UP)
# button_b = Pin(2, Pin.IN, Pin.PULL_UP)
button_a = Button(19)
button_b = Button(2)
# apu @K210
apu = APU()

# motor @K210
motor = apu.motor
camera_light = apu.light
ultrasonic = apu.ultrasonic
btn_left = apu.btn_left
btn_right = apu.btn_right
btn_up = apu.btn_up
btn_down = apu.btn_down
btn_ok = apu.btn_ok
