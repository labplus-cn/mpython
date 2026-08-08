from mpython import i2c, sleep_ms, MPythonPin, PinMode
from machine import UART,Pin
import parrot
import time

class CHOLLIMA(object):

    def __init__(self,i2c=i2c, uart2_rx0=33, uart2_tx0=32):
        self.i2c=i2c
        self.I2C_ADR=0x10
        self.I2C_ADR2=0x39
        self.buf1=bytes(1)
        self.buf4=bytes(2)
        self.threshold=100
        self.wb_rgb = [1,1.7,2]
        self.colorsenser()
        self.i2c.writeto_mem(0x10, 3, b'\x00')
        self.uart = UART(2, baudrate=115200, rx=uart2_rx0,
                        tx=uart2_tx0, timeout=1000)
        self.ai_read_data = [0, 0, 0, 0, 0, 0] 
        self.ai_key_name = []
        self.wait_for_power_on()

    def light_switch(self,switch):
        self.i2c.writeto_mem(0x10, 3, bytearray([switch]))

    def forward(self,speed=100):
        if speed<0:
            speed=0-speed
        parrot.set_speed(parrot.MOTOR_1, speed)   
        parrot.set_speed(parrot.MOTOR_2, speed)

    def backward(self,speed=-100):
        if speed>0:
            speed=0-speed
        parrot.set_speed(parrot.MOTOR_1, speed)
        parrot.set_speed(parrot.MOTOR_2, speed)

    def turn_l(self,r_speed=100,l_speed=0,):
        parrot.set_speed(parrot.MOTOR_1, l_speed)   
        parrot.set_speed(parrot.MOTOR_2, r_speed)

    def turn_r(self,l_speed=100,r_speed=0):
        parrot.set_speed(parrot.MOTOR_1, l_speed)   
        parrot.set_speed(parrot.MOTOR_2, r_speed)

    def stop(self):
        parrot.set_speed(parrot.MOTOR_1, 0)
        parrot.set_speed(parrot.MOTOR_2, 0)

    def set_motor_speed(self,l_speed,r_speed):
        parrot.set_speed(parrot.MOTOR_2, l_speed)
        parrot.set_speed(parrot.MOTOR_1, r_speed)
    
    def read_sensor(self,num):
        self.i2c.writeto(self.I2C_ADR, bytearray([33+num]))
        return self.i2c.readfrom(self.I2C_ADR,1)[0]

    def set_line_threshold(self,data=100):
        self.threshold = data
        
    def touch_line(self,num):
        if self.read_sensor(num)>self.threshold: 
            return True
        else:
            return False

    def colorsenser(self):
        self.i2c.writeto_mem(self.I2C_ADR2, 0x80, b'\x03')
        time.sleep_ms(10)
        self.i2c.writeto_mem(self.I2C_ADR2, 0x81, b'\xD5')
        self.i2c.writeto_mem(self.I2C_ADR2, 0x8F, b'\x01')
        self.light_switch(0)
    
    def setbw_rgb(self,r,g,b):
        self.wb_rgb = [r,g,b]

    def getRGB(self):
        color = [0, 0, 0]
        buf=self.i2c.readfrom_mem(self.I2C_ADR2, 0x96, 6)
        color_r=buf[1]*256 +buf[0]
        color_g=buf[3]*256 +buf[2]
        color_b=buf[5]*256 +buf[4]
        color_r=int(color_r/self.wb_rgb[0])
        color_g=int(color_g/self.wb_rgb[1])
        color_b=int(color_b/self.wb_rgb[2])
        maxColor = max(color_r, color_g, color_b)
        if maxColor > 255:
            scale = 255 / maxColor
            color_r = int(color_r * scale)
            color_g = int(color_g * scale)
            color_b = int(color_b * scale)
        return (color_r,color_g,color_b)

    def getHSV(self):
        rgb = self.getRGB()
        r, g, b = rgb[0], rgb[1], rgb[2]
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df / mx
        v = mx
        return round(h, 1), round(s, 1), round(v, 1)
    
    def discern(self):
        hsv=self.getHSV()
        if 0<=hsv[1]<=0.3:
            return 'none'
        elif 0<=hsv[0]<=6 or 340<=hsv[0]<=360:
            return 'red'
        elif 6<=hsv[0]<=25:
            return 'orange'
        elif 25<=hsv[0]<=70:
            return 'yellow'
        elif 70<=hsv[0]<=150:
            return 'green'
        elif 150<=hsv[0]<=180:
            return 'cyan'
        elif 180<=hsv[0]<=250:
            return 'blue'
        elif 250<=hsv[0]<=340:
            return 'purple'
        else:
            return 'null'

    def discern_red(self):
        if self.discern()=='red':
            return True
        else:
            return False

    def discern_orange(self):
        if self.discern()=='orange':
            return True
        else:
            return False

    def discern_yellow(self):
        if self.discern()=='yellow':
            return True
        else:
            return False

    def discern_green(self):
        if self.discern()=='green':
            return True
        else:
            return False

    def discern_cyan(self):
        if self.discern()=='cyan':
            return True
        else:
            return False

    def discern_blue(self):
        if self.discern()=='blue':
            return True
        else:
            return False

    def discern_purple(self):
        if self.discern()=='purple':
            return True
        else:
            return False

    def distance(self):
        self.i2c.writeto(0x13, b'\x20')
        buf = self.i2c.readfrom(0x13,2)
        distance_mm = (buf[0]*256+buf[1])        
        return distance_mm

