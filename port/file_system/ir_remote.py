from machine import Pin,PWM
import time
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


class IRReceiver():
    """ IR Decode """

    def __init__(self, pin):
        self.pulse_buffer = []
        self._prev_time = 0
        self.callback = None
        self.recv = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.recv.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
                      handler=self._pulse_width_record)
        self.lenth = 0
        self.waittime = 150000

        self.debug = False
        

    def _pulse_width_record(self, pin):
        """record the width of th IR remote signal."""
        self._time = time.ticks_us()
        if self._prev_time == 0:
            self._prev_time = self._time
            return
        self.pulse_buffer.append(self._time - self._prev_time)
        self._prev_time = self._time
        self.lenth = self.lenth + 1

    def _lead_cheak(self,pulse_width_list):
        """function to cheak the lead code """
        return (abs(pulse_width_list[0] - _Const.NEC_HDR_MARK) <
                _Const.NEC_HDR_MARK * _Const.TOLERANCE) and (
                    abs(pulse_width_list[1] - _Const.NEC_HDR_SPACE) <
                    _Const.NEC_HDR_SPACE * _Const.TOLERANCE)

    
    def _ir_recv_daemon(self):
        """ background handles ir signal """
        while True:
            if (time.ticks_us()-self._prev_time) > self.waittime and self.pulse_buffer != []:
                dec = self.decode_buff()
                if self.callback:
                    self.callback(dec & 0xff, (dec >> 16) & 0xff)

    def daemon(self):
        """ daemon start """
        _thread.start_new_thread(self._ir_recv_daemon, ())

    def set_callback(self,callback = None):
        """ function to allow the user to set or change the callback function """
        self.callback = callback


    def find_start_index(self,pulse_width_list):
        """ find the acceptable start of the pulse_buffer. """
        for i in range(len(pulse_width_list)):
            if abs(pulse_width_list[i] - _Const.NEC_HDR_MARK) < _Const.NEC_HDR_MARK * _Const.TOLERANCE:
                return i
        return
    
    def decode_buff(self):
        """ decode pulse to hex str """
        decstr = 0xffff
        try:
            if self.debug:
                print(self.pulse_buffer)
            if len(self.pulse_buffer) > 66:
                pulse_width_list = self.pulse_buffer[self.find_start_index(self.pulse_buffer):]
                if self._lead_cheak(pulse_width_list):
                    # decstr = self.bin2hex(self.pulse_width2bit_line(pulse_width_list))
                    decstr = int(self.pulse_width2bit_line(pulse_width_list), 2)
                else:
                    # print("Warning: Buffer lead code error!")
                    pass
            else:
                # print("Warning: Buffer length too short!")
                pass
        except Exception as e:
            print(e)
            pass
        self._prev_time = 0
        self.pulse_buffer.clear()
        gc.collect()
        return decstr


    @staticmethod
    def pulse_width2bit_line(pulse_width_list):
        """ pulses width list to bit list"""
        bit_list = list()
        for i in range(_Const.STARTDATAINDEX,len(pulse_width_list),2):
            if i+1 < len(pulse_width_list):
                if abs(pulse_width_list[i+1] - _Const.NEC_ONE_SPACE) < _Const.NEC_ONE_SPACE * _Const.TOLERANCE:
                    bit_list.append(1)
                elif abs(pulse_width_list[i+1] - _Const.NEC_ZERO_SPACE) < _Const.NEC_ZERO_SPACE * _Const.TOLERANCE:
                    bit_list.append(0)
                else:
                    break
        bit_list.reverse()
        bit_line = ''.join([str(i) for i in bit_list])
        return bit_line

    @staticmethod
    def bin2hex(bit_line):
        """ bit str to hex str """
        return '{:x}'.format(int(bit_line,2))


class IRSender():
    """ IR NEC Sender """
    def __init__(self,pin):
        # 38Khz
        self.ir_pin = PWM(Pin(pin,Pin.OUT), duty=0, freq=38000)

    def _lead(self):
        """ send lead signal """
        self.ir_pin.duty(512)
        time.sleep_us(_Const.NEC_HDR_MARK)
        self.ir_pin.duty(0)
        time.sleep_us(_Const.NEC_HDR_SPACE)
    
    def _end(self):
        """ send lead signal """
        self.ir_pin.duty(512)
        time.sleep_us(_Const.NEC_BIT_MARK)
        self.ir_pin.duty(0)

    def _reverseduty(self):
        """ reverse ir pin duty """
        if self.ir_pin.duty() == 0:
            self.ir_pin.duty(512)
        else:
            self.ir_pin.duty(0)

    def send(self,cmd):
        """ send hex code to ir signal """
        bit_list = '{:b}'.format(int(cmd,16))
        self._lead()
        for i in bit_list:
            self.ir_pin.duty(512)
            time.sleep_us(_Const.NEC_BIT_MARK)
            self.ir_pin.duty(0)
            if i == '0':
                time.sleep_us(_Const.NEC_ZERO_SPACE)
            else:
                time.sleep_us(_Const.NEC_ONE_SPACE)
        self._end()

    def sender(self,cmd):
        pulse_width_list = self.coding(cmd)
        for i in pulse_width_list:
            self._reverseduty()
            time.sleep_us(i)
        self.ir_pin.duty(0)

    @staticmethod
    def coding(cmd):
        """ send hex code to ir signal by precoding """
        bit_list = '{:b}'.format(int(cmd,16))
        pulse_width_list = [_Const.NEC_HDR_MARK,_Const.NEC_HDR_SPACE]
        for i in bit_list:
            pulse_width_list.append(_Const.NEC_BIT_MARK)
            if i == '0':
                pulse_width_list.append(_Const.NEC_ZERO_SPACE)
            else:
                pulse_width_list.append(_Const.NEC_ONE_SPACE)
        pulse_width_list.append(_Const.NEC_BIT_MARK)
        return pulse_width_list



# if __name__ == "__main__":
    # Reciver
    # receiver = IRReceiver(33)
    # receiver.callback = print
    # 当Receiver daemon开启时会对Sender的计时器造成严重的误差,不建议监听的同时发送红外信号
    # receiver.daemon()


    # Sender
    # sender = IRSender(27)
    # sender.sender('c3f9070005000200000400a0e2')