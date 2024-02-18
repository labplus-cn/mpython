import time
from .public import *
import gc

OBJ_TYPE = ['飞机','自行车','鸟','船','瓶子','公交车','汽车','猫','椅子','奶牛','餐桌','狗','屋子','摩托','人','盆栽','羊','沙发','火车','电视']
SEC = 0.05

class MNIST(object):
    '''
    手写数字
    '''
    def __init__(self, uart, choice=1):
        self.uart = uart
        self.choice = choice
        self.cmd = []
        self.id = None
        self.max_score = 0
        self._task = None
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['mnist'][0], AI['mnist'][1], cmd_data=[self.choice])
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(25)
        AI_Uart_CMD(self.uart, 0x01, AI['mnist'][0], AI['mnist'][2])


class YOLO(object):
    '''物体识别'''
    def __init__(self, uart, choice=1, flag=1):
        self.uart = uart
        self.choice = choice
        self.category_list = OBJ_TYPE
        self.id = None
        self.max_score = 0
        self.objnum = 0
        self._task = None
        self.lock = False
        if(flag):
            AI_Uart_CMD(self.uart, 0x01, AI['20yolo'][0], AI['20yolo'][1], cmd_data=[self.choice])
        time.sleep(0.5)
    
    def recognize(self):
        time.sleep_ms(25)
        if(not self.lock):
            AI_Uart_CMD(self.uart, data_type=1, cmd=AI['20yolo'][0], cmd_type=AI['20yolo'][2])

class FACE_DETECT(object):
    """人脸检测"""
    def __init__(self, uart, choice=1):
        self.uart = uart
        self.choice = choice
        self.face_num = None
        self.max_score = None
        self._task = None
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['face_detection'][0], AI['face_detection'][1], cmd_data=[self.choice])
        time.sleep(1)

    def recognize(self):
        time.sleep_ms(25)
        if(not self.lock):
            AI_Uart_CMD(self.uart, data_type=1, cmd=AI['face_detection'][0], cmd_type=AI['face_detection'][2])


class Face_recogization(object):
    """ maix人脸识别类"""
    def __init__(self, uart, face_num=1, accuracy=85, choice=1):
        self.uart = uart
        self.face_num = face_num
        self.accuracy = accuracy
        self.choice = choice
        self.id = None
        self.max_score = None
        self._task = None
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['face_recognize'][0], AI['face_recognize'][1], cmd_data=[self.face_num,self.accuracy,self.choice])

    def add_face(self):
        time.sleep_ms(20)
        AI_Uart_CMD(self.uart, 0x01, AI['face_recognize'][0], AI['face_recognize'][2])

    def recognize(self):
        time.sleep_ms(25)
        AI_Uart_CMD(self.uart, 0x01, AI['face_recognize'][0], AI['face_recognize'][3])


class Self_learning_classfier(object):
    """ maix自学习分类"""
    def __init__(self, uart=None, class_num=1, sample_num=5, choice=1):
        self.uart = uart
        self.class_num = class_num
        self.sample_num = sample_num
        self.choice = choice
        self.id = None
        self.max_score = None
        self._task = None
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['self_learn'][0], AI['self_learn'][1], cmd_data=[self.class_num,self.sample_num,self.choice])
        time.sleep(0.5)
        
    def add_class_img(self):
        AI_Uart_CMD(self.uart, 0x01, AI['self_learn'][0], AI['self_learn'][2])
        time.sleep_ms(25)

    def add_sample_img(self):
        pass

    def train(self):
        pass

    def predict(self):
        time.sleep_ms(30)
        AI_Uart_CMD(self.uart, data_type=1, cmd=AI['self_learn'][0], cmd_type=AI['self_learn'][3])

    def save_classifier(self, name):
        AI_Uart_CMD_String(uart=self.uart, cmd=AI['self_learn'][0], cmd_type=AI['self_learn'][4], str_buf=name)
        time.sleep_ms(50)

    def load_classifier(self, name):
        AI_Uart_CMD_String(uart=self.uart, cmd=AI['self_learn'][0], cmd_type=AI['self_learn'][5], str_buf=name)
        time.sleep_ms(50)



