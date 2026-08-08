from mpython import *
import time
import struct

def get_distance():
    i2c.writeto(0x10, bytearray([7]))
    return struct.unpack('H', i2c.readfrom(16, 2))[0]/10

MOTOR_right = const(0x01)
"""
M1电机编号，0x01
"""

MOTOR_left = const(0x02)
"""
M2电机编号，0x02
"""

i2c_scan = i2c.scan()
if 16 in i2c_scan and 18 not in i2c_scan:
    print('掌控魔盒：电机(旧)')
elif 18 in i2c_scan:
    print('掌控魔盒：编码电机(新)')
else:
    print('掌控魔盒电机有故障！')

_speed_buf = {}

def set_speed(motor_no, speed):
    """
    设置电机速度

    :param int motor_no: 控制电机编号，可以使用 ``MOTOR_left``, ``MOTOR_right`` ,或者直接写入电机编号。
    :param int speed: 电机速度，范围-100~100，负值代表反转。

    """
    global _speed_buf
    speed = max(min(speed, 100), -100)
    _speed_buf.update({motor_no: speed})
    attempts = 0
    while True:
        try:
            i2c.writeto(0x10, bytearray([1, motor_no, speed]))
        except Exception as e:
            attempts = attempts + 1
            time.sleep_ms(500)
            if attempts > 2:
                break
        else:
            break

def get_speed(motor_no):
    """
    返回电机速度

    :param int motor_no: 控制电机编号，可以使用 ``MOTOR_left``, ``MOTOR_right``,或者直接写入电机编号。
    :rtype: int
    :return: 返回该电机速度
    """
    global _speed_buf
    if motor_no in _speed_buf:
        return _speed_buf[motor_no]
    else:
        return None

'''line follow'''
"""
因循迹较耗电，不使用该功能时，关闭其电源。
从MCU中读出的5路循迹值为模拟量， 需要跟给定的阈值比较，大于阈值定义为黑线，值为1
5路循迹值序号：从左到右对应list索引值0-4
"""
class Line_follow(object):
    def __init__(self):
        i2c.writeto(16, bytearray([3, 1])) # 开循迹电源
        self.power_status = 1 # status: power on
        self.threshold = [2000, 2000, 2000, 2000, 2000]

    def get_val(self):
        i2c.writeto(16, bytearray([5]))
        tmp = struct.unpack('5H', i2c.readfrom(16, 10))
        list = [0]*5
        for i in range(5):
            if tmp[i] > self.threshold[i]:
                list[i] = 1
            else:
                list[i] = 0
        return list

    def get_raw_val(self):
        '''获取循迹值裸数据，模拟值'''
        i2c.writeto(16, bytearray([5]))
        tmp = struct.unpack('5H', i2c.readfrom(16, 10))
        return tmp

    def set_threshold(self, threshold):
        self.threshold = threshold

    def get_threshold(self):
        return self.threshold

    def on_off(self, on_off):
        if on_off == 1 and self.power_status == 2:
            i2c.writeto(16, bytearray([3, 1])) # 开
            self.power_status = 1
        elif on_off == 2 and self.power_status == 1:
            i2c.writeto(16, bytearray([3, 2])) # 关
            self.power_status = 2            


"""
获取电池电量，单位mV
"""
def get_bat_level():
    i2c.writeto(0x10, bytearray([4]))
    return struct.unpack('H', i2c.readfrom(16, 2))



