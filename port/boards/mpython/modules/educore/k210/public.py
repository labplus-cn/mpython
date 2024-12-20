import gc
import _thread
from time import sleep,sleep_ms

AI ={
    'reset':[0xff, 0x01, 0x02],
    'sw_mode':[],
    'config':[0x03,0x01,0x02],
    'lcd':[0x10,0x01,0x02],
    'image':[0x64,0x01],
    'sensor':[0x64,0x01],
    'kpu':[],
    'light':[],
    'button':[],
    'button_A':[],
    'button_B':[],
    'mnist':[0x02,0x01,0x02],
    '20yolo':[0x03,0x01,0x02],
    'face_detection':[0x04,0x01,0x02],
    'face_recognize':[0x05,0x01,0x02,0x03,0x04,0x05],
    'self_learn':[0x06,0x01,0x02,0x03,0x04,0x05],
    'color':[0x07,0x01,0x02,0x03],
    'qrcode':[0x08,0x01,0x02,0x03],
    'asr':[0x09,0x01,0x02,0x03],
    'guidepost':[0x0a,0x01,0x02],
    'kpu_model':[0x0b,0x01,0x02,0x03],
    'track':[0x0c,0x01,0x02,0x03,0x04],
    'color_statistics':[0x0d,0x01,0x02,0x03,0x04],
    'color_extracto':[0x0e,0x01,0x02],
    'apriltag':[0x0f,0x01,0x02,0x03],
    'kpu_model_yolo':[0x10,0x01,0x02,0x03],
    'video': [0x14,0x01,0x02],
    'factory':[99,0x01,0x02,0x03,0x04,0x05]
}

DEFAULT_MODE = 1 #默认
MNIST_MODE = 2 #数字识别
OBJECT_RECOGNIZATION_MODE = 3 #20类物体识别
FACE_DETECTION_MODE = 4 #人脸检测
FACE_RECOGNIZATION_MODE = 5 #人脸识别
SELF_LEARNING_CLASSIFIER_MODE = 6 #自学习分类
COLOE_MODE = 7 #颜色识别
QRCODE_MODE = 8 #二维码识别
SPEECH_RECOGNIZATION_MODE = 9 #语音识别
GUIDEPOST_MODE = 10 #交通标志识别
KPU_MODEL_MODE = 11 #自定义模型
TRACK_MODE = 12 #寻找色块识别
COLOR_STATISTICS_MODE = 13 #图像处理
COLOR_EXTRACTO_MODE = 14 # LAB颜色提取器
APRILTAG_MODE = 15 # AprilTag模式
KPU_YOLO_MODEL_MODE = 16 # 自定义yolo模型
VIDEO_MODE = 20 # 采集图像

FACTORY_MODE = 99 


MODE=['保留','默认','数字识别','物体识别','人脸检测','人脸识别','自学习分类','颜色识别','二维码识别','语音识别','交通标志识别','KPU自定义模型','寻找色块识别','图像处理','LAB颜色提取器','AprilTag']

def CheckCode(tmp):
    sum = 0
    for i in range(len(tmp)):
        sum += tmp[i]
    return sum & 0xff

