#mPythonType:0
from mpython import i2c, sleep_ms, MPythonPin, PinMode
from machine import UART,Pin
import parrot
import time

class Color(object):

    def __init__(self, i2c=i2c):
        self.i2c = i2c
        self.I2C_ADR = 0x39
        self.wb_rgb = [0.52,1,1]
        self.i2c.writeto_mem(0x12, 3, b'\x00')
        self.setup()
        self.turn_on()
        
    def turn_on(self):
        self.i2c.writeto_mem(0x12, 3, b'\x00')

    def turn_off(self):
        self.i2c.writeto_mem(0x12, 3, b'\x01')

    def setup(self):
        self.i2c.writeto_mem(self.I2C_ADR, 0x80, b'\x03')
        time.sleep_ms(10)
        self.i2c.writeto_mem(self.I2C_ADR, 0x81, b'\xD5')
        self.i2c.writeto_mem(self.I2C_ADR, 0x8F, b'\x01')
        
    def setbw_rgb(self,r,g,b):
        self.wb_rgb = [r,g,b]

    def getRGB(self):
        color = [0, 0, 0]
        buf = self.i2c.readfrom_mem(self.I2C_ADR, 0x96, 6)
        color_r = buf[1]*256 + buf[0]
        color_g = buf[3]*256 + buf[2]
        color_b = buf[5]*256 + buf[4]
        color_r = int(color_r/self.wb_rgb[0])
        color_g = int(color_g/self.wb_rgb[1])
        color_b = int(color_b/self.wb_rgb[2])
        maxColor = max(color_r, color_g, color_b)
        if maxColor > 255:
            scale = 255 / maxColor
            color_r = int(color_r * scale)
            color_g = int(color_g * scale)
            color_b = int(color_b * scale)
        return (color_r, color_g, color_b)

    def getHSV(self):
        rgb = self.getRGB()
        r, g, b = rgb[0], rgb[1], rgb[2]
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df / mx
        v = mx
        return round(h, 1), round(s, 1), round(v, 1)

    def discern(self):
        hsv=self.getHSV()
        if 0<=hsv[1]<=0.3:
            return 'none'
        elif 0<=hsv[0]<=6 or 340<=hsv[0]<=360:
            return 'red'
        elif 6<=hsv[0]<=25:
            return 'orange'
        elif 25<=hsv[0]<=70:
            return 'yellow'
        elif 70<=hsv[0]<=150:
            return 'green'
        elif 150<=hsv[0]<=180:
            return 'cyan'
        elif 180<=hsv[0]<=250:
            return 'blue'
        elif 250<=hsv[0]<=340:
            return 'purple'
        else:
            return 'null'

    def discern_red(self):
        if self.discern() == 'red':
            return True
        else:
            return False

    def discern_orange(self):
        if self.discern() == 'orange':
            return True
        else:
            return False

    def discern_yellow(self):
        if self.discern() == 'yellow':
            return True
        else:
            return False

    def discern_green(self):
        if self.discern() == 'green':
            return True
        else:
            return False

    def discern_cyan(self):
        if self.discern() == 'cyan':
            return True
        else:
            return False

    def discern_blue(self):
        if self.discern() == 'blue':
            return True
        else:
            return False

    def discern_purple(self):
        if self.discern() == 'purple':
            return True
        else:
            return False

class Ultrasonic(object):
    """
    超声波控制类
    """
    def __init__(self, i2c=i2c, i2c_addr=0x13):
        self.i2c = i2c
        self.I2C_ADR = i2c_addr    

    def distance(self):
        self.i2c.writeto(self.I2C_ADR, b'\x20')
        time.sleep_ms(2)
        buf = self.i2c.readfrom(self.I2C_ADR, 2)
        distance_mm = (buf[0]*256+buf[1])
        return distance_mm
        

class Line(object):

    def __init__(self, i2c=i2c):
        self.i2c = i2c
        self.I2C_ADR = 0x12
        self.threshold = 100
        
    def read_sensor(self,num):
        self.i2c.writeto(self.I2C_ADR, bytearray([33+num]))
        return self.i2c.readfrom(self.I2C_ADR,1)[0]

    def set_line_threshold(self,data=100):
        self.threshold = data
        
    def touch_line(self,num):
        if self.read_sensor(num)>self.threshold: 
            return True
        else:
            return False


