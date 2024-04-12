from mpython import *
import time

def number_map(inputNum, bMin, bMax, cMin, cMax):
    outputNum = 0
    outputNum = ((cMax - cMin) / (bMax - bMin)) * (inputNum - bMin) + cMin
    return outputNum

class PM25_():
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
        
        print('测量中...')
        return dustDensity
        
    def dustDensity_average(self):
        dustDensity_list = []
        for i in range(3):
            time.sleep(0.3)
            _tmp = self.read()
            dustDensity_list.append(_tmp)
  
        dustDensity = sum(dustDensity_list)/len(dustDensity_list)
        
        return dustDensity


# constants
SAMPLING_TIME = 0.00028
DELTA_TIME = 0.00004
SLEEP_TIME = 0.00968
vcc = 3.3

class PM25():
    def __init__(self):
        self.digital_pin = MPythonPin(1, PinMode.OUT)
        self.analog_pin = MPythonPin(0, PinMode.ANALOG)
        self.delayTime = 280 
        self.delayTime2 = 40
        self.offTime = 9680
        self.dustVal = 0
        self.MAX = 0
        self.VOC = 0.6
        
    def read(self, sample_size=30):
        vals = []
        print('PM2.5测量中..')
        while True:
            sleep(0.002)
            try:
                self.digital_pin.write_digital(0)
                sleep(SAMPLING_TIME)
                vals.append(self.analog_pin.read_analog())
                sleep(DELTA_TIME)
                self.digital_pin.write_digital(1)
                sleep(SLEEP_TIME)
                if len(vals) == sample_size:
                    avg = sum(vals) / len(vals)
                    volt = self.calc_volt(avg)
                    density = self.calc_density(volt)
                    mv = volt * 1000
                    # print(
                    #     "{mv} mV / {density} ug/m3 (Voc={voc}) | Max: {max_} ug/m3".format(
                    #         mv=round(mv,2),
                    #         density=round(density,2),
                    #         voc=self.VOC,
                    #         max_=self.MAX,
                    #     )
                    # )
                    vals = []
                    return round(density,2)
            except KeyboardInterrupt:
                break
            except Exception:
                raise
            finally:
                self.digital_pin.write_digital(0)

    def calc_volt(self, val):
        return val * vcc / 1024

    def calc_density(self,vo, k=0.5):
        dv = vo - self.VOC
        if dv < 0:
            dv = 0
            self.VOC = vo
        density = dv / k * 100
        self.MAX = max(self.MAX, density)
        return density

    def dustDensity_average(self):
        return self.read()