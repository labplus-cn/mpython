from machine import Pin, UART
from v831.public import * 
from v831.ai import * 
import time
import gc
gc.collect()

class CameraV831:
    def __init__(self, rx=Pin.P15, tx=Pin.P16):
        self.uart = UART(2, baudrate=1500000, rx=rx, tx=tx, rxbuf=4096)
        self.mode = DEFAULT_MODE
        self.lock = False
        time.sleep(0.1)
        self.wait_for_ai_init()
        # self.uart_listen()

    def wait_for_ai_init(self): 
        self.lock = True
        num = 0        
        while True:
            gc.collect()
            time.sleep_ms(50)
            num +=1
            CMD_TEMP = []
            if(num>10000):
                print('错误:通信超时，请检查接线情况及拓展板电源是否打开！')
                print('Error: Communication timeout, please check the wiring and whether the expansion board is powered on！')
                break
            AI_Uart_CMD(self.uart,0x01,0x01,0xFF)
            if(self.uart.any()):
                head = self.uart.read(1)
                if(head and head[0] == 0xBB):
                    CMD_TEMP.extend([0xBB])
                    cmd_type = self.uart.read(1)
                    CMD_TEMP.append(cmd_type[0])
                    if(CMD_TEMP[1]==0x01):
                        res = self.uart.read(7)
                        if(res[0]==0x01 and res[1]==0xFF):
                            print("AI摄像头重启中...")
                            print("AI camera restarting...")
                            _cmd = self.uart.read()
                            del _cmd
                            gc.collect()
                            break
                else:
                    gc.collect()
                    _cmd = self.uart.read()
                    del _cmd
                    gc.collect()
        time.sleep(3) #等待v831重启
        num = 0
        while True:
            gc.collect()
            num +=1
            CMD_TEMP = []
            AI_Uart_CMD(self.uart,0x01,0x01,0x00) #通信握手
            time.sleep_ms(50)
            if(num>10000):
                print('错误:通信超时，请检查接线情况及掌控拓展电源是否打开！')
                print('Error: Communication timeout, please check the wiring and whether the expansion power is turned on!')
                self.lock = False
                break
            if(num%100==0 and num<10000):
                print('.'*int(num/100))
            if(self.uart.any()):
                head = self.uart.read(1)
                if(head and head[0] == 0xBB):
                    CMD_TEMP.extend([0xBB])
                    cmd_type = self.uart.read(1)
                    CMD_TEMP.append(cmd_type[0])
                    if(CMD_TEMP[1]==0x01):
                        res = self.uart.read(7)
                        for i in range(7):
                            CMD_TEMP.append(res[i])                  
                        checksum = CheckCode(CMD_TEMP[:8])
                        if(res and checksum == CMD_TEMP[8]):
                            if CMD_TEMP[2]==0x01 and CMD_TEMP[3]==0x00:
                                num += 1
                                AI_Uart_CMD(self.uart, 0x01, 0x01, 0x01)
                            elif CMD_TEMP[2]==0x01 and CMD_TEMP[3]==0x01:
                                print('==AI摄像头通信成功==')
                                print('==AI camera communication successful==')
                                self.lock = False
                                _cmd = self.uart.read()
                                del _cmd
                                gc.collect()
                                time.sleep_ms(50)
                                break
                    elif(CMD_TEMP[1]==0x02):
                        pass
                else:
                    # _cmd = self.uart.read()
                    # del _cmd
                    gc.collect()
    
    def Generate_CMD(self, cmd_data=[0]):
        check_sum = 0
        CMD = [0xEF]
        CMD.extend(cmd_data)
        
        for i in range(len(CMD)):
            check_sum = check_sum + CMD[i]
        
        CMD.extend([check_sum & 0xFF])
        return CMD

    # def uart_listen(self):
    #     self._task = TASK(func=self.uart_thread,sec=0.03)
    #     self._task.start()

    def face_detect_init(self):
        self.face_detect = FACE_DETECT(self.uart)
        self.mode = FACE_DETECTION_MODE
    
    def mnist_init(self):
        self.mnist = MNIST(self.uart)
        self.mode = MNIST_MODE

    def yolo_detect_init(self):
        self.yolo_detect = YOLO(self.uart)
        self.mode = OBJECT_RECOGNIZATION_MODE

    def face_recognize_init(self, face_num, accuracy):
        self.fcr = Face_recogization(self.uart, face_num=face_num, accuracy=accuracy)
        self.mode = FACE_RECOGNIZATION_MODE

    def self_learning_classifier_init(self, class_num, sample_num):
        self.slc = Self_learning_classfier(self.uart, class_num=class_num, sample_num=sample_num)
        self.mode = SELF_LEARNING_CLASSIFIER_MODE
        self.slc_parameter = [class_num, sample_num]

    def qrcode_init(self):
        self.qrcode = QRCode_recognization(self.uart)
        self.mode = QRCODE_MODE
    
    def apriltag_init(self):
        self.apriltag = Apriltag(self.uart)
        self.mode = APRILTAG_MODE
    
    def find_line_init(self):
        self.find_line = VisualTracking(self.uart)
        self.mode = VISUAL_TRACKING_MODE

    def color_extracto_init(self):
        self.color_extracto = Color_Extracto(self.uart)
        self.mode = COLOR_EXTRACTO_MODE

    def color_init(self):
        self.color = Color_recognization(self.uart)
        self.mode = COLOE_MODE

    def track_init(self):
        self.track = Track(self.uart)
        self.mode = TRACK_MODE
    
    def track_set_up(self,threshold,area_threshold):
        self.track.set_up(threshold=threshold,area_threshold=area_threshold)

    def model_yolo_init(self, labels, model_param, model_bin, width, height, anchors):
        self.yolo_model = YOLO_MODEL(uart=self.uart, labels=labels, model_param=model_param, model_bin=model_bin, width=width, height=height, anchors=anchors)
        self.mode = MODEL_YOLO_MODE 
    
    def model_restnet18_init(self, labels, model_param, model_bin, width, height):
        self.restnet18_model = Restnet18_MODEL(uart=self.uart, labels=labels, model_param=model_param, model_bin=model_bin, width=width, height=height)
        self.mode = MODEL_resnet18_MODE

    def guidepost_init(self):
        self.guidepost = Guidepost(self.uart)
        self.mode = GUIDEPOST_MODE

    def factory_init(self):
        AI_Uart_CMD(self.uart, 0x01, 0x01, 0xFD)
        self.mode = Factory_MODE

    def restnet1000_init(self):
        self.restnet1000 = Restnet18_MODEL_1000(self.uart)
        self.mode = RESNET18_1000_MODE

    def lpr_init(self):
        self.lpr = LPR(self.uart)
        self.mode = LPR_MODE

    def set_led(self,power=False):
        if(power):
            AI_Uart_CMD(self.uart, 0x01, 0x01, 0xFC, [0x01])
        else:
            AI_Uart_CMD(self.uart, 0x01, 0x01, 0xFC, [0x02])
        time.sleep(0.1)
        
    def set_rgb(self,r=255,g=255,b=255):
        AI_Uart_CMD(self.uart, 0x01, 0x01, 0xFB, [0x01,int(r),int(g),int(b)])
        time.sleep(0.1)
    
    def rgb_off(self,r=255,g=255,b=255):
        AI_Uart_CMD(self.uart, 0x01, 0x01, 0xFB, [0x02])
        time.sleep(0.1)

    def switcher_mode(self, mode=-1):
        '''切换模式'''
        self.lock = True
        
        if(self.mode==mode):
            print('模式相同，未切换')
            print('当前模式:',MODE[self.mode])
            self.lock = False
            time.sleep(1.5)
            return

        if(self.mode==VISUAL_TRACKING_MODE):
            self.find_line.lock = True
        elif(self.mode==TRACK_MODE):
            self.track.lock = True
        elif(self.mode==GUIDEPOST_MODE):
            self.guidepost.lock = True
        elif(self.mode==MNIST_MODE):
            self.mnist.lock = True
        elif(self.mode==OBJECT_RECOGNIZATION_MODE):
            self.yolo_detect.lock = True
        elif(self.mode==FACE_DETECTION_MODE):
            self.face_detect.lock = True
        elif(self.mode==FACE_RECOGNIZATION_MODE):
            self.fcr.lock = True
        elif(self.mode==SELF_LEARNING_CLASSIFIER_MODE):
            self.slc.lock = True
        elif(self.mode==COLOE_MODE):
            self.color.lock = True
        elif(self.mode==QRCODE_MODE):
            self.qrcode.lock = True
        elif(self.mode==COLOR_EXTRACTO_MODE):
            self.color_extracto.lock = True
        elif(self.mode==APRILTAG_MODE):
            self.apriltag.lock = True
        elif(self.mode==MODEL_YOLO_MODE):
            self.yolo_model.lock = True
        elif(self.mode==MODEL_resnet18_MODE):
            self.restnet18_model.lock = True
        
        num = 0        
        while True:
            gc.collect()
            time.sleep_ms(50)
            num += 1
            CMD_TEMP = []
            if(num>1000):
                print('错误:切换模式超时！\n')
                self.lock = False
                break
            AI_Uart_CMD(self.uart,0x01,0x01,0xFE,[mode])#切换模式
            if(self.uart.any()):
                head = self.uart.read(1)
                if(head and head[0] == 0xBB):
                    CMD_TEMP.extend([0xBB])
                    cmd_type = self.uart.read(1)
                    CMD_TEMP.append(cmd_type[0])
                    if(CMD_TEMP[1]==0x01):
                        res = self.uart.read(7)
                        if(res and res[0]==0x01 and res[1]==0xFE):
                            print("AI摄像头正在切换模式...\n")
                            break
                else:
                    _cmd = self.uart.read()
                    del _cmd
                    gc.collect()

        gc.collect()
        time.sleep(1)
        if(mode==GUIDEPOST_MODE):
            self.guidepost_init()    
        elif(mode==TRACK_MODE):
            self.track_init()
        elif(mode==VISUAL_TRACKING_MODE):
            self.find_line_init()
        elif(mode==COLOR_EXTRACTO_MODE):
            self.color_extracto_init()
        elif(mode==APRILTAG_MODE):
            self.apriltag_init()
        elif(mode==SELF_LEARNING_CLASSIFIER_MODE):
            self.self_learning_classifier_init(3,15)
        elif(mode==OBJECT_RECOGNIZATION_MODE):
            self.yolo_detect_init()
        elif(mode==MODEL_YOLO_MODE):
            self.mode = MODEL_YOLO_MODE

        time.sleep(0.5)
        print('当前模式:',MODE[self.mode])
        self.lock = False

    # def uart_thread(self):           
    #     if(self.lock==False):
    #         CMD = uart_handle(self.uart)
    #         if(CMD==None or CMD==[]):
    #             return

    #         if(self.mode==DEFAULT_MODE):
    #             pass
    #         elif(self.mode==MNIST_MODE and self.mnist!=None):
    #             if(len(CMD)>0):
    #                 if(CMD[3]==MNIST_MODE and CMD[4]==0x02):
    #                     if(CMD[5]==0xff):
    #                         self.mnist.id,self.mnist.max_score = None,0
    #                     else:
    #                         self.mnist.id,self.mnist.max_score = CMD[5],round(int(CMD[6])/100,2)
    #                 elif(CMD[2]==0x02):
    #                     pass
    #             else:
    #                 pass
    #         elif(self.mode==OBJECT_RECOGNIZATION_MODE and self.yolo_detect!=None):
    #             if(len(CMD)>0):
    #                 if(CMD[3]==OBJECT_RECOGNIZATION_MODE and CMD[4]==0x02):
    #                     if(CMD[5]==0xff):
    #                         self.yolo_detect.id,self.yolo_detect.max_score,self.yolo_detect.objnum = None,0,0
    #                     else:
    #                         self.yolo_detect.id,self.yolo_detect.max_score,self.yolo_detect.objnum = CMD[5],round(int(CMD[6])/100,2),CMD[7]
    #                 elif(CMD[2]==0x02):
    #                     pass
    #             else:
    #                 pass
    #         elif(self.mode==FACE_DETECTION_MODE and self.face_detect!=None):
    #             if(len(CMD)>0):
    #                 if(CMD[3]==FACE_DETECTION_MODE and CMD[4]==0x02):
    #                     if(CMD[5]==0xff):
    #                         self.face_detect.face_num,self.face_detect.max_score = None,0
    #                     else:
    #                         self.face_detect.face_num,self.face_detect.max_score = CMD[5],round(int(CMD[6])/100,2)
    #                 elif(CMD[2]==0x02):
    #                     pass
    #             else:
    #                 pass
    #         elif(self.mode==FACE_RECOGNIZATION_MODE and self.fcr!=None):#5
    #             if(len(CMD)>0):
    #                 if(CMD[3]==FACE_RECOGNIZATION_MODE and CMD[4]==0x03):
    #                     if(CMD[5]==0xff):
    #                         self.fcr.id,self.fcr.max_score = None,0
    #                     else:
    #                         self.fcr.id,self.fcr.max_score = CMD[5],round(int(CMD[6])/100,2)
    #                 elif(CMD[2]==0x02):
    #                     pass
    #             else:
    #                 pass
    #         elif(self.mode==SELF_LEARNING_CLASSIFIER_MODE and self.slc!=None):#6
    #             if(len(CMD)>0):
    #                 if(CMD[3]==SELF_LEARNING_CLASSIFIER_MODE and CMD[4]==0x03):
    #                     if(CMD[5]==0xff):
    #                         self.slc.id,self.slc.max_score = None,None
    #                     else:
    #                         self.slc.id,self.slc.max_score = CMD[5],CMD[6]/10
    #                 elif(CMD[2]==0x02):
    #                     pass
    #             else:
    #                 pass
    #         elif(self.mode==COLOE_MODE and self.color!=None):#7
    #             try:
    #                 if(len(CMD)>0):
    #                     if(CMD[3]==COLOE_MODE and CMD[4]==0x03):
    #                         if(CMD[5]==0xff):
    #                             self.color.id = None
    #                         else:
    #                             self.color.id = int(CMD[5])
    #                 else:
    #                     self.color.id = None
    #             except:
    #                 self.color.id = None
    #         elif(self.mode==QRCODE_MODE and self.qrcode!=None):
    #             try:
    #                 if(len(CMD)>0):
    #                     if(CMD[3]==QRCODE_MODE and CMD[4]==0x03):
    #                         if(CMD[5]==0xff):
    #                             self.qrcode.id = None
    #                         else:
    #                             self.qrcode.id = int(CMD[5])
    #                     elif(CMD[2]==0x02):
    #                         self.qrcode.id = None
    #                 else:
    #                     self.qrcode.id = None
    #             except:
    #                 self.qrcode.id = None
    #         elif(self.mode==GUIDEPOST_MODE and self.guidepost!=None):#10
    #             if(len(CMD)>0):
    #                 if(CMD[3]==GUIDEPOST_MODE and CMD[4]==0x02):
    #                     if(CMD[5]==0xff):
    #                         self.guidepost.id,self.guidepost.max_score = None,0
    #                     else:
    #                         max_index,self.guidepost.max_score = CMD[5],round(int(CMD[6])/100,2)
    #                         self.guidepost.id = self.guidepost.labels[max_index]
    #                         # self.guidepost.id,self.guidepost.max_score = CMD[5],round(int(CMD[6])/100,2)
    #                 elif(CMD[2]==0x02):
    #                     pass
    #             else:
    #                 self.guidepost.id,self.guidepost.max_score = None,0
    #         elif(self.mode==KPU_MODEL_MODE and self.kpu_model!=None):
    #             if(len(CMD)>0):
    #                 if(CMD[3]==KPU_MODEL_MODE and CMD[4]==0x03):
    #                     if(CMD[5]==0xff):
    #                         self.kpu_model.id,self.kpu_model.max_score = None,0
    #                     else:
    #                         self.kpu_model.id ,self.kpu_model.max_score = CMD[5],round(int(CMD[6])/100,2)
    #                 elif(CMD[2]==0x02):
    #                     pass
    #             else:
    #                 self.kpu_model.id ,self.kpu_model.max_score = None,0
    #         elif(self.mode==TRACK_MODE and self.track!=None):
    #             if(len(CMD)>0):
    #                 if(CMD[2]==0x01 and CMD[3]==TRACK_MODE and CMD[4]==0x02 and CMD[5]==0xff):
    #                     self.track.x,self.track.y,self.track.cx,self.track.cy,self.track.w,self.track.h,self.track.pixels,self.track.count,self.track.code = None,None,None,None,None,None,None,None,None
    #                 elif(CMD[2]==0x02 and CMD[3]==TRACK_MODE and CMD[4]==0x02):
    #                     _str = str(bytes(CMD[21:-1]).decode('UTF-8','ignore'))
    #                     data = _str.split('|')
    #                     self.track.x,self.track.y,self.track.cx,self.track.cy,self.track.w,self.track.h,self.track.pixels,self.track.count,self.track.code = int(data[0]),int(data[1]),int(data[2]),int(data[3]),int(data[4]),int(data[5]),int(data[6]),int(data[7]),hammingWeight(int(CMD[5]))        
    #                 else:
    #                     self.track.x,self.track.y,self.track.cx,self.track.cy,self.track.w,self.track.h,self.track.pixels,self.track.count,self.track.code = None,None,None,None,None,None,None,None,None          
    #             else:
    #                 self.track.x,self.track.y,self.track.cx,self.track.cy,self.track.w,self.track.h,self.track.pixels,self.track.count,self.track.code = None,None,None,None,None,None,None,None,None
    #         elif(self.mode==COLOR_STATISTICS_MODE and self.color_statistics!=None):
    #             if(len(CMD)>0):
    #                 if(CMD[2]==0x01 and CMD[3]==AI['color_statistics'][0] and CMD[4]==AI['color_statistics'][2] and CMD[5]==0xff):
    #                     self.color_statistics.row_data1,self.color_statistics.row_data2,self.color_statistics.row_data3,self.color_statistics.line_get_regression_data = [None,None,None,None,None],[None,None,None,None,None],[None,None,None,None,None],[None,None,None,None,None,None,None,None]
    #                 elif(CMD[2]==0x02 and CMD[3]==AI['color_statistics'][0] and CMD[4]==AI['color_statistics'][2]):
    #                     _str = str(bytes(CMD[21:-1]).decode('UTF-8','ignore'))
    #                     data = _str.split(',')
    #                     self.color_statistics.row_data1,self.color_statistics.row_data2,self.color_statistics.row_data3,self.color_statistics.line_get_regression_data = [int(CMD[5]),int(CMD[6]),int(CMD[7]),int(CMD[8]),int(CMD[9])],[int(CMD[10]),int(CMD[11]),int(CMD[12]),int(CMD[13]),int(CMD[14])],[int(CMD[15]),int(CMD[16]),int(CMD[17]),int(CMD[18]),int(CMD[19])],[int(data[0]),int(data[1]),int(data[2]),int(data[3]),int(data[4]),int(data[5]),int(data[6]),int(data[7])]
    #                 self.color_statistics.data = [self.color_statistics.row_data1,self.color_statistics.row_data2,self.color_statistics.row_data3]
    #             else:
    #                 self.color_statistics.row_data1,self.color_statistics.row_data2,self.color_statistics.row_data3,self.color_statistics.line_get_regression_data = [None,None,None,None,None],[None,None,None,None,None],[None,None,None,None,None],[None,None,None,None,None,None,None,None]
    #                 self.color_statistics.data = [self.color_statistics.row_data1,self.color_statistics.row_data2,self.color_statistics.row_data3]
    #         elif(self.mode==COLOR_EXTRACTO_MODE and self.color_extracto!=None):
    #             if(len(CMD)>0):
    #                 if(CMD[2]==0x01 and CMD[3]==AI['color_extracto'][0] and CMD[4]==AI['color_extracto'][2] and CMD[5]==0xff):
    #                     self.color_extracto.L,self.color_extracto.A,self.color_extracto.B = None,None,None
    #                 elif(CMD[2]==0x02 and CMD[3]==AI['color_extracto'][0] and CMD[4]==AI['color_extracto'][2]):
    #                     _str = str(bytes(CMD[21:-1]).decode('UTF-8','ignore'))
    #                     data = _str.split('|')
    #                     self.color_extracto.L,self.color_extracto.A,self.color_extracto.B = int(data[0]),int(data[1]),int(data[2])
    #                 self.color_extracto.LAB_Data = [self.color_extracto.L,self.color_extracto.A,self.color_extracto.B]
    #             else:
    #                 self.color_extracto.L,self.color_extracto.A,self.color_extracto.B = None,None,None
    #                 self.color_extracto.LAB_Data = [self.color_extracto.L,self.color_extracto.A,self.color_extracto.B]
    #         elif(self.mode==APRILTAG_MODE and self.apriltag!=None):
    #             if(len(CMD)>0):
    #                 if(CMD[2]==0x01 and CMD[3]==AI['apriltag'][0] and CMD[4]==AI['apriltag'][2] and CMD[5]==0xff):
    #                     self.apriltag.tag_family,self.apriltag.tag_id = None,None
    #                 elif(CMD[2]==0x02 and CMD[3]==AI['apriltag'][0] and CMD[4]==AI['apriltag'][2]):
    #                     _str = str(bytes(CMD[21:-1]).decode('UTF-8','ignore'))
    #                     data = _str.split('|')
    #                     self.apriltag.tag_family,self.apriltag.tag_id = int(data[0]),int(data[1])
    #             else:
    #                 self.apriltag.tag_family,self.apriltag.tag_id = None,None
    #         else:
    #             return

