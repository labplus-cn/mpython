from mpython import *
import time
 
tone = [262,294,330,349,392,440,494]     #七音阶
 
def playMusic(tune,duration):
    buzz.on()
    for i in range(len(tune)):
        buzz.freq(int(tune[i]))
        time.sleep_ms(duration)
    buzz.off()
 

playMusic(tone,500)