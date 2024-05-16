from machine import Pin, UART
from .k210.public import * 
import time
import gc
gc.collect()

class FCR:
    def __init__(self):
        self.id = None
        self.blinks = None
        self.mouth = None
        self.status = 0

class Camera1956:
    def __init__(self, rx=Pin.P16, tx=Pin.P15):
        self.fcr = FCR()
        self.fcr.blinks = None
        self.fcr.mouth = None
        self.fcr.id = None
        self.fun = 1
        self.uart = UART(2, baudrate=1500000, rx=rx, tx=tx, rxbuf=512)
        self.lock = False
        time.sleep(0.1)
        self.wait_for_ai_init()
        self.uart_listen()

    def wait_for_ai_init(self): 
        shake_cmd = 0xEF
        num = 0        
        while True:
            time.sleep_ms(100)
            gc.collect()
            num += 1
            CMD_TEMP = []
            self.uart.write(bytes(self.Generate_CMD([shake_cmd]))) #通信握手
            if(num>1000):
                print('错误:通信超时！')
                self.lock = False
                break

            if(num%50==0 and num<500):
                print('.'*int(num/50))
            if(self.uart.any()):
                head = self.uart.read(1)
                # print(head)
                if(head and head[0] == 0xFE):
                    CMD_TEMP.extend([0xFE])
                    res = self.uart.read(4)
                    # print(res)
                    for i in range(4):
                        CMD_TEMP.append(res[i])  
                    if CMD_TEMP[1]==0xFE and CMD_TEMP[2]==0xFE and CMD_TEMP[3]==0xFE:
                        shake_cmd=0xFF #通信握手
                    elif CMD_TEMP[1]==0xFE and CMD_TEMP[2]==0xFE and CMD_TEMP[3]==0xFF:
                        print('==1956摄像头通信成功==')
                        # self.lock = False
                        # time.sleep_ms(100)
                        _cmd = self.uart.read()
                        del _cmd
                        gc.collect()
                        time.sleep_ms(100)
                        break
    
    def Generate_CMD(self, cmd_data=[0]):
        check_sum = 0
        CMD = [0xEF]
        CMD.extend(cmd_data)

        # for i in range(3-len(cmd_data)):
        #     CMD.append(0)
        
        for i in range(len(CMD)):
            check_sum = check_sum + CMD[i]
        
        CMD.extend([check_sum & 0xFF])
        return CMD

    def uart_listen(self):
        self._task = TASK(func=self.uart_thread,sec=0.03)
        self._task.start()

    def uart_thread(self):
        while True:
            gc.collect()
            CMD_TEMP = []
            if(self.uart.any()):
                head = self.uart.read(1)
                if(head and head[0] == 0xFE):
                    CMD_TEMP.extend([0xFE])
                    res = self.uart.read(5)
                    for i in range(5):
                        CMD_TEMP.append(res[i])  

                    checksum = CheckCode(CMD_TEMP[:5])
                    if(checksum==CMD_TEMP[5]):
                        # print(CMD_TEMP[1:5])
                        self.process_messages(CMD_TEMP[1:5])
                else:
                    pass
    
    def process_messages(self,CMD):
        if(CMD[0]==1 and CMD[1]!=0xff and CMD[2]!=0xff):
            self.fcr.blinks = CMD[1]
            self.fcr.mouth = CMD[2]
            self.fcr.id = None
            self.fcr.status = 1
        elif(CMD[0]==1 and CMD[1]==0xff and CMD[2]==0xff):
            self.fcr.blinks = None
            self.fcr.mouth = None
            self.fcr.status = 0
        elif(CMD[0]==2):
            if(CMD[2]==0xFF):
                self.fcr.id = None
            else:
                self.fcr.id = CMD[2]

    def result(self):
        d = {"blink":self.fcr.blinks,"mouth_open":self.fcr.mouth,"status":self.fcr.status}
        return d
    
    def init(self, *args, **kwargs):
        args_list = []
        self.model_choose = kwargs.get('model', None)
        for arg in args:
            args_list.append(arg)
        args_len = len(args_list)
        if(self.model_choose is None and args_len<1):
            print('参数错误')
        else:
            self.model_choose = args_list[0]
        
        if(self.model_choose=='BLINK_MOUTH_DETECT' and args_len==1):
            self.mode = self.model_choose
        elif(self.model_choose=='FACE_DETECT' and args_len==1):
            self.mode = self.model_choose
        
    def stop(self):
        '''停止'''
        self.uart.write(bytes(self.Generate_CMD([0xEE])))

