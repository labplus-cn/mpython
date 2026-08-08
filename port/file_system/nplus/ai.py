#mPythonType:0
from mpython import i2c, sleep_ms, MPythonPin, PinMode
from machine import UART,Pin
import time

'''
小方舟AI类
2021-03-19
'''
class NPLUS_AI(object):
    def __init__(self, uart2_rx0=33, uart2_tx0=32):  
        self.uart = UART(2, baudrate=115200, rx=uart2_rx0,
                         tx=uart2_tx0, timeout=1000)
        self.ai_read_data = [0, 0, 0, 0, 0, 0]  
        self.ai_key_name = []
        self.learn_id_flag=[]
        self.wait_for_power_on()

    
    def AI_Uart_CMD(self, cmd, cmd_data=[0, 0, 0, 0], str_buf=0):
        check_sum = 0
        CMD_TEMP = [0xAA, 0x55, cmd]
        CMD_TEMP.extend(cmd_data)
        for i in range(4-len(cmd_data)):
            CMD_TEMP.append(0)
        for i in range(len(CMD_TEMP)):
            check_sum = check_sum+CMD_TEMP[i]
        #print_x16(CMD_TEMP)
        self.uart.write(bytes(CMD_TEMP))
        if str_buf:
            str_temp = bytes(str_buf, 'utf-8')
            self.uart.write(str_temp)
            for i in range(len(str_temp)):
                check_sum = check_sum + str_temp[i]
            self.uart.write(bytes([(check_sum >> 8) & 0xFF, check_sum & 0xFF]))
        
    
    def print_x16(self,date):
        for i in range(len(date)):
            print('{:2x}'.format(date[i]),end=' ')
        print('')
    
    def AI_WaitForARP(self,cmd,data=[0,0,0,0],str_buf=0): 
        num = 0
        while self.uart.any():
            a = self.uart.read(1)
            num = num+1
            #print(a)
            if num>100:
                break
        self.AI_Uart_CMD(cmd,data,str_buf)
        wait_time = 0
        if cmd&0xF0 == 0x20 or cmd&0x0F > 0x09:
            while (not self.uart.any()):
                wait_time = wait_time+1
                time.sleep_ms(10)
                if wait_time>300:
                    print("UART_NO_ACK_ERR")
                    break
            else:
                res=False
                time.sleep_ms(10)
                TEMP = []
                num = 0
                while 1:
                    num = num+1
                    buf = self.uart.read(1)
                    if buf and buf[0] == 0x55:
                        buf = self.uart.read(1)
                        if buf and buf[0] == 0xAA:
                            TEMP = self.uart.read(7)
                            #self.print_x16(TEMP)
                            break
                    if num>1000:
                        break
                if len(TEMP) > 3:
                    if TEMP[0]==cmd:
                        #self.print_x16(TEMP[2:])
                        res = True
                        self.ai_read_data = list(TEMP[1:]) 
                    elif cmd&0x0F > 0x09:
                        #print("uart_cmd_sent_failed")
                        res = self.AI_WaitForARP(cmd,data,str_buf)
                return res   

    def wait_for_power_on(self): #等待电源启动完成
        while True:
            res=self.uart.read()
            self.AI_Uart_CMD(0x20)
            time.sleep_ms(500)  
            res = self.uart.read(9)
            #self.print_x16(res) 
            if res and res[0]==0x55 and res[1]==0xAA:
                break


    def get_ai_data(self):  
        return self.AI_WaitForARP(0x21)
           
    def get_id_data(self, id):  
        return self.AI_WaitForARP(0x20, [id])
        
    def color_id_data(self,read_id,num):    
        return self.ai_read_data[:4] if self.AI_WaitForARP(0x20,[read_id,num+1,0,0]) else None

    def get_id_color_amount(self):  
        return self.ai_read_data[5]

    def get_class_value(self):    
        return self.ai_read_data[5]

    def get_class_id(self):  
        return self.ai_read_data[4]

    def get_class_value(self):  
        return self.ai_read_data[5]
    
    def get_coord_result(self,coord):  
        if not self.ai_read_data:
            return None
        self.coord_result=[int(self.ai_read_data[0] + self.ai_read_data[2]/2),int(self.ai_read_data[1] + self.ai_read_data[3]/2),self.ai_read_data[2],self.ai_read_data[3]]
        return self.coord_result[coord]
    
    def mode_change(self,mode): 
        self.AI_Uart_CMD(0x10,[mode,0,0,0])

    def learn_from_center(self):  
        self.AI_WaitForARP(0x11)

    def clean_data(self):  
        self.AI_WaitForARP(0X12)

    def get_QR_str(self): #读取识别结果的字符信息
        res = b''
        if self.AI_WaitForARP(0x23,[0,0,0,0]):
            if self.uart.any():
                res = self.uart.read()
        return res.decode('UTF-8','ignore')

    def add_sample_img(self,class_id):
        if not len(self.learn_id_flag):
            raise OSError("请先初始化分类器！")
        if class_id >= len(self.learn_id_flag):
            raise OSError("添加的分类ID超出范围！")
        self.learn_id_flag[class_id] = 1
        self.AI_WaitForARP(0x13,[class_id,0,0,0]) 
        
    def knn_model_train(self): 
        if self.learn_id_flag.count(0):
            raise OSError("分类ID%d未添加样本！"% self.learn_id_flag.index(0))
        self.AI_WaitForARP(0x14,[0,0,0,0])

    def color_parameter_set(self, color_multiple=0, thr_l=0):
        self.AI_WaitForARP(0x15, [color_multiple, thr_l, 0, 0])

    def color_recognize_roi(self, roi):  
        self.AI_WaitForARP(0x16, roi)

    def loading_sd_model(self,mode,model_name,class_name): 
        mode = [mode]
        if model_name.endswith(".kmodel"):
            mode.append(1)
        else:
            mode.append(0)
        self.AI_WaitForARP(0x1A,mode,model_name[0:-7]+':'+class_name)
    
    def load_knn_model(self,class_name): 
        self.learn_id_flag = []
        for i in range(len(class_name.split(','))):
            self.learn_id_flag.append(0)
        self.AI_WaitForARP(0x1B,[0,len(self.learn_id_flag),0,0],class_name)
        
    def save_knn_file(self,name): 
        self.AI_WaitForARP(0x1B,[1,0,0,0],name)
        
    def load_knn_file(self,file_name,class_name): 
        self.AI_WaitForARP(0x1B,[2,len(class_name.split(',')),0,0],file_name+':'+class_name)
        
    def lcd_senser_rotation(self,rotation): 
        self.AI_Uart_CMD(0x31,[rotation,0,0,0])
        
    def lcd_display_color(self,r=0,g=128,b=255): 
        self.AI_Uart_CMD(0x32,[r,g,b,0])
        
    def lcd_display_clear(self): 
        self.AI_Uart_CMD(0x33)
        
    def change_save_sensor(self,camera_num=1):  #OV=1 #GC=2
        self.AI_Uart_CMD(0x34,[camera_num,0,0,0])

    def camera_set_gain(self, auto=1,gain=0x86):  #增加自动增益的切换，auto=0为手动增益（两个摄像头增益数值gain不一样的）
        self.AI_Uart_CMD(0x36, [auto, gain, 0, 0])
        
    def picture_capture(self,mode=0): 
        self.AI_WaitForARP(0x3A,[mode,0,0,0])

    def video_capture(self,time): 
        self.AI_WaitForARP(0x3B,[int(time/2),0,0,0])
    
    def lcd_display_str(self,x,y,str_buf): 
        self.AI_WaitForARP(0x3C,[x,y,0,0],str_buf)
        
    def buzzer_piano_ring(self,pitch,time): 
        self.AI_Uart_CMD(0x45,[pitch,time])
        
    def set_ws2812_rgb(self,num,r,g,b): 
        self.AI_Uart_CMD(0x46,[num,r,g,b])

    def rgb_off(self): 
        self.AI_Uart_CMD(0x46,[0,0,0,0])
        self.AI_Uart_CMD(0x46,[1,0,0,0])
    
    def ram_format(self): 
        self.AI_Uart_CMD(0x39)

    def record_isolated_word(self, asr_id, noise_thr): 
        self.AI_WaitForARP(0x17,[asr_id,asr_thr,0,100])

    def addCommand(self,key_name,num):
        if len(self.ai_key_name) > num:
            self.ai_key_name[num] = key_name
        if len(self.ai_key_name) == num:
            self.ai_key_name.append(key_name)
        if len(self.ai_key_name) < num:
            while len(self.ai_key_name) < num:
                self.ai_key_name.append("pou-jian")
            self.ai_key_name.append(key_name)

    def asr_start(self, asr_thr): #
        str_buf = ",".join(self.ai_key_name)
        print(str_buf)
        self.AI_WaitForARP(0x1C,[asr_thr,0,0,0],str_buf)

    def get_object_name(self):
        name_id = self.ai_read_data[4]
        self.object_name = ['飞机','自行车','鸟','船','瓶子','公共汽车','车','猫','椅子','牛','桌子','狗','马','摩托车','人','盆栽','羊','沙发','火车','屏幕']
        return self.object_name[name_id]