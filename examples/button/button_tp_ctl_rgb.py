from mpython import *

while True:
    if(touchPad_P.read() < 100):
        rgb[0] = (255,0,0)    # 开灯，设置红色
        rgb[1] = (255,0,0)  # 设定为红色
        rgb[2] = (255,0,0)   # 设置为红色
        rgb.write()
    elif(touchPad_Y.read() < 100):
        rgb[0] = (0,255,0) #关灯
        rgb[1] = (0,255,0)
        rgb[2] = (0,255,0)
        rgb.write()
    elif(touchPad_T.read() < 100):
        rgb[0] = (0,0,255) #关灯
        rgb[1] = (0,0,255)
        rgb[2] = (0,0,255)
        rgb.write()
    elif(touchPad_H.read() < 100):
        rgb[0] = (255,255,0) #关灯
        rgb[1] = (255,255,0)
        rgb[2] = (255,255,0)
        rgb.write()
    elif(touchPad_O.read() < 100):
        rgb[0] = (255,0,255) #关灯
        rgb[1] = (255,0,255)
        rgb[2] = (255,0,255)
        rgb.write()
    elif(touchPad_N.read() < 100):
        rgb[0] = (0,255,255) #关灯
        rgb[1] = (0,255,255)
        rgb[2] = (0,255,255)
        rgb.write()