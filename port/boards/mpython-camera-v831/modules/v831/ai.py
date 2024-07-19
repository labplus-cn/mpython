from v831.public import *
import gc
import time
import math

OBJ_TYPE = ['飞机','自行车','鸟','船','瓶子','公交车','汽车','猫','椅子','奶牛','餐桌','狗','屋子','摩托','人','盆栽','羊','沙发','火车','电视']

class Face_recogization(object):
    """ maix人脸识别类"""
    def __init__(self, uart, face_num=1, accuracy=80):
        self.uart = uart
        self.face_num = face_num
        self.accuracy = accuracy
        self.id = None
        self.max_score = None
        self.count = 0
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['face_recognize'][0], AI['face_recognize'][1], cmd_data=[self.face_num,self.accuracy])
        time.sleep(2)

    def add_face(self):
        AI_Uart_CMD(self.uart, 0x01, AI['face_recognize'][0], AI['face_recognize'][2])

    def recognize(self):
        time.sleep_ms(20)
        try:
            self.id,self.max_score=self.AI_WaitForK210(0x01, AI['face_recognize'][0], AI['face_recognize'][3])
        except Exception as e:
            # print('err:',e)
            self.id,self.max_score=None,None


    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]):   
        if(not self.lock):           
            # print('AI_Uart_CMD'+str(time.time_ns()))            
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)
        CMD = uart_handle(self.uart)

        if(len(CMD)>0):
            if(CMD[1]==0x01):
                if(CMD[2]==0x05 and CMD[3]==0x03):
                    if(CMD[4]==0xff):
                        self.lock = True
                        return None,None
                    else:
                        return CMD[4],round(int(CMD[5])/100,2)
            elif(CMD[1]==0x02):
                pass
        else:
            return None,None

class Self_learning_classfier(object):
    """ maix自学习分类"""
    def __init__(self, uart=None, class_num=1, sample_num=5):
        self.uart = uart
        self.class_num = class_num
        self.sample_num = sample_num
        self.id = None
        self.max_score = None
        self.count = 0
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['self_learn'][0], AI['self_learn'][1], cmd_data=[self.class_num,self.sample_num])
        time.sleep(2)
        
    def add_class_img(self):
        AI_Uart_CMD(self.uart, 0x01, AI['self_learn'][0], AI['self_learn'][2])
        time.sleep_ms(10)

    def add_sample_img(self):
        pass

    def train(self):
        pass

    def predict(self):
        # self.count += 1
        time.sleep_ms(20)
        try:
            self.id,self.max_score = self.AI_WaitForK210(0x01, AI['self_learn'][0], AI['self_learn'][3])
        except:
            self.id,self.max_score = None,None

    def save_classifier(self, name):
        AI_Uart_CMD_String(uart=self.uart, cmd=AI['self_learn'][0], cmd_type=AI['self_learn'][4], str_buf=name)
        time.sleep_ms(50)

    def load_classifier(self, name):
        AI_Uart_CMD_String(uart=self.uart, cmd=AI['self_learn'][0], cmd_type=AI['self_learn'][5], str_buf=name)
        time.sleep_ms(50)

    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]):        
        if(not self.lock):     
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)

        CMD = uart_handle(self.uart)

        if(len(CMD)>0):
            if(CMD[2]==AI['self_learn'][0] and CMD[3]==0x03):
                if(CMD[4]==0xff):
                    return None,None
                else:
                    self.lock = True
                    return CMD[4],CMD[5]/100
            elif(CMD[1]==0x02):
                pass
        else:
            return None,None

class YOLO(object):
    ''' 物体识别20类 '''
    def __init__(self, uart):
        self.uart = uart
        self.category_list = OBJ_TYPE
        self.id = None
        self.max_score = None
        self.lock = False
        self.count = 0
        self.status = False
        AI_Uart_CMD(self.uart, 0x01, AI['20yolo'][0], AI['20yolo'][1])
        time.sleep(0.1)

    def recognize(self):
        self.count += 1
        time.sleep_ms(20)
        try:
            self.id,self.max_score = self.AI_WaitForK210(0x01, AI['20yolo'][0], AI['20yolo'][2])
        except Exception as e:
            self.id,self.max_score = None,None

    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]):  
        if(not self.lock):           
            # print('AI_Uart_CMD'+str(time.time_ns()))
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)
        CMD = uart_handle(self.uart)
        if(len(CMD)>0):
            if(CMD[2]==0x03 and CMD[3]==0x02):
                if(CMD[4]==0xff):
                    self.lock = True
                    return None,None
                else:
                    return CMD[4],round(int(CMD[5])/100,2)
            elif(CMD[1]==0x02):
                pass
        else:
            return None,None


