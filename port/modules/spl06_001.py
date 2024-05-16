from time import sleep_ms
from mpython import i2c as _i2c

class Barometric(object):
    """SPL06-001"""
    '''乐动模块 气压传感器'''
    def __init__(self,i2c=None):
        if(i2c==None):
            self.i2c = _i2c
        else:
            self.i2c = i2c
        addr = self.i2c.scan()

        if 119 in addr:
            self.IIC_ADDR = 119
        else:
            raise OSError("SPL06-001 init error, not found device!!!")
        
        self._writeReg(0x06, 0x01) # 压力配置寄存器
        self._writeReg(0x07, 0x80) # 温度配置寄存器
        self._writeReg(0x08, 0x07) # 设置连续的压力和温度测量
        self._writeReg(0x09, 0x00) 
        sleep_ms(100)

        try:
            id = self._readReg(0x0D)
            if(id[0]!=0x10):
                print('SPL06 ID error:',id)
        except OSError as e:
            print(e)


    def _readReg(self, reg, nbytes=1):
        return self.i2c.readfrom_mem(self.IIC_ADDR, reg, nbytes)

    def _writeReg(self, reg, value):
        self.i2c.writeto_mem(self.IIC_ADDR, reg, value.to_bytes(1, 'little'))

    def get_traw(self):
        tmp_MSB = self._readReg(0x03)
        tmp_LSB = self._readReg(0x04)
        tmp_XLSB = self._readReg(0x05)

        tmp = (tmp_MSB[0] << 16) | (tmp_LSB[0] << 8) | tmp_XLSB[0]
        if(tmp & (1 << 23)):
            tmp= -((tmp ^ 0xffffff) +1)

        return tmp

    def get_temperature_scale_factor(self):
        tmp_Byte = self._readReg(0x07)
        tmp_Byte = tmp_Byte[0] & 0B111 

        if(tmp_Byte == 0B000):
            k = 524288.0
        elif(tmp_Byte == 0B001):
            k = 1572864.0
        elif(tmp_Byte == 0B010):
            k = 3670016.0
        elif(tmp_Byte == 0B011):
            k = 7864320.0
        elif(tmp_Byte == 0B100):
            k = 253952.0
        elif(tmp_Byte == 0B101):
            k = 516096.0
        elif(tmp_Byte == 0B110):
            k = 1040384.0
        elif(tmp_Byte == 0B111):
            k = 2088960.0 

        return k

    def get_pressure_scale_factor(self):
        tmp_Byte = self._readReg(0x06)
        tmp_Byte = tmp_Byte[0] & 0B111 

        if(tmp_Byte == 0B000):
            k = 524288.0
        elif(tmp_Byte == 0B001):
            k = 1572864.0
        elif(tmp_Byte == 0B010):
            k = 3670016.0
        elif(tmp_Byte == 0B011):
            k = 7864320.0
        elif(tmp_Byte == 0B100):
            k = 253952.0
        elif(tmp_Byte == 0B101):
            k = 516096.0
        elif(tmp_Byte == 0B110):
            k = 1040384.0
        elif(tmp_Byte == 0B111):
            k = 2088960.0

        return k

    def get_praw(self):
        tmp_MSB = self._readReg(0x00)
        tmp_LSB = self._readReg(0x01)
        tmp_XLSB = self._readReg(0x02)

        tmp = ((tmp_MSB[0] << 16) | (tmp_LSB[0] << 8) | tmp_XLSB[0] ) & 0x00ffffff

        if(tmp & (1 << 23)):
            tmp= -((tmp ^ 0xffffff) +1)

        return tmp

    def get_c0(self):
        tmp_MSB = self._readReg(0x10)
        tmp_LSB = self._readReg(0x11)

        tmp_LSB = tmp_LSB[0] >> 4
        tmp = tmp_MSB[0] << 4 | tmp_LSB

        if (tmp & (1 << 11)):
            tmp= -((tmp ^ 0xfff) +1)
            
        return tmp
    
    def get_c1(self):
        tmp_MSB = self._readReg(0x11)
        tmp_LSB = self._readReg(0x12)

        tmp = ((tmp_MSB[0] & 0xF) << 8) | tmp_LSB[0]

        if (tmp & (1 << 11)):
            tmp= -((tmp ^ 0xfff) +1)

        return tmp
    
    def get_c00(self):
        tmp_MSB = self._readReg(0x13)
        tmp_LSB = self._readReg(0x14)
        tmp_XLSB = self._readReg(0x15)

        tmp = ((tmp_MSB[0] << 12) | (tmp_LSB[0] << 4) | (tmp_XLSB[0] >> 4))

        if(tmp & (1 << 19)):
            tmp = -((tmp ^ 0xfffff) +1)
        
        return tmp

    def get_c10(self):
        tmp_MSB = self._readReg(0x15)
        tmp_LSB = self._readReg(0x16)
        tmp_XLSB = self._readReg(0x17)

        tmp_MSB = tmp_MSB[0] & 0x0F

        tmp = (tmp_MSB << 16) | (tmp_LSB[0]  << 8) | tmp_XLSB[0]

        if(tmp & (1 << 19)):
            tmp= -((tmp ^ 0xFFFFF) +1)

        return tmp

    def get_c01(self):
        tmp_MSB = self._readReg(0x18)
        tmp_LSB = self._readReg(0x19)

        tmp = (tmp_MSB[0] << 8) | tmp_LSB[0]

        if(tmp & (1 << 15)):
            tmp= -((tmp ^ 0xFFFF) +1)

        return tmp

    def get_c11(self):
        tmp_MSB = self._readReg(0x1A)
        tmp_LSB = self._readReg(0x1B)

        tmp = (tmp_MSB[0] << 8) | tmp_LSB[0]

        if(tmp & (1 << 15)):
            tmp= -((tmp ^ 0xFFFF) +1)

        return tmp

    def get_c20(self):
        tmp_MSB = self._readReg(0x1C)
        tmp_LSB = self._readReg(0x1D)

        tmp = (tmp_MSB[0] << 8) | tmp_LSB[0]
        
        if(tmp & (1 << 15)):
            tmp= -((tmp ^ 0xFFFF) +1)

        return tmp

    def get_c21(self):
        tmp_MSB = self._readReg(0x1E)
        tmp_LSB = self._readReg(0x1F)
        tmp = (tmp_MSB[0] << 8) | tmp_LSB[0]
        
        if(tmp & (1 << 15)):
            tmp= -((tmp ^ 0xFFFF) +1)

        return tmp

    def get_c30(self):
        tmp_MSB = self._readReg(0x20)
        tmp_LSB = self._readReg(0x21)

        tmp = (tmp_MSB[0] << 8) | tmp_LSB[0]
        
        if(tmp & (1 << 15)):
            tmp= -((tmp ^ 0xFFFF) +1)

        return tmp
    
    def temperature(self):
        """
        获取温度
        :return: 温度,单位摄氏度
        """
        c0 = self.get_c0()
        c1 = self.get_c1()
        traw = self.get_traw()
        t_scale = self.get_temperature_scale_factor()

        traw_sc = traw / t_scale
        temp_c = ((c0) * 0.5) + ((c1) * traw_sc)
        temp_f = (temp_c * 9/5) + 32 #华氏度

        return temp_c

    def pressure(self):
        """
        获取气压
        :return: 气压,单位Pa
        """
        pcomp = None
        try:
            traw = self.get_traw()
            t_scale = self.get_temperature_scale_factor()
            traw_sc = traw / t_scale
            praw = self.get_praw()
            p_scale = self.get_pressure_scale_factor()
            praw_sc = praw / p_scale

            pcomp = self.get_c00()+ praw_sc*(self.get_c10()+ praw_sc*(self.get_c20()+ praw_sc*self.get_c30())) + traw_sc*self.get_c01() + traw_sc*praw_sc*(self.get_c11()+praw_sc*self.get_c21())
        except:
            pass

        return pcomp
