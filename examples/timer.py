from mpython import *
from machine import Timer
import music

def playMusic(_):
    music.play(music.BA_DING)

tim1 = Timer(1)

tim1.init(period=5000, mode=Timer.PERIODIC,callback=playMusic)

while True:
    timerNum=tim1.value()
    oled.DispChar("定时器：%d ms" %timerNum,20,25)
    oled.show()
    oled.fill(0)
    sleep_ms(50)

