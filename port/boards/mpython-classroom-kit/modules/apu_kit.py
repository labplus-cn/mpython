""" 盛思人工智能交互实验箱 K210部分驱动
"""
from k210 import *
from repl import *
import time
# 通讯接口初始化

class APU:
    def __init__(self, rx=14, tx=13):
        # 通讯串口口初始化
        # global repl
        # self.repl = repl            
        self.serial = Serial(baudrate=2000000, rx_pin=rx, tx_pin=tx)
        # 使用REPL接口协议
        self.repl = REPL(self.serial)
        # 等待K210复位完成
        time.sleep(3)

        self.repl.enter_raw_repl(5)
        # try:
        #     self.repl.enter_raw_repl(5, True)
        # except:
        #     raise OSError(uerrno.ENODEV)

        """ 图形图像和AI运算
        """
        # 主绘图对象
        self.image = Image(self.repl, 'img')
        # 显示屏
        self.lcd = LCD(self.repl)
        # 摄像头
        self.sensor = Sensor(self.repl)
        # AI运算
        self.kpu = KPU(self.repl)

        """ 外设驱动
        """
        # 电机控制
        self.motor = Motor(1, self.repl)
        # 按键
        self.btn_left = Button(self.repl, name='btn_left')
        self.btn_right = Button(self.repl, name='btn_right')
        self.btn_up = Button(self.repl, name='btn_up')
        self.btn_down = Button(self.repl, name='btn_down')
        self.btn_ok = Button(self.repl, name='btn_ok')
        # 超声波
        self.ultrasonic = Ultrasonic(self.repl)
        # 补光灯
        self.light = Light(self.repl)

