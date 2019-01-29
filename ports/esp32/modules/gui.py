# gui for mpython
# MIT license; Copyright (c) 2019 Zhang Kaihua(apple_eat@126.com)
import time, math

class UI():
    def __init__(self, oled):
        self.display = oled

    def ProgressBar(self, x, y, width, height, progress):
        radius = int(height / 2)
        xRadius = x + radius
        yRadius = y + radius
        doubleRadius = 2 * radius
        innerRadius = radius - 2

        self.display.RoundRect(x,y,width,height,radius,1)
        maxProgressWidth = int((width - doubleRadius + 1) * progress / 100)
        self.display.fill_circle(xRadius, yRadius, innerRadius,1)
        self.display.fill_rect(xRadius + 1, y + 2, maxProgressWidth, height - 3,1)
        self.display.fill_circle(xRadius + maxProgressWidth, yRadius, innerRadius,1)

    def stripBar(self, x, y, width, height, progress,dir=1,frame=1):

        self.display.rect(x,y,width,height,frame)
        if  dir:
            Progress=int(progress/100 *width)
            self.display.fill_rect(x,y,Progress,height,1)
        else:
            Progress=int(progress/100 *height)
            self.display.fill_rect(x,y+(height-Progress),width,Progress,1)

class multiScreen():
    def __init__(self,oled, framelist, w, h):
        self.display = oled
        self.framelist=framelist
        self.width=w
        self.hight=h
        self.frameCount=len(framelist)
        self.activeSymbol =bytearray([0x00, 0x18, 0x3c, 0x7e, 0x7e, 0x3c, 0x18, 0x00])
        self.inactiveSymbol =bytearray([0x00, 0x0, 0x0, 0x18, 0x18, 0x0, 0x0, 0x00])
        self.SymbolInterval=1
        

    def drawScreen(self,index):
        self.index=index
        self.display.fill(0)
        self.display.Bitmap(int(64-self.width/2),int(0.3*self.hight),self.framelist[self.index], self.width,self.hight,1)
        SymbolWidth=self.frameCount*8+(self.frameCount-1)*self.SymbolInterval
        SymbolCenter=int(SymbolWidth/2)
        starX=64-SymbolCenter
        for i in range(self.frameCount):
            x=starX+i*8+i*self.SymbolInterval
            y=int(1.1*self.hight)+8
            if i==self.index:
                self.display.Bitmap(x,y,self.activeSymbol,8,8,1)
            else:
                self.display.Bitmap(x,y,self.inactiveSymbol,8,8,1)

    def nextScreen(self):
        self.index=(self.index+1)%self.frameCount
        self.drawScreen(self.index)

class Clock:
    def __init__(self,oled, x, y, radius):          #定义时钟中心点和半径
        self.display = oled
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

        self.display.circle(self.xc, self.yc, self.r, 1)
        self.display.fill_circle(self.xc, self.yc, 2, 1)

        for h in range(12):
            at = math.pi * 2.0 * h / 12.0
            x1 =round(self.xc + r_tic1 * math.sin(at))
            x2 = round(self.xc + r_tic2 * math.sin(at))
            y1 = round(self.yc - r_tic1 * math.cos(at))
            y2 = round(self.yc - r_tic2 * math.cos(at))
            self.display.line(x1,y1,x2,y2,1)

    def drawHour(self):                      #画时针

        r_hour=int(self.r/10.0*5)
        ah=math.pi*2.0*(( self.hour%12)+self.min/60.0)/12.0
        xh=int(self.xc + r_hour * math.sin(ah))
        yh = int(self.yc - r_hour * math.cos(ah))
        self.display.line(self.xc, self.yc, xh, yh, 1)

    def drawMin(self):                       #画分针

        r_min=int(self.r/10.0*7)
        am=math.pi*2.0*self.min/60.0

        xm = round(self.xc + r_min * math.sin(am))
        ym = round(self.yc - r_min * math.cos(am))
        self.display.line(self.xc,self.yc, xm, ym, 1)

    def drawSec(self):                        #画秒针
        
        r_sec=int(self.r/10.0*9)
        asec = math.pi * 2.0 * self.sec / 60.0
        xs = round(self.xc + r_sec * math.sin(asec))
        ys = round(self.yc - r_sec * math.cos(asec))
        self.display.line(self.xc, self.yc, xs, ys, 1)
    
    def drawClock(self):                      #画完整钟表
        self.drawDial()
        self.drawHour()
        self.drawMin()
        self.drawSec()

    def clear(self):                           #清除
        self.display.fill_circle(self.xc, self.yc, self.r, 0)
