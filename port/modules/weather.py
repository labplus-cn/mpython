import struct
from machine import UART, Pin
import time

class modus_crc():
  def __init__(self):
    pass   

  def calculateCRC(self, dataarray):#输入是列表，输出是带CRC校验的列表
    datalist = dataarray
    date03 = dataarray[:]
    try:
      # print (u'对应的序列：{0}'.format(datalist))
      # 处理第1个字节数据
      temp = self.calculateonebyte(datalist[0], 0xFFFF)
      # 循环处理其它字节数据
      for data in datalist[1:]:
        temp = self.calculateonebyte(data,temp)
      date03.append(temp & 0xff)
      date03.append(temp >> 8)
      return date03
    except:
      pass

  def calculateonebyte(self,databyte, tempcrc): 
    """
    计算1字节数据的CRC值
    :param databyte: 需计算的字节数据
    :param tempcrc: 当前的CRC值
    :return: 当道新的CRC值
    """
    # databyte必须为字节数据
    # assert 0x00 <= databyte <= 0xFF
    # 同上字节数据检查
    if not 0x00 <= databyte <= 0xFF:
      raise Exception((u'数据：0x{0:<02X}不是字节数据[0x00-0xFF]'.format(databyte)).encode('utf-8'))
 
    # 把字节数据根CRC当前值的低8位相异或
    low_byte = (databyte ^ tempcrc) & 0x00FF
    # 当前CRC的高8位值不变
    resultCRC = (tempcrc & 0xFF00) | low_byte
    # 循环计算8位数据
    for index in range(8):
      # 若最低为1：CRC当前值跟生成多项式异或;为0继续
      if resultCRC & 0x0001 == 1:
        #print("[%d]: 0x%4X ^^^^ 0x%4X" % (index,resultCRC>>1,resultCRC^GENERATOR_POLYNOMIAL))
        resultCRC >>= 1
        resultCRC ^= 0xA001 # 0xA001是0x8005循环右移16位的值
      else:
        # print ("[{0}]: 0x{1:X} >>>> 0x{2:X}".format(index,resultCRC,resultCRC>>1))
        resultCRC >>= 1
    return resultCRC

  def into(self, strr):#输入串口数据,b'\x01\x02'
    try :
      # into0=self.calculateCRC(list(struct.unpack('%dB'%len(strr),strr)))#先变元祖再转列表
      into0 = self.calculateCRC(strr)
      into0 = struct.pack('%dB' %len(into0), *into0)
      return into0
    except:
      pass

