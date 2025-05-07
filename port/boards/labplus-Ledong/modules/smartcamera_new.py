from machine import Pin, UART
from lib.k210_ai import *
import time
import gc
gc.collect()

class SmartCamera:
    def __init__(self, rx=Pin.P15, tx=Pin.P16):
        self.sensor_choice = 1
        self.uart = UART(2, baudrate=1152000, rx=rx, tx=tx, rxbuf=2048)
        self.mode = DEFAULT_MODE
        self.lock = False
        time.sleep(0.05)
        self.wait_for_ai_init()
        self.thread_listen()
        self.slc_parameter = [3, 15, 11, 1]
        self.a_status = 0
        self.b_status = 0
        self.tf_status = 0
        self.tf_sn = ''

    def wait_for_ai_init(self): 
        self.lock = True
        num = 0        
        while True:
            gc.collect()
            time.sleep_ms(100)
            num +=1
            CMD_TEMP = []
            if(num>5000):
                print('错误:通信超时，请检查接线情况及掌控拓展电源是否打开！')
                print('Error: Communication timeout, please check the wiring and control whether the expansion power is turned on!')
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
                            print("AI camera is restarting")
                            time.sleep(0.5)
                            _cmd = self.uart.read()
                            del _cmd
                            gc.collect()
                            break
                else:
                    _cmd = self.uart.read()
                    del _cmd
                    gc.collect()
        time.sleep(1) #等待k210重启
        num = 0
        
        while True:
            time.sleep_ms(100)
            gc.collect()
            num +=1
            CMD_TEMP = []
            if(num>1000):
                print('错误:通信超时，请检查接线情况及掌控拓展电源是否打开！')
                print('Error: Communication timeout, please check the wiring and control whether the expansion power is turned on!')
                self.lock = False
                break
            if(num%30==0 and num<500):
                print('.'*int(num/30))
            AI_Uart_CMD(self.uart,0x01,0x01,0x00) #通信握手
            time.sleep_ms(50)
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
                                print('==AI camera communication successful==')
                                self.lock = False
                                time.sleep_ms(200)
                                _cmd = self.uart.read()
                                del _cmd
                                gc.collect()
                                time.sleep_ms(50)
                                break
                    elif(CMD_TEMP[2]==0x02):
                        pass
                else:
                    gc.collect()

    def image_init(self):
        # 主绘图对象
        pass
    
    def sensor_config(self,_choice,_framesize,_pixformat,_w,_h,_vflip,_hmirror,_brightness,_contrast,_saturation,_gain,_whitebal,_freq,_dual_buff):
        self.lock=True
        _str = str(_framesize)+'|'+ str(_pixformat)+'|'+ str(_vflip)+'|'+ str(_hmirror)+'|'+ str(_brightness)+'|'+ str(_contrast)+'|'+ str(_saturation)+'|'+ str(_gain)+'|'+ str(_whitebal)+'|'+ str(_w)+'|'+ str(_h)+'|'+ str(_freq)+'|'+ str(_dual_buff)
        AI_Uart_CMD_String(uart=self.uart, cmd=AI['sensor'][0], cmd_type=AI['sensor'][1], cmd_data=[_choice,0,0], str_buf=_str)
        self.lock=False

    def mnist_init(self, _choice):
        self.mnist = MNIST(self.uart, choice=_choice)
        self.mode = MNIST_MODE

    def yolo_detect_init(self, _choice):
        self.yolo_detect = YOLO(self.uart, choice=_choice)
        self.mode = OBJECT_RECOGNIZATION_MODE

    def face_detect_init(self, _choice):
        self.face_detect = FACE_DETECT(self.uart, choice=_choice)
        self.mode = FACE_DETECTION_MODE

    def face_recognize_init(self, _face_num, _accuracy, _choice):
        self.fcr = Face_recogization(self.uart, face_num=_face_num, accuracy=_accuracy, choice=_choice)
        self.mode = FACE_RECOGNIZATION_MODE

    def asr_init(self):
        self.asr = Maix_asr(self.uart)
        self.mode = SPEECH_RECOGNIZATION_MODE
    
    def self_learning_classifier_init(self, _class_num, _sample_num, _threshold, _choice):
        self.slc = Self_learning_classfier(self.uart, class_num=_class_num, sample_num=_sample_num, choice=_choice)
        self.mode = SELF_LEARNING_CLASSIFIER_MODE
        self.slc_parameter = [_class_num, _sample_num, 11, _choice]

    def qrcode_init(self, _choice):
        self.qrcode = QRCode_recognization(self.uart, choice=_choice)
        self.mode = QRCODE_MODE

    def color_init(self, _choice):
        self.color = Color_recognization(self.uart, choice=_choice)
        self.mode = COLOE_MODE

    def guidepost_init(self, _choice):
        self.guidepost = Guidepost(self.uart, choice=_choice)
        self.mode = GUIDEPOST_MODE

    def kmodel_init(self, _choice, _komodel_path, width, height):
        self.kpu_model = KPU_MODEL(self.uart, choice=_choice, komodel_path=_komodel_path, width=width, height=height)
        self.mode = KPU_MODEL_MODE

    def track_init(self, _choice):
        self.track = Track(self.uart, choice=_choice)
        self.mode = TRACK_MODE
    
    def track_set_up(self,threshold,area_threshold):
        self.track.set_up(threshold=threshold,area_threshold=area_threshold)

    def color_statistics_init(self, _choice):
        self.color_statistics = Color_Statistics(self.uart, choice=_choice)
        self.mode = COLOR_STATISTICS_MODE

    def color_extracto_init(self, _choice):
        self.color_extracto = Color_Extracto(self.uart, choice=_choice)
        self.mode = COLOR_EXTRACTO_MODE

    def apriltag_init(self, _choice):
        self.apriltag = Apriltag(self.uart, choice=_choice)
        self.mode = APRILTAG_MODE

    def video_capture(self, choice=1, path="/sd/capture.avi", interval=100000, quality=50, width=320, height=240, duration=10):
        parameter = str(path)+'|'+ str(interval)+'|'+ str(width)+'|'+ str(height)+'|'+ str(duration)
        AI_Uart_CMD_String(uart=self.uart, cmd=AI['video'][0], cmd_type=AI['video'][1], cmd_data=[choice,quality,0], str_buf=parameter)

    def kmodel_yolo_init(self, _choice, _komodel_path, width, height, anchors):
        self.kpu_yolo_model = KPU_YOLO_MODEL(self.uart, choice=_choice, komodel_path=_komodel_path, width=width, height=height, anchors=anchors)
        self.mode = KPU_YOLO_MODEL_MODE 
        
    def canvas_init(self):
        AI_Uart_CMD(self.uart, 0x01, 0x01, 0xFA, [0x01])
        self.mode = DEFAULT_MODE
        time.sleep_ms(50)
    
    def canvas_clear(self):
        AI_Uart_CMD(self.uart, 0x01, 0x01, 0xFA, [0x02])
        time.sleep_ms(20)
    
    def canvas_txt(self,txt='',scale=1,x=0,y=0):
        _str = str([x,y,txt])
        AI_Uart_CMD_String(uart=self.uart, cmd=0x01, cmd_type=0xFA, cmd_data=[scale], str_buf=_str)
        time.sleep_ms(20)
    
    def rgb(self,r=0,g=0,b=0):
        AI_Uart_CMD(self.uart, 0x01, 0x01, 0xFA, [0x03,int(r),int(g),int(b)])
        time.sleep_ms(20)
    
    def led(self,mode=0):
        AI_Uart_CMD(self.uart, 0x01, 0x01, 0xFA, [0x04,int(mode)])
        time.sleep_ms(20)
    
    def factory_init(self):
        self.mode = FACTORY_MODE
        AI_Uart_CMD(self.uart, 0x01, 0x01, FACTORY_MODE, [0x01])
        time.sleep(1)
    
    def factory_lcd(self):
        AI_Uart_CMD(self.uart, 0x01, 0x01, FACTORY_MODE, [0x02])
        time.sleep(1) 
    
    def factory_sensor(self):
        AI_Uart_CMD(self.uart, 0x01, 0x01, FACTORY_MODE, [0x03])
        time.sleep(1)  
    
    def factory_rgb(self,r=0,g=0,b=0):
        AI_Uart_CMD(self.uart, 0x01, 0x01, FACTORY_MODE, [0x04,int(r),int(g),int(b)])
        time.sleep(1)
    
    def factory_light(self,light=1):
        AI_Uart_CMD(self.uart, 0x01, 0x01, FACTORY_MODE, [0x05])
        time.sleep(1)   
    
    def factory_write_sn(self,sn='sn'):
        _str = str([sn])
        AI_Uart_CMD_String(uart=self.uart, cmd=FACTORY_MODE, cmd_type=0x01, str_buf=_str)
        time.sleep(1)

    def thread_listen(self):
        self._task = TASK(func=self.uart_thread,sec=0.005)
        self._task.start()

    def switcher_mode(self, mode, choice):
        '''切换模式'''
        self.lock = True
        
        if(self.mode==mode):
            print('模式相同，未切换')
            print('当前模式:',MODE[self.mode])
            self.lock = False
            time.sleep(0.01)
            return

        if(self.mode==COLOR_STATISTICS_MODE):
            self.color_statistics.lock = True
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
        elif(self.mode==SPEECH_RECOGNIZATION_MODE):
            self.asr.lock = True
        elif(self.mode==KPU_MODEL_MODE):
            self.kpu_model.lock = True
        elif(self.mode==COLOR_EXTRACTO_MODE):
            self.color_extracto.lock = True
        elif(self.mode==APRILTAG_MODE):
            self.apriltag.lock = True
        elif(self.mode==KPU_YOLO_MODEL_MODE):
            self.kpu_yolo_model.lock = True
        
        num = 0        
        while True:
            time.sleep_ms(50)
            gc.collect()
            num += 1
            CMD_TEMP = []
            if(num>1000):
                print('错误:切换模式超时！\n')
                self.lock = False
                print('当前模式:\n',MODE[self.mode])
                return 
            
            AI_Uart_CMD(self.uart,0x01,0x01,0xFE,[mode])#切换模式指令
            time.sleep_ms(50)
            if(self.uart.any()):
                head = self.uart.read(2)
                if(head and head[0] == 0xBB and head[1] == 0xAA):
                    CMD_TEMP.extend([0xBB,0xAA])
                    cmd_type = self.uart.read(1)
                    CMD_TEMP.append(cmd_type[0])
                    if(CMD_TEMP[2]==0x01):
                        time.sleep_ms(1)
                        res = self.uart.read(9)
                        if(res[0]==0x01 and res[1]==0xFE):
                            print("AI摄像头正在切换模式...\n")
                            gc.collect()
                            break
                else:
                    gc.collect()
        
        time.sleep(2)
        _cmd = self.uart.read()
        del _cmd   
        gc.collect()
      
        if(mode==GUIDEPOST_MODE):
            self.guidepost_init(choice)    
        elif(mode==TRACK_MODE):
            self.track_init(choice)
        elif(mode==COLOR_STATISTICS_MODE):
            self.color_statistics_init(_choice=choice)
        elif(mode==COLOR_EXTRACTO_MODE):
            self.color_extracto_init(_choice=choice)
        elif(mode==APRILTAG_MODE):
            self.apriltag_init(_choice=choice)
        elif(mode==SELF_LEARNING_CLASSIFIER_MODE):
            self.self_learning_classifier_init(self.slc_parameter[0],self.slc_parameter[1],self.slc_parameter[2],_choice=choice)
            self.slc_parameter[3]=choice
        elif(mode==OBJECT_RECOGNIZATION_MODE):
            self.yolo_detect_init(_choice=choice)
        elif(mode==FACE_DETECTION_MODE):
            self.face_detect_init(_choice=choice)
        elif(mode==FACE_RECOGNIZATION_MODE):
            self.face_recognize_init(1,80,1)

        time.sleep(1)
        print('当前模式:\n',MODE[self.mode])
        self.lock = False

    def uart_thread(self):           
        if(self.lock==False):
            CMD = uart_handle(self.uart)
            if(CMD==None):
                return

            if(self.mode==DEFAULT_MODE):
                pass
            elif(self.mode==MNIST_MODE and self.mnist!=None):
                if(len(CMD)>0):
                    if(CMD[3]==MNIST_MODE and CMD[4]==0x02):
                        if(CMD[5]==0xff):
                            self.mnist.lock = True
                            self.mnist.id,self.mnist.max_score = None,0
                        else:
                            self.mnist.id,self.mnist.max_score = CMD[5],round(int(CMD[6])/100,2)
                    elif(CMD[2]==0x02):
                        pass
                else:
                    pass
            elif(self.mode==OBJECT_RECOGNIZATION_MODE and self.yolo_detect!=None):
                if(len(CMD)>0):
                    if(CMD[3]==OBJECT_RECOGNIZATION_MODE and CMD[4]==0x02):
                        if(CMD[5]==0xff):
                            self.yolo_detect.lock = True
                            self.yolo_detect.id,self.yolo_detect.max_score,self.yolo_detect.objnum = None,0,0
                        else:
                            self.yolo_detect.id,self.yolo_detect.max_score,self.yolo_detect.objnum = CMD[5],round(int(CMD[6])/100,2),CMD[7]
                    elif(CMD[2]==0x02):
                        pass
                else:
                    pass
            elif(self.mode==FACE_DETECTION_MODE and self.face_detect!=None):
                if(len(CMD)>0):
                    if(CMD[3]==FACE_DETECTION_MODE and CMD[4]==0x02):
                        if(CMD[5]==0xff):
                            self.face_detect.lock = True
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
                            self.fcr.lock = True
                            self.fcr.id,self.fcr.max_score = None,0
                        else:
                            self.fcr.id,self.fcr.max_score = CMD[5],round(int(CMD[6])/100,2)
                    elif(CMD[2]==0x02):
                        pass
                else:
                    pass
            elif(self.mode==SELF_LEARNING_CLASSIFIER_MODE and self.slc!=None):#6
                if(len(CMD)>0):
                    if(CMD[3]==SELF_LEARNING_CLASSIFIER_MODE and CMD[4]==0x03):
                        if(CMD[5]==0xff):
                            self.slc.lock = True
                            self.slc.id,self.slc.max_score = None,None
                        else:
                            self.slc.id,self.slc.max_score = CMD[5],CMD[6]/10
                    elif(CMD[2]==0x02):
                        pass
                else:
                    pass
            elif(self.mode==COLOE_MODE and self.color!=None):#7
                try:
                    if(len(CMD)>0):
                        if(CMD[3]==COLOE_MODE and CMD[4]==0x03):
                            if(CMD[5]==0xff):
                                self.color.lock = True
                                self.color.id = None
                            else:
                                self.color.id = int(CMD[5])
                    else:
                        self.color.id = None
                except:
                    self.color.id = None
            elif(self.mode==QRCODE_MODE and self.qrcode!=None):
                try:
                    if(len(CMD)>0):
                        if(CMD[2]==0x01 and CMD[3]==QRCODE_MODE and CMD[4]==0x03):
                            if(CMD[5]==0xff):
                                self.qrcode.lock = True
                                self.qrcode.id = None
                        elif(CMD[2]==0x02 and CMD[3]==QRCODE_MODE and CMD[4]==0x03):
                            _str = str(CMD[-2].decode('UTF-8','ignore'))
                            data = eval(_str)
                            self.qrcode.id = data[0]
                            self.qrcode.info = data[1]
                    else:
                        self.qrcode.id = None
                        self.qrcode.info = None
                except:
                    self.qrcode.id = None
            elif(self.mode==SPEECH_RECOGNIZATION_MODE and self.asr!=None):
                try:
                    if(len(CMD)>0):
                        if(CMD[3]==SPEECH_RECOGNIZATION_MODE and CMD[4]==0x03):
                            if(CMD[5]==0xff):
                                self.asr.lock = True
                                self.asr.result = None
                            else:
                                self.asr.result = int(CMD[5])
                        elif(CMD[2]==0x02):
                            self.asr.result = None
                    else:
                        self.asr.result = None
                except:
                    self.asr.result = None
            elif(self.mode==GUIDEPOST_MODE and self.guidepost!=None):#10
                if(len(CMD)>0):
                    if(CMD[3]==GUIDEPOST_MODE and CMD[4]==0x02):
                        if(CMD[5]==0xff):
                            self.guidepost.lock = True
                            self.guidepost.id,self.guidepost.max_score = None,0
                        else:
                            max_index,self.guidepost.max_score = CMD[5],round(int(CMD[6])/100,2)
                            self.guidepost.id = self.guidepost.labels[max_index]
                    elif(CMD[2]==0x02):
                        pass
                else:
                    self.guidepost.id,self.guidepost.max_score = None,0
            elif(self.mode==KPU_MODEL_MODE and self.kpu_model!=None):
                if(len(CMD)>0):
                    if(CMD[3]==KPU_MODEL_MODE and CMD[4]==0x03):
                        if(CMD[5]==0xff):
                            self.kpu_model.lock = True
                            self.kpu_model.id,self.kpu_model.max_score = None,0
                        else:
                            self.kpu_model.id ,self.kpu_model.max_score = CMD[5],round(int(CMD[6])/100,2)
                    elif(CMD[2]==0x02):
                        pass
                else:
                    self.kpu_model.id ,self.kpu_model.max_score = None,0
            elif(self.mode==TRACK_MODE and self.track!=None):
                if(len(CMD)>0):
                    if(CMD[2]==0x01 and CMD[3]==TRACK_MODE and CMD[4]==0x02 and CMD[5]==0xff):
                        self.track.lock = True
                        self.track.x,self.track.y,self.track.cx,self.track.cy,self.track.w,self.track.h,self.track.pixels,self.track.count,self.track.code = None,None,None,None,None,None,None,None,None
                    elif(CMD[2]==0x02 and CMD[3]==TRACK_MODE and CMD[4]==0x02):
                        self.track.lock = True
                        _str = str(CMD[-2].decode('UTF-8','ignore'))
                        data = _str.split('|')
                        self.track.x,self.track.y,self.track.cx,self.track.cy,self.track.w,self.track.h,self.track.pixels,self.track.count,self.track.code = int(data[0]),int(data[1]),int(data[2]),int(data[3]),int(data[4]),int(data[5]),int(data[6]),int(data[7]),hammingWeight(int(CMD[5]))        
                    else:
                        self.track.x,self.track.y,self.track.cx,self.track.cy,self.track.w,self.track.h,self.track.pixels,self.track.count,self.track.code = None,None,None,None,None,None,None,None,None          
                else:
                    self.track.x,self.track.y,self.track.cx,self.track.cy,self.track.w,self.track.h,self.track.pixels,self.track.count,self.track.code = None,None,None,None,None,None,None,None,None
            elif(self.mode==COLOR_STATISTICS_MODE and self.color_statistics!=None):
                if(len(CMD)>0):
                    if(CMD[2]==0x01 and CMD[3]==AI['color_statistics'][0] and CMD[4]==AI['color_statistics'][2] and CMD[5]==0xff):
                        self.color_statistics.lock = True
                        self.color_statistics.row_data1,self.color_statistics.row_data2,self.color_statistics.row_data3,self.color_statistics.line_get_regression_data = [None,None,None,None,None],[None,None,None,None,None],[None,None,None,None,None],[None,None,None,None,None,None,None,None]
                    elif(CMD[2]==0x02 and CMD[3]==AI['color_statistics'][0] and CMD[4]==AI['color_statistics'][2]):
                        self.color_statistics.lock = True
                        _str = str(CMD[-2].decode('UTF-8','ignore'))
                        data = eval(_str)
                        self.color_statistics.row_data1,self.color_statistics.row_data2,self.color_statistics.row_data3,self.color_statistics.line_get_regression_data = [int(CMD[5]),int(CMD[6]),int(CMD[7]),int(CMD[8]),int(CMD[9])],[int(CMD[10]),int(CMD[11]),int(CMD[12]),int(CMD[13]),int(CMD[14])],[int(CMD[15]),int(CMD[16]),int(CMD[17]),int(CMD[18]),int(CMD[19])],[int(data[0]),int(data[1]),int(data[2]),int(data[3]),int(data[4]),int(data[5]),int(data[6]),int(data[7])]
                    self.color_statistics.data = [self.color_statistics.row_data1,self.color_statistics.row_data2,self.color_statistics.row_data3]
                # else:
                #     self.color_statistics.row_data1,self.color_statistics.row_data2,self.color_statistics.row_data3,self.color_statistics.line_get_regression_data = [None,None,None,None,None],[None,None,None,None,None],[None,None,None,None,None],[None,None,None,None,None,None,None,None]
                #     self.color_statistics.data = [self.color_statistics.row_data1,self.color_statistics.row_data2,self.color_statistics.row_data3]
            elif(self.mode==COLOR_EXTRACTO_MODE and self.color_extracto!=None):
                if(len(CMD)>0):
                    if(CMD[2]==0x01 and CMD[3]==AI['color_extracto'][0] and CMD[4]==AI['color_extracto'][2] and CMD[5]==0xff):
                        self.color_extracto.lock = True
                        self.color_extracto.L,self.color_extracto.A,self.color_extracto.B = None,None,None
                    elif(CMD[2]==0x02 and CMD[3]==AI['color_extracto'][0] and CMD[4]==AI['color_extracto'][2]):
                        _str = str(CMD[-2].decode('UTF-8','ignore'))
                        data = _str.split('|')
                        self.color_extracto.L,self.color_extracto.A,self.color_extracto.B = int(data[0]),int(data[1]),int(data[2])
                    self.color_extracto.LAB_Data = [self.color_extracto.L,self.color_extracto.A,self.color_extracto.B]
                else:
                    self.color_extracto.L,self.color_extracto.A,self.color_extracto.B = None,None,None
                    self.color_extracto.LAB_Data = [self.color_extracto.L,self.color_extracto.A,self.color_extracto.B]
            elif(self.mode==APRILTAG_MODE and self.apriltag!=None):
                # print(CMD)
                if(len(CMD)>0):
                    if(CMD[2]==0x01 and CMD[3]==AI['apriltag'][0] and CMD[4]==AI['apriltag'][2] and CMD[5]==0xff):
                        self.apriltag.lock = True
                        self.apriltag.tag_family,self.apriltag.tag_id = None,None
                    elif(CMD[2]==0x02 and CMD[3]==AI['apriltag'][0] and CMD[4]==AI['apriltag'][2]):
                        self.apriltag.lock = True
                        # _str = str(bytes(CMD[21:-1]).decode('UTF-8','ignore'))
                        _str = str(CMD[-2].decode('UTF-8','ignore'))
                        data = _str.split('|')
                        self.apriltag.tag_family,self.apriltag.tag_id = int(data[0]),int(data[1])
                else:
                    self.apriltag.tag_family,self.apriltag.tag_id = None,None
            elif(self.mode==KPU_YOLO_MODEL_MODE and self.kpu_yolo_model!=None):
                if(len(CMD)>0):
                    if(CMD[3]==KPU_YOLO_MODEL_MODE and CMD[4]==0x03):
                        if(CMD[5]==0xff):
                            self.kpu_yolo_model.lock = True
                            self.kpu_yolo_model.id,self.kpu_yolo_model.max_score = None,0
                        else:
                            self.kpu_yolo_model.id ,self.kpu_yolo_model.max_score = CMD[5],round(int(CMD[6])/100,2)
                    elif(CMD[2]==0x02):
                        pass
                else:
                    self.kpu_yolo_model.id ,self.kpu_yolo_model.max_score = None,0
            elif(self.mode==FACTORY_MODE):
                if(len(CMD)>0):
                    # if(CMD[2]==0x01 and CMD[3]==FACTORY_MODE and CMD[4]==0x01):
                    #     self.a_status,self.b_status,self.tf_status = CMD[5],CMD[6],CMD[7]
                    if(CMD[2]==0x02 and CMD[3]==FACTORY_MODE and CMD[4]==0x01):
                        _str = str(CMD[-2].decode('UTF-8','ignore'))
                        data = eval(_str)
                        self.a_status,self.b_status,self.tf_status = CMD[5],CMD[6],CMD[7]
                        self.tf_sn = data[0]
                else:
                    pass
            else:
                pass
            