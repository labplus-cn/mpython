from machine import UART
from mpython import *
import gc

class utf8_gb2312(object):
    def __init__(self):
        self.f = open('gb2312_font.txt', 'r', encoding='utf-8')

    def b2i(self, byte):  # bytes转int
        r = 0
        for i in range(len(byte)):
            r = (r << 8) + byte[i]
        return r

    def i2b(self, num):  # int转bytes
        num = int(num, 16)
        return num.to_bytes(2, 'big')

    def one_char(self, char):  # 将一个字符转化成gb2312
        utf_byte = char.encode('utf-8')
        r = self.B_S(0, 7296, self.b2i(utf_byte))
        gb2312_byte = self.i2b(r)
        return gb2312_byte

    def str(self, st):  # 将字符串转化成gb2312
        r = b''
        for s in st:
            # print(s.encode('utf-8'))
            if len(s.encode('utf-8')) <= 1:
                r += s.encode('utf-8')
            else:
                r += self.one_char(s)
        return r

    def B_S(self, low, high, m):  # 二分查找
        if 0 <= low <= high <= 7296:
            mid = (low + high) // 2
            self.f.seek(mid * 12)
            data = self.f.read(12)
            utf = data[0:6]
            if int(utf, 16) < m:
                return self.B_S(mid + 1, high, m)
            elif int(utf, 16) > m:
                return self.B_S(low, mid - 1, m)
            else:
                return data[7:-1]

    def __del__(self):
        self.f.close()


class SpeechSynthesis(object):
    def __init__(self,uart_num=1, pin_tx=Pin.P16, pin_rx=Pin.P15):
        gc.collect()
        self.font_gb2312 = utf8_gb2312()
        self.uart = UART(uart_num, baudrate=115200, tx=pin_tx, rx=pin_rx)
        self.cache_s = '语音合成'
        self.cache_byte = b'\xd3\xef\xd2\xf4\xba\xcf\xb3\xc9'

    def play(self,s):
        busy_status = self.busy_status()
        s_len = len(s)
        wait_ms = 250 * s_len
        if(not busy_status):
            print('Synthetic audio ...')
            if(s == self.cache_s):
                r = self.cache_byte
            else:
                r = self.font_gb2312.str(str(s))
                self.cache_s = s
                self.cache_byte = r
            data_len = len(list(r)) + 2 
            revise_cmd = [0xFD, data_len >> 8, data_len & 0xff, 0x01, 0x00] + list(r)
            self.uart.write(bytes(revise_cmd))
            sleep_ms(wait_ms)
        else:
            print('busy status')
            pass

    def busy_status(self):
        try:
            self.uart.write(bytes([0xFD, 0x00, 0x01, 0x21]))
            sleep_ms(10)
            if (self.uart.any()):
                tmp = self.uart.read().decode('utf-8').strip()
                if(tmp=='O'):
                    return False
                elif(tmp=='AN'):
                    return True
        except:
            return True

    def release(self):
        self.font_gb2312.__del__()
        gc.collect()

# speech_synthesis = SpeechSynthesis(uart_num=1, pin_tx=Pin.P16, pin_rx=Pin.P15)
# speech_synthesis.play('行路难（其一）【唐】 李白 金樽清酒斗十千，玉盘珍羞直万钱。停杯投箸不能食，拔剑四顾心茫然。欲渡黄河冰塞川，将登太行雪满山。闲来垂钓碧溪上，忽复乘舟梦日边。行路难，行路难，多歧路，今安在？长风破浪会有时，直挂云帆济沧海。')
