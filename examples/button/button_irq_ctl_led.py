from mpython import *     #导入mpython模块
import music              #导入music模块

def ledon(_):             #先定义中断处理函数：开灯和蜂鸣器
    rgb.fill((128,0,0))   #打开板载灯，全部设置为红色，半亮度
    rgb.write()           #将颜色输出到灯
    music.pitch(1000)     #打开蜂鸣器：1000赫兹

def ledoff(_):            #先定义中断处理函数：关灯和蜂鸣器
    rgb.fill((0,0,0))     #关闭全部板载灯
    rgb.write()           #将颜色输出到灯
    music.pitch(0)        #关闭蜂鸣器

button_a.irq(trigger=Pin.IRQ_FALLING, handler=ledon)     #设置按键 A 中断,下降沿触发，开灯和蜂鸣器

button_b.irq(trigger=Pin.IRQ_FALLING, handler=ledoff)    #设置按键 B 中断,下降沿触发，关灯和蜂鸣器

while True:                            #在没有中断时，程序执行在循环内
    pass