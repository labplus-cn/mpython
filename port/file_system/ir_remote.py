from machine import Pin,PWM
import time
import utime
import _thread
import machine
import gc
# machine.freq(160000000)


class _Const:
    """ NEC Const """
    # 引导码：9000us 的载波+ 4500us  的空闲
    # 比特值“0”：560us 的载波+ 560us 的空闲
    # 比特值“1”：560us 的载波+ 1690us 的空闲
    NEC_HDR_MARK = 9000
    NEC_HDR_SPACE = 4500

    NEC_BIT_MARK = 560 
    NEC_ONE_SPACE = 1690
    NEC_ZERO_SPACE = 560

    NEC_RPT_SPACE = 2250

    TOLERANCE = 0.3
    STARTDATAINDEX = 2


# class IRReceiver():
#     """ IR Decode """

#     def __init__(self, pin):
#         self.pulse_buffer = []
#         self._prev_time = 0
#         self.callback = None
#         self.recv = Pin(pin, Pin.IN, Pin.PULL_UP)
#         self.recv.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
#                       handler=self._pulse_width_record)
#         self.lenth = 0
#         self.waittime = 150000

#         self.debug = False
        

#     def _pulse_width_record(self, pin):
#         """record the width of th IR remote signal."""
#         self._time = time.ticks_us()
#         if self._prev_time == 0:
#             self._prev_time = self._time
#             return
#         self.pulse_buffer.append(self._time - self._prev_time)
#         self._prev_time = self._time
#         self.lenth = self.lenth + 1

#     def _lead_cheak(self,pulse_width_list):
#         """function to cheak the lead code """
#         return (abs(pulse_width_list[0] - _Const.NEC_HDR_MARK) <
#                 _Const.NEC_HDR_MARK * _Const.TOLERANCE) and (
#                     abs(pulse_width_list[1] - _Const.NEC_HDR_SPACE) <
#                     _Const.NEC_HDR_SPACE * _Const.TOLERANCE)

    
#     def _ir_recv_daemon(self):
#         """ background handles ir signal """
#         while True:
#             if (time.ticks_us()-self._prev_time) > self.waittime and self.pulse_buffer != []:
#                 dec = self.decode_buff()
#                 if self.callback:
#                     self.callback(dec & 0xff, (dec >> 16) & 0xff)

#     def daemon(self):
#         """ daemon start """
#         _thread.start_new_thread(self._ir_recv_daemon, ())

#     def set_callback(self,callback = None):
#         """ function to allow the user to set or change the callback function """
#         self.callback = callback


#     def find_start_index(self,pulse_width_list):
#         """ find the acceptable start of the pulse_buffer. """
#         for i in range(len(pulse_width_list)):
#             if abs(pulse_width_list[i] - _Const.NEC_HDR_MARK) < _Const.NEC_HDR_MARK * _Const.TOLERANCE:
#                 return i
#         return
    
#     def decode_buff(self):
#         """ decode pulse to hex str """
#         decstr = 0xffff
#         try:
#             if self.debug:
#                 print(self.pulse_buffer)
#             if len(self.pulse_buffer) > 66:
#                 pulse_width_list = self.pulse_buffer[self.find_start_index(self.pulse_buffer):]
#                 if self._lead_cheak(pulse_width_list):
#                     # decstr = self.bin2hex(self.pulse_width2bit_line(pulse_width_list))
#                     decstr = int(self.pulse_width2bit_line(pulse_width_list), 2)
#                 else:
#                     # print("Warning: Buffer lead code error!")
#                     pass
#             else:
#                 # print("Warning: Buffer length too short!")
#                 pass
#         except Exception as e:
#             # print(e)
#             pass
#         self._prev_time = 0
#         self.pulse_buffer.clear()
#         gc.collect()
#         return decstr


#     @staticmethod
#     def pulse_width2bit_line(pulse_width_list):
#         """ pulses width list to bit list"""
#         bit_list = list()
#         for i in range(_Const.STARTDATAINDEX,len(pulse_width_list),2):
#             if i+1 < len(pulse_width_list):
#                 if abs(pulse_width_list[i+1] - _Const.NEC_ONE_SPACE) < _Const.NEC_ONE_SPACE * _Const.TOLERANCE:
#                     bit_list.append(1)
#                 elif abs(pulse_width_list[i+1] - _Const.NEC_ZERO_SPACE) < _Const.NEC_ZERO_SPACE * _Const.TOLERANCE:
#                     bit_list.append(0)
#                 else:
#                     break
#         bit_list.reverse()
#         bit_line = ''.join([str(i) for i in bit_list])
#         return bit_line

#     @staticmethod
#     def bin2hex(bit_line):
#         """ bit str to hex str """
#         return '{:x}'.format(int(bit_line,2))


# class IRSender():
#     """ IR NEC Sender """
#     def __init__(self,pin):
#         # 38Khz
#         self.ir_pin = PWM(Pin(pin,Pin.OUT), duty=0, freq=38000)

#     def _lead(self):
#         """ send lead signal """
#         self.ir_pin.duty(512)
#         time.sleep_us(_Const.NEC_HDR_MARK)
#         self.ir_pin.duty(0)
#         time.sleep_us(_Const.NEC_HDR_SPACE)
    
#     def _end(self):
#         """ send lead signal """
#         self.ir_pin.duty(512)
#         time.sleep_us(_Const.NEC_BIT_MARK)
#         self.ir_pin.duty(0)

