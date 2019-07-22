# MIT license; Copyright (c) 2019 Labplus & mPython Development 
# V1.0 Tangliufeng
# 掌控板PPT翻页遥控器
# 使用方式: 短按键A-上页；短按键B-下页；长按键A-进入放映；长按键B-退出放映
#
from mpython import *
from bluetooth import ble
import time
# 按键状态标志
btn_a_status, btn_b_status = [0, 0]

oled.DispChar('PPT 翻页控制器',20,20)
oled.show()

# ble初始化
ble.init('PPT_Remote')
# 等待蓝牙主机
sleep(2)

while True:
    # 当按键A为低电平且标志为0
    if button_a.value() == 0 and btn_a_status == 0:
        btn_a_time = time.ticks_ms()
        # 按键保持标志
        a_hold_flag = False
        # 当按键一直按下
        while not button_a.value():
            # 当按下保持2秒
            if time.ticks_diff(time.ticks_ms(), btn_a_time) > 2000:
                # 发送 F5,放映幻灯片
                ble.hidd_send_keyboard([ble.HID_KEY_F5])
                print("Pressed F5")
                # 按键保持标志置为1
                a_hold_flag = True
                break
        # 如果没有持续按下按键
        if a_hold_flag is False:
            # 发送 LeftArrow,幻灯片上页
            ble.hidd_send_keyboard([ble.HID_KEY_LEFT_ARROW])
            print("Pressed LeftArrow")
        # 按键状态置为1
        btn_a_status = 1

    # 当按键A为高电平且标志为1时,释放按键
    elif button_a.value() == 1 and btn_a_status == 1:
        print("Relesed Button A")
        ble.hidd_send_keyboard([0])
        btn_a_status = 0

    if button_b.value() == 0 and btn_b_status == 0:
        btn_b_time = time.ticks_ms()
        b_hold_flag = False

        while not button_b.value():
            if time.ticks_diff(time.ticks_ms(), btn_b_time) > 2000:
                # 发送 ESC,退出放映幻灯片
                ble.hidd_send_keyboard([ble.HID_KEY_ESCAPE])
                print("Pressed ESC")
                b_hold_flag = True
                break

        if b_hold_flag is False:
            # 发送 RightArrow,幻灯片翻页
            ble.hidd_send_keyboard([ble.HID_KEY_RIGHT_ARROW])
            print("Pressed RightArrow")

        btn_b_status = 1

    elif button_b.value() == 1 and btn_b_status == 1:
        print("Relesed Button B")
        ble.hidd_send_keyboard([0])
        btn_b_status = 0