class MNIST(object):
    '''手写数字v831'''
    def __init__(self, uart):
        self.uart = uart
        self.id = None
        self.max_score = None
        self.count = 0
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['mnist'][0], AI['mnist'][1])
        time.sleep(0.2)

    def recognize(self):
        # self.count += 1
        time.sleep_ms(10)
        try:
            self.id,self.max_score = self.AI_WaitForK210(0x01, AI['mnist'][0], AI['mnist'][2])
        except Exception as e:
            print('MNIST err:',e)
            self.id,self.max_score =  None,None

    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]):          
        if(not self.lock):   
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)

        CMD = uart_handle(self.uart)

        if(len(CMD)>0):
            if(CMD[2]==0x02 and CMD[3]==0x02):
                if(CMD[4]==0xff):
                    self.lock = True
                    return None,None
                else:
                    return CMD[4],round(int(CMD[5])/100,2)
            elif(CMD[1]==0x02):
                pass
        else:
            return None,None


class FACE_DETECT(object):
    """人脸检测v831"""
    def __init__(self, uart):
        self.uart = uart
        self.face_num = None
        self.max_score = None
        self.count = 0
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['face_detection'][0], AI['face_detection'][1])
        time.sleep(0.2)

    def recognize(self):
        time.sleep_ms(20)
        try:
            self.face_num,self.max_score = self.AI_WaitForK210(0x01, AI['face_detection'][0], AI['face_detection'][2])
        except Exception as e:
            print('err:',e)
            self.face_num,self.max_score = None,None

    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]):  
        if(not self.lock):         
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)

        CMD = uart_handle(self.uart)
        if(len(CMD)>0):
            if(CMD[2]==0x04 and CMD[3]==0x02):
                if(CMD[4]==0xff):
                    self.lock = True
                    return None,None
                else:
                    return CMD[4],round(int(CMD[5])/100,2)
            elif(CMD[1]==0x02):
                pass
        else:
            return None,None


class Color_recognization(object):
    """ 颜色识别"""
    def __init__(self, uart=None):
        self.uart = uart
        self.id = None
        self.count = 0
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['color'][0], AI['color'][1])
        time.sleep(0.1)

    def add_color(self, num):
        AI_Uart_CMD(self.uart, 0x01, AI['color'][0], AI['color'][2], cmd_data=[num])
        time.sleep_ms(50)
        
    def recognize(self):
        # self.count += 1
        time.sleep_ms(10)
        try:
            self.id = self.AI_WaitForK210(0x01, AI['color'][0], AI['color'][3])
        except:
            self.id = None
    
    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]):    
        if(not self.lock):        
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)
            # print('cmd')
        CMD = uart_handle(self.uart)

        if(len(CMD)>0):
            if(CMD[2]==0x07 and CMD[3]==0x03):
                if(CMD[4]==0xff):
                    self.lock = True
                    return None
                else:
                    return CMD[4]
            elif(CMD[1]==0x02):
                pass
        else:
            return None

class QRCode_recognization(object):
    """ 二维码识别类"""
    def __init__(self, uart=None):
        self.uart = uart
        self.id = None
        self.info = None
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['qrcode'][0], AI['qrcode'][1], cmd_data=[])
        time.sleep(0.2)

    def add_qrcode(self, num):
        AI_Uart_CMD(self.uart, 0x01, AI['qrcode'][0], AI['qrcode'][2], cmd_data=[num])
        time.sleep_ms(50)

    def recognize(self):
        # self.count += 1
        time.sleep_ms(10)
        try:
            tmp = self.AI_WaitForK210(0x01, AI['qrcode'][0], AI['qrcode'][3])
            self.id = tmp[0]
            self.info = tmp[1]
        except:
            self.id = None
            self.info = None

    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]):    
        if(not self.lock):   
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)
        CMD = uart_handle(self.uart)

        if(len(CMD)>0):
            if(CMD[1]==0x01):
                if(CMD[2]==0x08 and CMD[3]==0x03):
                    if(CMD[4]==0xff):
                        self.lock = True
                        return None,None
            elif(CMD[1]==0x02):
                if(CMD[2]==AI['qrcode'][0] and CMD[3]==AI['qrcode'][3]):
                    id = CMD[4]
                    info = str(bytes(CMD[20:-1]).decode('UTF-8','ignore'))
                    return id,info
        else:
            return None,None