class Color_recognization(object):
    """ 颜色识别"""
    def __init__(self, uart=None, choice=1):
        self.uart = uart
        self.choice = choice
        self.id = None
        self._task = None
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['color'][0], AI['color'][1], cmd_data=[self.choice])
        time.sleep(1)

    def add_color(self, num):
        AI_Uart_CMD(self.uart, 0x01, AI['color'][0], AI['color'][2], cmd_data=[num])
        time.sleep_ms(50)
        
    def recognize(self):
        time.sleep_ms(20)
        AI_Uart_CMD(self.uart, 0x01, AI['color'][0], AI['color'][3])


class QRCode_recognization(object):
    """ 二维码识别类"""
    def __init__(self, uart=None, choice=1):
        self.uart = uart
        self.choice = choice
        self.id = None
        self.info = None
        self._task = None
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['qrcode'][0], AI['qrcode'][1], cmd_data=[self.choice])
        time.sleep(1)

    def add_qrcode(self, num):
        AI_Uart_CMD(self.uart, 0x01, AI['qrcode'][0], AI['qrcode'][2], cmd_data=[num])
        time.sleep_ms(50)

    def recognize(self):
        time.sleep_ms(30)
        if(not self.lock):
            AI_Uart_CMD(self.uart, data_type=0x01, cmd=AI['qrcode'][0], cmd_type=AI['qrcode'][3])

class Guidepost(object):
    '''路标识别'''
    def __init__(self, uart, choice=1):
        self.uart = uart
        self.choice = choice
        self.id = None
        self.max_score = 0
        self.labels = ['stop','none','left','right']
        self._task = None
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['guidepost'][0], AI['guidepost'][1], cmd_data=[self.choice])
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(30)
        if(not self.lock):
            try:
                AI_Uart_CMD(self.uart, data_type=1, cmd=AI['guidepost'][0], cmd_type=AI['guidepost'][2])
            except Exception as e:
                print('err:'+str(e))
                pass


class KPU_MODEL(object):
    """ 使用自定义模型 """
    def __init__(self, uart, choice=1, komodel_path=''):
        self.uart = uart
        self.choice = choice
        self.CommandList = AI['kpu_model']
        self.id = None
        self.max_score = 0
        self._task = None
        self.lock = False
        self.send_num = 0
        AI_Uart_CMD_String(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[2], cmd_data=[self.choice,0,0], str_buf=komodel_path)
        time.sleep(0.5)

    def recognize(self):
        self.send_num += 1
        time.sleep_ms(30)
        if(not self.lock and self.send_num<=500):
            AI_Uart_CMD(self.uart, data_type=1, cmd=self.CommandList[0], cmd_type=self.CommandList[3])
    

class Track(object):
    '''查找最大色块 '''
    def __init__(self, uart, choice=1, flag=1, threshold=[[0, 80, 15, 127, 15, 127]], area_threshold=50):
        self.uart = uart
        self.choice = choice
        self.threshold = threshold #
        self.area_threshold = area_threshold
        self.x = None
        self.y = None
        self.cx = None
        self.cy = None
        self.w = None
        self.h = None
        self.pixels = None
        self.count = None
        self.code = None
        self._task = None
        self.lock = False
        self.send_num = 0
        if(flag):
            AI_Uart_CMD(self.uart, 0x01, AI['track'][0], AI['track'][1], cmd_data=[self.choice])
        time.sleep(0.3)

    def recognize(self):
        self.send_num += 1
        time.sleep_ms(30)
        if(not self.lock and self.send_num<500):
            try:
                AI_Uart_CMD(self.uart, data_type=1, cmd=AI['track'][0], cmd_type=AI['track'][2])
            except Exception as e:
                print('err:'+str(e))
                pass
    
    def set_up(self,threshold,area_threshold):
        self.threshold = threshold
        self.area_threshold = area_threshold
        _str=''
        list_len=len(threshold)
        for i in range(list_len):
            if(threshold[i]!=None):
                _str = _str + str(threshold[i][0])+'|'+ str(threshold[i][1])+'|'+ str(threshold[i][2])+'|'+ str(threshold[i][3])+'|'+ str(threshold[i][4])+'|'+ str(threshold[i][5])+'|'
            else:
                list_len = list_len -1
        _str = _str + str(area_threshold)
        AI_Uart_CMD_String(uart=self.uart, cmd=AI['track'][0], cmd_type=AI['track'][3], cmd_data=[int(list_len),0,0], str_buf=_str)
        time.sleep_ms(20)

    
    
