# labplus mPython analogClock driver
# MIT license; Copyright (c) 2018 labplus
# V1.0 Tangliufeng   2018.11.8

from mpython import oled
import math
import time

class Clock:
    def __init__(self,x,y,radius):          #定义时钟中心点和半径
        self.xc=x
        self.yc=y
        self.r=radius

    def settime(self):          #设定时间
        t = time.localtime()
        self.hour=t[3]
        self.min=t[4]
        self.sec=t[5]

    def drawDial(self):                    #画钟表刻度
        r_tic1=self.r-1
        r_tic2=self.r-2

        oled.circle(self.xc, self.yc, self.r, 1)
        oled.fill_circle(self.xc, self.yc, 2, 1)

        for h in range(12):
            at = math.pi * 2.0 * h / 12.0
            x1 =round(self.xc + r_tic1 * math.sin(at))
            x2 = round(self.xc + r_tic2 * math.sin(at))
            y1 = round(self.yc - r_tic1 * math.cos(at))
            y2 = round(self.yc - r_tic2 * math.cos(at))
            oled.line(x1,y1,x2,y2,1)

    def drawHour(self):                      #画时针

        r_hour=int(self.r/10.0*5)
        ah=math.pi*2.0*(( self.hour%12)+self.min/60.0)/12.0
        xh=int(self.xc + r_hour * math.sin(ah))
        yh = int(self.yc - r_hour * math.cos(ah))
        oled.line(self.xc, self.yc, xh, yh, 1)

    def drawMin(self):                       #画分针

        r_min=int(self.r/10.0*7)
        am=math.pi*2.0*self.min/60.0

        xm = round(self.xc + r_min * math.sin(am))
        ym = round(self.yc - r_min * math.cos(am))
        oled.line(self.xc,self.yc, xm, ym, 1)

    def drawSec(self):                        #画秒针
        
        r_sec=int(self.r/10.0*9)
        asec = math.pi * 2.0 * self.sec / 60.0
        xs = round(self.xc + r_sec * math.sin(asec))
        ys = round(self.yc - r_sec * math.cos(asec))
        oled.line(self.xc, self.yc, xs, ys, 1)
       
    def drawClock(self):                      #画完整钟表
        
        self.drawDial()
        self.drawHour()
        self.drawMin()
        self.drawSec()

    def clear(self):                           #清除

        oled.fill_circle(self.xc, self.yc, self.r, 0)