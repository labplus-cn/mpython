钢琴
==========

使用music模块和掌控板上的触摸按键，制作一个简易的7音阶触摸钢琴。

::

    from mpython import *               # 导入mpython模块
    import music                        # 导入music模块

    note=["C4:2","D4:2","E4:2","F4:2","G4:2","A4:2","B4:2"]     # 定义7音阶的元组

    pStatus,yStatus,tStatus,hStatus,oStatus,nStatus,p0Status=[1]*7  # 按键状态标记变量
 
    p0 = TouchPad(Pin(33))              # 由于掌控板上的触摸按键只有6个，还需拓展多一个引脚P0，对应ESP32的IO33

    while True:
        if touchPad_P.read()<100 and pStatus==1:      # 检测按键按下和判断按键标记
            music.play(note[0])                       # 播放音符
            pStatus=0                                 # 按键标记置0
        elif touchPad_P.read()>=100:
            pStatus=1
        if touchPad_Y.read()<100 and yStatus==1:
            music.play(note[1])
            yStatus=0
        elif touchPad_Y.read()>=100:
            yStatus=1
        if touchPad_T.read()<100 and tStatus==1:
            music.play(note[2])
            tStatus=0
        elif touchPad_T.read()>=100:
            tStatus=1
        if touchPad_H.read()<100 and hStatus==1:
            music.play(note[3])
            hStatus=0
        elif touchPad_H.read()>=100:
            hStatus=1
        if touchPad_O.read()<100 and oStatus==1:
            music.play(note[4])
            oStatus=0
        elif touchPad_O.read()>=100:
            oStatus=1
        if touchPad_N.read()<100 and nStatus==1:
            music.play(note[5])
            nStatus=0
        elif touchPad_N.read()>=100:
            nStatus=1
        if p0.read()<100 and p0Status==1:
            music.play(note[6])
            p0Status=0
        elif p0.read()>=100:
            p0Status=1

    
.. image:: /images/classic/piano.gif