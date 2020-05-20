# labplus mPython-box for maixpy by uart library
# MIT license; Copyright (c) 2018 labplus

# mpython-box buildin periphers drivers

# history:
# V1.0 zhaohuijiang
from repl import REPL, Serial
from machine import Pin, ADC, UART
import time
import ujson
from mpython import i2c
import ubinascii
from k210 import *


# 通讯接口初始化
mpython_box = Serial(baudrate=2000000, rx_pin=14, tx_pin=13)
repl = REPL(mpython_box)
time.sleep(3)
repl.enter_raw_repl()

""" MaixPy功能实例 """
# 主绘图对象
image = Image(repl, ref='img')
# 显示屏
lcd = LCD(repl)
# 摄像头
sensor = Sensor(repl)
# AI运算
kpu = KPU(repl)


""" MaixPy端的外设实例 """
# 电机控制
motor = Motor(1, repl)
# 按键
btn_left = Button(repl, name='btn_left')
btn_right = Button(repl, name='btn_right')
btn_up = Button(repl, name='btn_up')
btn_down = Button(repl, name='btn_down')
btn_ok = Button(repl, name='btn_ok')
# 超声波
ultrasonic = Ultrasonic(repl)
# 补光灯
light = Light(repl)

# def get_distance():
#     """超声波,范围2~340cm"""
#     return ultrasonic.distance

# def get_key():
#     """方向按键,返回按键列表"""
#     keys = set()
#     if btn_left.was_pressed():
#         keys.add('left')
#     if btn_right.was_pressed():
#         keys.add('right')
#     if btn_up.was_pressed():
#         keys.add('up')
#     if btn_down.was_pressed():
#         keys.add('down')
#     if btn_ok.was_pressed():
#         keys.add('ok')
#     return keys

# def set_motor(speed):
#     """马达,范围±100"""
#     if speed < -100 or speed > 100:
#             raise ValueError("Invalid value,Range in -100~100")
#     motor.speed = speed


""" mPython端的外设实例 """
# human infrared
pir = Pin(21, mode=Pin.IN, pull=None)

# slide POT
slider_res = ADC(Pin(34))
slider_res.atten(slider_res.ATTN_11DB)


""" 实验箱兼容旧版驱动,内置模型应用。
"""


class Model(object):

    def __init__(self, repl):
        self.repl = repl
        self.task = None

        self.FACE_YOLO = 1
        self.CLASS_20_YOLO = 2
        self.MNIST_NET = 3
        self.CLASS_1000_NET = 4

        # self.YOLO2 = 1
        # self.MOBILENET = 2
        
    def select_model(self, builtin=None):
        """内置模型选择"""
        if builtin == self.FACE_YOLO:
            sensor.reset()
            sensor.set_framesize(Sensor.QVGA)
            sensor.set_pixformat(Sensor.RGB565)
            self.task = kpu.load(0x300000)
            kpu.init_yolo2(self.task,0.5, 0.3, 5, (1.889, 2.5245, 2.9465, 3.94056,
                                         3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025))
            self.classes = ['face']
        elif builtin == self.CLASS_20_YOLO:
            sensor.reset()
            sensor.set_framesize(Sensor.QVGA)
            sensor.set_pixformat(Sensor.RGB565)
            self.task = kpu.load(0x640000)
            kpu.init_yolo2(self.task, 0.5, 0.3, 5, (1.08, 1.19, 3.42, 4.41,
                                                    6.63, 11.38, 9.42, 5.11, 16.62, 10.52))
            self.classes = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow',
                            'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor']

        elif builtin == self.MNIST_NET:
            sensor.reset()
            sensor.set_framesize(Sensor.QVGA)
            sensor.set_pixformat(Sensor.GRAYSCALE)
            sensor.set_windowing((224, 224))
            sensor.set_hmirror(0)
            self.task = kpu.load(0x600000)
        else:
            raise ValueError('not support model')
        self.__model = builtin
        lcd.clear()

    def detect_yolo(self):
        _img = sensor.snapshot()
        if not self.task:
            raise TypeError('Not load model!')
        code = kpu.run_yolo2(self.task, _img)
        if code:
            for c in code:
                _img.draw_rectangle(c['x'], c['y'], c['w'], c['h'])
            lcd.display(_img)
            for c in code:
                lcd.draw_string(
                    c['x'], c['y']-16, '{}:{:0.2f}' .format(self.classes[c['classid']], c['value']), lcd.RED, lcd.WHITE)
        else:
            lcd.display(_img)
       
        return code


    def predict_net(self):
        """MobileNet模型预测"""
        # 内置手写数字应用
        if self.__model == self.MNIST_NET:
            img_cap = sensor.snapshot()
            img_cap = img_cap.resize(28, 28)
            img.draw_image(img_cap, 0, 0, x_scale=4.0, y_scale=4.0)
            img_cap.invert()
            img_cap.strech_char(1)
            img_cap.pix_to_ai()
            plist = kpu.forward(self.task, img_cap)
            pmax = max(plist)
            max_index = plist.index(pmax)
            lcd.display(img)
            lcd.draw_string(224, 0, "%d: %.3f" % (max_index, pmax), lcd.WHITE)
            return plist
        # 自定义MobileNet

    def deinit_yolo(self):
        """yolo释放"""
        kpu.deinit(self.task)

    def deinit_net(self):
        """net释放"""
        kpu.deinit(self.task)

# 实例内置模型应用
model = Model(repl)