class Guidepost(object):
    '''路标识别'''
    def __init__(self, uart):
        self.uart = uart
        self.id = None
        self.max_score = None
        self.labels = ["right","left",'stop']
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['guidepost'][0], AI['guidepost'][1])
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(10)
        try:
            max_index,self.max_score = self.AI_WaitForK210(0x01, AI['guidepost'][0], AI['guidepost'][2])
            self.id = self.labels[max_index]
        except Exception as e:
            self.id,self.max_score =  None,None
       
    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]):  
        if(not self.lock):           
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)

        CMD = uart_handle(self.uart)
        # print(CMD)
        if(len(CMD)>0):
            if(CMD[2]==AI['guidepost'][0] and CMD[3]==0x02):
                if(CMD[4]==0xff):
                    self.lock = True
                    return None,None
                else:
                    self.lock = True
                    return CMD[4],round(int(CMD[5])/100,2)
            elif(CMD[1]==0x02):
                pass
        else:
            return None,None


class V831_MODEL(object):
    """ 使用自定义模型 """
    def __init__(self, uart, komodel_path=''):
        self.uart = uart
        self.CommandList = AI['kpu_model']
        self.id = None
        self.max_score = None
        AI_Uart_CMD_String(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[2], str_buf=komodel_path)
        time.sleep(0.5)

    def recognize(self):
        time.sleep_ms(5)
        try:
            self.id,self.max_score = self.AI_WaitForK210(0x01, self.CommandList[0], self.CommandList[3])
        except:
            self.id,self.max_score = None,None

    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]):            
        AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)
        _CMD = uart_handle(self.uart)

        if(len(_CMD)>0):
            if(_CMD[3]==self.CommandList[0] and _CMD[4]==self.CommandList[3]):
                if(_CMD[5]==0xff):
                    return None,None
                else:
                    return _CMD[5],round(int(_CMD[6])/100,2)
            elif(_CMD[2]==0x02):
                pass
        else:
            return None,None


class Track(object):
    '''查找最大色块 '''
    def __init__(self, uart, threshold=[[0, 80, 15, 127, 15, 127]], area_threshold=50):
        self.uart = uart
        self.threshold = threshold 
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
        self.lock = False
        self.tmp_count = 0
        AI_Uart_CMD(self.uart, 0x01, AI['track'][0], AI['track'][1])
        time.sleep(0.1)

    def recognize(self):
        self.tmp_count += 1
        time.sleep_ms(5)
        try:
            self.x,self.y,self.cx,self.cy,self.w,self.h,self.pixels,self.count,self.code = self.AI_WaitForK210(0x01, AI['track'][0], AI['track'][2])
        except Exception as e:
            print(e)
            self.x,self.y,self.cx,self.cy,self.w,self.h,self.pixels,self.count,self.code = None,None,None,None,None,None,None,None,None


    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]): 
        gc.collect()           
        if(not self.lock): 
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)
     
        CMD = uart_handle(self.uart)
        if(len(CMD)>0):
            if(CMD[1]==0x01 and CMD[2]==0x0c and CMD[3]==0x02 and CMD[4]==0xff):
                self.lock = True
                return None,None,None,None,None,None,None,None,None
            elif(CMD[1]==0x02 and CMD[2]==0x0c and CMD[3]==0x02):
                _str = str(bytes(CMD[20:-1]).decode('UTF-8','ignore'))
                # print(_str)
                data = _str.split('|')
                return int(data[0]),int(data[1]),round(float(data[2]),2),round(float(data[3]),2),int(data[4]),int(data[5]),int(data[6]),int(data[7]),hammingWeight(int(CMD[4]))
                    
        else:
            return None,None,None,None,None,None,None,None,None
    
    def set_up(self,threshold,area_threshold):
        self.threshold = threshold
        self.area_threshold = area_threshold
        _str = str(self.threshold) + '|' + str(area_threshold)
        AI_Uart_CMD_String(uart=self.uart, cmd=AI['track'][0], cmd_type=AI['track'][3], str_buf=_str)

    
