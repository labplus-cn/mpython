import gc
import _thread
import time

DISPLAY_WIDTH = 544
DISPLAY_HEIGHT = 368

DEFAULT_MODE = 0 # 默认UI
SENSOR_MODE = -1 # 摄像头

FACE_DETECTION_MODE = 1
OBJECT_RECOGNIZATION_MODE = 2 
HAND_DETECTION = 3
HAND_KEYPOINT_CLASS = 4
QRCODE_MODE = 5
PERSON_DETECTION = 6
FALL_DETECTION = 7 
LICENSE_PLATE_RECOGNITION = 8
CANNY_FIND_EDGES = 9
PERSON_KEYPOINT_DETECT = 10 # 人体关键点数据

PERSON_KEYPOINT_DETECT_PLUS = 11 
COLOR_STATISTICS_MODE = 13 # 颜色的统计信息
COLOR_EXTRACTO_MODE = 14 # LAB颜色提取器
APRILTAG_DETECT_MODE = 15 # AprilTag 检测

COLOE_MODE = 16
SPEECH_RECOGNIZATION_MODE = 17
SELF_LEARNING_CLASSIFIER_MODE = 18 # 自学习
GUIDEPOST_MODE = 19 #清华教材交通标志识别
KPU_MODEL_MODE = 20 #自定义模型 

HAND_RECOGNIZATION_MODE = 21
BARCODE_MODE = 23

DYNAMIC_GESTURE = 25 #动态手势
FACE_LANDMARK = 26  # 人脸关键点
FACE_LANDMARK_LIVING_BODY = 27 #活体检测
FACE_LANDMARK_EXPRESSION = 28 #表情识别

COLOR_OBJECT_COUNT_MODE = 29 #颜色物体计数
LAB_COLOR_OBJECT_COUNT_MODE = 22 #颜色物体计数

FACE_REG_MODE = 30 # 人脸注册
FACE_RECOGNITION_MODE = 31 #人脸识别
CLASSIFY_MODEL_MODE = 32 # 分类模型
DETECT_MODEL_MODE = 33  # 检测模型
HAND_KEYPOINT = 34 # 手部关键点
FACE_REG_PLUS_MODE = 35 # 人脸拍照+注册 
APS_MODE = 36  # 道路自动驾驶系统

LINEAR_REGRESSION_MODE = 40 #快速线性回归
LINEAR_REGRESSION_V3_MODE = 41 #快速线性回归 v3

FACTORY_MODE = 99 

# OBJ_TYPE = ['飞机','自行车','鸟','船','瓶子','公交车','汽车','猫','椅子','奶牛','餐桌','狗','屋子','摩托','人','盆栽','羊','沙发','火车','电视']

YOLO80_ZH = ["人","自行车","汽车","摩托车","飞机","公共汽车","火车","卡车","船","交通灯","消防栓","停车标志","泊车计时器","长椅","鸟","猫","狗","马","绵羊","奶牛","大象","熊","斑马","长颈鹿","背包","雨伞","手提包","领带","手提箱","飞盘","滑雪板","运动球","风筝","棒球","蝙蝠","棒球手套","滑板","冲浪板","网球拍","瓶子","酒杯","杯子","叉子","刀","勺子","碗","香蕉","苹果","三明治","橙子","西兰花","胡萝卜","热狗","披萨","甜甜圈","蛋糕","椅子","沙发","盆栽","床","餐桌","厕所","电视","笔记本电脑","鼠标","遥控器","键盘","手机","微波炉","烤箱","烤面包机", "水槽","冰箱","书籍","时钟","花瓶","剪刀","泰迪熊","吹风机","牙刷"] 
HAND_KEYPOINT_CLASS_GESTURE = ['fist','five','gun','love','one','six','three','thumbUp','yeah']
FACE_LANDMARK_EXPRESSION_ZH = ['正常','开心','伤心','惊讶','生气']
DYNAMIC_GESTURE_STR = ['上','下','左','右'] 

MODE=['默认','数字识别','物体识别','人脸检测','人脸识别','自学习分类','颜色识别','二维码识别','语音识别','交通标志识别','KPU自定义模型','寻找色块识别','图像处理','LAB颜色提取器','AprilTag']

