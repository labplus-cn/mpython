import time
from k230_ai.public import *
import gc
import json

class YOLO80(object):
    '''物体识别'''
    def __init__(self, uart):
        self.uart = uart
        self.category_list = YOLO80_ZH
        self.id = None
        self.max_score = 0
        self.objnum = 0
        self.category_name = None
        self.lock = False
        AI_Uart_CMD(self.uart, AI['OBJECT_RECOGNIZATION_MODE'][0], AI['OBJECT_RECOGNIZATION_MODE'][1])
        time.sleep(0.5)
    
    def recognize(self):
        time.sleep_ms(20)
        if(not self.lock):
            AI_Uart_CMD(self.uart, cmd=AI['OBJECT_RECOGNIZATION_MODE'][0], cmd_type=AI['OBJECT_RECOGNIZATION_MODE'][1])

class FACE_DETECT(object):
    """人脸检测"""
    def __init__(self, uart):
        self.uart = uart
        self.face_num = None
        self.coord_list = []
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=AI['FACE_DETECTION_MODE'][0], cmd_type=AI['FACE_DETECTION_MODE'][1])
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(50)
        if(not self.lock):
            AI_Uart_CMD(uart=self.uart, cmd=AI['FACE_DETECTION_MODE'][0], cmd_type=AI['FACE_DETECTION_MODE'][1])


class ClassifyMODEL(object):
    """ 使用自定义 分类模型 """
    def __init__(self, uart, param):
        self.uart = uart
        self.CommandList = AI['CLASSIFY_MODEL_MODE']
        self.id = None
        self.score = 0
        self.num = 0
        self.result = {"id": None, "score": 0}
        self.lock = False
        parameter = str(param)
        AI_Uart_CMD_String(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1], str_buf=parameter)
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(20)
        if(not self.lock):
            AI_Uart_CMD(self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])


class DetectMODEL(object):
    """ 使用自定义模型 DETECT"""
    def __init__(self, uart, param):
        self.uart = uart
        self.CommandList = AI['DETECT_MODEL_MODE']
        self.id = None
        self.score = 0
        self.num = 0
        self.result = {"id": None, "score": 0, "num": 0}
        self.lock = False
        parameter = str(param)
        AI_Uart_CMD_String(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1], str_buf=parameter)
        time.sleep(1)

    def recognize(self):
        time.sleep_ms(20)
        if(not self.lock):
            AI_Uart_CMD(self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
    
    
class Color_Statistics(object):
    '''图像处理 线性回归'''
    def __init__(self, uart):
        self.uart = uart
        self.img_grayscale_threshold = (200,255)
        self.line_grayscale_threshold = (230,255)
        self.row_data1 = [None,None,None,None,None]
        self.row_data2 = [None,None,None,None,None]
        self.row_data3 = [None,None,None,None,None]
        self.data = [self.row_data1,self.row_data2,self.row_data3]
        self.line_get_regression_data = [None,None,None,None,None,None,None,None]
        self._task = None
        self.lock = False
        self.send_num = 0
        AI_Uart_CMD(uart=self.uart, cmd=AI['color_statistics'][0], cmd_type=AI['color_statistics'][1])
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(30)
        if(not self.lock):
            try:
                AI_Uart_CMD(self.uart, cmd=AI['color_statistics'][0], cmd_type=AI['color_statistics'][2])
            except Exception as e:
                print('err:'+str(e))
                pass

    def set_img_grayscale_threshold(self, img_grayscale_threshold):
        self.img_grayscale_threshold = img_grayscale_threshold
        # print(img_grayscale_threshold)
        AI_Uart_CMD(self.uart, AI['color_statistics'][0], AI['color_statistics'][3], cmd_data=[img_grayscale_threshold[0],img_grayscale_threshold[1],0])
        time.sleep_ms(50)

    def set_line_grayscale_threshold(self, line_grayscale_threshold):
        self.line_grayscale_threshold = line_grayscale_threshold
        # print(line_grayscale_threshold)
        AI_Uart_CMD(self.uart, AI['color_statistics'][0], AI['color_statistics'][4], cmd_data=[line_grayscale_threshold[0],line_grayscale_threshold[1],0])
        time.sleep_ms(50)


class LPR(object):
    """车牌识别 """
    def __init__(self, uart):
        self.uart = uart
        self.CommandList = AI['LICENSE_PLATE_RECOGNITION']
        self.lpr_str = None
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            try:
                AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
            except Exception as e:
                print('err:' + str(e))


class HandDetect(object):
    """手掌检测"""
    def __init__(self, uart):
        self.uart = uart
        self.hand_num = 0
        self.coord_list = []
        self.flag = False
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=AI['HAND_DETECTION'][0], cmd_type=AI['HAND_DETECTION'][1])
        time.sleep(1)

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            AI_Uart_CMD(uart=self.uart, cmd=AI['HAND_DETECTION'][0], cmd_type=AI['HAND_DETECTION'][1])


