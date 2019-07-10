from mpython import *

while True:
    # 按键A按下为低电平
    if button_a.value() == 0 :    
        # 按键延时
        sleep_ms(20)
        # 再次检测是否按下
        if button_a.value()==0:
            # 设置为红色
            rgb[0] = (255,0,0)  
            rgb[1] = (255,0,0)
            rgb[2] = (255,0,0)
        rgb.write()
    # 按键B按下为低电平
    if button_b.value() == 0 :    
        # 按键延时
        sleep_ms(20)
        # 再次检测是否按下
        if button_b.value()==0:
            # 关灯
            rgb[0] = (0, 0, 0)    
            rgb[1] = (0, 0, 0)
            rgb[2] = (0, 0, 0)
            rgb.write()