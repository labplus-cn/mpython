照度/噪声计
==========

::
    from mpython import *

    u=UI()
    while True:
        oled.fill(0)
        lightValue=numberMap(light.read(),0,4093,0,100)
        soundValue=numberMap(sound.read(),0,4093,0,100)
        u.stripBar(35,8,10,40,soundValue,0)
        u.stripBar(90,8,10,40,lightValue,0)
        oled.DispChar("噪声计",23,50)
        oled.DispChar("照度计",76,50)
        oled.show()
