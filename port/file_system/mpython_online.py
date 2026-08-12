# -*- coding:utf-8 -*-
# @Time     : 2022/08/08
# @Author   : Wu Wen Jie(6692776@qq.com)
# @FileName : mpython_online.py
# @Description : A transfer protocol between mPython board and Labplus software
# @Version  : 1.1

from mpython import *
from bluebit import *
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
oled.DispChar("\u4e92\u52a8\u6a21\u5f0f", 41, 23, 1)
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

_is_shaked = _is_thrown = False
_last_x = _last_y = _last_z = _count_shaked = _count_thrown = _count_radio = 0
_pind = {}
_pina = {}
_i2c = {}

# I2C 传感器定义
_ultrasonic = None  # 超声波传感器
_sht20 = None  # 温湿度传感器
_rfid = None  # RFID射频卡
_color = None  # 颜色传感器
_barometric = None  # 气压传感器
_force = None  # 力传感器
_voltage = None  # 电压传感器
_current = None  # 电流传感器
_ph = None  # PH值传感器
_conductivity = None  # 电导率传感器
_magnetic = None  # 磁场传感器
_gesture = None  # 手势传感器

# 超声波
def init_ultrasonic():
    global _i2c
    _i2c['iu'] = None

def del_ultrasonic():
    global _i2c, _ultrasonic
    del _i2c['iu']
    _ultrasonic = None

# 温湿度
def init_sht20():
    global _i2c
    _i2c['ist'] = None

def del_sht20():
    global _i2c, _sht20
    del _i2c['ist']
    del _i2c['ish']
    _sht20 = None

# RFID
def init_rfid():
    global _i2c
    _i2c['irs'] = None

def del_rfid():
    global _i2c, _rfid
    del _i2c['irs']
    del _i2c['irv']
    _rfid = None

def rfid_increment(_value):
    global _rfid
    if _rfid is None: return
    _rf = _rfid.scanning()
    if _rf: _rf.increment(_value)

def rfid_decrement(_value):
    global _rfid
    if _rfid is None: return
    _rf = _rfid.scanning()
    if _rf: _rf.decrement(_value)

# 颜色
def init_color():
    global _i2c
    _i2c['icr'] = None

def del_color():
    global _i2c, _color
    del _i2c['icr']
    del _i2c['icg']
    del _i2c['icb']
    del _i2c['ich']
    del _i2c['ics']
    del _i2c['icv']
    _color = None

# 气压
def init_barometric():
    global _i2c
    _i2c['ibp'] = None

def del_barometric():
    global _i2c, _barometric
    del _i2c['ibp']
    del _i2c['ibt']
    _barometric = None

# 力
def init_force():
    global _i2c
    _i2c['if0'] = None

def del_force():
    global _i2c, _force
    del _i2c['if0']
    _force = None

# 电压
def init_voltage():
    global _i2c
    _i2c['iv0'] = None

def del_voltage():
    global _i2c, _voltage
    del _i2c['iv0']
    _voltage = None

# 电流
def init_current():
    global _i2c
    _i2c['ia0'] = None

def del_current():
    global _i2c, _current
    del _i2c['ia0']
    _current = None

# PH
def init_ph():
    global _i2c
    _i2c['ih0'] = None

def del_ph(_index):
    global _i2c, _ph
    del _i2c['ih0']
    _ph = None

# 电导率
def init_conductivity():
    global _i2c
    _i2c['id0'] = None

def del_conductivity():
    global _i2c, _conductivity
    del _i2c['id0']
    _conductivity = None

# 磁场
def init_magnetic():
    global _i2c
    _i2c['im0'] = None

def del_magnetic():
    global _i2c, _magnetic
    del _i2c['im0']
    _magnetic = None

# 手势
def init_gesture():
    global _i2c
    _i2c['ig'] = None

def del_gesture():
    global _i2c, _gesture
    del _i2c['ig']
    _gesture = None

# ext = ADC(Pin(34))