class HandKeypointClass(object):
    """ 手势识别 """
    def __init__(self, uart):
        self.uart = uart
        self.CommandList = AI['HAND_KEYPOINT_CLASS']
        self.gesture_id = None
        self.gesture_str = None
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
        time.sleep(1)

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            try:
                AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
            except Exception as e:
                print('err:' + str(e))


class DG(object):
    """ 动态手势 """
    def __init__(self, uart):
        self.uart = uart
        self.CommandList = AI['DYNAMIC_GESTURE']
        self.gesture_id = None
        self.gesture_str = None
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
        time.sleep(1)

    def recognize(self):
        time.sleep_ms(20)
        if(not self.lock):
            AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
        

class PersonDetect(object):
    """人体检测"""
    def __init__(self, uart):
        self.uart = uart
        self.flag = False
        self.person_num = 0
        self.coord_list = []
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=AI['PERSON_DETECTION'][0], cmd_type=AI['PERSON_DETECTION'][1])
        time.sleep(1)

    def recognize(self):
        time.sleep_ms(20)
        if(not self.lock):
            AI_Uart_CMD(uart=self.uart, cmd=AI['PERSON_DETECTION'][0], cmd_type=AI['PERSON_DETECTION'][1])


class PersonKeypointDetct(object):
    """ 人体骨架关键点识别 """
    def __init__(self, uart):
        self.uart = uart
        self.CommandList = AI['PERSON_KEYPOINT_DETECT']
        self.keypoints = []
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
        time.sleep(1)

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            try:
                AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
            except Exception as e:
                print('err:' + str(e))


class PersonKeypointDetctPlus(object):
    """ 人体姿势识别 PERSON_KEYPOINT_DETECT_PLUS"""
    def __init__(self, uart):
        self.uart = uart
        self.CommandList = AI['PERSON_KEYPOINT_DETECT_PLUS']
        self.id = None
        self.keypoints = []
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
        time.sleep(1)

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            try:
                AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
            except Exception as e:
                print('err:' + str(e))
                
            
class FaceExpressionDetct(object):
    """ 表情识别 """
    def __init__(self, uart):
        self.uart = uart
        self.CommandList = AI['FACE_LANDMARK_EXPRESSION']
        self.expression = 0
        self.expression_str = FACE_LANDMARK_EXPRESSION_ZH[0]
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
        time.sleep(1)

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            try:
                AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
            except Exception as e:
                print('err:' + str(e))
                
class FaceLivingBodyDetct(object):
    """ 眨眼张嘴检测 """
    def __init__(self, uart):
        self.uart = uart
        self.CommandList = AI['FACE_LANDMARK_LIVING_BODY']
        self.mouth_blink_counter = [-1,-1]
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
        time.sleep(1)

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            try:
                AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
            except Exception as e:
                print('err:' + str(e))


class QRCodeRecognization(object):
    """ 二维码识别类"""
    def __init__(self, uart=None):
        self.uart = uart
        self.CommandList = AI['QRCODE_MODE']
        self.info = None
        self.lock = False
        AI_Uart_CMD(self.uart, self.CommandList[0], self.CommandList[1])
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            AI_Uart_CMD(self.uart, self.CommandList[0], self.CommandList[1])


class BarCodeRecognization(object):
    """ 条形码识别类"""
    def __init__(self, uart=None):
        self.uart = uart
        self.CommandList = AI['BARCODE_MODE']
        self.type = None
        self.info = None
        self.lock = False
        AI_Uart_CMD(self.uart, self.CommandList[0], self.CommandList[1])
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            AI_Uart_CMD(self.uart, self.CommandList[0], self.CommandList[1])


