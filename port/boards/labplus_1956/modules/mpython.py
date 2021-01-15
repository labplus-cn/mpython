# labplus mPython library
# MIT license; Copyright (c) 2018 labplus
# V1.0 Zhang KaiHua(apple_eat@126.com)

# mpython buildin periphers drivers

# history:
# V1.1 add oled draw function,add buzz.freq().  by tangliufeng
# V1.2 add servo/ui class,by tangliufeng

from machine import I2C, PWM, Pin, ADC, UART
import esp, math, time, network,audio
import ustruct, array, ujson
from neopixel import NeoPixel
from esp import dht_readinto
from time import sleep_ms, sleep_us, sleep
import motion_mpu6050
from apu_1956 import APU

i2c = I2C(0, scl=Pin(Pin.P19), sda=Pin(Pin.P20), freq=400000)

class Motion():

    class Accelerometer():
        """Accelerometer mpu6050的加速度传感器
        """

        def get_x(self):
            return -motion_mpu6050.accel()[1]/65536

        def get_y(self):
            return motion_mpu6050.accel()[0]/65536

        def get_z(self):
            return -motion_mpu6050.accel()[2]/65536
        
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
            return -motion_mpu6050.gyro()[1]/65536

        def get_y(self):
            return motion_mpu6050.gyro()[0]/65536

        def get_z(self):
            return -motion_mpu6050.gyro()[2]/65536
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

    # def get_accel(self):
    #     n =  list(motion_mpu6050.accel())
    #     n[0] = -n[0]
    #     n[2] = -n[2]
    #     return tuple([i/65536 for i in n])

    # def get_gyro(self):
    #     return tuple([i/65536 for i in motion_mpu6050.gyro()])

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

