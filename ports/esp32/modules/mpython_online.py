# -*- coding:utf-8 -*-
# @Time     : 2019/06/28
# @Author   : Wu Wen Jie(6692776@qq.com)
# @FileName : mpython_online.py
# @Description : A transfer protocol between mPython board and Labplus software
# @Version  : 1.0

from mpython import *
from servo import Servo
import machine
import time
import music
import framebuf
import re
import radio

def display_pbm_data(_data, _x, _y):
    oled.blit(framebuf.FrameBuffer(_data[2], _data[0], _data[1], framebuf.MONO_HLSB), _x, _y)

def get_pbm_data(_path):
    f = open(_path, 'rb')
    f.readline()
    line2 = f.readline()
    width = 0; height = 0; param = b''
    matcher = re.match(r'\d+\s\d+', line2)
    if matcher: param = matcher.group(0)
    else:
        matcher = re.match(r'\d+\s', line2)
        if matcher: param = matcher.group(0)
        param += f.readline()
    result = param.decode('utf-8').replace('\n', ' ')
    arr = result.split(' ')
    if len(arr) > 1: width = int(arr[0]); height = int(arr[1])
    return (width, height, bytearray(f.read()))
    
oled.fill(0)
oled.DispChar("Online Mode", 30, 16)
oled.show()

def getTouchpad():
    val=0x00
    if touchPad_P.read() < 400:
        val=val|0x80
    else:
        val=val&0x7F
    if touchPad_Y.read() < 400:
        val=val|0x40
    else:
        val=val&0xBF
    if touchPad_T.read() < 400:
        val=val|0x20
    else:
        val=val&0xDF
    if touchPad_H.read() < 400:
        val=val|0x10
    else:
        val=val&0xEF
    if touchPad_O.read() < 400:
        val=val|0x08
    else:
        val=val&0xF7
    if touchPad_N.read() < 400:
        val=val|0x04
    else:
        val=val&0xFB
    if button_a.value() == 0:
        val=val|0x02
    else:
        val=val&0xFD
    if button_b.value() == 0:
        val=val|0x01
    else:
        val=val&0xFE
    return val
    
def run_code(_code):
    try:
        eval("exec(\"" + _code + "\",globals())")
    except:
        print(_code)

try: tim1.deinit()
except: pass
try: tim2.deinit()
except: pass
try: tim4.deinit()
except: pass
try: tim7.deinit()
except: pass
try: tim8.deinit()
except: pass
try: tim9.deinit()
except: pass
try: tim10.deinit()
except: pass
try: tim11.deinit()
except: pass
try: tim12.deinit()
except: pass
try: tim13.deinit()
except: pass
try: tim14.deinit()
except: pass

_is_shaked = False
_last_x = _last_y = _last_z = _count_shaked = _count_radio = 0
_pind = {}
_pina = {}

ext  = ADC(Pin(34))

def timer11_tick(_):
    global _is_shaked, _last_x, _last_y, _last_z, _count_shaked
    if _is_shaked:
        _count_shaked += 1
        if _count_shaked == 5: _count_shaked = 0
    x=accelerometer.get_x(); y=accelerometer.get_y(); z=accelerometer.get_z()
    if _last_x == 0 and _last_y == 0 and _last_z == 0:
        _last_x = x; _last_y = y; _last_z = z; return
    diff_x = x - _last_x; diff_y = y - _last_y; diff_z = z - _last_z
    _last_x = x; _last_y = y; _last_z = z
    if _count_shaked > 0: return
    _is_shaked = (diff_x * diff_x + diff_y * diff_y + diff_z * diff_z > 1)

def timer12_tick(_):
    global _pind, _pina, _count_radio
    dict = {}
    dict["l"] = light.read()
    dict["s"] = sound.read()
    dict["e"] = ext.read()
    dict["x"] = accelerometer.get_x()
    dict["y"] = accelerometer.get_y()
    dict["z"] = accelerometer.get_z()
    dict["d"] = getTouchpad()
    dict["t"] = 1 if _is_shaked else 0
    if _count_radio < 5:
        _count_radio += 1
        if _count_radio == 5:
            r = radio.receive()
            if not r is None: dict["r"] = r
            _count_radio = 0
    for i in _pind.keys():
        dict["d" + str(i)] = MPythonPin(i, PinMode.IN).read_digital()
        time.sleep_ms(20)
    for i in _pina.keys():
        dict["a" + str(i)] = MPythonPin(i, PinMode.ANALOG).read_analog()
        time.sleep_ms(20)
    print(dict)

tim11 = machine.Timer(11)
tim12 = machine.Timer(12)

tim11.init(period=100, mode=machine.Timer.PERIODIC, callback=timer11_tick)
tim12.init(period=100, mode=machine.Timer.PERIODIC, callback=timer12_tick)

while True:
    run_code(input())
