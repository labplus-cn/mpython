import ntptime
from mpython import*
from machine import Timer,RTC
import _thread
from random import randint
from math import sin, cos

data=(2018, 12, 15, 6, 8,30, 0, 0)
RTC().datetime(data)
clock=UI.Clock(64,32,30)

mode=0
modeNum=5
Center_x=63
Center_y=31

def scanBtnThread(_):
    global mode
    aState=0
    bState=0
    lastaState =0
    lastbState =0
    while True:
        aState=button_a.value()
        bState=button_b.value()
        if aState!=lastaState:
            sleep_ms(20)
            if aState==0:
                mode=mode-1
                mode=mode % modeNum
                print("mode:%d" %mode)
            lastaState=aState
        if bState!=lastbState:
            sleep_ms(20)
            if bState==0:
                mode=mode+1
                mode=mode % modeNum
                print("mode:%d" %mode)
            lastbState=bState

_thread.start_new_thread(scanBtnThread,(1,))
    
def Refresh(_):
    if mode ==0:
        oled.DispChar("钟表",0,0)
        clock.settime()
        clock.drawClock()
        oled.show()
        oled.fill(0)


tim1 = Timer(1)
tim1.init(period=1000, mode=Timer.PERIODIC, callback=Refresh)

class snow():
    def __init__(self):
        self.x = randint(0,127)         #随机生成雪花的起始坐标点
        self.y = randint(0,10)
        self.r = randint(1,2)           #随机生成雪花的半径大小
        self.vx = randint(-2,2)         #随机生成雪花的x,y移动路径
        self.vy = randint(1,3)

    def refresh(self):
        self.x += self.vx               #下移坐标，雪花落下
        self.y += self.vy
        if self.x > 128 or self.x < 0:
            self.x = randint(0,127)
        if self.y > 63 or self.y < 0:
            self.y = 0

    def run(self):
            self.refresh()
            oled.fill_circle(self.x,self.y,self.r,1)     #画雪花

balls = []
for x in range(20):              #生成20个雪花点
    balls.append(snow())

import music                        # 导入music模块

note=["C4:2","D4:2","E4:2","F4:2","G4:2","A4:2","B4:2"]     # 定义7音阶的元组

pStatus,yStatus,tStatus,hStatus,oStatus,nStatus,p0Status=[1]*7  # 按键状态标记变量

p0 = TouchPad(Pin(33))              # 由于掌控板上的触摸按键只有6个，还需拓展多一个引脚P0，对应ESP32的IO33

def drawPiano(x,y,w,h,num):
    if num==0:
        for i in range(7):
            oled.rect((x+i*w),y,w,h,1)
    else:
        oled.fill_rect((x+(num-1)*w),y,w,h,1)

X = const(64)
Y = const(32)

f = [[0.0 for _ in range(3)] for _ in range(8)]
cube = ((-20,-20, 20), (20,-20, 20), (20,20, 20), (-20,20, 20),
        (-20,-20,-20), (20,-20,-20), (20,20,-20), (-20,20,-20))


