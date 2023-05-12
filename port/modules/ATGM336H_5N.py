from machine import UART, Pin
import time

class GPS():
    def __init__(self,uart_num=1, pin_tx=Pin.P14, pin_rx=Pin.P13):
        self.__uart_port = UART(uart_num, baudrate=9600, tx=pin_tx, rx=pin_rx)
        self.GNSS_RX_Buffer = ""
        self.GNSS_Buffer = ""
        self.UTC_Time = ""
        self.latitude = ""
        self.N_S = ""
        self.longitude = ""
        self.E_W = ""
        self.speed_to_groud = ""
        self.speed_to_groud_kh = 0
        self.course_over_ground = ""
        self.date = ""
        self.isDecodeData = False
        self.isParseData = False
        self.DataIsUseful = False # 是否有有效数据信息

    def GNSS_Read(self):
        self.GNSS_RX_Buffer = self.__uart_port.read(1200)
        while type(self.GNSS_RX_Buffer)!=bytes:
            self.GNSS_RX_Buffer = self.__uart_port.read(1200)

        # 由于电路连接不可靠等原因，有时接收到的信息含有非 ASCII 字符，引发 UnicodeError
        # AttributeError 引发原因未知
        while self.isDecodeData==False:
            try:
                self.GNSS_Buffer = self.GNSS_RX_Buffer.decode('ASCII')
                self.isDecodeData = True
            except UnicodeError:
                self.GNSS_RX_Buffer = self.__uart_port.read(1200)
            except AttributeError:
                self.GNSS_RX_Buffer = self.__uart_port.read(1200)

        # 测试模块工作是否正常的代码，实际应用请注释掉以避免输出信息过多
        #print("This is GNSS_RX_Buffer, origin data from uart:")
        #print(self.GNSS_RX_Buffer)
        #print("This is GNSS_Buffer, after decoding:")
        #print(self.GNSS_Buffer)

        # 模块输出的信息很多，为了简便起见我们只选择 RMC 最小定位信息，此部分代码用于从 GNSS_Buffer 中截取 RMC 部分
        GNSS_BufferHead = self.GNSS_Buffer.find("$GPRMC,")
        if GNSS_BufferHead == -1:
            GNSS_BufferHead = self.GNSS_Buffer.find("GNRMC,")
        #print(GNSS_BufferHead)
        if GNSS_BufferHead == -1:
            print("Cannot read the GPS , RMC imformation")
            self.isDecodeData = False
        else:
            GNSS_BufferTail = self.GNSS_Buffer[GNSS_BufferHead:].find("\r\n")
            #print(GNSS_BufferTail)
            if GNSS_BufferTail == -1:
                print("Not end with newline")
                self.isDecodeData = False

            self.GNSS_Buffer=self.GNSS_Buffer[GNSS_BufferHead:GNSS_BufferHead+GNSS_BufferTail]

        # 测试模块工作是否正常的代码，实际应用请注释掉以避免输出信息过多
        # print("This is GNSS_RX_Buffer, origin data from uart:")
        # print(self.GNSS_RX_Buffer)
        # print("This is GNSS_Buffer, including RMC info:")
        # print(self.GNSS_Buffer)

    def GNSS_Parese(self):
        if(self.isDecodeData == True):
            self.isDecodeData= False
            print("*****************************************")

            temp = self.GNSS_Buffer.split(',')

            try:
                # RMC 信息中自带的标识符， A 代表有效， V 代表无效
                if temp[2] == 'A':
                    self.DataIsUseful = True 
                else:
                    self.DataIsUseful = False

                if temp[1] == "":
                    self.UTC_Time = "-1"
                else:
                    self.UTC_Time = temp[1]
                    self.UTC_Time_Beijing = str(int(self.UTC_Time[0:2])+8)+':'+self.UTC_Time[2:4]+':'+self.UTC_Time[4:6]
                    self.UTC_Time = self.UTC_Time[0:2]+':'+self.UTC_Time[2:4]+':'+self.UTC_Time[4:6]

                if temp[3] == "":
                    self.latitude = "-1"
                else:
                    self.latitude = temp[3]
                    self.latitude = self.latitude[0:2]+' degree '+self.latitude[2:]+'\''

                self.N_S = temp[4]

                if temp[5] == "":
                    self.longitude = "-1"
                else:
                    self.longitude = temp[5]
                    #self.longitude = self.longitude[0:3]+'°'+self.latitude[3:]
                    self.longitude = self.longitude[0:3]+' degree '+self.longitude[3:]+'\''

                self.E_W = temp[6]
                
                # RMC 中的速度以节为单位
                if temp[7] != "":
                    try:
                        self.speed_to_groud = float(temp[7])
                        self.speed_to_groud_kh = self.speed_to_groud*1.852
                    except ValueError:
                        pass
                else:
                    self.speed_to_groud = -1
                    self.speed_to_groud_kh = -1

                if temp[8] != "":
                    try:
                        self.course_over_ground = float(temp[8])
                    except ValueError:
                        pass
                else:
                    self.course_over_ground = -1

                if temp[9] == "":
                    self.date = "-1"
                else:
                    self.date = temp[9]
                    self.date = self.date[4:6]+'.'+self.date[2:4]+'.'+self.date[0:2]

                self.isParseData = True
            except IndexError:
                pass

    def print_GNSS_info(self):
        if(self.isParseData):
            self.isParseData = False
            if(self.DataIsUseful):
                print("维度: %s %s",self.latitude,self.N_S)
                print("经度: %s %s",self.longitude,self.E_W)
                print("日期: %s",self.date,end=' ')
                print("UTC时间: %s",self.UTC_Time)
                print("卫星对地速度: %f km/h",self.speed_to_groud_kh)
                # print("course_over_groud: %f°",self.course_over_ground)
            else:
                print(" !")