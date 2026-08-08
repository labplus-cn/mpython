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

DEBUG = False  # 是否开启调试模式
MAX_BUF_SIZE = 1024  # 缓冲区最大字节数

def CheckCode(tmp):
    sum = 0
    for i in range(len(tmp)):
        sum += tmp[i]
    return sum & 0xff

def uart_handle(uart):
    """
    处理 UART 数据，解析命令并返回完整的命令包。
    增加粘包处理逻辑。
    """
    rx_buf = bytearray()  # 全局接收缓冲区

    # 初始化缓冲区
    if not hasattr(uart_handle, "rx_buf"):
        rx_buf = bytearray()

    # 读取 UART 数据
    if uart.any():
        data = uart.read()
        if data:
            rx_buf.extend(data)
            # if DEBUG:
            #     print("[UART RX] " + ' '.join('{:02X}'.format(b) for b in data))

            # 缓冲区保护，防止溢出
            if len(rx_buf) > MAX_BUF_SIZE:
                if DEBUG:
                    print("[UART] 缓冲区超限，清空缓冲区")
                rx_buf = bytearray()

    # 解析命令包
    while True:
        # 至少要有包头(2字节) + 命令类型(1字节)
        if len(rx_buf) < 3:
            break

        # 检查包头
        if not (rx_buf[0] == 0xBB and rx_buf[1] == 0xAA):
            if DEBUG:
                print("[UART] 丢弃无效字节: 0x{:02X}".format(rx_buf[0]))
            rx_buf = rx_buf[1:]
            continue

        # 获取命令类型
        cmd_type = rx_buf[2]

        # 处理固定长度命令 (cmd_type == 0x01)
        if cmd_type == 0x01:
            total_len = 12  # 固定长度
            if len(rx_buf) < total_len:
                if DEBUG:
                    print("[UART] 等待 0x01 包数据到齐")
                break
            pkt = rx_buf[:total_len]
            checksum = CheckCode(pkt[:11])  # 校验包头+命令+数据(共11字节)
            if checksum == pkt[11]:
                if DEBUG:
                    print("[UART] 校验成功: " + ' '.join('{:02X}'.format(b) for b in pkt))
                rx_buf = rx_buf[total_len:]  # 移除已处理的数据
                return pkt
            else:
                if DEBUG:
                    print("[UART] 校验失败 (计算={:02X}, 接收={:02X})".format(checksum, pkt[11]))
            rx_buf = rx_buf[total_len:]  # 移除已处理的数据

        # 处理可变长度命令 (cmd_type == 0x02)
        elif cmd_type == 0x02:
            if len(rx_buf) < 21:  # 至少要有包头+命令+固定头+2字节长度
                if DEBUG:
                    print("[UART] 等待 0x02 头部数据到齐")
                break
            # 获取字符串长度（2字节，高字节在前，低字节在后）
            str_len = rx_buf[20]
            total_len = 21 + str_len + 1  # 包头+命令+固定头+字符串长度+校验
            if len(rx_buf) < total_len:
                if DEBUG:
                    print("[UART] 等待 0x02 字符串数据到齐 (len={})".format(str_len))
                break
            pkt = rx_buf[:total_len]
            if pkt[-1] != 0xAB:  # 校验包尾
                if DEBUG:
                    print("[UART] 包尾校验失败 (期望=0xAB, 接收={:02X})".format(pkt[-1]))
                rx_buf = rx_buf[1:]  # 丢弃第一个字节
                continue
            # checksum = CheckCode(pkt[:-1])  # 校验数据
            # if checksum == pkt[-1]:
            #     if DEBUG:
            #         print("[UART] 校验成功: " + pkt.hex(' ').upper())
            #     rx_buf = rx_buf[total_len:]  # 移除已处理的数据
            #     return pkt
            # else:
            #     if DEBUG:
            #         print("[UART] 校验失败 (计算={:02X}, 接收={:02X})".format(checksum, pkt[-1]))
            # rx_buf = rx_buf[total_len:]  # 移除已处理的数据
            else:
                if DEBUG:
                    print("[UART] 解析到 0x02 包")
                    # print("complete packet:", pkt)
                rx_buf = rx_buf[total_len:]
        
                return pkt  # 返回完整包

        # 未知命令类型
        else:
            if DEBUG:
                print("[UART] 未知命令类型 0x{:02X}，丢弃第一个字节".format(cmd_type))
            rx_buf = rx_buf[1:]

            return None  # 无有效包返回

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