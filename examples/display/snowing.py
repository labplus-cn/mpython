
# 使用random随机生成飘雪效果

from mpython import *
from random import randint

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

while True:
    sleep_ms(50)                 #刷新时间
    oled.fill(0)                 #清屏
    for b in balls:              #雪花落下
        b.run()
    oled.show()                  #显示oled


