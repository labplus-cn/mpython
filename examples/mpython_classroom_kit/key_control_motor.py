from mpython_classroom_kit import *
import music

while True:
    # 按下左键,马达左转
    if get_key() == {'left'}:
        set_motor(-100)

    # 按下右键,马达右转
    elif get_key() == {'right'}:
        set_motor(100)
    # 同时按下OK、下键,马达停止
    elif get_key() == {'ok', 'down'}:
        set_motor(0)