AI ={
    'reset':[0xff, 0x01, 0x02],
    'sw_mode':[],
    'config':[0x99,0x01,0x02],
    'lcd':[0x10,0x01,0x02],
    'image':[0x64,0x01],
    'sensor':[0x64,0x01],
    'DEFAULT_MODE':[DEFAULT_MODE,0x01],
    'light':[],
    'button':[],
    'button_A':[],
    'button_B':[],
    'FACE_DETECTION_MODE':[FACE_DETECTION_MODE,0x01],
    'OBJECT_RECOGNIZATION_MODE':[OBJECT_RECOGNIZATION_MODE,0x01],
    'HAND_DETECTION':[HAND_DETECTION,0x01],
    'HAND_RECOGNIZATION_MODE':[HAND_RECOGNIZATION_MODE,0x01],
    'HAND_KEYPOINT_CLASS':[HAND_KEYPOINT_CLASS,0x01],
    'LICENSE_PLATE_RECOGNITION':[LICENSE_PLATE_RECOGNITION,0x01],
    'PERSON_DETECTION':[PERSON_DETECTION,0x01],
    'PERSON_KEYPOINT_DETECT':[PERSON_KEYPOINT_DETECT,0x01],
    'PERSON_KEYPOINT_DETECT_PLUS':[PERSON_KEYPOINT_DETECT_PLUS,0x01],
    'APRILTAG_DETECT_MODE':[APRILTAG_DETECT_MODE,0x01],
    'FACE_LANDMARK':[FACE_LANDMARK,0x01],
    'FACE_LANDMARK_LIVING_BODY':[FACE_LANDMARK_LIVING_BODY,0x01],
    'FACE_LANDMARK_EXPRESSION':[FACE_LANDMARK_EXPRESSION,0x01],
    'QRCODE_MODE':[QRCODE_MODE,0x01],
    'BARCODE_MODE':[BARCODE_MODE,0x01],
    'FALL_DETECTION':[FALL_DETECTION,0x01],
    'FACE_RECOGNITION_MODE':[FACE_RECOGNITION_MODE,0x01],
    'LAB_COLOR_OBJECT_COUNT_MODE':[LAB_COLOR_OBJECT_COUNT_MODE,0x01],
    'COLOR_OBJECT_COUNT_MODE':[COLOR_OBJECT_COUNT_MODE,0x01],
    'DYNAMIC_GESTURE':[DYNAMIC_GESTURE,0x01],
    'CLASSIFY_MODEL_MODE':[CLASSIFY_MODEL_MODE,0x01],
    'DETECT_MODEL_MODE':[DETECT_MODEL_MODE,0x01],
    'FACE_REG_PLUS_MODE':[FACE_REG_PLUS_MODE,0x01],
    'APS_MODE':[APS_MODE,0x01],
    'LINEAR_REGRESSION_MODE':[LINEAR_REGRESSION_MODE,0x01],
    'LINEAR_REGRESSION_V3_MODE':[LINEAR_REGRESSION_V3_MODE,0x01],
    'factory':[99,0x01,0x02,0x03,0x04,0x05]
}


def CheckCode(tmp):
    sum = 0
    for i in range(len(tmp)):
        sum += tmp[i]
    return sum & 0xff


DEBUG = False  # 增加全局debug控制变量
MAX_BUF_SIZE = 4096  # 缓冲区最大字节数


