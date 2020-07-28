""" 盛思1956 K210部分驱动
"""
from k210 import *
from repl import *
import time
# 通讯接口初始化

class APU:
    def __init__(self, rx=14, tx=12):
        # 通讯串口口初始化
        # global repl
        # self.repl = repl            
        self.serial = Serial(baudrate=2000000, rx_pin=rx, tx_pin=tx)
        # 使用REPL接口协议
        self.repl = REPL(self.serial)
        # 等待K210复位完成
        time.sleep(4)

        self.repl.enter_raw_repl()
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
        self.m1 = Motor(1, self.repl)
        self.m2 = Motor(2, self.repl)
        self.m3 = Motor(3, self.repl)
        self.m4 = Motor(4, self.repl)

        # 音频切换开关
        self.audio_en = Light(self.repl, name="audio_enb")
        

        




