print('educore init')

from ._educore import *
# from ._educore import _pin as pin
from ._camera1956 import Camera1956
from ._smartcamera import EduSmartCamera
from ._ble import *


'''继承AI摄像头'''
class smartcamera(EduSmartCamera):
    def __init__(self, tx=16, rx=15):
        _tx = pins_esp32[tx]
        _rx = pins_esp32[rx]
        super().__init__(tx=_tx, rx=_rx)


class smartcamera1956(Camera1956):
    def __init__(self, tx=15, rx=16):
        _tx = pins_esp32[tx]
        _rx = pins_esp32[rx]
        super().__init__(tx=_tx, rx=_rx)

# wifi
wifi = WiFi()

# OLED
oled = OLED()

# MQTT 
mqttclient = MqttClient()

# educore定时器
# edu = EduCoreTIMER()

# 六轴加速度计数据
# accelerometer = edu.accelerometer

# 网页版人工智能摄像头
webcamera = webcamera()

# 按键A/B
# button_a = EduButton('a')
# button_b = EduButton('b')

# 电机
# parrot = PARROT()



# print('done')