def uart_handle(uart):
    gc.collect()
    CMD = []
    HEAD = []
    # while True:
    if(uart.any()):
        head = uart.read(3)
    
        if b"\xbb" in head:
            for i in range(len(head)):
                HEAD.append(head[i])
        
            if(HEAD[0] == 0xBB):
                CMD.extend([HEAD[0],HEAD[1],HEAD[2]])
                if(CMD[2]==0x01):
                    res = uart.read(9)
                    
                    for i in range(9):
                        CMD.append(res[i])                  
                    checksum = CheckCode(CMD[:11])
                    if(res and checksum == CMD[11]):
                        return CMD
                    else:
                        print(CMD)
                elif(CMD[2]==0x02):
                    res = uart.read(18)
                    
                    str_len = res[17]
                    sleep_ms(1)
                    str_temp = uart.read(str_len)
                    checksum  = uart.read(1)
                    for i in range(18):
                        CMD.append(res[i])
        
                    CMD.append(str_temp)
                    CMD.append(checksum[0])
                
                    return CMD
            elif(HEAD[1] == 0xBB):
                CMD.extend([HEAD[1],HEAD[2]])
                CMD.append(uart.read(1))
                if(CMD[2]==0x01):
                    res = uart.read(9)
                    
                    for i in range(9):
                        CMD.append(res[i])                  
                    checksum = CheckCode(CMD[:11])
                    if(res and checksum == CMD[11]):
                        return CMD
                    else:
                        print(CMD)
                elif(CMD[2]==0x02):
                    res = uart.read(18)
                    str_len = res[17]
                    sleep_ms(1)
                    str_temp = uart.read(str_len)
                    checksum  = uart.read(1)

                    for i in range(18):
                        CMD.append(res[i])
                
                    CMD.append(str_temp)
                    CMD.append(checksum[0])

                    return CMD
            elif(HEAD[2] == 0xBB):
                CMD.append(HEAD[2])
                tmp = uart.read(2)
                for i in range(2):
                    CMD.append(tmp[i]) 
                if(CMD[2]==0x01):
                    res = uart.read(9)
                    
                    for i in range(9):
                        CMD.append(res[i])                  
                    checksum = CheckCode(CMD[:11])
                    if(res and checksum == CMD[11]):
                        return CMD
                    else:
                        print(CMD)
                elif(CMD[2]==0x02):
                    res = uart.read(18)
                    str_len = res[17]
                    sleep_ms(1)
                    str_temp = uart.read(str_len)
                    checksum  = uart.read(1)

                    for i in range(18):
                        CMD.append(res[i])
                    
                    CMD.append(str_temp)
                    CMD.append(checksum[0])
            
                    return CMD
        else:
            # print(head)
            # print('&===111===&')
            return []
    else:
        # print('&222')
        return []

def AI_Uart_CMD(uart, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0, 0, 0]):
    gc.collect()
    check_sum = 0
    CMD = [0xAA, 0xBB, data_type, cmd, cmd_type]
    CMD.extend(cmd_data)
    for i in range(8-len(cmd_data)):
        CMD.append(0)
    for i in range(len(CMD)):
        check_sum = check_sum+CMD[i]

    CMD.append(check_sum & 0xFF)
    uart.write(bytes(CMD))


def AI_Uart_CMD_String(uart=None, cmd=0xfe, cmd_type=0xfe, cmd_data=[0, 0, 0], str_len=0, str_buf=''):
    gc.collect()
    check_sum = 0
    CMD = [0xAA, 0xBB, 0x02, cmd, cmd_type]
    CMD.extend(cmd_data)
    for i in range(3-len(cmd_data)):
        CMD.append(0)
    for i in range(len(CMD)):
        check_sum = check_sum+CMD[i]
  
    str_temp = bytes(str_buf, 'utf-8')
    str_len = len(str_temp)
    
    for i in range(len(str_temp)):
        check_sum = check_sum + str_temp[i]  

    CMD = bytes(CMD) + bytes([str_len]) + str_temp + bytes([check_sum & 0xFF])
    uart.write(CMD)

def print_x16(date):
    for i in range(len(date)):
        print('{:2x}'.format(date[i]),end=' ')
    print('')

def hammingWeight(n):
    '''
    判断16bit中哪一位为1
    '''
    ans = 0
    for i in range(16):
        if n & 1 == 1:
          ans = i
        n >>= 1
    return ans

class TASK:
    """创建新线程并循环运行指定函数"""
    def __init__(self, func=lambda: None, sec=-1, *args, **kwargs):
        """
        * func 需要循环运行的函数
        * sec  每次循环的延迟，负数则只运行一次
        * args kwagrs 函数的参数
        * enable 使能运行
        """
        self._thread = _thread
        self.sec = sec
        self.func = func
        self.args, self.kwargs = args, kwargs
        self.enable = True
        self.lock = self._thread.allocate_lock()
        self.stop_lock = self._thread.allocate_lock()
        self.lock.acquire()
        self.stop_lock.acquire()
        self._thread.stack_size(8192)
        self.thread_id = self._thread.start_new_thread(self.__run, ())
        
    def __run(self):
        """
        请勿调用
        线程运行函数
        """
        while True:
            self.lock.acquire()
            try:
                self.func(*self.args, **self.kwargs)
            except Exception as e:
                print('Task_function_error:', e)
                pass
            if self.sec < 0 or not self.enable:
                self.stop_lock.release()
            else:
                sleep(self.sec)
                self.lock.release()

    def start(self):
        """运行线程"""
        self.lock.release()

    def stop(self):
        """暂停线程"""
        self.enable = False
        self.stop_lock.acquire()
        self.enable = True

    # def kill(self):
    #     pass