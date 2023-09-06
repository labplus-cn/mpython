from machine import UART, Pin
from mpython import *
import time
import hrcalc

# i2c 地址
I2C_WRITE_ADDR = 0xAE
I2C_READ_ADDR = 0xAF

#设备内部寄存器地址
REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01

REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03

REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08

REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1_PA = 0x0C

REG_LED2_PA = 0x0D
REG_PILOT_PA = 0x10
REG_MULTI_LED_CTRL1 = 0x11
REG_MULTI_LED_CTRL2 = 0x12

REG_TEMP_INTR = 0x1F
REG_TEMP_FRAC = 0x20
REG_TEMP_CONFIG = 0x21
REG_PROX_INT_THRESH = 0x30
REG_REV_ID = 0xFE
REG_PART_ID = 0xFF

class MAX30102():
    #默认使用引脚X1作为中断引脚，连接模块的INT引脚
    def __init__(self):
        self.ir_D = None
        self.red_D = None
        self.i2c = i2c
        self.address = 0x57
        # self.interrupt = MPythonPin(15, PinMode.IN)  #设置中断引脚为输入模式
        self.reset() 
        # print("intpin: {0}, address: {1}".format(self.address))   
        time.sleep(0.5)
        addr = self.i2c.scan()
        if self.address not in addr:
            print('max30102 device not found!\n')
        else:
            self.setup()
        time.sleep(1)
        print('max30102 device init.\n')

    def _writeReg(self, value, reg):
        self.i2c.writeto_mem(self.address, reg, value.to_bytes(1, 'little'))
    
    def _readReg(self, reg, nbytes=1):
        return self.i2c.readfrom_mem(self.address, reg, nbytes)

    def shutdown(self):
        """
        关闭模块
        """
        self._writeReg(0x80, REG_MODE_CONFIG)

    def reset(self):
        """
        Reset the device, this will clear all settings,
        so after running this, run setup() again.
        """
        self._writeReg(0x40,  REG_MODE_CONFIG)

    def setup(self, led_mode=0x03):
        """
        模块的初始化设置
        """
        self._writeReg(0xc0, REG_INTR_ENABLE_1)
        self._writeReg(0x00, REG_INTR_ENABLE_2)
        self._writeReg(0x00, REG_FIFO_WR_PTR)
        self._writeReg(0x00, REG_OVF_COUNTER)
        self._writeReg(0x00, REG_FIFO_RD_PTR)
        self._writeReg(0x4f, REG_FIFO_CONFIG)
        self._writeReg(led_mode, REG_MODE_CONFIG)
        self._writeReg(0x27, REG_SPO2_CONFIG)
        self._writeReg(0x24, REG_LED1_PA)
        self._writeReg(0x24, REG_LED2_PA)
        self._writeReg(0x7f, REG_PILOT_PA)


    def set_config(self, reg, value):
        self._writeReg(value, reg)

    def read_fifo(self):
        """
        读取寄存器的数据
        """
        red_led = None
        ir_led = None

        #从寄存器中读取1个字节的数据
        reg_INTR1 = self._readReg(REG_INTR_STATUS_1,1)
        reg_INTR2 = self._readReg(REG_INTR_STATUS_2,1)

        d = self._readReg(REG_FIFO_DATA,6)

        # mask MSB [23:18]
        red_led = (d[0] << 16 | d[1] << 8 | d[2]) & 0x03FFFF
        ir_led = (d[3] << 16 | d[4] << 8 | d[5]) & 0x03FFFF

        return red_led, ir_led
    def read_sequential(self, amount=100):
        """
        读取模块上红色LED和红外光LED测量的数据
        """
        red_buf = []
        ir_buf = []
        for i in range(amount):
            # while(self.interrupt.read_digital() == 1):
            #     #等待中断信号
            #     pass
            time.sleep_ms(30)
            red, ir = self.read_fifo()

            red_buf.append(red)
            ir_buf.append(ir)

        return red_buf, ir_buf

    def measurement(self):
        time.sleep(0.5)
        try:
            print('In the measurement, it takes approximately 30 seconds.\n')
            # print('测量中，将手指放在传感器上保持不动，大约需要30-60秒\n')
            #采样数据，大约30秒钟
            red, ir = self.read_sequential(1000)
            #进行分析
            ir_avg = []
            red_avg = []
            for i in range(37):
                d = hrcalc.calc_hr_and_spo2(ir[25*i:25*i+100], red[25*i:25*i+100])
                # print(d)
                if(d[1] and d[0]<110 and d[0]>40):
                    ir_avg.append(d[0])
                if(d[3] and d[2]>80):
                    red_avg.append(d[2])
            if(len(ir_avg) >=3):
                self.ir_D = (sum(ir_avg) - max(ir_avg) - min(ir_avg)) // (len(ir_avg) - 2)
                self.red_D = (sum(red_avg) - max(red_avg) - min(red_avg)) // (len(red_avg) - 2)
            else:
                self.ir_D = (sum(ir_avg)) // len(ir_avg)
                self.red_D = (sum(red_avg)) // len(red_avg)
            # print(ir_avg)
            print('Measurement completed.\n')
            self.ir_D = int(self.ir_D)
            self.red_D = int(self.red_D)
            # print('测试完成\n')
            # print('****************************\n')
        except Exception as e:
            print("An error occurred.\n")
            print('测量出错。\n')
            print(e)
            self.ir_D = None
            self.red_D = None