class FallDetection(object):
    """ 跌倒检测 """
    def __init__(self, uart):
        self.uart = uart
        self.CommandList = AI['FALL_DETECTION']
        self.id = None
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            try:
                AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
            except Exception as e:
                print('err:' + str(e))


class FaceRecogization(object):
    """ 人脸识别类"""
    def __init__(self, uart):
        self.uart = uart
        self.face_num = -1
        self.id = None
        self.score = None
        self.CommandList = AI['FACE_RECOGNITION_MODE']
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(20)
        if(not self.lock):
            AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])


class ColorCount(object):
    """ 颜色计数 """
    def __init__(self, uart, cur_mode=0):
        self.uart = uart
        self.color_count = None
        self.CommandList = AI['COLOR_OBJECT_COUNT_MODE']
        self.lock = False
        self.cur_mode = cur_mode 
        AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1], cmd_data=[cur_mode])
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1],cmd_data=[self.cur_mode])


class LABColorCount():
    """ lab颜色 """
    def __init__(self, uart, color):
        self.uart = uart
        self.CommandList = AI['LAB_COLOR_OBJECT_COUNT_MODE']
        self.flag = False
        self.color_count = None
        self.lock = False
        parameter = str(color)
        AI_Uart_CMD_String(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1], str_buf=parameter)
        time.sleep(1)

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
     

class LINEAR_REGRESSION():
    """ 快速线性回归 """
    def __init__(self, uart, threshold=(0, 100)):
        self.lock = False
        self.uart = uart
        self.CommandList = AI['LINEAR_REGRESSION_MODE']
        self.line = {"x1":None, "y1":None, "x2":None, "y2":None, "length":None, "magnitude":None, "theta":None, "rho":None}
        self.parameter = str(threshold)
        AI_Uart_CMD_String(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1], str_buf=self.parameter)
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(5)
        if(not self.lock):
            AI_Uart_CMD_String(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1], str_buf=self.parameter)


class LINEAR_V3_REGRESSION():
    """ 快速线性回归v3  T字路口 斑马线 识别"""
    def __init__(self, uart, line_color="black", detect_intersections=True, detect_zebra=True):
        self.lock = False
        self.uart = uart
        self.CommandList = AI['LINEAR_REGRESSION_V3_MODE']
        self.data = {"cx": None, "cy": None, "angle": None, "is_int": False, "is_zebra": False}
        self.parameter = json.dumps({"color": line_color,'int':detect_intersections, 'zebra':detect_zebra})
        self.sleep_time_ms = 50 
        AI_Uart_CMD_String(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1], str_buf=self.parameter)
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(self.sleep_time_ms)
        if(not self.lock):
            AI_Uart_CMD_String(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1], str_buf=self.parameter)


class AMR(object):
    """ 自动驾驶 Autonomous Mobile Robot """
    def __init__(self, uart):
        self.uart = uart
        self.pid = PIDController(kp=1.55, ki=0.0, kd=0.2, min_out=-25, max_out=25) 
        self.res = {
                        "F": "none",
                        "AGL": 0,
                        "SW": [],
                        "GL": [],
                        "RL": [],
                        "UT": []
                    }
        self.CommandList = AI['APS_MODE']
        self.lock = False
        AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
        time.sleep(0.5)

    def pid_controller(self, kp=1.55, ki=0, kd=0.2, min_out=-25, max_out=25):
        self.pid = PIDController(kp=kp, ki=ki, kd=kd, min_out=min_out, max_out=max_out) 

    def recognize(self):
        time.sleep_ms(10)
        if(not self.lock):
            AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])


class APRILTAG_DETECT(object):
    """ AprilTag 检测 """
    def __init__(self, uart):
        self.lock = False
        self.uart = uart
        self.CommandList = AI['APRILTAG_DETECT_MODE']
        self.data = {'family': None, 'id': None, 'rect': [], 'rotation': None, 'cx': None, 'cy': None}
        self.tag_family = None
        self.tag_id = None
        self.sleep_time_ms = 50 
        AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(self.sleep_time_ms)
        if(not self.lock):
            AI_Uart_CMD(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1])