class Color_Statistics(object):
    '''图像处理 线性回归'''
    def __init__(self, uart, choice=1):
        self.uart = uart
        self.choice = choice
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
        AI_Uart_CMD(self.uart, 0x01, AI['color_statistics'][0], AI['color_statistics'][1], cmd_data=[self.choice,0,0])
        time.sleep(0.5)

    def recognize(self):
        self.send_num += 1
        time.sleep_ms(30)
        if(not self.lock and self.send_num<500):
            try:
                AI_Uart_CMD(self.uart, data_type=1, cmd=AI['color_statistics'][0], cmd_type=AI['color_statistics'][2])
            except Exception as e:
                print('err:'+str(e))
                pass

    def set_img_grayscale_threshold(self, img_grayscale_threshold):
        self.img_grayscale_threshold = img_grayscale_threshold
        # print(img_grayscale_threshold)
        AI_Uart_CMD(self.uart, 0x01, AI['color_statistics'][0], AI['color_statistics'][3], cmd_data=[img_grayscale_threshold[0],img_grayscale_threshold[1],0])
        time.sleep_ms(30)

    def set_line_grayscale_threshold(self, line_grayscale_threshold):
        self.line_grayscale_threshold = line_grayscale_threshold
        # print(line_grayscale_threshold)
        AI_Uart_CMD(self.uart, 0x01, AI['color_statistics'][0], AI['color_statistics'][4], cmd_data=[line_grayscale_threshold[0],line_grayscale_threshold[1],0])
        time.sleep_ms(30)


    
class Color_Extracto(object):
    '''LAB颜色提取器'''
    def __init__(self, uart, choice=1):
        self.uart = uart
        self.choice = choice
        self.lock = False
        self.L = None 
        self.A = None 
        self.B = None 
        self.LAB_Data = [None,None,None]
        self._task = None
        self.send_num = 0
        AI_Uart_CMD(self.uart, 0x01, AI['color_extracto'][0], AI['color_extracto'][1], cmd_data=[self.choice,0,0])
        time.sleep(0.5)

    def recognize(self):
        self.send_num += 1
        time.sleep_ms(30)
        if(not self.lock and self.send_num<500):
            try:
                AI_Uart_CMD(self.uart, data_type=1, cmd=AI['color_extracto'][0], cmd_type=AI['color_extracto'][2])
            except Exception as e:
                print('err:'+str(e))
                pass


class Apriltag(object):
    '''图像处理 Apriltag'''
    def __init__(self, uart, choice=1):
        self.uart = uart
        self.choice = choice
        self.tag_families = 0
        self.tag_family = None
        self.tag_id = None
        self._task = None
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['apriltag'][0], AI['apriltag'][1], cmd_data=[self.choice,self.tag_families,0])
        time.sleep(0.5)

    def recognize(self): 
        time.sleep_ms(30)
        if(not self.lock):
            try:
                AI_Uart_CMD(self.uart, data_type=1, cmd=AI['apriltag'][0], cmd_type=AI['apriltag'][2])
            except Exception as e:
                print('err:'+str(e))
                pass

    def set_tag_families(self, tag_families):
        self.tag_families = tag_families
        AI_Uart_CMD(self.uart, 0x01, AI['apriltag'][0], AI['apriltag'][3], cmd_data=[tag_families,0,0])
        time.sleep_ms(30)
