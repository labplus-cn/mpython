from mpython import i2c
from micropython import const
import time

MOTOR_1 = const(0x01)
"""
M1电机编号，0x01
"""

MOTOR_2 = const(0x02)
"""
M2电机编号，0x02
"""

_speed_buf = {}


def set_speed(motor_no, speed):
    """
    设置电机速度

    :param int motor_no: 控制电机编号，可以使用 ``MOTOR_1``, ``MOTOR_2`` ,或者直接写入电机编号。
    :param int speed: 电机速度，范围-100~100，负值代表反转。

    """
    global _speed_buf
    speed = max(min(speed, 100), -100)
    _speed_buf.update({motor_no: speed})
    attempts = 0
    while True:
        try:
            i2c.writeto(0x10, bytearray([motor_no, speed]))
        except Exception as e:
            attempts = attempts + 1
            time.sleep_ms(500)
            if attempts > 2:
                break
        else:
            break

def get_speed(motor_no):
    """
    返回电机速度

    :param int motor_no: 控制电机编号，可以使用 ``MOTOR_1``, ``MOTOR_2``,或者直接写入电机编号。
    :rtype: int
    :return: 返回该电机速度
    """
    global _speed_buf
    if motor_no in _speed_buf:

        return _speed_buf[motor_no]
    else:
        return None


def led_on(no, brightness=50):
    """
    打开灯。电机接口,除了可以驱动电机,还能做灯的控制。

    :param int no: 控制电机编号，可以使用 ``MOTOR_1``, ``MOTOR_2``,或者直接写入电机编号。
    :param int brightness: 设置亮度,范围0~100
    """
    brightness = max(min(brightness, 100), 0)
    attempts = 0
    while True:
        try:
            i2c.writeto(0x10, bytearray([no, brightness]))
        except Exception as e:
            attempts = attempts + 1
            time.sleep_ms(500)
            if attempts > 2:
                break
        else:
            break


def led_off(no):
    """
    关闭灯。

    :param int no: 控制电机编号，可以使用 ``MOTOR_1``, ``MOTOR_2``,或者直接写入电机编号。
    """
    attempts = 0
    while True:
        try:
            i2c.writeto(0x10, bytearray([no, 0]))
        except Exception as e:
            attempts = attempts + 1
            time.sleep_ms(500)
            if attempts > 2:
                break
        else:
            break