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
    'VISUAL_TRACKING_MODE':[0x0d,0x01,0x02,0x03,0x04],
    'color_extracto':[0x0e,0x01,0x02],
    'apriltag':[0x0f,0x01,0x02,0x03],
    'model_yolo':[0x10,0x01,0x02],#16
    'model_restnet18':[0x11,0x01,0x02],
}

DEFAULT_MODE = 1 #默认
MNIST_MODE = 2 #数字识别
OBJECT_RECOGNIZATION_MODE = 3 #20类物体识别
FACE_DETECTION_MODE = 4 #人脸检测
FACE_RECOGNIZATION_MODE = 5 #人脸识别
SELF_LEARNING_CLASSIFIER_MODE = 6 #自学习分类
COLOE_MODE = 7 #颜色识别
QRCODE_MODE = 8 #二维码识别
# SPEECH_RECOGNIZATION_MODE = 9 #语音识别
GUIDEPOST_MODE = 10 #交通标志识别
KPU_MODEL_MODE = 11 #自定义模型
TRACK_MODE = 12 #寻找色块识别
VISUAL_TRACKING_MODE = 13 # 寻找黑线
COLOR_EXTRACTO_MODE = 14 # LAB颜色提取器
APRILTAG_MODE = 15 # AprilTag模式
MODEL_YOLO_MODE = 16
MODEL_resnet18_MODE = 17

Factory_MODE = 0xFD

MODE=['保留','默认','数字识别','物体识别','人脸检测','人脸识别','自学习分类','颜色识别','二维码识别','语音识别','交通标志识别','自定义模型','寻找色块识别','图像寻线','LAB颜色提取器','AprilTag','自定义模型','resnet18模型']

def CheckCode(tmp):
    sum = 0
    for i in range(len(tmp)):
        sum += tmp[i]
    return sum & 0xff

def uart_handle(uart):
    num = 0
    while True:
        gc.collect()
        num +=1
        CMD = []
        if(uart.any()):
            head = uart.read(2)
            if(head==None or len(head)!=2):
                return []
            elif(head and head[0] == 0xBB):
                CMD.extend([0xBB])
                CMD.append(head[1])
                if(CMD[1]==0x01):
                    res = uart.read(9)
                    if(res==None or len(res)!=9):
                        # print('!')
                        return []
                    for i in range(9):
                        CMD.append(res[i])                  
                    checksum = CheckCode(CMD[:10])
                    if(res and checksum == CMD[10]):
                        # print('CMD===')
                        return CMD
                elif(CMD[1]==0x02):
                    res = uart.read(18)
                    if(res==None or len(res)!=18):
                        return []
                    str_len = res[17]
                    str_temp = uart.read(str_len)
                    checksum  = uart.read(1)
                    for i in range(18):
                        CMD.append(res[i])
                    for i in range(int(str_len)):
                        CMD.append(str_temp[i])
                    CMD.append(checksum[0])
                    # print(len(CMD))
                    # print('===CMD===')
                    return CMD
            else:
                gc.collect()
        elif num>6:
            # print('uart num timeout')
            return CMD

def AI_Uart_CMD(uart, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0, 0, 0]):
    gc.collect()
    check_sum = 0
    CMD = [0xAA, data_type, cmd, cmd_type]
    CMD.extend(cmd_data)
    for i in range(8-len(cmd_data)):
        CMD.append(0)
    for i in range(len(CMD)):
        check_sum = check_sum+CMD[i]
    # print_x16(CMD)
    # print(CMD)
    # print('===')
    uart.write(bytes(CMD))
    uart.write(bytes([check_sum & 0xFF]))


def AI_Uart_CMD_String(uart=None, cmd=0xfe, cmd_type=0xfe, cmd_data=[0, 0, 0], str_len=0, str_buf=''):
    gc.collect()
    check_sum = 0
    CMD = [0xAA, 0x02, cmd, cmd_type]
    CMD.extend(cmd_data)
    for i in range(3-len(cmd_data)):
        CMD.append(0)
    for i in range(len(CMD)):
        check_sum = check_sum+CMD[i]
    # print_x16(CMD)
    uart.write(bytes(CMD))
    str_temp = bytes(str_buf, 'utf-8')
    str_len = len(str_temp)
    uart.write(bytes([str_len]))
    uart.write(str_temp)
    for i in range(len(str_temp)):
        check_sum = check_sum + str_temp[i]
    uart.write(bytes([check_sum & 0xFF]))   

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