class Magnetic(object):
    """ MMC5983MA driver """

    def __init__(self):
        self.addr = 48
        self.i2c = i2c
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

        self.i2c.writeto(self.addr, b'\x09\x20\xbd\x00', True)
        # self.i2c.writeto(self.addr, b'\x09\x21', True)

    def _set_offset(self):
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
        # print(self.x_offset)
        # print(self.y_offset)
        # print(self.z_offset)

    # def _get_raw(self):
    #     retry = 0
    #     if (retry < 5):
    #         try:
    #             self.i2c.writeto(self.addr, b'\x09\x08', True)  #set

    #             self.i2c.writeto(self.addr, b'\x09\x01', True)
    #             while True:
    #                 self.i2c.writeto(self.addr, b'\x08', False)
    #                 buf = self.i2c.readfrom(self.addr, 1)
    #                 status = ustruct.unpack('B', buf)[0]
    #                 if(status & 0x01):
    #                     break
    #             self.i2c.writeto(self.addr, b'\x00', False)
    #             buf = self.i2c.readfrom(self.addr, 6)
    #             data = ustruct.unpack('>3H', buf)
    #             print(data)

    #             self.i2c.writeto(self.addr, b'\x09\x10', True)  #reset

    #             self.i2c.writeto(self.addr, b'\x09\x01', True)
    #             while True:
    #                 self.i2c.writeto(self.addr, b'\x08', False)
    #                 buf = self.i2c.readfrom(self.addr, 1)
    #                 status = ustruct.unpack('B', buf)[0]
    #                 if(status & 0x01):
    #                     break
    #             self.i2c.writeto(self.addr, b'\x00', False)
    #             buf = self.i2c.readfrom(self.addr, 6)
    #             data1 = ustruct.unpack('>3H', buf)
    #             print(data1)

    #             self.raw_x = -((data[0] - data1[0])/2)
    #             self.raw_y = -((data[1] - data1[1])/2)
    #             self.raw_z = -((data[2] - data1[2])/2)
    #             # print(str(self.x) + "   " + str(self.y) + "  " + str(self.z))
    #         except:
    #             retry = retry + 1
    #     else:
    #         raise Exception("i2c read/write error!")     

    def _get_raw(self):

        self.i2c.writeto(self.addr, b'\x09\x08', True)  #set

        self.i2c.writeto(self.addr, b'\x09\x01', True)
        time.sleep_ms(1)
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
        self.raw_y = ((data[1] - data1[1])/2)
        self.raw_z = ((data[2] - data1[2])/2)
        # print(str(self.x) + "   " + str(self.y) + "  " + str(self.z))

    def peeling(self):
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
        self._get_raw()
        return self.raw_x * 0.25

    def get_y(self):
        self._get_raw()
        return self.raw_y * 0.25

    def get_z(self):
        self._get_raw()
        return self.raw_z * 0.25 
    
    @property
    def x(self):
        return self.get_x()
    @property
    def y(self):
        return self.get_y()
    @property
    def z(self):
        return self.get_z()
        
    def get_field_strength(self):
        self._get_raw()
        if self.is_peeling == 1:
            return (math.sqrt((self.raw_x - self.peeling_x)*(self.raw_x - self.peeling_x) + (self.raw_y - self.peeling_y)*(self.raw_y - self.peeling_y) + (self.raw_z - self.peeling_z)*(self.raw_z - self.peeling_z)))*0.25
        return (math.sqrt(self.raw_x * self.raw_x + self.raw_y * self.raw_y + self.raw_z * self.raw_z))*0.25

    def calibrate(self):

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
        ticks_start = time.ticks_ms()
        while (time.ticks_diff(time.ticks_ms(), ticks_start) < 15000) :
            self._get_raw()
            min_z = min(self.raw_z, min_z)
            # min_y = min(self.raw_y, min_y)
            max_z = max(self.raw_z, max_z)
            # max_y = max(self.raw_y, max_y)
            time.sleep_ms(100)
        self.cali_offset_z = (max_z + min_z) / 2
        # self.cali_offset_y = (max_y + min_y) / 2
        print('cali_offset_z: ' + str(self.cali_offset_z))
        # print('cali_offset_y: ' + str(self.cali_offset_y))



    def get_heading(self):
        self._get_raw()

        # if (accelerometer):
        #     # use accelerometer get inclination   
        #     x = accelerometer.get_x()
        #     y = accelerometer.get_y()
        #     z = accelerometer.get_z()

        #     phi = math.atan2(x, -z)
        #     theta = math.atan2(y, (x*math.sin(phi) - z*math.cos(phi)))
        #     sinPhi = math.sin(phi)
        #     cosPhi = math.cos(phi)
        #     sinTheta = math.sin(theta)
        #     cosTheta = math.cos(theta)
        #     heading = (math.atan2(x*cosTheta + y*sinTheta*sinPhi + z*sinTheta*cosPhi, z*sinPhi - y*cosPhi)) * (180 / 3.14159265) + 180
        #     return heading

        temp_x = self.raw_x - self.cali_offset_x
        temp_y = self.raw_y - self.cali_offset_y
        temp_z = self.raw_z - self.cali_offset_z
        heading = math.atan2(temp_y, -temp_x) * (180 / 3.14159265) + 180
        return heading

    def _get_temperature(self):
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

    def _get_id(self):
        retry = 0
        if (retry < 5):
            try:
                self.i2c.writeto(self.addr, bytearray([0x2f]), False)
                buf = self.i2c.readfrom(self.addr, 1, True)
                # print(buf)
                id = ustruct.unpack('B', buf)[0]
                return id
            except:
                retry = retry + 1
        else:
            raise Exception("i2c read/write error!")    

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


""" devices on-board
"""
# apu @K210
apu = APU()

# motor @K210
MR1 = apu.m1
MR2 = apu.m2
ML1 = apu.m4
ML2 = apu.m3

# 6-axies motion sensor:mpu6050
motion = Motion()
accelerometer = motion.accelerometer
gyroscope = motion.gyroscope

# 3-axies megnetic sensor:MMC5983MA
magnetic = Magnetic()

# 3 rgb leds
rgb = NeoPixel(Pin(17, Pin.OUT), 3, 3, 1)
rgb.write()

# light sensor
light = ADC(Pin(39))
light.atten(light.ATTN_11DB)

# sound sensor
class sound():

    @staticmethod
    def init():
        audio.recorder_init()
        audio.set_volume(0)

    @staticmethod
    def deinit():
        audio.recorder_deinit()

    @staticmethod
    def read():
        loudness = audio.loudness()
        if loudness:
            return loudness

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


# buttons
# button_a = Pin(0, Pin.IN, Pin.PULL_UP)
# button_b = Pin(2, Pin.IN, Pin.PULL_UP)
# button_c = Pin(4, Pin.IN, Pin.PULL_UP)
button_a = Button(0)
button_b = Button(2)
button_c = Button(4)