class Motor(object):
    """
    电机控制模块控制类
    """
    def __init__(self, i2c=i2c,i2c_addr=0x11):
        self.i2c = i2c
        self.I2C_ADR = i2c_addr
        
    def motor1(self, speed=100):
        i2c.writeto_mem(self.I2C_ADR, 1, bytearray([speed]))

    def motor2(self, speed=100):
        i2c.writeto_mem(self.I2C_ADR, 2, bytearray([speed]))
        
    def read_battery_voltage(self):
        self.i2c.writeto(self.I2C_ADR, b'\x25')
        buf = self.i2c.readfrom(self.I2C_ADR, 2)
        battery_voltage = (buf[0]*256+buf[1])
        return battery_voltage


class SHT20(object):

    def __init__(self, i2c=i2c):
        self.i2c = i2c

    def temperature(self):
        """
        获取温度
        """
        self.i2c.writeto(0x40, b'\xf3')
        time.sleep_ms(70)
        t = i2c.readfrom(0x40, 2)
        return -46.86 + 175.72 * (t[0] * 256 + t[1]) / 65535

    def humidity(self):
        """
        获取湿度
        """
        self.i2c.writeto(0x40, b'\xf5')
        time.sleep_ms(25)
        t = i2c.readfrom(0x40, 2)
        return -6 + 125 * (t[0] * 256 + t[1]) / 65535


'''
MPU6050类
'''
class MPU6050(object):
    def __init__(self,i2c=i2c):
        self.i2c = i2c
        
    def Write_Mpu6050_REG(self, reg, dat):
        buf = bytearray(1)
        buf[0] = dat
        self.i2c.writeto_mem(0x68, reg, buf)
        
    def Read_Mpu6050_REG(self, reg):
        t = self.i2c.readfrom_mem(0x68, reg, 1)[0]
        return (t >> 4)*10 +(t % 16)

    def Read_Mpu6050_Len(self, reg, len, buffer):
        self.i2c.readfrom_mem_into(0x68, reg, buffer)
        
    ##fsr:0,�250dps;1,�500dps;2,�1000dps;3,�2000dps
    def MPU_Set_Gyro_Fsr(self, fsr):
        return self.Write_Mpu6050_REG(0x1B, fsr << 3)
    
    #fsr:0,�2g;1,�4g;2,�8g;3,�16g
    def MPU_Set_Accel_Fsr(self, fsr):
        return self.Write_Mpu6050_REG(0x1C, fsr << 3)
        
    def MPU_Set_LPF(self, lpf):
        if(lpf >= 188):
            data = 1
        elif(lpf >=98):
            data = 2
        elif(lpf >= 42):
            data = 3
        elif(lpf >= 20):
            data = 4
        elif(lpf >= 10):
            data = 5
        else:
            data = 6
        self.Write_Mpu6050_REG(0x1A, data)
    
    #rate:4~1000hz
    def MPU_Set_Rate(self, rate):
        if(rate > 1000):
            rate = 1000
        if(rate < 4):
            rate = 4
        data = int(1000/rate-1)
        datas = self.Write_Mpu6050_REG(0x19, data)
        return self.MPU_Set_LPF(rate/2)
        
    def MPU_Init(self):
        self.Write_Mpu6050_REG(0x6B, 0x80)
        time.sleep_ms(100)
        self.Write_Mpu6050_REG(0x6B, 0x00)
        self.MPU_Set_Gyro_Fsr(3)
        self.MPU_Set_Accel_Fsr(0)
        self.MPU_Set_Rate(50)
        self.Write_Mpu6050_REG(0x38, 0x00)
        self.Write_Mpu6050_REG(0x6A, 0x00)
        self.Write_Mpu6050_REG(0x23, 0x00)
        self.Write_Mpu6050_REG(0x37, 0x80)
        res = self.Read_Mpu6050_REG(0x75)
        if(res == 68):
            self.Write_Mpu6050_REG(0x6B,0x01)
            self.Write_Mpu6050_REG(0x6C,0x00)
            self.MPU_Set_Rate(50)
        else:
            return 1
        return 0

    def Get_Gyro_x(self):
        buf = bytearray(2)
        res = self.Read_Mpu6050_Len(0x43, 2, buf)
        gx = (buf[0] << 8) | buf[1]
        if(gx >= 0x8000):
            gx = -((65535 - gx) + 1)
        return 2000*gx/32768
    
    def Get_Gyro_y(self):
        buf = bytearray(2)
        res = self.Read_Mpu6050_Len(0x45, 2, buf)
        gy = (buf[0] << 8) | buf[1]
        if(gy >= 0x8000):
            gy = -((65535 - gy) + 1)
        return 2000*gy/32768
        
    def Get_Gyro_z(self):
        buf = bytearray(2)
        res = self.Read_Mpu6050_Len(0x47, 2, buf)
        gz = (buf[0] << 8) | buf[1]
        if(gz >= 0x8000):
            gz = -((65535 - gz) + 1)
        return 2000*gz/32768
        
    def Get_Accel_x(self):
        buf = bytearray(2)
        res = self.Read_Mpu6050_Len(0x3B, 2, buf)
        ax = (buf[0] << 8) | buf[1]
        if(ax >= 0x8000):
            ax = -((65535 - ax) + 1)
        return 2*9.8*ax/32768
        
    def Get_Accel_y(self):
        buf = bytearray(2)
        res = self.Read_Mpu6050_Len(0x3D, 2, buf)
        ay = (buf[0] << 8) | buf[1]
        if(ay >= 0x8000):
            ay = -((65535 - ay) + 1)
        return 2*9.8*ay/32768
        
    def Get_Accel_z(self):
        buf = bytearray(2)
        res = self.Read_Mpu6050_Len(0x3F, 2, buf)
        az = (buf[0] << 8) | buf[1]
        if(az >= 0x8000):
            az = -((65535 - az) + 1)
        return 2*9.8*az/32768