class WEATHER(object):
    def __init__(self, uart_num=1, pin_tx = Pin.P14, pin_rx = Pin.P13):
      self.wait_time = 200
      self.crc = modus_crc()
      self.uart = UART(uart_num, baudrate = 4800, tx = pin_tx, rx = pin_rx)
      self.rainfall = None # 降雨量，单位mm
      self.wind_power = None # 风速 m/s
      self.wind_dir = None
      self.wind_dir_angle = None 
      self.humidity = None 
      self.temperature = None 
      self.pressure = None 
      ''' 
      地址码	功能码	  起始地址	   数据长度	 校验码低位	校验码高位
      0x01	0x03	0x00 0x00	0x00 0x02	xx	     xx        风向命令
      0x02	0x03	0x00 0x00	0x00 0x01	xx	     xx        风速
      0x03	0x03	0x01 0xF4	0x00 0x0B	xx	     xx        百叶箱 温湿度 气压
      0x04	0x03	0x00 0x00	0x00 0x01	xx	     xx        雨量
      0x04	0x06	0x00 0x00	0x00 0x5A	xx	     xx        清除雨量
        '''
    def _write_cmd(self, cmd):
      while self.uart.any():
        tmp = self.uart.read(1)
      tmp = self.crc.into(cmd)
      self.uart.write(tmp)

    def _read(self, num):
      if self.uart.any():
          return self.uart.read(num)
      
    def read_rainfall(self):
      '''读总降雨量值
      返回数据包示例
      地址码	功能码	返回有效字节数	雨量值	 校验码低位	校验码高位
      0x04	0x06	0x02	    0x00 0x5A	xx	     xx
      '''
      cmd_rainfall = [0x0a, 0x03, 0x00, 0x00, 0x00, 0x01]
      self._write_cmd(cmd_rainfall)
      time.sleep_ms(self.wait_time)
      tmp = self._read(7)
      # print(tmp)
      if tmp != None and len(tmp) == 7:
          l = struct.unpack(">H", tmp[3:])
          return l[0]/10 # 降雨量要除以10，单位mm
      return None

    def rainfall_clear(self):
      '''清除降雨量值
      返回数据包示例
      地址码	功能码	  起始寄存器	  清除命令	   校验码低位	校验码高位
      0x04    0x06     0x00 0x00	    0x00 0x1A	   xx	     xx
      '''
      cmd_rainfall_clear = [0x0a, 0x06, 0x00, 0x00, 0x00, 0x5A]
      self._write_cmd(cmd_rainfall_clear)
      time.sleep_ms(self.wait_time)
      tmp = self._read(8)
      # print(tmp)

    def read_wind_power(self):
      '''
      地址码	功能码	返回有效字节数	当前风速值(m/s)	 当前风速值(级)  校验码低位	校验码高位
      0x01	0x03	0x04	     0x00   0x56      0x00   0x02     xx	    xx
      # 0x02, 0x03, 0x00, 0x00, 0x00, 0x02, 0xc4, 0x38
      '''
      cmd_wind_power = [0x02, 0x03, 0x00, 0x00, 0x00, 0x02]
      self._write_cmd(cmd_wind_power)
      time.sleep_ms(self.wait_time)
      tmp = self._read(9)
      if tmp != None and len(tmp) == 9:
          l = struct.unpack(">2H", tmp[3:7])
          return l[0]/10,l[1]  # 风速m/s 风速 X级， 风速要除以10 
      return None
     
    def read_wind_direction(self):
      '''
      地址码	功能码	返回有效字节数	风向(0-7档)	风向(0-360°)	校验码低位	校验码高位
      0x01	0x03	0x04	      0x00 0x02	 0x00 0x5A	       xx       xx
      0x01, 0x03, 0x00, 0x00, 0x00, 0x02 ,196,11
      '''
      cmd_wind_direction = [0x01, 0x03, 0x00, 0x00, 0x00, 0x02]
      self._write_cmd(cmd_wind_direction)
      time.sleep_ms(self.wait_time)
      tmp = self._read(9)
      if tmp != None and len(tmp) == 9:
          l = struct.unpack(">2H", tmp[3:7])
          return l[0],l[1]  # 风向 0-7 对应北风 -> 西北风 风向 度，
      return None,None

    def read_T_H_P(self):
      '''
      地址码	功能码	有效字节数	湿度值	   温度值	  校验码低位	校验码高位
      0x03	0x03	0x04	0x02 0x92	0xFF 0x9B	0x79	    0xFD
      '''
      cmd_T_H_P = [0x03, 0x03, 0x01, 0xf4, 0x00, 0x06]
      self._write_cmd(cmd_T_H_P)
      time.sleep_ms(self.wait_time)
      tmp = self._read(17)
      if tmp != None and len(tmp) == 17:
          l = struct.unpack(">6H", tmp[3:])
          return l[0],l[1],l[5]  # l[0]温度 l[1]湿度 都要除以10 l[5]气压 单位kpa
      return None,None,None
    
    def update_data(self):
      '''
      '''
      time.sleep_ms(50)
      self.rainfall = self.read_rainfall() # 降雨量，单位mm
      time.sleep_ms(200)
      self.wind_power = self.read_wind_power() # 风速 m/s
      time.sleep_ms(200)
      self.wind_dir,self.wind_dir_angle = self.read_wind_direction() #
      time.sleep_ms(200)
      self.humidity, self.temperature, self.pressure = self.read_T_H_P()
      time.sleep_ms(100)


