from mpython import i2c,numberMap
import struct

# 太阳能板模块
class SolarPanel():
    def __init__(self):
        self.i2c = i2c
        if 18 in self.i2c.scan():
            print('Solar panel initialization')
        else:
            print('Solar panel initialization error')
            print(self.i2c.scan())
            
    def set_servo(self, servo_num, angle):
        """
        设置舵机转动角度

        参数
        :servo_num: 舵机编号：1~2
        :angle: 舵机角度：-90~90

        返回值：无
        """
        angle = max(min(angle, 180), 0)
        if(servo_num==1):
            angle = int(numberMap(angle,0,180,-90,90))
        elif(servo_num==2):
            angle = int(max(min(angle, 90), 10))
            # angle = numberMap(angle,10,90,10,90)

        try:
            angle = max(min(angle, 90), -90)
            self.i2c.writeto(18, bytearray([servo_num, angle]))
        except Exception as e:
            print(e)
     

    def get_light_val(self):
        """
        获取太阳能板4组光线值
        参数：无
        返回值：列表[1号光线值,2,3,4]
        """
        try:
            self.i2c.writeto(18, b'\x03')
            tmp = self.i2c.readfrom(18, 8)
            tmp = struct.unpack('4H', tmp)
            if(tmp!=None):
                return tmp
            else:
                return [None]*4
        except Exception as e:
            print(e)
            return [None]*4


# import time
# solar_panel = SolarPanel()

# while True:
#     solar_panel.set_servo(1, 0)
#     solar_panel.set_servo(2, 0)
#     time.sleep(1)
#     solar_panel.set_servo(1, -90)
#     solar_panel.set_servo(2, -90)
#     time.sleep(1)
#     solar_panel.set_servo(1, 90)
#     solar_panel.set_servo(2, 90)
#     time.sleep(1)
#     print(solar_panel.get_light_val())