#     def _reverseduty(self):
#         """ reverse ir pin duty """
#         if self.ir_pin.duty() == 0:
#             self.ir_pin.duty(512)
#         else:
#             self.ir_pin.duty(0)

#     def send(self,cmd):
#         """ send hex code to ir signal """
#         bit_list = '{:b}'.format(int(cmd,16))
#         self._lead()
#         for i in bit_list:
#             self.ir_pin.duty(512)
#             time.sleep_us(_Const.NEC_BIT_MARK)
#             self.ir_pin.duty(0)
#             if i == '0':
#                 time.sleep_us(_Const.NEC_ZERO_SPACE)
#             else:
#                 time.sleep_us(_Const.NEC_ONE_SPACE)
#         self._end()

#     def sender(self,cmd):
#         pulse_width_list = self.coding(cmd)
#         for i in pulse_width_list:
#             self._reverseduty()
#             time.sleep_us(i)
#         self.ir_pin.duty(0)

#     @staticmethod
#     def coding(cmd):
#         """ send hex code to ir signal by precoding """
#         bit_list = '{:b}'.format(int(cmd,16))
#         pulse_width_list = [_Const.NEC_HDR_MARK,_Const.NEC_HDR_SPACE]
#         for i in bit_list:
#             pulse_width_list.append(_Const.NEC_BIT_MARK)
#             if i == '0':
#                 pulse_width_list.append(_Const.NEC_ZERO_SPACE)
#             else:
#                 pulse_width_list.append(_Const.NEC_ONE_SPACE)
#         pulse_width_list.append(_Const.NEC_BIT_MARK)
#         return pulse_width_list



# if __name__ == "__main__":
    # Reciver
    # receiver = IRReceiver(33)
    # receiver.callback = print
    # 当Receiver daemon开启时会对Sender的计时器造成严重的误差,不建议监听的同时发送红外信号
    # receiver.daemon()


    # Sender
    # sender = IRSender(27)
    # sender.sender('c3f9070005000200000400a0e2')



class IRReceiver(object):
    CODE = {
        176: 0, 0: 1, 128: 2, 64: 3,32: 4, 160: 5, 96: 6,16: 7, 144: 8, 80: 9, 
        48:12, 112:14, 136: 17, 152: 25, 40:20, 104:22, 168:21
        }
 
    def __init__(self, pin):
        self.irRecv = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.irRecv.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.__handler)  # 配置中断信息
        self.ir_step = 0
        self.ir_count = 0
        self.buf64 = [0 for i in range(64)]
        self.recived_ok = False
        self.cmd = None
        self.cmd_last = None
        self.repeat = 0
        self.repeat_last = None
        self.t_ok = None
        self.t_ok_last = None
        self.start = 0
        self.start_last = 0        
        self.changed = False
 
    def __handler(self, source):
        """
        中断回调函数
        """
        thisComeInTime = utime.ticks_us()
 
        # 更新时间
        curtime = utime.ticks_diff(thisComeInTime, self.start)
        self.start = thisComeInTime
        
 
        if curtime >= 8500 and curtime <= 9500:
            self.ir_step = 1
            return
 
        if self.ir_step == 1:
            if curtime >= 4000 and curtime <= 5000:
                self.ir_step = 2
                self.recived_ok = False
                self.ir_count = 0
                self.repeat = 0
            elif curtime >= 2000 and curtime <= 3000:  # 长按重复接收
                self.ir_step = 3
                self.repeat += 1
 
        elif self.ir_step == 2:  # 接收4个字节
            self.buf64[self.ir_count] = curtime
            self.ir_count += 1
            if self.ir_count >= 64:
                self.recived_ok = True
                self.t_ok = self.start #记录最后ok的时间
                self.ir_step = 0
 
        elif self.ir_step == 3:  # 重复
            if curtime >= 500 and curtime <= 650:
                self.repeat += 1
 
    def __check_cmd(self):
        byte4 = 0
        for i in range(32):
            x = i * 2
            t = self.buf64[x] + self.buf64[x+1]
            byte4 <<= 1
            if t >= 1800 and t <= 2800:
                byte4 += 1
        user_code_hi = (byte4 & 0xff000000) >> 24
        user_code_lo = (byte4 & 0x00ff0000) >> 16
        data_code = (byte4 & 0x0000ff00) >> 8
        data_code_r = byte4 & 0x000000ff
        self.cmd = data_code
 
    def scan(self):        
        # 接收到数据
        if self.recived_ok:
            self.__check_cmd()
            self.recived_ok = False
            
        # 数据有变化
        if self.cmd != self.cmd_last or self.repeat != self.repeat_last or self.t_ok != self.t_ok_last:
            self.changed = True
        else:
            self.changed = False
 
        # 更新
        self.cmd_last = self.cmd
        self.repeat_last = self.repeat
        self.t_ok_last = self.t_ok
        # 对应按钮字符
        # print(self.cmd)
        s = self.CODE.get(self.cmd)
    
        return self.changed, s, self.repeat, self.t_ok, self.cmd

    def _ir_recv_daemon(self):
        while(True):
            # time.sleep_ms(100)
            try:
                changed, s, repeat, t_ok, cmd = self.scan()
            except Exception as e:
                pass
            if(changed and cmd!=None):
                if self.callback:
                    self.callback(cmd & 0xff, s)

    def daemon(self):
        _thread.start_new_thread(self._ir_recv_daemon, ())

    def set_callback(self,callback = None):
        self.callback = callback