while True:
    if mode ==1:
        oled.DispChar("水平仪",0,0)
        x=accelerometer.get_x()
        y=accelerometer.get_y()
        if y<=1 and y>=-1:
            offsetX=int(numberMap(y,1,-1,-64,64))
        if x<=1 and x>=-1:
            offsetY=int(numberMap(x,1,-1,32,-32))
        move_x=Center_x+offsetX
        move_y=Center_y+offsetY
        oled.circle(Center_x,Center_y,6,1)
        oled.fill_circle(move_x,move_y,4,1)
        oled.DispChar("%0.1f,%0.1f" %(x,y),85,0)
        if offsetX==0 and offsetY==0:
            rgb.fill((0,10,0))
            rgb.write()
        else:
            rgb.fill((0,0,0))
            rgb.write()
        oled.show()
        oled.fill(0)

    if mode ==2:
        oled.DispChar("钢琴",0,0)
        drawPiano(28,20,10,35,0)
        if touchPad_P.read()<100 and pStatus==1:      # 检测按键按下和判断按键标记
            music.play(note[0],wait=False)                       # 播放音符
            drawPiano(28,20,10,35,1)
            pStatus=0                                 # 按键标记置0
        elif touchPad_P.read()>=100:
            pStatus=1
        if touchPad_Y.read()<100 and yStatus==1:
            music.play(note[1],wait=False)
            drawPiano(28,20,10,35,2)
            yStatus=0
        elif touchPad_Y.read()>=100:
            yStatus=1
        if touchPad_T.read()<100 and tStatus==1:
            music.play(note[2],wait=False)
            drawPiano(28,20,10,35,3)
            tStatus=0
        elif touchPad_T.read()>=100:
            tStatus=1
        if touchPad_H.read()<100 and hStatus==1:
            music.play(note[3],wait=False)
            drawPiano(28,20,10,35,4)
            hStatus=0
        elif touchPad_H.read()>=100:
            hStatus=1
        if touchPad_O.read()<100 and oStatus==1:
            music.play(note[4],wait=False)
            drawPiano(28,20,10,35,5)
            oStatus=0
        elif touchPad_O.read()>=100:
            oStatus=1
        if touchPad_N.read()<100 and nStatus==1:
            music.play(note[5],wait=False)
            drawPiano(28,20,10,35,6)
            nStatus=0
        elif touchPad_N.read()>=100:
            nStatus=1
        if p0.read()<100 and p0Status==1:
            music.play(note[6],wait=False)
            drawPiano(28,20,10,35,7)
            p0Status=0
        elif p0.read()>=100:
            p0Status=1
        oled.show()
        oled.fill(0)

    if mode ==3:
        oled.DispChar("飘雪",0,0)
        for b in balls:              #雪花落下
            b.run()
        oled.show()                  #显示oled
        oled.fill(0)                 #清屏
        sleep_ms(50)                 #刷新时间

    if mode ==4:
        loatmode=mode
        for angle in range(0, 361, 5):  # 0 to 360 deg 3step
            if loatmode !=mode:
                break
            for i in range(8):
                r  = angle * 0.0174532  # 1 degree
                x1 = cube[i][2] * sin(r) + cube[i][0] * cos(r)  # rotate Y
                ya = cube[i][1]
                z1 = cube[i][2] * cos(r) - cube[i][0] * sin(r)
                x2 = x1
                y2 = ya * cos(r) - z1 * sin(r)  # rotate X
                z2 = ya * sin(r) + z1 * cos(r)
                x3 = x2 * cos(r) - y2 * sin(r)  # rotate Z
                y3 = x2 * sin(r) + y2 * cos(r)
                z3 = z2
                x3 = x3 + X
                y3 = y3 + Y
                f[i][0] = x3  # store new values
                f[i][1] = y3
                f[i][2] = z3
           
            oled.line(int(f[0][0]), int(f[0][1]), int(f[1][0]), int(f[1][1]), 1)
            oled.line(int(f[1][0]), int(f[1][1]), int(f[2][0]), int(f[2][1]), 1)
            oled.line(int(f[2][0]), int(f[2][1]), int(f[3][0]), int(f[3][1]), 1)
            oled.line(int(f[3][0]), int(f[3][1]), int(f[0][0]), int(f[0][1]), 1)
            oled.line(int(f[4][0]), int(f[4][1]), int(f[5][0]), int(f[5][1]), 1)
            oled.line(int(f[5][0]), int(f[5][1]), int(f[6][0]), int(f[6][1]), 1)
            oled.line(int(f[6][0]), int(f[6][1]), int(f[7][0]), int(f[7][1]), 1)
            oled.line(int(f[7][0]), int(f[7][1]), int(f[4][0]), int(f[4][1]), 1)
            oled.line(int(f[0][0]), int(f[0][1]), int(f[4][0]), int(f[4][1]), 1)
            oled.line(int(f[1][0]), int(f[1][1]), int(f[5][0]), int(f[5][1]), 1)
            oled.line(int(f[2][0]), int(f[2][1]), int(f[6][0]), int(f[6][1]), 1)
            oled.line(int(f[3][0]), int(f[3][1]), int(f[7][0]), int(f[7][1]), 1)
            oled.line(int(f[1][0]), int(f[1][1]), int(f[3][0]), int(f[3][1]), 1)  # cross
            oled.line(int(f[0][0]), int(f[0][1]), int(f[2][0]), int(f[2][1]), 1)  # cross
            oled.DispChar('3D cube', 0, 0)
            oled.show()  # display
            oled.fill(0)  # clear
