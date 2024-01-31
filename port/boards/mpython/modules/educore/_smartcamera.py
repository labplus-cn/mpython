from machine import Pin, UART
from .k210 import *
import time
import gc
# gc.collect()

class EduSmartCamera:
    def __init__(self, rx=Pin.P15, tx=Pin.P16):
        self.sensor_choice = 1
        self.uart = UART(2, baudrate=1152000, rx=rx, tx=tx ,rxbuf=256)
        self.mode = DEFAULT_MODE
        self.lock = False
        time.sleep(0.2)
        self.wait_for_ai_init()
        self.thread_listen()

    def wait_for_ai_init(self): 
        self.lock = True
        num = 0        
        while True:
            gc.collect()
            time.sleep_ms(20)
            num +=1
            CMD_TEMP = []
            if(num>2000):
                print('错误:通信超时，请检查接线情况及掌控拓展电源是否打开！')
                break
            AI_Uart_CMD(self.uart,0x01,0x01,0xFF) # 发送k210软重启命令
            if(self.uart.any()):
                head = self.uart.read(2)
                if(head and head[0] == 0xBB and head[1] == 0xAA):
                    CMD_TEMP.extend([0xBB,0xAA])
                    cmd_type = self.uart.read(1)
                    CMD_TEMP.append(cmd_type[0])
                    if(CMD_TEMP[2]==0x01):
                        res = self.uart.read(9)
                        if(res[0]==0x01 and res[1]==0xff):
                            print("AI摄像头重启中...")
                            _cmd = self.uart.read()
                            del _cmd
                            gc.collect()
                            break
                else:
                    gc.collect()
                    _cmd = self.uart.read()
                    del _cmd
                    gc.collect()
        time.sleep(1.5) #等待k210重启
        num = 0
        while True:
            gc.collect()
            num +=1
            CMD_TEMP = []
            AI_Uart_CMD(self.uart,0x01,0x01,0x00) #通信握手
            time.sleep_ms(100)
            if(num>1000):
                print('错误:通信超时，请检查接线情况及掌控拓展电源是否打开！')
                self.lock = False
                break
            if(num%30==0 and num<500):
                print('.'*int(num/30))
            if(self.uart.any()):
                head = self.uart.read(2)
                if(head and head[0] == 0xBB and head[1] == 0xAA):
                    CMD_TEMP.extend([0xBB,0xAA])
                    cmd_type = self.uart.read(1)
                    CMD_TEMP.append(cmd_type[0])
                    if(CMD_TEMP[2]==0x01):
                        res = self.uart.read(9)
                        for i in range(9):
                            CMD_TEMP.append(res[i])                  
                        checksum = CheckCode(CMD_TEMP[:11])
                        if(res and checksum == CMD_TEMP[11]):
                            if CMD_TEMP[3]==0x01 and CMD_TEMP[4]==0x00:
                                num += 1
                                AI_Uart_CMD(self.uart, 0x01, 0x01, 0x01)
                            elif CMD_TEMP[3]==0x01 and CMD_TEMP[4]==0x01:
                                print('==AI摄像头通信成功==')
                                self.lock = False
                                _cmd = self.uart.read()
                                del _cmd
                                gc.collect()
                                time.sleep_ms(50)
                                break
                    elif(CMD_TEMP[2]==0x02):
                        pass
                else:
                    # _cmd = self.uart.read()
                    # del _cmd
                    gc.collect()
    
    # def sensor_config(self,_choice,_framesize,_pixformat,_w,_h,_vflip,_hmirror,_brightness,_contrast,_saturation,_gain,_whitebal,_freq,_dual_buff):
    #     self.lock=True
    #     _str = str(_framesize)+'|'+ str(_pixformat)+'|'+ str(_vflip)+'|'+ str(_hmirror)+'|'+ str(_brightness)+'|'+ str(_contrast)+'|'+ str(_saturation)+'|'+ str(_gain)+'|'+ str(_whitebal)+'|'+ str(_w)+'|'+ str(_h)+'|'+ str(_freq)+'|'+ str(_dual_buff)
    #     AI_Uart_CMD_String(uart=self.uart, cmd=AI['sensor'][0], cmd_type=AI['sensor'][1], cmd_data=[_choice,0,0], str_buf=_str)
    #     self.lock=False

    # def mnist_init(self, _choice):
    #     self.mnist = MNIST(self.uart, choice=_choice)
    #     self.mode = MNIST_MODE

    # def yolo_detect_init(self, _choice):
    #     self.yolo_detect = YOLO(self.uart, choice=_choice)
    #     self.mode = OBJECT_RECOGNIZATION_MODE

    # def face_detect_init(self, _choice):
    #     self.face_detect = FACE_DETECT(self.uart, choice=_choice)
    #     self.mode = FACE_DETECTION_MODE

    def face_recognize_init(self, _face_num, _accuracy, _choice):
        self.fcr = Face_recogization(self.uart, face_num=_face_num, accuracy=_accuracy, choice=_choice)
        self.mode = FACE_RECOGNIZATION_MODE

    def thread_listen(self):
        self._task = TASK(func=self.uart_thread,sec=0.03)
        self._task.start()

    def uart_thread(self):           
        if(self.lock==False):
            CMD = uart_handle(self.uart)
            if(CMD==None or CMD==[]):
                return

            if(self.mode==DEFAULT_MODE):
                pass
            elif(self.mode==FACE_DETECTION_MODE and self.face_detect!=None):
                if(len(CMD)>0):
                    if(CMD[3]==FACE_DETECTION_MODE and CMD[4]==0x02):
                        if(CMD[5]==0xff):
                            self.face_detect.face_num,self.face_detect.max_score = None,0
                        else:
                            self.face_detect.face_num,self.face_detect.max_score = CMD[5],round(int(CMD[6])/100,2)
                    elif(CMD[2]==0x02):
                        pass
                else:
                    pass
            elif(self.mode==FACE_RECOGNIZATION_MODE and self.fcr!=None):#5
                if(len(CMD)>0):
                    if(CMD[3]==FACE_RECOGNIZATION_MODE and CMD[4]==0x03):
                        if(CMD[5]==0xff):
                            self.fcr.id,self.fcr.max_score = None,0
                        else:
                            self.fcr.id,self.fcr.max_score = CMD[5],round(int(CMD[6])/100,2)
                    elif(CMD[2]==0x02):
                        pass
                else:
                    pass
        
          