def timer11_tick(_):
    global _is_shaked, _is_thrown, _last_x, _last_y, _last_z, _count_shaked, _count_thrown
    if _is_shaked:
        _count_shaked += 1
        if _count_shaked == 5: _count_shaked = 0
    if _is_thrown:
        _count_thrown += 1
        if _count_thrown == 10: _count_thrown = 0
    x=accelerometer.get_x(); y=accelerometer.get_y(); z=accelerometer.get_z()
    if _count_thrown == 0: _is_thrown = (x * x + y * y + z * z < 0.25)
    if _last_x == 0 and _last_y == 0 and _last_z == 0:
        _last_x = x; _last_y = y; _last_z = z; return
    diff_x = x - _last_x; diff_y = y - _last_y; diff_z = z - _last_z
    _last_x = x; _last_y = y; _last_z = z
    if _count_shaked > 0: return
    _is_shaked = (diff_x * diff_x + diff_y * diff_y + diff_z * diff_z > 1)
    
def timer13_tick(_):
    global _i2c, _ultrasonic, _rfid, _sht20, _color, _barometric, _force, _voltage, _current, _ph, _conductivity, _magnetic, _gesture
    if "iu" in _i2c:
        if _ultrasonic is None:
            _ultrasonic = Ultrasonic()
        else:
            _i2c["iu"] = _ultrasonic.distance()
    if "ist" in _i2c:
        if _sht20 is None:
            _sht20 = SHT20()
        else:
            _i2c["ist"] = _sht20.temperature()
            _i2c["ish"] = _sht20.humidity()
    if "irs" in _i2c:
        if _rfid is None:
            _rfid = Scan_Rfid()
        else:
            _rf = _rfid.scanning()
            if _rf:
                _b = _rf.get_balance()
                if _b == 0: _rf.set_purse()
                _i2c["irs"] = _rf.serial_number()
                _i2c["irv"] = _b
            else:
                _i2c["irs"] = None
                _i2c["irv"] = None
    if "icr" in _i2c:
        if _color is None:
            _color = Color()
        else:
            _rgb = _color.getRGB()
            _hsv = _color.getHSV()
            _i2c["icr"] = _rgb[0]
            _i2c["icg"] = _rgb[1]
            _i2c["icb"] = _rgb[2]
            _i2c["ich"] = _hsv[0]
            _i2c["ics"] = _hsv[1]
            _i2c["icv"] = _hsv[2]
    if "ibp" in _i2c:
        if _barometric is None:
            _barometric = Barometric()
        else:
            _i2c["ibp"] = _barometric.pressure()
            _i2c["ibt"] = _barometric.temperature()
    if "id0" in _i2c:
        if _conductivity is None:
            _conductivity = DelveBit(0x6C)
        else:
            _i2c["id0"] = _conductivity.common_measure()
    if "iv0" in _i2c:
        if _voltage is None:
            _voltage = DelveBit(0x6D)
        else:
            _i2c["iv0"] = _voltage.common_measure()
    if "ia0" in _i2c:
        if _current is None:
            _current = DelveBit(0x6E)
        else:
            _i2c["ia0"] = _current.common_measure()
    if "if0" in _i2c:
        if _force is None:
            _force = DelveBit(0x6F)
        else:
            _i2c["if0"] = _force.common_measure()
    if "ih0" in _i2c:
        if _ph is None:
            _ph = DelveBit(0x71)
        else:
            _i2c["ih0"] = _ph.common_measure()
    if "im0" in _i2c:
        if _magnetic is None:
            _magnetic = DelveBit(0x72)
        else:
            _i2c["im0"] = _magnetic.common_measure()
    if "ig" in _i2c:
        if _gesture is None:
            _gesture = Gesture()
        else:
            _i2c["ig"] = _gesture.readGesture()

def timer12_tick(_):
    global _pind, _pina, _count_radio
    dict = {}
    dict["l"] = light.read()
    dict["s"] = sound.read()
    # dict["e"] = ext.read()
    dict["x"] = accelerometer.get_x()
    dict["y"] = accelerometer.get_y()
    dict["z"] = accelerometer.get_z()
    dict["d"] = getTouchpad()
    dict["t"] = 2 if _is_thrown else 1 if _is_shaked else 0
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
    dict.update(_i2c)
    print(dict)

tim11 = machine.Timer(11)
tim12 = machine.Timer(12)
tim13 = machine.Timer(13)

tim11.init(period=100, mode=machine.Timer.PERIODIC, callback=timer11_tick)
tim13.init(period=1000, mode=machine.Timer.PERIODIC, callback=timer13_tick)
tim12.init(period=100, mode=machine.Timer.PERIODIC, callback=timer12_tick)

while True:
    run_code(input())
