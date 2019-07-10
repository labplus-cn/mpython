
#按键常规使用方法

from mpython import *

def blinkRGB(_):            #闪烁板载rgb
  
    rgb.fill((50,0,0))
    rgb.write()
    sleep_ms(100)
    rgb.fill((0,0,0))
    rgb.write()

button_a.irq(trigger=Pin.IRQ_FALLING, handler=blinkRGB)    #按键b中断触发blinkRGB，触发方式下降沿，

while True:
    if button_b.value()==0:           #当按键b按下触发蜂鸣器
        buzz.on(1000)
    else:
        buzz.off()
