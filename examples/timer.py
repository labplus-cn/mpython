from mpython import *
from machine import Timer
import music

def playMusic(_):             #定义定时器回调函数，播放音乐
    music.play(music.BA_DING)

tim1 = Timer(1)           #创建定时器1

tim1.init(period=5000, mode=Timer.PERIODIC,callback=playMusic)         #配置定时器，模式为循环执行，循环周期为5秒

while True:
    timerNum=tim1.value()
    oled.DispChar("定时器：%d ms" %timerNum,20,25)
    oled.show()
    oled.fill(0)
