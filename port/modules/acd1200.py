from mpython import *
from machine import UART, Pin
import time 

class ACD1200(object):
    def __init__(self, tx=Pin.P16, rx=Pin.P15, uart_num=1):
        self.uart = UART(uart_num, baudrate=1200, tx=tx, rx=rx, timeout = 40)
        self.auto_calibration_mode()
        self.read()
        time.sleep(2)

    def read(self):
        co2 = -1 # 单位ppm（百万分比浓度） 在大自然环境里，空气中二氧化碳的正常含量是0.04%（400 PPM)，在大城市里有时候达到500 PPM。室内没有人的情况下，二氧化碳浓度一般在500到1000 PPM左右。
        self.uart.write(bytes([0xFE,0xA6,0x00,0x01,0xA7]))
        time_cnt = time.ticks_ms()
        time.sleep_ms(800)
        while True:
            if self.uart.any():
                data = self.uart.read()
                if len(data)>=9 and data[0]==0xFE and data[1]==0xA6:
                    co2 = (data[4] << 8) + data[5]
                # print(co2)
                break
            if time.ticks_ms() - time_cnt > 50:
                break
        return co2
    
    def auto_calibration_mode(self):
        self.uart.write(bytes([0xFE,0xA6,0x02,0x04,0x00,0x01,0xAD]))
        try_num = 0
        time.sleep_ms(800)
        while True:
            if try_num >=5:
                return False
            time_cnt = time.ticks_ms()
            while True:
                if self.uart.any():
                    data = self.uart.read()
                    # print(data)
                    if(len(data) >= 5 and data[0] == 0xFE and data[1] == 0xA6 and data[1] + data[2] + data[3] == data[4]):
                        print('Set co2 auto calibration mode success!')
                        return True
                    
                if time.ticks_ms() - time_cnt > 100:
                    print('Retry Set co2 auto calibration mode.')
                    self.uart.write(bytes([0xFE,0xA6,0x02,0x04,0x00,0x01,0xAD]))
                    try_num = try_num + 1
                    break
                
'''
acd = ACD1200()

while True:
    sleep(1)
    co2 = acd.read()# 单位ppm（百万分比浓度） 在大自然环境里，空气中二氧化碳的正常含量是0.04%（400 PPM)，在大城市里有时候达到500 PPM。室内没有人的情况下，二氧化碳浓度一般在500到1000 PPM左右。
    print(co2)
'''