#头灯        
    def set_ws2812_rgb(self,num,r,g,b):
        i2c.writeto(0x13, (bytearray([num+4,r,g,b])), True)
        
    def read_battery_voltage(self):
        self.i2c.writeto(0x10, b'\x25')
        buf = self.i2c.readfrom(0x10, 2)
        battery_voltage = (buf[0]*256+buf[1])
        return battery_voltage
        
    def get_motor_l_encoder(self):
        self.i2c.writeto(0x10, b'\x27')
        buf = self.i2c.readfrom(0x10,2)
        motor_encoder = (buf[0]*256+buf[1])
        return motor_encoder
        
    def get_motor_r_encoder(self):
        self.i2c.writeto(0x10, b'\x26')
        buf = self.i2c.readfrom(0x10,2)
        motor_encoder = (buf[0]*256+buf[1])
        return motor_encoder
    
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
                        self.ai_read_data = list(TEMP[1:]) #起始x,y,w,h
                    elif cmd&0x0F > 0x09:
                        #print("uart_cmd_sent_failed")
                        res = self.AI_WaitForARP(cmd,data,str_buf)
                return res   #返回False代表无识别数据#

    def wait_for_power_on(self): #等待电源启动完成
        while True:
            a=self.uart.read()
            self.AI_Uart_CMD(0x20)
            time.sleep_ms(500)  
            if self.uart.read(1)==b'\x55' and self.uart.read(1)==b'\xAA':
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

    def add_sample_img(self,class_id):
        self.AI_WaitForARP(0x13,[class_id,0,0,0]) 
        
    def knn_model_train(self): 
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
        self.AI_WaitForARP(0x1B,[0,len(class_name.split(',')),0,0],class_name)
        
    def save_knn_file(self,name): 
        self.AI_WaitForARP(0x1B,[1,0,0,0],name)
        
    def load_knn_file(self,file_name,class_name): 
        self.AI_WaitForARP(0x1B,[2,len(class_name.split(',')),0,0],file_name+':'+class_name)
        

    def lcd_rotation(self,rotation): 
        self.AI_Uart_CMD(0x30,[rotation,0,0,0])
        
    def lcd_display_color(self,r=0,g=128,b=255): 
        self.AI_Uart_CMD(0x32,[r,g,b,0])
        
    def lcd_display_clear(self): 
        self.AI_Uart_CMD(0x33)

    def camera_set_gain(self, gain):  
        self.AI_Uart_CMD(0x36, [gain, 0, 0, 0])
        
    def picture_capture(self,mode=0): 
        self.AI_WaitForARP(0x3A,[mode,0,0,0])

    def video_capture(self,time): 
        self.AI_WaitForARP(0x3B,[int(time/2),0,0,0])
    
    def lcd_display_str(self,x,y,str_buf): 
        self.AI_WaitForARP(0x3C,[x,y,0,0],str_buf)
        
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

    def asr_start(self, asr_thr): 
        str_buf = ",".join(self.ai_key_name)
        print(str_buf)
        self.AI_WaitForARP(0x1C,[asr_thr,0,0,0],str_buf)

    def get_object_name(self):
        name_id = self.ai_read_data[4]
        self.object_name = ['飞机','自行车','鸟','船','瓶子','公共汽车','车','猫','椅子','牛','桌子','狗','马','摩托车','人','盆栽','羊','沙发','火车','屏幕']
        return self.object_name[name_id]

    def set_motor_l(self,l_speed):
        parrot.set_speed(parrot.MOTOR_2, l_speed)

    def set_motor_r(self,r_speed):
        parrot.set_speed(parrot.MOTOR_1, r_speed)

    def motor_circle_l(self,speed,circle,threshold):
        buf = self.get_motor_l_encoder()
        while abs(buf - self.get_motor_l_encoder()) < threshold*circle:
            self.set_motor_l(speed)
        self.set_motor_l(0)
        
    def motor_circle_r(self,speed,circle,threshold):
        buf = self.get_motor_r_encoder()
        while abs(buf - self.get_motor_r_encoder()) < threshold*circle:
            self.set_motor_r(speed)
        self.set_motor_r(0)