class Color_Extracto(object):
    '''LAB颜色提取器'''
    def __init__(self, uart):
        self.uart = uart
        self.LAB_Data = [None,None,None]
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['color_extracto'][0], AI['color_extracto'][1])
        time.sleep(0.1)

    def recognize(self):
        # self.count += 1
        gc.collect()   
        time.sleep_ms(10)
        try:
            self.L,self.A,self.B = self.AI_WaitForK210(0x01, AI['color_extracto'][0], AI['color_extracto'][2])
        except Exception as e:
            self.L,self.A,self.B = None,None,None
        self.LAB_Data = [self.L,self.A,self.B]

    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]): 
        # gc.collect()           
        if(not self.lock):
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)

        CMD = uart_handle(self.uart)
        if(len(CMD)>0):
            if(CMD[1]==0x01 and CMD[2]==AI['color_extracto'][0] and CMD[3]==AI['color_extracto'][2] and CMD[4]==0xff):
                self.lock = True
                return None,None,None
            elif(CMD[1]==0x02 and CMD[2]==AI['color_extracto'][0] and CMD[3]==AI['color_extracto'][2]):
                self.lock = True
                _str = str(bytes(CMD[20:-1]).decode('UTF-8','ignore'))
                data = _str.split('|')
                return int(data[0]),int(data[1]),int(data[2])
        else:
            return None,None,None


class Apriltag(object):
    def __init__(self, uart):
        self.uart = uart
        self.tag_families = 0
        self.tag_family = None
        self.tag_id = None
        self.x_tran = None
        self.y_tran = None
        self.z_tran = None
        self.x_rol = None
        self.y_rol = None
        self.z_rol = None
        self.length = None
        self.lock = False
        self.none_result = None,None,None,None,None,None,None,None,None
        AI_Uart_CMD(self.uart, 0x01, AI['apriltag'][0], AI['apriltag'][1], cmd_data=[self.tag_families])
        time.sleep(0.1)
    
    def update(self,data):
        self.tag_family,self.tag_id,self.x_tran,self.y_tran,self.z_tran,self.x_rol,self.y_rol,self.z_rol,self.length = data

    def recognize(self):
        time.sleep_ms(5)
        try:
            data = self.AI_WaitForK210(0x01, AI['apriltag'][0], AI['apriltag'][2])
            self.update(data)
        except Exception as e:
            self.update(self.none_result)

    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]): 
        gc.collect()           
        if(not self.lock): 
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)

        CMD = uart_handle(self.uart)
        if(len(CMD)>0):
            if(CMD[1]==0x01 and CMD[2]==AI['apriltag'][0] and CMD[3]==AI['apriltag'][2] and CMD[4]==0xff):
                self.lock = True
                return self.none_result
            elif(CMD[1]==0x02 and CMD[2]==AI['apriltag'][0] and CMD[3]==AI['apriltag'][2]):
                self.lock = True
                _str = str(bytes(CMD[20:-1]).decode('UTF-8','ignore'))
                data = eval(_str)
                return int(data[0]),int(data[1]),float(data[2]),float(data[3]),float(data[4]),float(data[5]),float(data[6]),float(data[7]),float(data[8])
        else:
            return self.none_result

    def set_tag_families(self, tag_families):
        self.tag_families = tag_families
        AI_Uart_CMD(self.uart, 0x01, AI['apriltag'][0], AI['apriltag'][3], cmd_data=[tag_families])



class YOLO_MODEL(object):
    """ 使用自定义模型 YOLO"""
    def __init__(self, uart, labels=["id1","id2",'id3'], model_param='', model_bin='', width=224, height=224, anchors=[]):
        self.uart = uart
        self.CommandList = AI['model_yolo']
        self.id = None
        self.max_score = 0
        # self._task = None
        self.lock = False
        parameter = str(labels)+'|'+str(model_param)+'|'+str(model_bin)+'|'+str(width)+'|'+str(height)+'|'+str(anchors)
        AI_Uart_CMD_String(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1], cmd_data=[], str_buf=parameter)
        time.sleep(0.3)

    def recognize(self):
        time.sleep_ms(1)
        try:
            self.id,self.max_score = self.AI_WaitForK210(0x01, self.CommandList[0], self.CommandList[2])
        except:
            self.id,self.max_score = None,None

    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]):            
        gc.collect()           
        if(not self.lock): 
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)
        _CMD = uart_handle(self.uart)

        # print(_CMD)

        if(len(_CMD)>0):
            if(_CMD[2]==self.CommandList[0] and _CMD[3]==self.CommandList[2]):
                if(_CMD[4]==0xff):
                    self.lock = True
                    return None,None
                else:
                    return _CMD[4],round(int(_CMD[5])/100,2)
            elif(_CMD[1]==0x02):
                self.lock = True
                _str = str(bytes(CMD[20:-1]).decode('UTF-8','ignore'))
                data = _str.split('|')
                return int(data[0]),int(data[1])
        else:
            return None,None