def uart_handle(uart):
    rx_buf = bytearray()

    # 读取 UART 数据
    if uart.any():
        data = uart.read()
        if data:
            if DEBUG:
                print("[UART RX] " + data.hex(' ').upper())
            rx_buf.extend(data)

            # 缓冲区保护
            if len(rx_buf) > MAX_BUF_SIZE:
                if DEBUG:
                    print("[UART] 缓冲区超限({} > {})，清空".format(len(rx_buf), MAX_BUF_SIZE))
                rx_buf = bytearray()

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

        cmd_type = rx_buf[2]

        # 命令 0x01: 固定长度 2(包头) + 1(命令) + 2 +6(数据) + 1(校验) = 12字节
        if cmd_type == 0x01:
            total_len = 12
            if len(rx_buf) < total_len:
                if DEBUG:
                    print("[UART] 等待 0x01 包数据到齐")
                break
            pkt = rx_buf[:total_len]
            checksum = CheckCode(pkt[:11])  # 校验包头+命令+数据(共11字节)
            if DEBUG:
                print("[UART] 解析到 0x01 包: " + pkt.hex(' ').upper())
            if checksum == pkt[11]:
                if DEBUG:
                    print("[UART] 校验成功")
                return pkt  # 返回完整包
            else:
                if DEBUG:
                    print("[UART] 校验失败 (计算={:02X}, 接收={:02X})".format(checksum, pkt[11]))
            rx_buf = rx_buf[total_len:]

        # 命令 0x02: 2(包头) + 3(命令) + 15(固定头) +2(字符串长度) + N(字符串) + 1(校验)
        elif cmd_type == 0x02:
            if len(rx_buf) < 22:  # 至少要有包头+命令+固定头+2字节长度
                if DEBUG:
                    print("[UART] 等待 0x02 头部数据到齐")
                break
            # 两字节长度，高字节在前，低字节在后
            str_len = (rx_buf[20] << 8) | rx_buf[21]
            total_len = 22 + str_len + 1
            if len(rx_buf) < total_len:
                if DEBUG:
                    print("[UART] 等待 0x02 字符串数据到齐 (len={})".format(str_len))
                break
            pkt = rx_buf[:total_len]
           
            if pkt[-1] != 0xAB:
                if DEBUG:
                    print("[UART] 0x02 包尾校验失败 (期望=AB, 接收={:02X})，丢弃第一个字节".format(pkt[-1]))
                rx_buf = rx_buf[1:]
                continue
            if DEBUG:
                print("[UART] 解析到 0x02 包")
                print(pkt)
            rx_buf = rx_buf[total_len:]
        
            return pkt  # 返回完整包

        else:
            if DEBUG:
                print("[UART] 未知命令 0x{:02X}，丢弃第一个字节".format(cmd_type))
            rx_buf = rx_buf[1:]

            return None  # 无有效包返回

def AI_Uart_CMD(uart, cmd=0, cmd_type=0, cmd_data=[0, 0, 0, 0, 0, 0, 0, 0]):
    gc.collect()
    data_type = 0x01
    check_sum = 0
    CMD = [0xAA, 0xBB, data_type, cmd, cmd_type]
    CMD.extend(cmd_data)
    for i in range(8-len(cmd_data)):
        CMD.append(0)
    for i in range(len(CMD)):
        check_sum = check_sum+CMD[i]

    CMD.append(check_sum & 0xFF)
    # print(CMD)
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
    
    # for i in range(len(str_temp)):
    #     check_sum = check_sum + str_temp[i]  
    CMD = bytes(CMD) + bytes([str_len]) + str_temp + bytes([0xAB])  # 0xAB为结束符
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
        self._thread.stack_size(4096)
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
                time.sleep(self.sec)
                self.lock.release()

    def start(self):
        """运行线程"""
        self.lock.release()

    def stop(self):
        """暂停线程"""
        self.enable = False
        self.stop_lock.acquire()
        self.enable = True

class PIDController:
    def __init__(self, kp, ki, kd, min_out=-25, max_out=25):
        """
        :param kp: 比例系数 (响应速度)
        :param ki: 积分系数 (消除静态误差)
        :param kd: 微分系数 (减少震荡)
        :param min_out: 输出下限
        :param max_out: 输出上限
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.min_out = min_out
        self.max_out = max_out
        
        self.prev_error = 0
        self.integral = 0
        self.last_time = time.time()

    def compute(self, target, current):
        """
        计算PID输出
        :param target: 目标角度 (通常是 0)
        :param current: 当前角度
        :return: 修正量 (turn_speed)
        """
        now = time.time()
        dt = now - self.last_time
        
        # 防止除以0（如果是第一次运行或运行过快）
        if dt <= 0: dt = 0.001 

        error = target - current
        
        # P项
        p_out = self.kp * error
        
        # I项
        self.integral += error * dt
        i_out = self.ki * self.integral
        
        # D项 (变化率)
        derivative = (error - self.prev_error) / dt
        d_out = self.kd * derivative

        # 总输出
        output = p_out + i_out + d_out
        
        # 保存状态
        self.prev_error = error
        self.last_time = now
        
        # 限幅 (防止输出超出电机允许范围)
        return max(self.min_out, min(output, self.max_out))