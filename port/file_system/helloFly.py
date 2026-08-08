

#from mySerial import vcp
from math import sqrt
from time import sleep,time
from struct import pack, unpack
from random import randint
#from myVoice import textToSpeed
from _thread import start_new_thread

from machine import UART,Pin

'''
修改print显示字体颜色

值	描述
0	默认值
1	加粗
22	非粗体
4	下划线
24	非下划线
5	闪烁
25	非闪烁
7	反显
27	非反显

前景色	背景色	描述
30	    40	    黑色
31	    41	    红色
32	    42	    绿色
33	    43	    黄色
34	    44	    蓝色
35	    45	    洋红
36	    46	    青色
37	    47	    白色

'''

def pyLink_pack(fun,buff):

    pack_data = bytearray([0xBB,0x00,fun])#包头
    pack_data.extend(buff)#数据包
    pack_data[1] = len(pack_data)-2;#有效数据个数

    sum = 0
    for temp in pack_data:
        sum = sum + temp

    pack_data.extend(pack('<B', sum%256))#和校验
    
    return pack_data

#传感器数据结构体
class sensor(object):
    id = 0
    vol = 0
    ssi = 0
    state = 0
    mv_flag = 0
    mv_tagId = 0
    obs_dist = [0xFF,0xFF,0xFF,0xFF]
    imu = [0,0,0]
    loc = [0,0,0]
    locErr = [0,0,0]
    ai_id = 0
    
    laserTarget_count = 0
    laserTarget_result = 0
    laserTarget_x = 0 
    laserTarget_y = 0 
    scale_weight = 0 
    
    newsCount = 0
    newsLen = 0
    news = ""

#协议接收结构体
class receive(object):
    head = 0
    len = 0
    date = []
    cnt = 0
    state = 0
    fps = 0
    fpsCnt = 0

