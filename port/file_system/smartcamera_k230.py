from machine import Pin, UART
from lib.k230_ai import *
import time
import gc
from machine import Timer
gc.collect()

class SmartCameraK230:
    def __init__(self, tx=Pin.P1, rx=Pin.P0):
        self.uart = UART(2, baudrate=1152000, rx=rx, tx=tx, rxbuf=1024)
        # self.uart = UART(2, baudrate=1152000, tx=tx, rx=rx)
        self.mode = DEFAULT_MODE
        self.lock = False
        self.slc_parameter = [3, 15, 11, 1]
        self.a_status = 0
        self.b_status = 0
        self.tf_status = 0
        self.tf_sn = ''
        self.rx_buffer = bytearray()

        time.sleep(0.01)
        self.wait_for_ai_init()
        self.tim9 = Timer(-1)
        self.tim9.init(period=50, mode=Timer.PERIODIC, callback=self.timer9_tick)
        # self.thread_listen()
  
    def wait_for_ai_init(self): 
        self.lock = True
        num = 0
        rx_buffer = bytearray()  # 接收缓冲区
        
        while True:
            gc.collect()
            num += 1
            
            if num > 200:
                print('错误:通信超时，请检查接线情况及掌控拓展电源是否打开！')
                print('Error: Communication timeout, please check the wiring and control whether the expansion power is turned on!')
                break
                
            # 发送初始化命令
            AI_Uart_CMD(self.uart, 0x01, 0xFF)
            time.sleep_ms(100)
            
            # 读取可用数据到缓冲区
            if self.uart.any():
                new_data = self.uart.read()
                if new_data:
                    rx_buffer.extend(new_data)
            
            # 处理缓冲区中的数据包
            while len(rx_buffer) >= 2:
                # 查找包头 0xBB 0xAA
                packet_start = -1
                for i in range(len(rx_buffer) - 1):
                    if rx_buffer[i] == 0xBB and rx_buffer[i + 1] == 0xAA:
                        packet_start = i
                        break
                
                if packet_start == -1:
                    # 没有找到包头，清除无效数据
                    rx_buffer = bytearray()
                    break
                
                # 移除包头前的无效数据
                if packet_start > 0:
                    rx_buffer = rx_buffer[packet_start:]
                
                # 检查是否有足够的数据来解析命令类型
                if len(rx_buffer) < 3:
                    break
                
                cmd_type = rx_buffer[2]
                
                # 处理 0x01 类型命令（固定长度包）
                if cmd_type == 0x01:
                    # 0x01 包总长度：2(包头) + 1(命令类型) + 9(数据) = 12字节
                    if len(rx_buffer) < 12:
                        break
                    
                    # 提取完整的数据包
                    packet = rx_buffer[:12]
                    
                    # 验证校验和
                    checksum = 0
                    for i in range(11):  # 前11字节的校验和
                        checksum += packet[i]
                    checksum &= 0xFF
                    
                    if checksum == packet[11]:  # 校验成功
                        # 检查是否是期望的初始化响应
                        if packet[3] == 0x01 and packet[4] == 0xFF:
                            print("AI摄像头4.0初始化完成")
                            print("AI camera 4.0 init end")
                            time.sleep(0.1)
                            # 清空缓冲区中的剩余数据
                            rx_buffer = self.uart.read()
                            del rx_buffer
                            gc.collect()
                            self.lock = False
                            return
                        else:
                            # 不是期望的响应，移除这个包继续处理
                            rx_buffer = rx_buffer[12:]
                    else:
                        # 校验失败，移除第一个字节继续查找
                        rx_buffer = rx_buffer[1:]
                
                # 不处理 0x02 类型命令，直接跳过
                elif cmd_type == 0x02:
                    # 跳过 0x02 包，移除第一个字节继续查找
                    rx_buffer = rx_buffer[1:]
                
                else:
                    # 未知命令类型，移除第一个字节继续查找
                    rx_buffer = rx_buffer[1:]
            
            # 防止缓冲区过大
            if len(rx_buffer) > MAX_BUF_SIZE:
                print("警告: 接收缓冲区过大，清空缓冲区")
                rx_buffer = bytearray()
                gc.collect()
    
    def model_init(self,cur_state):
        if(self.mode == cur_state):
            print('模式相同,无需切换')
            time.sleep_ms(0.1)
            return
        elif(cur_state==DEFAULT_MODE):
            for i in range(5):
                AI_Uart_CMD(self.uart,DEFAULT_MODE,0x01)
                time.sleep_ms(100) 
        elif(cur_state==FACE_REG_PLUS_MODE):
            AI_Uart_CMD(self.uart,FACE_REG_PLUS_MODE,0x01)
        elif(cur_state==FACE_DETECTION_MODE):
            self.face_detect = FACE_DETECT(self.uart)
        elif(cur_state==HAND_DETECTION):
            self.hand_detect = HandDetect(self.uart)
        elif(cur_state==HAND_KEYPOINT_CLASS):
            self.hand_keypoint_class = HandKeypointClass(self.uart)
        elif(cur_state==DYNAMIC_GESTURE):
            self.dynamic_gesture = DG(self.uart)
        elif(cur_state==LICENSE_PLATE_RECOGNITION):
            self.lpr = LPR(self.uart)
        elif(cur_state==PERSON_DETECTION):
            self.person_detect = PersonDetect(self.uart)
        elif(cur_state==PERSON_KEYPOINT_DETECT):
            self.person_keypoint_detect = PersonKeypointDetct(self.uart)
        elif(cur_state==PERSON_KEYPOINT_DETECT_PLUS):
            self.person_keypoint_detect_plus = PersonKeypointDetctPlus(self.uart)
        elif(cur_state==FACE_LANDMARK_LIVING_BODY):
            self.face_living_body = FaceLivingBodyDetct(self.uart)
        elif(cur_state==FACE_LANDMARK_EXPRESSION):
            self.face_expression = FaceExpressionDetct(self.uart)
        elif(cur_state==OBJECT_RECOGNIZATION_MODE):
            self.yolo_detect = YOLO80(self.uart)
        elif(cur_state==FALL_DETECTION):
            self.fall = FallDetection(self.uart)
        elif(cur_state==QRCODE_MODE):
            self.qrcode = QRCodeRecognization(self.uart)
        elif(cur_state==BARCODE_MODE):
            self.bar_code = BarCodeRecognization(self.uart)
        elif(cur_state==FACE_RECOGNITION_MODE):
            self.fcr = FaceRecogization(self.uart)
        elif(cur_state==APS_MODE):
            self.amr = AMR(self.uart)
        elif(cur_state==APRILTAG_DETECT_MODE):
            self.apriltag = APRILTAG_DETECT(self.uart)
        
        self.mode = cur_state
    
    def switcher_mode(self, mode):
        self.model_init(mode) # mode-0默认 1人脸检测 2目标识别 3手势检测 4手势分类 5车牌识别 6人体检测 7跌倒检测 8二维码识别 9条码识别 10人脸识别 36道路自动驾驶系统

    def color_obj_count_init(self,cur_mode):
        self.color_obj_count = ColorCount(self.uart, cur_mode=cur_mode)
        self.mode = COLOR_OBJECT_COUNT_MODE
    
    def lab_color_count_init(self,color):
        self.lab_color_count = LABColorCount(self.uart, color=color)
        self.mode = LAB_COLOR_OBJECT_COUNT_MODE

    def classify_kmodel_init(self, param={"kmodel_path":'/data/xxx.kmodel', "labels":["0","1","2"], "confidence_threshold":0.3, "nms_threshold":0.45, "max_boxes_num":50}):
        self.classify_model = ClassifyMODEL(self.uart, param)
        self.classify_model.results = []
        self.mode = CLASSIFY_MODEL_MODE
    
    def detect_kmodel_init(self, param={"kmodel_path":'/data/xxx.kmodel', "labels":["0","1","2"], "confidence_threshold":0.3, "nms_threshold":0.45, "max_boxes_num":50}):
        self.detect_kmodel = DetectMODEL(self.uart, param)
        self.detect_kmodel.results = []
        self.mode = DETECT_MODEL_MODE
    
    def linear_regression_fast_init(self, threshold=(0,100)):
        self.linear_regression_fast = LINEAR_REGRESSION(self.uart,threshold=threshold)
        self.mode = LINEAR_REGRESSION_MODE 
    
    def linear_regression_fast_v3_init(self, line_color="black", detect_intersections=True, detect_zebra=True):
        self.linear_regression_fast_v3 = LINEAR_V3_REGRESSION(self.uart, line_color=line_color, detect_intersections=detect_intersections, detect_zebra=detect_zebra)
        self.mode = LINEAR_REGRESSION_V3_MODE 
    
    # def led(self,mode=0):
    #     AI_Uart_CMD(self.uart, 0x01, 0xFA, [0x04,int(mode)])
    #     time.sleep_ms(20)

    def thread_listen(self):
        self._task = TASK(func=self.uart_thread,sec=0.05)
        self._task.start()
    
    def timer9_tick(self,_):
        self.uart_thread()

    def uart_thread(self): 
        gc.collect()
        try:          
            if(self.lock==False):
                CMD = uart_handle(self.uart)
                # print(CMD)
                # print('=====CMD=====')
                if(CMD==None or len(CMD)==0):
                    return

                if(self.mode==DEFAULT_MODE):
                    pass
                elif(self.mode==OBJECT_RECOGNIZATION_MODE and self.yolo_detect!=None):
                    if(len(CMD)>0):
                        if(CMD[3]==OBJECT_RECOGNIZATION_MODE and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.yolo_detect.lock = True
                                self.yolo_detect.id,self.yolo_detect.max_score,self.yolo_detect.objnum = None,0,0
                                self.yolo_detect.category_name = None
                            else:
                                self.yolo_detect.id,self.yolo_detect.max_score,self.yolo_detect.objnum = CMD[5],round(int(CMD[6])/100,2),CMD[7]
                                self.yolo_detect.category_name = self.yolo_detect.category_list[self.yolo_detect.id]
                elif(self.mode==FACE_DETECTION_MODE and self.face_detect!=None):
                    if(len(CMD)>0):
                        if(CMD[2]==0x01 and CMD[3]==FACE_DETECTION_MODE and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.face_detect.lock = True
                                self.face_detect.face_num = None
                            else:
                                self.face_detect.lock = True
                                self.face_detect.face_num = CMD[5]
                        elif(CMD[2]==0x02 and CMD[3]==FACE_DETECTION_MODE and CMD[4]==0x01):
                            b = bytes(CMD[22:-1])  
                            data = json.loads(b.decode('UTF-8','ignore'))
                            self.face_detect.lock = True
                            self.face_detect.face_num = data.get('num',None)
                            self.face_detect.coord_list = data.get('coord_list',[])
                elif(self.mode==HAND_DETECTION and self.hand_detect!=None):
                    if(len(CMD)>0):
                        if(CMD[2]==0x01 and CMD[3]==HAND_DETECTION and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.hand_detect.lock = True
                                self.hand_detect.flag = False
                                self.hand_detect.hand_num = 0
                            elif(CMD[5]==0xee):
                                self.hand_detect.lock = True
                                self.hand_detect.flag = True
                                self.hand_detect.hand_num = CMD[6]
                        elif(CMD[2]==0x02 and CMD[3]==HAND_DETECTION and CMD[4]==0x01):
                            b = bytes(CMD[22:-1])  
                            data = json.loads(b.decode('UTF-8','ignore'))
                            self.hand_detect.lock = True
                            self.hand_detect.flag = True
                            self.hand_detect.hand_num = data.get('num',None)
                            self.hand_detect.coord_list = data.get('coord_list',[])
                        
                elif(self.mode==HAND_KEYPOINT_CLASS and self.hand_keypoint_class!=None):
                    if(len(CMD)>0):
                        if(CMD[3]==HAND_KEYPOINT_CLASS and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.hand_keypoint_class.lock = True
                                self.hand_keypoint_class.gesture_id = None
                                self.hand_keypoint_class.gesture_str = None
                            else:
                                self.hand_keypoint_class.gesture_id = CMD[5]
                                self.hand_keypoint_class.gesture_str = HAND_KEYPOINT_CLASS_GESTURE[CMD[5]]
                elif(self.mode==DYNAMIC_GESTURE and self.dynamic_gesture!=None):
                    if(len(CMD)>0):
                        if(CMD[3]==DYNAMIC_GESTURE and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.dynamic_gesture.lock = True
                                self.dynamic_gesture.gesture_id,self.dynamic_gesture.gesture_str = None,None
                            else:
                                self.dynamic_gesture.gesture_id = CMD[5]
                                self.dynamic_gesture.gesture_str = DYNAMIC_GESTURE_STR[CMD[5]]
                elif(self.mode==PERSON_DETECTION and self.person_detect!=None):
                    if(len(CMD)>0):
                        if(CMD[2]==0x01 and CMD[3]==PERSON_DETECTION and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.person_detect.lock = True
                                self.person_detect.flag = False
                                self.person_detect.person_num = 0 
                            elif(CMD[5]==0xee):
                                self.person_detect.lock = True
                                self.person_detect.flag = True
                                self.person_detect.person_num = CMD[6]
                        elif(CMD[2]==0x02 and CMD[3]==PERSON_DETECTION and CMD[4]==0x01):
                            b = bytes(CMD[22:-1])  
                            data = json.loads(b.decode('UTF-8','ignore'))
                            self.person_detect.lock = True
                            self.person_detect.person_num = data.get('num',None)
                            self.person_detect.coord_list = data.get('coord_list',[])
                            if (self.person_detect.person_num > 0):
                                self.person_detect.flag = True
                elif(self.mode==PERSON_KEYPOINT_DETECT and self.person_keypoint_detect!=None):
                    if(len(CMD)>0):
                        if(CMD[2]==0x01 and CMD[3]==PERSON_KEYPOINT_DETECT and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.person_keypoint_detect.lock = True
                                self.person_keypoint_detect.keypoints = []
                        elif(CMD[2]==0x02 and CMD[3]==PERSON_KEYPOINT_DETECT and CMD[4]==0x01):
                            b = bytes(CMD[22:-1])  
                            data = json.loads(b.decode('UTF-8','ignore'))
                            self.person_keypoint_detect.lock = True
                            self.person_keypoint_detect.keypoints = data.get('keypoints',[])
                elif(self.mode==PERSON_KEYPOINT_DETECT_PLUS and self.person_keypoint_detect_plus!=None):
                    if(len(CMD)>0):
                        if(CMD[3]==PERSON_KEYPOINT_DETECT_PLUS and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.person_keypoint_detect_plus.id = None
                            else:
                                self.person_keypoint_detect_plus.id = CMD[5]
                elif(self.mode==FACE_LANDMARK_LIVING_BODY and self.face_living_body!=None):
                    if(len(CMD)>0):
                        if(CMD[3]==FACE_LANDMARK_LIVING_BODY and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.face_living_body.lock = True
                                self.face_living_body.mouth_blink_counter = [0,0]
                            else:
                                self.face_living_body.lock = True
                                self.face_living_body.mouth_blink_counter = CMD[5],CMD[6]
                elif(self.mode==FACE_LANDMARK_EXPRESSION and self.face_expression!=None):
                    if(len(CMD)>0):
                        if(CMD[3]==FACE_LANDMARK_EXPRESSION and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.face_expression.lock = True
                                self.face_expression.expression = None
                                self.face_expression.expression_str = None
                            else:
                                self.face_expression.lock = True
                                self.face_expression.expression = CMD[5]
                                self.face_expression.expression_str = FACE_LANDMARK_EXPRESSION_ZH[CMD[5]]
                elif(self.mode==FALL_DETECTION and self.fall!=None):
                    if(len(CMD)>0):
                        if(CMD[3]==FALL_DETECTION and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.fall.lock = True
                                self.fall.id = None
                            else:
                                self.fall.lock = True
                                self.fall.id = CMD[5]
                elif(self.mode==FACE_RECOGNITION_MODE and self.fcr!=None):
                    if(len(CMD)>0):
                        if(CMD[3]==FACE_RECOGNITION_MODE and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.fcr.lock = True
                                self.fcr.id,self.fcr.score = None,None
                            elif(CMD[5]==0xfe):
                                self.fcr.lock = True
                                self.fcr.id,self.fcr.score = -1,0
                            else:
                                self.fcr.lock = True
                                self.fcr.id,self.fcr.score = CMD[5],round(int(CMD[6])/100,3)
                elif(self.mode==COLOR_OBJECT_COUNT_MODE and self.color_obj_count!=None):
                    if(len(CMD)>0):
                        if(CMD[3]==COLOR_OBJECT_COUNT_MODE and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.color_obj_count.lock = True
                                self.color_obj_count.color_count = None
                            else:
                                self.color_obj_count.lock = True
                                self.color_obj_count.color_count = CMD[5]
                elif(self.mode==LAB_COLOR_OBJECT_COUNT_MODE and self.lab_color_count!=None):
                    if(len(CMD)>0):
                        if(CMD[2]==0x01 and CMD[3]==LAB_COLOR_OBJECT_COUNT_MODE and CMD[4]==0x01):
                            if(CMD[5]==0xff):
                                self.lab_color_count.lock = True
                                self.lab_color_count.flag = False
                                self.lab_color_count.color_count = None
                            elif(CMD[5]==0):
                                self.lab_color_count.lock = True
                                self.lab_color_count.flag = False
                                self.lab_color_count.color_count = None
                            else:
                                self.lab_color_count.lock = True
                                self.lab_color_count.flag = True
                                self.lab_color_count.color_count = CMD[5]
                        elif(CMD[2]==0x02 and CMD[3]==LAB_COLOR_OBJECT_COUNT_MODE and CMD[4]==0x01):
                            b = bytes(CMD[22:-1])  
                            _str = str(b.decode('UTF-8','ignore'))
                            data = eval(_str)
                            if(sum(data)==0):
                                self.lab_color_count.lock = True
                                self.lab_color_count.flag = False
                                self.lab_color_count.color_count = None
                            else:
                                self.lab_color_count.lock = True
                                self.lab_color_count.flag = True
                                self.lab_color_count.color_count = data
                elif(self.mode==QRCODE_MODE and self.qrcode!=None):
                    try:
                        if(len(CMD)>0):
                            if(CMD[2]==0x01 and CMD[3]==QRCODE_MODE and CMD[4]==0x01):
                                if(CMD[5]==0xff):
                                    self.qrcode.lock = True
                                    self.qrcode.info = None
                            elif(CMD[2]==0x02 and CMD[3]==QRCODE_MODE and CMD[4]==0x01):
                                b = bytes(CMD[22:-1])  
                                _str = str(b.decode('UTF-8','ignore'))
                                # data = eval(_str)
                                self.qrcode.lock = True
                                self.qrcode.info = _str
                        else:
                            self.qrcode.info = None
                    except:
                        self.qrcode.info = None
                elif(self.mode==LICENSE_PLATE_RECOGNITION):
                    if(len(CMD)>0):
                        if(CMD[2]==0x02 and CMD[3]==LICENSE_PLATE_RECOGNITION and CMD[4]==0x01):
                            # _str = str(CMD[-2].decode('UTF-8','ignore'))
                            b = bytes(CMD[22:-1])  
                            _str = str(b.decode('UTF-8','ignore'))
                            self.lpr.lpr_str = _str
                            self.lpr.lock = True
                        elif(CMD[2]==0x01 and CMD[3]==LICENSE_PLATE_RECOGNITION and CMD[4]==0x01):
                            self.lpr.lpr_str = None
                            self.lpr.lock = True
                elif(self.mode==BARCODE_MODE):
                    if(len(CMD)>0):
                        if(CMD[2]==0x02 and CMD[3]==BARCODE_MODE and CMD[4]==0x01):
                            # _str = str(CMD[-2].decode('UTF-8','ignore'))
                            b = bytes(CMD[22:-1])  
                            _str = str(b.decode('UTF-8','ignore'))
                            data = eval(_str)
                            self.bar_code.type = data[0]
                            self.bar_code.info = data[1]
                            self.bar_code.lock = True
                        elif(CMD[2]==0x01 and CMD[3]==BARCODE_MODE and CMD[4]==0x01):
                            self.bar_code.type = None
                            self.bar_code.info = None
                            self.bar_code.lock = True
                elif(self.mode==LINEAR_REGRESSION_MODE and self.linear_regression_fast!=None):
                    if(len(CMD)>0):
                        if(CMD[2]==0x02 and CMD[3]==LINEAR_REGRESSION_MODE and CMD[4]==0x01):
                            b = bytes(CMD[22:-1])  
                            data = json.loads(b.decode('UTF-8','ignore'))
                            self.linear_regression_fast.line = data
                            self.linear_regression_fast.lock = True
                        elif(CMD[2]==0x01 and CMD[3]==LINEAR_REGRESSION_MODE and CMD[4]==0x01 and CMD[5]==0xff):
                            self.linear_regression_fast.line = {"x1":None, "y1":None, "x2":None, "y2":None, "length":None, "magnitude":None, "theta":None, "rho":None}
                            self.linear_regression_fast.lock = True
                elif(self.mode==LINEAR_REGRESSION_V3_MODE and self.linear_regression_fast_v3!=None):
                    if(len(CMD)>0):
                        if(CMD[2]==0x02 and CMD[3]==LINEAR_REGRESSION_V3_MODE and CMD[4]==0x01):
                            b = bytes(CMD[22:-1])  
                            data = json.loads(b.decode('UTF-8','ignore'))
                            self.linear_regression_fast_v3.data = data
                            self.linear_regression_fast_v3.lock = True
                            self.linear_regression_fast_v3.sleep_time_ms = 5
                        elif(CMD[2]==0x01 and CMD[3]==LINEAR_REGRESSION_V3_MODE and CMD[4]==0x01 and CMD[5]==0xff):
                            # self.linear_regression_fast_v3.data = {"cx": None, "cy": None, "angle": None, "is_int": False, "is_zebra": False}
                            self.linear_regression_fast_v3.lock = True
                            self.linear_regression_fast_v3.sleep_time_ms = 5
                elif(self.mode==CLASSIFY_MODEL_MODE and self.classify_model!=None):
                    if(len(CMD)>0):
                        if(CMD[2]==0x01 and CMD[3]==CLASSIFY_MODEL_MODE and CMD[4]==0x01 and CMD[5]==0xff):
                            self.classify_model.lock = True
                            self.classify_model.result = {"id": None, "score": 0, "results": []}
                            self.classify_model.results = []
                            self.classify_model.id,self.classify_model.score = None,0
                        elif(CMD[2]==0x02 and CMD[3]==CLASSIFY_MODEL_MODE and CMD[4]==0x01):
                            self.classify_model.lock = True
                            b = bytes(CMD[22:-1])  
                            data = json.loads(b.decode('UTF-8','ignore'))
                            self.classify_model.result = data
                            self.classify_model.results = data.get('results', [])
                            self.classify_model.id = data.get('id', None)
                            self.classify_model.score = data.get('score', 0)
                            # self.classify_model.num = data.get('num', 0)
                    else:
                        self.classify_model.result = {"id": None, "score": 0, "results": []}
                        self.classify_model.results = []
                        self.classify_model.id,self.classify_model.score = None,0
                elif(self.mode==DETECT_MODEL_MODE and self.detect_kmodel!=None):
                    if(len(CMD)>0):
                        if(CMD[2]==0x01 and CMD[3]==DETECT_MODEL_MODE and CMD[4]==0x01 and CMD[5]==0xff):
                            self.detect_kmodel.lock = True
                            self.detect_kmodel.result = {"id": None, "score": 0, "num": 0, "results": []}
                            self.detect_kmodel.results = []
                            self.detect_kmodel.id,self.detect_kmodel.score,self.detect_kmodel.num = None,0,0
                        elif(CMD[2]==0x02 and CMD[3]==DETECT_MODEL_MODE and CMD[4]==0x01):
                            self.detect_kmodel.lock = True
                            b = bytes(CMD[22:-1])  
                            data = json.loads(b.decode('UTF-8','ignore'))
                            self.detect_kmodel.result = data
                            self.detect_kmodel.results = data.get('results', [])
                            self.detect_kmodel.id = data.get('id', None)
                            self.detect_kmodel.score = data.get('score', 0)
                            self.detect_kmodel.num = data.get('num', 0)
                    else:
                        self.detect_kmodel.result = {"id": None, "score": 0, "num": 0, "results": []}
                        self.detect_kmodel.results = []
                        self.detect_kmodel.id,self.detect_kmodel.score,self.detect_kmodel.num = None,0,0
                elif(self.mode==APS_MODE and self.amr!=None):
                    if(len(CMD)>0):
                        if(CMD[2]==0x02 and CMD[3]==APS_MODE and CMD[4]==0x01):
                            b = bytes(CMD[22:-1])  
                            data = json.loads(b.decode('UTF-8','ignore'))
                            self.amr.lock = True
                            self.amr.res = data
                elif(self.mode==APRILTAG_DETECT_MODE and self.apriltag!=None):
                    if(len(CMD)>0):
                        if(CMD[2]==0x01 and CMD[3]==APRILTAG_DETECT_MODE and CMD[4]==0x01 and CMD[5]==0xff):
                            self.apriltag.lock = True
                            self.apriltag.tag_family,self.apriltag.tag_id = None,None
                        elif(CMD[2]==0x02 and CMD[3]==APRILTAG_DETECT_MODE and CMD[4]==0x01):
                            self.apriltag.lock = True
                            b = bytes(CMD[22:-1])  
                            self.apriltag.data = json.loads(b.decode('UTF-8','ignore'))
                            self.apriltag.tag_family = self.apriltag.data.get('family', None)
                            self.apriltag.tag_id = self.apriltag.data.get('id', None)
                else:
                    gc.collect()
                    pass
        except Exception as e:
            print(e)