class Restnet18_MODEL(object):
    """ 使用自定义模型 restnet18"""
    def __init__(self, uart, labels=["id1","id2",'id3'], width=224, height=224, model_param='', model_bin=''):
        self.uart = uart
        self.CommandList = AI['model_restnet18']
        self.id = None
        self.max_score = 0
        self.lock = False
        parameter = str(labels)+'|'+str(model_param)+'|'+str(model_bin)+'|'+str(width)+'|'+str(height)
        AI_Uart_CMD_String(uart=self.uart, cmd=self.CommandList[0], cmd_type=self.CommandList[1], cmd_data=[], str_buf=parameter)
        time.sleep(0.3)

    def recognize(self):
        time.sleep_ms(1)
        try:
            self.id,self.max_score = self.AI_WaitForK210(0x01, self.CommandList[0], self.CommandList[2])
        except:
            self.id,self.max_score = None,None

    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]):            
        gc.collect()           
        if(not self.lock): 
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)
        _CMD = uart_handle(self.uart)

        if(len(_CMD)>0):
            if(_CMD[1]==0x01 and _CMD[2]==self.CommandList[0] and _CMD[3]==self.CommandList[2]):
                if(_CMD[4]==0xff):
                    self.lock = True
                    return None,None
                else:
                    return _CMD[4],round(int(_CMD[5])/100,2)
            elif(_CMD[1]==0x02  and _CMD[2]==self.CommandList[0] and _CMD[3]==self.CommandList[2]):
                self.lock = True
                _str = str(bytes(_CMD[20:-1]).decode('UTF-8','ignore'))
                data = eval(_str)
                # print(data)
                return int(data[0]),int(data[1])
        else:
            return None,None



    
class VisualTracking(object):
    '''图像处理 寻线（黑线）'''
    def __init__(self, uart):
        self.uart = uart
        self.lock = False
        self.line_data = {'rect': None, 'pixels': None, 'cx': None, 'cy': None, 'rotation': None}
        self.rotation_angle = None
        AI_Uart_CMD(self.uart, 0x01, AI['VISUAL_TRACKING_MODE'][0], AI['VISUAL_TRACKING_MODE'][1])
        time.sleep(0.1)

    def recognize(self):
        time.sleep_ms(5)
        gc.collect()
        try:
            tmp = self.AI_WaitForK210(0x01, AI['VISUAL_TRACKING_MODE'][0], AI['VISUAL_TRACKING_MODE'][2])
            self.line_data = tmp
            self.rotation_angle = round(self.line_data['rotation']*180/math.pi,2)
        except Exception as e:
            # print('err:',e)
            self.line_data = {'rect': None, 'pixels': None, 'cx': None, 'cy': None, 'rotation': None}
            self.rotation_angle = None

    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]): 
        if(not self.lock):    
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)

        CMD = uart_handle(self.uart)
        if(len(CMD)>=5):
            # print(CMD)
            if(CMD[1]==0x01 and CMD[2]==AI['VISUAL_TRACKING_MODE'][0] and CMD[3]==AI['VISUAL_TRACKING_MODE'][2] and CMD[4]==0xff):
                self.lock = True
                return {'rect': None, 'pixels': None, 'cx': None, 'cy': None, 'rotation': None}
            elif(CMD[1]==0x02 and CMD[2]==AI['VISUAL_TRACKING_MODE'][0] and CMD[3]==AI['VISUAL_TRACKING_MODE'][2]):
                self.lock = True
                _str = str(bytes(CMD[20:-1]).decode('UTF-8','ignore'))
                data = eval(_str)
                return data
        else:
            return {'rect': None, 'pixels': None, 'cx': None, 'cy': None, 'rotation': None}