class fly():

    #初始化
    def __init__(self,showTextEnable=False):

        self.maxNum = 10 #最多支持maxNum台飞机
        self.showTextEn = showTextEnable
        self.flySensor = []
        self.count = randint(0,255)
        self.time = time()
        self.isDelay = True
        self.horSpeed = 100
        self.verSpeed = 100

        #self.voice = textToSpeed() #语音播报
        self.rx = receive() #数据接收结构体
        
        self.usart = UART(1, baudrate=460800, tx=Pin.P16, rx=Pin.P15) #初始化串口（这里需要根据不同的平台进行相应的修改）

        for i in range(self.maxNum):
            self.flySensor.append(sensor()) 

        #运行数据接收线程
        start_new_thread(self.Receive_Thread, ())
        start_new_thread(self.Loop_1Hz_Thread, ())
        print("准备就绪，开始起飞。\n")

    #自动延时
    def setAutoDelay(self,auto):
        self.isDelay = auto

    #语音播报
    def tts(self,string,wait=True):
        #self.voice.speak(string,wait)
        return

    #串口数据解析
    def Receive_Anl(self):
        
        #和校验
        sum = 0
        sum = self.rx.head + self.rx.len
        for temp in self.rx.date:
            sum = sum + temp

        sum = (sum-self.rx.date[self.rx.len])%256 #求余

        if sum != self.rx.date[self.rx.len]:
            return
        
        self.rx.fpsCnt = self.rx.fpsCnt + 1
        
        #和校验通过
        if self.rx.date[0]==0x01:

            pack = unpack('<3BHBH4B6h3bB', bytearray(self.rx.date)[1:self.rx.len]) #从第1字节开始解析
            
            id = pack[0]
            
            if id<self.maxNum:
            
                self.flySensor[id].id = pack[0]
                self.flySensor[id].vol = pack[1]*0.1
                self.flySensor[id].ssi = pack[2]
                self.flySensor[id].state = pack[3]
                self.flySensor[id].mv_flag = pack[4]
                self.flySensor[id].mv_tagId = pack[5]
                self.flySensor[id].obs_dist = [pack[6],pack[7],pack[8],pack[9]]
                self.flySensor[id].imu = [pack[10]*0.1,pack[11]*0.1,pack[12]*0.1]
                self.flySensor[id].loc = [pack[13],pack[14],pack[15]]
                self.flySensor[id].locErr = [pack[16],pack[17],pack[18]]
                self.flySensor[id].ai_id = pack[19]
                
        elif self.rx.date[0]==0x02:

            pack = unpack('<4B2h4Bf', bytearray(self.rx.date)[1:self.rx.len]) #从第1字节开始解析，跳过fun
            
            id = pack[0]
            
            if id<self.maxNum:
            
                self.flySensor[id].id = pack[0]
                self.flySensor[id].ssi = pack[1]
                self.flySensor[id].laserTarget_count = pack[2]
                self.flySensor[id].laserTarget_result = pack[3]
                self.flySensor[id].laserTarget_x = pack[4]
                self.flySensor[id].laserTarget_y = pack[5]
                self.flySensor[id].obs_dist = [pack[6],pack[7],pack[8],pack[9]]
                self.flySensor[id].scale_weight = pack[10]
                
        elif self.rx.date[0]==0xF6 or self.rx.date[0]==0xFF :

            pack = unpack('<3B', bytearray(self.rx.date)[1:4]) #从第1字节开始解析，跳过fun
            
            id = pack[0]
            if self.flySensor[id].newsCount == pack[1]:
                return;
            
            if id<self.maxNum:
            
                self.flySensor[id].id = pack[0]
                self.flySensor[id].newsCount = pack[1]
                self.flySensor[id].newsLen = pack[2]
                news = bytearray(self.rx.date)[4:(4+pack[2])].decode("utf-8")

                if self.rx.date[0]==0xF6:
                    self.flySensor[id].news = news
                    print( '\33[1;36m' + str(id)+"号(消息)："+news + '\33[0m')
                else:
                    print( '\33[1;31m' + str(id)+"号(提示)："+news + '\33[0m')

    #串口通信协议接收
    def Receive_Prepare(self,data):

        if self.rx.state==0:#header

            if data == 0xAA:
                self.rx.state = 1
                self.rx.head = data

        elif self.rx.state==1:#len

            if data>0 and data<30:
                self.rx.state = 2
                self.rx.len = data
                self.rx.cnt = 0
            else:
                self.rx.state = 0

        elif self.rx.state==2:#date[]

            self.rx.date.append(data)
            self.rx.cnt = self.rx.cnt + 1
            if self.rx.cnt>=self.rx.len:
                self.rx.state = 3

        elif self.rx.state==3:#sum

            self.rx.state = 0
            self.rx.date.append(data)
            self.Receive_Anl()#接收完毕处理数据
            self.rx.date=[]#清空缓冲区，准备下次接收数据

        else:
            self.rx.state = 0

    #数据接收线程
    def Receive_Thread(self):
        
        while True:

            temp = self.usart.read(self.usart.any())
            size = len(temp)

            for i in range(size):
                self.Receive_Prepare(temp[i])

            sleep(0.02)
        
    #统计接收帧率线程
    def Loop_1Hz_Thread(self):

        while True:

            self.rx.fps = self.rx.fpsCnt
            self.rx.fpsCnt = 0
            sleep(1)

    #显示文字
    def showText(self,string):

        nowTime = time()
        dT = nowTime-self.time
        self.time = nowTime
        #黑色加粗字体
        print( '\33[1m' + string+ '\33[1;34m' +"---"+ ("%.1f" % dT) +"s"  + '\33[0m')

    #发送指令数据包
    def sendOrder(self,id,cmd,fmt,*args):

        self.count = self.count + 1
        buff = bytearray([id,cmd,self.count%6])
        buff = buff + pack(fmt,*args)
        dLen = 13 - len(buff)
        if(dLen>0):
            buff.extend(bytearray(dLen))

        self.usart.write(pyLink_pack(0xF3,buff+buff))

    #发送指令数据包
    def sendOrderPack(self,id,cmd,pack):

        self.count = self.count + 1
        buff = bytearray([id,cmd,self.count%6])
        buff = buff + pack
        dLen = 13 - len(buff)
        if(dLen>0):
            buff.extend(bytearray(dLen))

        self.usart.write(pyLink_pack(0xF3,buff+buff))

    #自动延时
    def autoDelay(self,id):

        if self.isDelay:
            sleep(1)
            dis = 100
            while dis>10:
                sleep(0.1)
                dx = self.flySensor[id].locErr[0]
                dy = self.flySensor[id].locErr[1]
                dz = self.flySensor[id].locErr[2]
                dis = sqrt(dx*dx+dy*dy+dz*dz)
            sleep(1)


    '''以下是发送部分'''

    # __号起飞__厘米
    def takeOff(self,id,high):

        high = int(high+0.5)#四舍五入取整
        self.sendOrder(id,0,'<h2B2h',high,50,0,0,0)
        self.showText("takeOff("+str(id)+","+str(high)+")")
        if self.isDelay:
            sleep(3+high/100)

    # __号__(0降落1刹车2悬停3急停4校准)
    def flyCtrl(self,id,mode):

        self.sendOrder(id,0xFE,'<B',mode)
        self.showText("flyCtrl("+str(id)+","+str(mode)+")")
        if self.isDelay:
            sleep(3)

    # __号切换为__模式(0光流定位1标签定位2自主巡线)
    def flyMode(self,id,mode):

        self.sendOrder(id,1,'<B',mode)
        self.showText("flyMode("+str(id)+","+str(mode)+")")
        sleep(0.1)

    # __号水平速度__厘米/秒
    def xySpeed(self,id,speed):

        speed = int(speed+0.5)
        self.horSpeed = speed
        self.sendOrder(id,2,'<h',speed)
        self.showText("xySpeed("+str(id)+","+str(speed)+")")
        sleep(0.1)

    # __号垂直速度__厘米/秒
    def zSpeed(self,id,speed):

        speed = int(speed+0.5)
        self.verSpeed = speed
        self.sendOrder(id,3,'<h',speed)
        self.showText("zSpeed("+str(id)+","+str(speed)+")")
        sleep(0.1)

    # __号从__位置移动(__,__,__)
    def move(self,id,mode,loc):

        loc[0] = int(loc[0]+0.5)
        loc[1] = int(loc[1]+0.5)
        loc[2] = int(loc[2]+0.5)
        self.sendOrder(id,29,'<B3h',mode,int(loc[0]),int(loc[1]),int(loc[2]))
        self.showText("move("+str(id)+","+str(mode)+",["+str(loc[0])+","+str(loc[1])+","+str(loc[2])+"])")
        self.autoDelay(id)
        
    # __号向__飞__厘米
    def moveCtrl(self,id,dir,distance):

        if dir>6:
            distance = int(distance*0.7071+0.5)
        else:
            distance = int(distance+0.5)
        self.sendOrder(id,5,'<Bh',dir,distance)
        self.showText("moveCtrl("+str(id)+","+str(dir)+","+str(distance)+")")
        self.autoDelay(id)

    # __号向__飞__厘米，寻找黑色色块
    def moveSearchDot(self,id,dir,distance):

        if dir>6:
            distance = int(distance*0.7071+0.5)
        else:
            distance = int(distance+0.5)
        self.sendOrder(id,6,'<Bh',dir,distance)
        self.showText("moveSearchDot("+str(id)+","+str(dir)+","+str(distance)+")")
        self.autoDelay(id)

    # __号向__飞__厘米，寻找色块__
    def moveSearchBlob(self,id,dir,distance,blob):

        if dir>6:
            distance = int(distance*0.7071+0.5)
        else:
            distance = int(distance+0.5)
        self.sendOrder(id,8,'<Bh6b',dir,distance,blob[0],blob[1],blob[2],blob[3],blob[4],blob[5])
        self.showText("moveSearchDot("+str(id)+","+str(dir)+","+str(distance)+",["+str(blob[0])+","+str(blob[1])+","+str(blob[2])+","+str(blob[3])+","+str(blob[4])+","+str(blob[5])+"])")
        self.autoDelay(id)

    # __号向__飞__厘米，寻找__号标签
    def moveSearchTag(self,id,dir,distance,tagID):

        if dir>6:
            distance = int(distance*0.7071+0.5)
        else:
            distance = int(distance+0.5)
        self.sendOrder(id,7,'<Bhh',dir,distance,tagID)
        self.showText("moveSearchTag("+str(id)+","+str(dir)+","+str(distance)+","+str(tagID)+")")
        self.autoDelay(id)

    # __号向__飞__厘米，跟随__号标签
    def moveFollowTag(self,id,dir,distance,tagID):

        if dir>6:
            distance = int(distance*0.7071+0.5)
        else:
            distance = int(distance+0.5)
        self.sendOrder(id,26,'<Bhh',dir,distance,tagID)
        self.showText("moveFollowTag("+str(id)+","+str(dir)+","+str(distance)+","+str(tagID)+")")
        self.autoDelay(id)

    # __号直达(__,__,__)
    def goTo(self,id,loc):

        loc[0] = int(loc[0]+0.5)
        loc[1] = int(loc[1]+0.5)
        loc[2] = int(loc[2]+0.5)
        self.sendOrder(id,9,'<3h',loc[0],loc[1],loc[2])
        self.showText("goTo("+str(id)+",["+str(loc[0])+","+str(loc[1])+","+str(loc[2])+"])")
        self.autoDelay(id)

    # __号直达__号标签
    def goToTag(self,id,tagID,high):

        high = int(high+0.5)
        self.sendOrder(id,28,'<2h',tagID,high)
        self.showText("goToTag("+str(id)+","+str(tagID)+","+str(high)+")")
        self.autoDelay(id)

    # __号旋转__度
    def rotation(self,id,angle):

        angle = int(angle+0.5)
        self.sendOrder(id,10,'<h',angle)
        self.showText("rotation("+str(id)+","+str(angle)+")")
        if self.isDelay:
            sleep(1+abs(angle)/20)

    # __号高度__厘米
    def flyHigh(self,id,high):

        high = int(high+0.5)
        self.sendOrder(id,11,'<h',high)
        self.showText("flyHigh("+str(id)+","+str(high)+")")
        self.autoDelay(id)

    # __号向__翻滚__圈
    def flipCtrl(self,id,dir,cir):
        
        self.sendOrder(id,12,'<2B',dir,cir)
        self.showText("flipCtrl("+str(id)+","+str(dir)+","+str(cir)+")")
        if self.isDelay:
            sleep(2)

    # __号灯光(__,__)
    def ledCtrl(self,id,mode,color):

        color[0] = int(color[0]+0.5)
        color[1] = int(color[1]+0.5)
        color[2] = int(color[2]+0.5)
        self.sendOrder(id,13,'<4B',mode,color[0],color[1],color[2])
        self.showText("ledCtrl("+str(id)+","+str(mode)+",["+str(color[0])+","+str(color[1])+","+str(color[2])+"])")
        sleep(0.1)

    # __号关闭灯光
    def closeLed(self,id):

        self.sendOrder(id,13,'<4B',0,0,0,0)
        self.showText(str(id)+"号关闭灯光")
        sleep(0.1)

    # __号检测__
    def mvCheckMode(self,id,mode):

        self.sendOrder(id,14,'<B6bh',mode,0,0,0,0,0,0,0)
        self.showText("mvCheckMode("+str(id)+","+str(mode)+")")
        sleep(0.1)

    # __号检测__号标签
    def mvCheckTag(self,id,tagID):

        self.sendOrder(id,14,'<B6bh',7,0,0,0,0,0,0,tagID)
        self.showText("mvCheckTag("+str(id)+","+str(tagID)+")")
        sleep(0.1)

    # __号检测色块(__,__,__,__,__,__,)
    def mvCheckBlob(self,id,blob):

        self.sendOrder(id,14,'<B6bh',6,blob[0],blob[1],blob[2],blob[3],blob[4],blob[5],0)
        self.showText("mvCheckBlob("+str(id)+",["+str(blob[0])+","+str(blob[1])+","+str(blob[2])+","+str(blob[3])+","+str(blob[4])+","+str(blob[5])+"])")
        sleep(0.1)

    # __号__回传
    def photographMode(self,id,mode):

        self.sendOrder(id,27,'<B',mode)
        self.showText("photographMode("+str(id)+","+str(mode)+")")
        sleep(0.1)

    # __号__发射激光
    def shootCtrl(self,id,mode):

        self.sendOrder(id,19,'<B',mode)
        self.showText("shootCtrl("+str(id)+","+str(mode)+")")
        sleep(0.1)

    # __号__电磁铁
    def magnetCtrl(self,id,mode):

        self.sendOrder(id,15,'<B',mode)
        self.showText("magnetCtrl("+str(id)+","+str(mode)+")")
        sleep(0.1)

    # __号舵机__度
    def servoCtrl(self,id,angle):

        angle = int(angle+0.5)
        self.sendOrder(id,16,'<B',angle)
        self.showText("servoCtrl("+str(id)+","+str(angle)+")")
        if self.isDelay:
            sleep(1)

    # __号__机头方向
    def lockDir(self,id,mode):

        self.sendOrder(id,18,'<B',mode)
        self.showText("lockDir("+str(id)+","+str(mode)+")")
        sleep(0.1)

    # __号发送__
    def roleCtrl(self,id,string):

        strBuf = string.encode("utf-8")
        strLen = len(strBuf)

        if strLen<11:
            self.sendOrderPack(id,17,strBuf)
            self.showText("roleCtrl("+str(id)+",\""+string+"\")")
            sleep(0.1)
        else:
            self.showText("发送失败：字符超过10字节")

    '''以下是回传部分'''

    #检测到__
    def isMvCheck(self,id,mode):

        return self.flySensor[id].mv_flag&(1<<mode)!=0

    #检测到__边有线
    def isMvCheckLine(self,id,dir):

        return self.flySensor[id].mv_flag&(1<<dir)!=0

    #__障碍物的距离
    def getObsDistance(self,id,dir):

        return self.flySensor[id].obs_dist[dir]

    #__
    def getFlySensor(self,id,type):

        if type == "tagID":
            return self.flySensor[id].mv_tagId
        elif type == "rol":
            return self.flySensor[id].imu[0]
        elif type == "pit":
            return self.flySensor[id].imu[1]
        elif type == "yaw":
            return self.flySensor[id].imu[2]
        elif type == "loc_x":
            return self.flySensor[id].loc[0]
        elif type == "loc_y":
            return self.flySensor[id].loc[1]
        elif type == "loc_z":
            return self.flySensor[id].loc[2]
        elif type == "err_x":
            return self.flySensor[id].locErr[0]
        elif type == "err_y":
            return self.flySensor[id].locErr[1]
        elif type == "err_z":
            return self.flySensor[id].locErr[2]
        elif type == "vol":
            return self.flySensor[id].vol

    #消息__
    def getRoleNews(self,id,type):

        if type=="details":
            return self.flySensor[id].news
        elif type=="id":
            return self.flySensor[id].newsCount

    #清除消息
    def clearRoleNews(self,id):

        self.flySensor[id].news = ""

    '''以下是互联模块部分'''

        # __号__开关
    def switchCtrl(self,id,mode):

        self.sendOrder(id,20,'<B',mode)
        self.showText("switchCtrl("+str(id)+","+str(mode)+")")
        sleep(0.1)

     # __号电子秤读数
    def getScaleWeight(self,id):

        return self.flySensor[id].scale_weight

     # __号电子秤读数
    def getShootResult(self,id,type):

        if type=="number":
            return self.flySensor[id].laserTarget_count
        elif type=="result":
            return self.flySensor[id].laserTarget_result
        elif type=="x":
            return self.flySensor[id].laserTarget_x
        elif type=="y":
            return self.flySensor[id].laserTarget_y

    '''以下是AI视觉部分'''

    # __号AI切换到__
    def aiCtrl(self,id,mode):

        self.sendOrder(id,21,'<B',mode)
        self.showText("aiCtrl("+str(id)+","+str(mode)+")")
        sleep(0.1)

    # __号AI学习ID___
    def aiLearning(self,id,learnID):

        self.sendOrder(id,22,'<B',learnID)
        self.showText("aiLearning("+str(id)+","+str(learnID)+")")
        sleep(0.1)

    # __号AI擦除记忆
    def aiForget(self,id):

        self.sendOrder(id,23,'<B',0)
        self.showText("aiForget("+str(id)+")")
        sleep(0.1)

    # __号AI__保存到SD卡
    def aiSaveImg(self,id,mode):

        self.sendOrder(id,21,'<B',mode)
        self.showText("aiSaveImg("+str(id)+","+str(mode)+")")
        sleep(0.1)

     # __号AI识别结果
    def aiGetResult(self,id):

        return self.flySensor[id].ai_id

    '''以下是部分函数名的重载，移植到其他平台时可以删掉'''

    def  take_off(self,id,high):

        self.takeOff(id,high)

    def auto_wait(self,auto):

        self.setAutoDelay(auto)

    def fly_mode(self,id,mode):

        self.flyMode(id,mode)

    def xy_speed(self,id,speed):

        self.xySpeed(id,speed)

    def z_speed(self,id,speed):

        self.zSpeed(id,speed)

    def fly(self,id,dir,distance):

        self.moveCtrl(id,dir,distance)

    def fly_tag(self,id,dir,distance,tagID):

        self.moveSearchTag(id,dir,distance,tagID)

    def xuanzhuan(self,id,angle):

        self.rotation(id,angle)

    def height(self,id,high):

        self.flyHigh(id,high)

    def check_data(self,id,mode):

        self.mvCheckMode(id,mode)

    def check_tag(self,id,tagID):

        self.mvCheckTag(id,tagID)

    def get_color(self,id,mode):

        self.photographMode(id,mode)

    def check_color(self,id,blob):

        self.mvCheckBlob(id,blob)

    def shoot(self,id,mode):

        self.shootCtrl(id,mode)

    def servo(self,id,angle):

        self.servoCtrl(id,angle)

    def is_check_tag_color(self,id,mode):

        return self.isMvCheck(id,mode)

    def is_check_line(self,id,dir):

        return self.isMvCheckLine(id,dir)

    def getTag(self,id,type):

        return self.getFlySensor(id,type)

        
