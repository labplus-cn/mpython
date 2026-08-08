""" 盛思AI摄像头驱动
"""
from repl import REPL, Serial
from machine import Pin, UART
from k210 import *
import uerrno
import time

class SmartCamera:

    def __init__(self, rx=Pin.P15, tx=Pin.P16):
        # 通讯串口口初始化
        # global repl
        # self.repl = repl            
        self.serial = Serial(baudrate=2000000, rx_pin=rx, tx_pin=tx)
        # 使用REPL接口协议
        self.repl = REPL(self.serial)
        # 等待K210复位完成
        time.sleep(3)

        # self.repl.enter_raw_repl(5, True)
        try:
            self.repl.enter_raw_repl(5, True)
        except:
            raise OSError(uerrno.ENODEV)

        # 主绘图对象
        # self.image = Image(self.repl, ref='img')
        # 显示屏
        self.lcd = LCD(self.repl)
        # 摄像头
        self.sensor = Sensor(self.repl)
        # AI运算
        self.kpu = KPU(self.repl)
        # 补光灯
        self.light = Light(self.repl)
        self.light.off()
        # 按键
        self.button = Button(self.repl)
        self.button_A = Button(self.repl, name='btn_A')
        self.button_B = Button(self.repl, name='btn_B')
        # RGB_LED
        self.rgb = Rgb_led(self.repl)
        # self.Easy_AI = Easy_AI(self.repl,self.serial)

    def image_init(self):
        # 主绘图对象
        # self.image = Image(self.repl, ref='img')
        self.image = Image(self.repl)

    def asr_init(self):
        self.asr = Maix_asr(self.repl)

    def asr_release(self):
        if self.asr != None:
            self.asr.release()

    def face_recognize_init(self, _face_num, _accuracy, _choice):
        self.fcr = Face_recogization(self.repl, face_num=_face_num, accuracy=_accuracy, choice=_choice)

    def self_learning_classifier_init(self, _class_num, _sample_num, _threshold, _choice):
        self.slc = Self_learning_classfier(self.repl, class_num=_class_num, sample_num=_sample_num, threshold=_threshold, choice=_choice)
        # return self.slc

    def qrcode_init(self, _choice):
        self.qrcode = QRCode_recognization(self.repl, choice=_choice)

    def color_init(self, _choice):
        self.color = color_recognization(self.repl, choice=_choice)