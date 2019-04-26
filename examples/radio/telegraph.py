import radio                                            # 导入radio
from mpython import *                                   # 导入mpython
import music                                            # 导入music

CH = 1                                                  # channel变量

radio.on()
radio.config(channel=CH)                                # radio通道设置

btna_stat, btna_stat, touch_stat = [0] * 3              # 按键状态标志


def set_channel():                                      # radio 通道设置函数

    global CH, btna_stat, btnb_stat
    if button_a.value() == 0 and btna_stat == 0:        # a按键,减通道
        CH -= 1
        if CH < 1:
            CH = 13
        radio.config(channel=CH)                        # radio通道设置
        oled.DispChar("Channel: %02d" % CH, 25, 5)      # 通道显示
        oled.show()
        btna_stat = 1
    elif button_a.value() == 1:
        btna_stat = 0

    if button_b.value() == 0 and btnb_stat == 0:        # b按键,加通道
        CH += 1
        if CH > 13:
            CH = 1
        radio.config(channel=CH)                        # radio通道设置
        oled.DispChar("Channel: %02d" % CH, 25, 5)      # 通道显示
        oled.show()
        btnb_stat = 1
    elif button_b.value() == 1:
        btnb_stat = 0


def ding():                                             # 叮叮响

    global touch_stat
    if touchPad_T.read() < 300 and touch_stat == 0:     # 检测按键按下时,发出‘ding’响,并广播
        music.pitch(500, 100, wait=False)              # 播放"ding"
        radio.send('ding')                              # radio 广播 "ding"
        touch_stat = 1
    elif touchPad_T.read() >= 300:
        touch_stat = 0


oled.DispChar("Channel: %d" % CH, 25, 5)                # 开机显示
oled.DispChar("电报机:触摸T", 25, 25)
oled.show()

while True:
    set_channel()                                       # 设置通道函数
    ding()                                              # 叮叮响函数
    temp = radio.receive()                              # radio接收广播

    if temp == 'ding':                                  # 当接收到"ding"广播,发出叮响
        rgb.fill((0, 10, 0))                            # 指示灯
        rgb.write()
        music.pitch(500, 100, wait=False)
    else:
        rgb.fill((0, 0, 0))
        rgb.write()