'''
编码电机 2023.3
'''
class EncoderMotor(object):
    def __init__(self):
        self.batch = -1 
        if 16 in i2c_scan and 18 not in i2c_scan:
            self.i2c_addr = 16
            self.batch = 0
            self.stop()
        elif 18 in i2c_scan:
            #编码电机(新)
            self.i2c_addr = 18
            self.batch = 1 
            self.stop()
        
        if(self.batch == -1):
            print('掌控魔盒电机有故障！')

    def stop(self):
        if (self.batch == 0):
          pass
        elif (self.batch == 1):
            attempts=0
            while True:
                try:
                    i2c.writeto(self.i2c_addr, bytearray([1]))
                except Exception as e:
                    attempts = attempts + 1
                    if attempts > 2:
                        break
                else:
                    break

    def move(self, speed_l, speed_r):
        """
        设置电机速度
        :param int motor_no: 控制电机编号，可以使用 ``MOTOR_left``, ``MOTOR_right`` ,或者直接写入电机编号。
        :param int speed: 电机速度，范围-100~100，负值代表反转。
        """
        """
        设置小车移动速度，可前进后退
        :param int speed_l: 左电机速度 -100 -- 100。
        :param int speed_r: 右电机速度 -100 -- 100。
        """
        if (self.batch == 0):
            global _speed_buf
            speed = max(min(speed, 100), -100)
            _speed_buf.update({motor_no: speed})
            attempts = 0
            while True:
                try:
                    i2c.writeto(0x10, bytearray([1, motor_no, speed]))
                except Exception as e:
                    attempts = attempts + 1
                    time.sleep_ms(500)
                    if attempts > 2:
                        break
                else:
                    break
        elif (self.batch == 1):
            if speed_l < -100:
                speed_l = -100
            if speed_r < -100:
                speed_r = -100
            if speed_l > 100:
                speed_l = 100
            if speed_r > 100:
                speed_r = 100
     
            attempts=0
            while True:
                try:
                    i2c.writeto(self.i2c_addr, bytearray([2, speed_l, speed_r]))
                except Exception as e:
                    attempts = attempts + 1
                    if attempts > 2:
                        break
                else:
                    break

    def turn_angle(self, dir, speed, angle):
        """
        设置电机转向 
        :param int dir: 左转： 3 右转： 4
        :param int speed: 左电机速度 0 -- 100。
        :param int angle: 左电机速度 0 -- 360
        """
        if (self.batch == 1):
            if speed < 0:
                speed = 0
            if speed > 100:
                speed = 100
            if dir !=3 and dir != 4:
                return
            tmp = [0]*2
            tmp[0] = angle & 0xff
            tmp[1] = (angle >> 8) & 0xff
            # try:        
            #     i2c.writeto(self.i2c_addr, bytearray([dir, speed, tmp[0], tmp[1]]))
            # except:
            #     pass
            attempts=0
            while True:
                try:
                    i2c.writeto(self.i2c_addr, bytearray([dir, speed, tmp[0], tmp[1]]))
                except Exception as e:
                    attempts = attempts + 1
                    if attempts > 2:
                        break
                else:
                    break
        elif (self.batch == 0):
            print('编码电机才支持')
            pass

    def move_distance(self, speed, distance):
        """
        设置小车移动动指定距离，单位:mm 可前进后退
        :param int speed: 电机速度 -100 -- 100。
        :param int distance: 移动距离 0 --- 65535 mm
        """
        distance = distance*10
        if (self.batch == 1):
            if distance < 0:
                distance = 0
            if distance > 65535:
                distance = 65535
            tmp = [0]*2
            tmp[0] = distance & 0xff
            tmp[1] = (distance >> 8) & 0xff
            attempts=0
            while True:
                try:
                    i2c.writeto(self.i2c_addr, bytearray([5, speed, tmp[0], tmp[1]]))
                except Exception as e:
                    attempts = attempts + 1
                    if attempts > 2:
                        break
                else:
                    break
        elif (self.batch == 0):
            print('新编码电机才支持')
            return

    def set_correct(self, correct):
        """
        设置小车移动指定距离可转向时修正系数，以修正精确度
        :param int correct: 修正系数 -100 -- 100
        """
        if (self.batch == 1):
            if correct < -100:
                correct = -100
            if correct > 100:
                correct = 100
            attempts=0
            while True:
                try:
                    i2c.writeto(self.i2c_addr, bytearray([6, correct]))
                except Exception as e:
                    attempts = attempts + 1
                    if attempts > 2:
                        break
                else:
                    break
        elif (self.batch == 0):
            print('新编码电机才支持')
            return

class Motor(object):
    def __init__(self):
        self.speed_memory = [0,0] 
        self.batch = -1 
        if 16 in i2c.scan():
            self.batch = 0
            self.set_speed(0,0)
        if 18 in i2c.scan():#编码电机(新)
            self.batch = 1 
            self.set_speed(0,0)
        if(self.batch == -1):
            print('掌控魔盒电机有故障！')

    def set_speed(self, motor_no, speed):
        if(motor_no == MOTOR_left):
            self.speed_memory[0] = speed
            if(self.batch == 0):
                set_speed(MOTOR_left,speed)
            elif(self.batch == 1):
                encoder_motor.move(self.speed_memory[0],self.speed_memory[1])
        elif(motor_no == MOTOR_right):
            self.speed_memory[1] = speed
            if(self.batch == 0):
                set_speed(MOTOR_right,speed)
            elif(self.batch == 1):
                encoder_motor.move(self.speed_memory[0],self.speed_memory[1])
        print(self.speed_memory)

    def get_speed(self, motor_no):
        if(self.batch == 0):
            return get_speed(motor_no)
        elif(self.batch == 1):
            if(motor_no == MOTOR_left):
                return self.speed_memory[0]
            elif(motor_no == MOTOR_right):
                return self.speed_memory[1]


encoder_motor = EncoderMotor()
# mohe_motor = Motor()