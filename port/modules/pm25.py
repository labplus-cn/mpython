from mpython import *
import time

def number_map(inputNum, bMin, bMax, cMin, cMax):
    outputNum = 0
    outputNum = ((cMax - cMin) / (bMax - bMin)) * (inputNum - bMin) + cMin
    return outputNum

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
        if (self.dustVal > 1024):
            self.dustVal = 1024
        calcVoltage = self.dustVal * (3.3 / 1024.0) #将模拟值转换为电压值
        dustDensity = (0.17 * (3.89 - calcVoltage) - 0.1)*1000 # 将电压值转换为粉尘密度输出单位 ug/m3
        if (dustDensity < 0 ):
            dustDensity = 0
        
        # print("原始信号值:")
        # print(self.dustVal)
        # print(" 电压:")
        # print(calcVoltage)
        # print("PM2.5粉尘密度:")
        # print(dustDensity)
        # print("ug/m3")
        print('测量中...')
        return dustDensity
        
    def dustDensity_average(self):
        dustDensity_list = []
        for i in range(3):
            time.sleep(0.3)
            _tmp = self.read()
            dustDensity_list.append(_tmp)
  
        dustDensity = sum(dustDensity_list)/len(dustDensity_list)
        # print(dustDensity_list)
        # print("平均粉尘密度:")
        # print(dustDensity)
        if (300>=dustDensity>150):
            dustDensity = dustDensity/1.5
        elif(500>=dustDensity>300):
            dustDensity = dustDensity/2.25
        elif(dustDensity>500):
            dustDensity = -1
        
        return dustDensity