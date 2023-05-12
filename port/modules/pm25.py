from mpython import *
import time

class PM25():
    def __init__(self):
        self.digital_pin = MPythonPin(1, PinMode.OUT)
        self.analog_pin = MPythonPin(0, PinMode.ANALOG)
        self.delayTime = 280 
        self.delayTime2 = 40
        self.offTime = 9680
        self.dustVal = 0

    def read(self): 
        self.digital_pin.write_digital(1)
        time.sleep_us(self.delayTime)
        self.dustVal = self.analog_pin.read_analog()
        time.sleep_us(self.delayTime2)
        self.digital_pin.write_digital(0)
        time.sleep_us(self.offTime)
        time.sleep(1)
        # print(self.dustVal)
        # if self.dustVal > 36.455:
        #     self.dustVal = (self.dustVal / 1024 - 0.0356) * 4200
        Voltage = self.dustVal * 3.3 / 4096
        self.dustVal = (Voltage + 1) * 1000 / 10 # *1000作用是将单位转换为ug/m3

        return self.dustVal