class Advance(object):
    """
    电机控制模块控制类
    """
    def __init__(self):
        self.i2c = i2c
        self.i2c_scan_addr=i2c.scan()
               
    def set_i2c_addr(self,first_addr,second_addr):
        if second_addr<0x7F and second_addr&0x78 and second_addr|0x07 !=0x7F and not(second_addr in self.i2c_scan_addr):
            self.i2c.writeto(first_addr, (bytearray([16, second_addr])))
            time.sleep_ms(100)
        else:
            raise OSError("地址设置异常，请更改I2C地址！")

    def motor(self, I2C_ADR,driver, speed):
        i2c.writeto_mem(I2C_ADR, driver, bytearray([speed]))

    def get_battery_voltage(self,I2C_ADR=0x11):
        self.i2c.writeto(I2C_ADR, b'\x25')
        buf = self.i2c.readfrom(I2C_ADR, 2)
        battery_voltage = (buf[0]*256+buf[1])
        return battery_voltage

    def distance(self,I2C_ADR):
        self.i2c.writeto(I2C_ADR, b'\x20')
        time.sleep_ms(2)
        buf = self.i2c.readfrom(I2C_ADR, 2)
        distance_mm = (buf[0]*256+buf[1])
        return distance_mm

class SpeechSynthesis(object):
    
    def __init__(self):
        self.uart= UART(1, baudrate=115200, tx=Pin.P1, rx=Pin.P0)
        self.head1 = [0xFD, 0x00, 0x06, 0x01,0x01,0x5B,0x76,0x35,0x5D]

    def speak(self,str_buf):
        head = [0xFD, 0x00, 0x00, 0x01,0x04]
        str_temp = bytes(str_buf, 'utf-8')
        length = len(str_temp) + 2
        head[1] = (length >> 8)
        head[2] = (length & 0xff)
        head.extend(str_temp)
        self.uart.write(bytes(head))
    
    def set_voice(self,voc):
        if voc > 9:
            voc = 9
        voc = 0x30 + voc
        self.head1[6]= 0x76
        self.head1[7] = voc
        self.uart.write(bytes(self.head1))

    def set_rate(self,rate):
        if rate > 9:
            rate = 9
        rate = 0x30 + rate
        self.head1[6]= 0x73
        self.head1[7] = rate
        self.uart.write(bytes(self.head1))

    def set_intonation(self,intonation):
        if intonation > 9:
            intonation = 9
        intonation = 0x30 + intonation
        self.head1[6]= 0x74
        self.head1[7] = intonation
        self.uart.write(bytes(self.head1))
        
