# labplus mPython-box library
# MIT license; Copyright (c) 2018 labplus

# mpython-box buildin periphers drivers

# history:
# V1.0 zhaohuijiang 

from machine import Pin, ADC
import time, ujson
from mpython_classroom_kit_driver import K210,K210Error
from mpython import i2c
import ubinascii
# human infrared
pir = Pin(21, mode=Pin.IN, pull=None)

# slide POT
slider_res = ADC(Pin(34))
slider_res.atten(slider_res.ATTN_11DB)

k210 = K210()


def get_distance():
    """超声波,范围2~340cm"""
    return k210.get_distance()


def get_key():
    """方向按键,返回按键列表"""
    key_map = {0: 'left', 1: 'right', 2: 'up', 3: 'down', 4: 'ok'}
    key_set = set()
    _key = k210.get_key()
    if _key:
        for i in range(5):
            if ((_key >> i) & 0x01):
                key_set.add(key_map[i])
    return key_set

def set_motor(speed):
    """马达,范围±100"""
    if speed < -100 or speed > 100:
            raise ValueError("Invalid value,Range in -100~100")
    return k210.set_motor(speed)

def k210_reset():
    k210.reset()

"""k210文件传送"""
def filefrom_k210(source,target=None):
    k210.file_open(source,'rb')
    if target ==None:
        target = source
    with open(target,'wb') as temp:
        while True:
            base_64_data= k210.file_read(512*3)
            churk=ubinascii.a2b_base64(base_64_data)
            if churk != b'':
                temp.write(churk)
            else:
                break
    k210.file_close()

def fileto_k210(source,target=None):
    if target ==None:
        target = source
    k210.file_open(target,'wb')
    with open(source,'rb') as temp:
        while True:
            buf = temp.read(512*3)
            base64_data = ubinascii.b2a_base64(buf).strip()
            if  base64_data != b'':
                k210.file_write(base64_data)
            else:
                break
    k210.file_close()


class Model(object):

    def __init__(self):
        self.FACE_YOLO = 1
        self.CLASS_20_YOLO = 2
        self.MNIST_NET = 3
        self.CLASS_1000_NET = 4
        self.YOLO2 = 1
        self.MOBILENET = 2

    def select_model(self, builtin=None):
        """内置模型选择"""
        k210.select_model(builtin)

    def load_model(self, path, model_type, classes, anchor=None):
        """加载外部模型"""
        k210.load_model(path=path, model_type=model_type,
                        classes=classes, anchor=anchor)

    def detect_yolo(self):
        """yolo模型应用"""
        return k210.detect_yolo()

    def predict_net(self):
        """MobileNet模型预测"""
        return k210.predict_net()

    def deinit_yolo(self):
        """yolo释放"""
        k210.deinit_yolo()

    def deinit_net(self):
        """net释放"""
        k210.deinit_net()
    


class LCD(object):
    BLACK = 0
    NAVY = 15
    DARKGREEN = 992
    DARKCYAN = 1007
    MAROON = 30720
    PURPLE = 30735
    OLIVE = 31712
    LIGHTGREY = 50712
    DARKGREY = 31727
    BLUE = 31
    GREEN = 2016
    RED = 63488
    MAGENTA = 63519
    YELLOW = 65504
    WHITE = 65535
    ORANGE = 64800
    GREENYELLOW = 45029
    PINK = 63519

    def init(self, *args,**kws):
        k210.lcd_init(*args,**kws)

    def display(self,**kws):
        k210.lcd_display(**kws)

    def clear(self, color=0):
        k210.lcd_clear(color=color)

    def draw_string(self, *args):
        k210.lcd_draw_string(*args)


class Camera(object):
    RGB565 = 2
    GRAYSCALE = 4
    def reset(self):
        k210.camera_reset()

    def set_cam_led(self, on_off):
        k210.set_cam_led(on_off)

    def run(self,*arg):
        k210.camera_run(*arg)

    def snapshot(self):
        k210.camera_snapshot()

    def set_pixformat(self,*arg):
        k210.camera_set_pixformat(*arg)

    def set_contrast(self,*arg):
        if arg[0] < -2 or arg[0] > 2:
            raise ValueError("Invalid value,Range in -2~2")
        k210.camera_set_contrast(*arg)

    def set_brightness(self,*arg):
        if arg[0] < -2 or arg[0] > 2:
            raise ValueError("Invalid value,Range in -2~2")
        k210.camera_set_brightness(*arg)

    def set_saturation(self,*arg):
        if arg[0] < -2 or arg[0] > 2:
            raise ValueError("Invalid value,Range in -2~2")
        k210.camera_set_saturation(*arg)

    def set_auto_gain(self,*arg,**kw):
        k210.camera_set_auto_gain(*arg,**kw)

    def set_auto_whitebal(self,*arg):
        k210.camera_set_auto_whitebal(*arg)

    def set_windowing(self,*arg):
        k210.camera_set_windowing(*arg)

    def set_hmirror(self,*arg):
        k210.camera_set_hmirror(*arg)

    def set_vflip(self,*arg):
        k210.camera_set_vflip(*arg)

    def skip_frames(self,*arg,**kw):
        k210.camera_skip_frames(*arg,**kw)


class Img(object):

    def load(self, *args, **kws):
        k210.image_load(*args, **kws)

    def width(self):
        return int(k210.image_width())

    def hight(self):
        return int(k210.image_hight())

    def format(self):
        return int(k210.image_format())

    def size(self):
        return int(k210.image_size())

    def get_pixel(self, *args, **kws):
        temp = k210.image_get_pixel(*args, **kws)
        if temp:
            return tuple(temp)

    def set_pixel(self, *args, **kws):
        k210.image_set_pixel(*args, **kws)

    def mean_pool(self, *args, **kws):
        k210.image_mean_pool(*args, **kws)

    def to_grayscale(self):
        k210.image_to_grayscale()

    def to_rainbow(self):
        k210.image_to_rainbow()

    def copy(self,*args, **kws):
        k210.image_copy(*args, **kws)

    def save(self,*args, **kws):
        k210.image_save(*args, **kws)

    def clear(self):
        k210.image_clear()

    def draw_line(self,*args, **kws):
        k210.image_draw_line(*args, **kws)

    def draw_rectangle(self,*args, **kws):
        k210.image_draw_rectangle(*args, **kws)

    def draw_circle(self,*args, **kws):
        k210.image_draw_circle(*args, **kws)

    def draw_string(self,*args, **kws):
        k210.image_draw_string(*args, **kws)

    def draw_cross(self,*args, **kws):
        k210.image_draw_cross(*args, **kws)

    def draw_arrow(self,*args, **kws):
        k210.image_draw_arrow(*args, **kws)

    def binary(self,*args, **kws):
        k210.image_binary(*args, **kws)

    def invert(self):
        k210.image_invert()

    def erode(self,*args, **kws):
        k210.image_erode(*args, **kws)

    def dilate(self,*args, **kws):
        k210.image_dilate(*args, **kws)

    def negate(self,*args, **kws):
        k210.image_negate(*args, **kws)

    def mean(self,*args, **kws):
        k210.image_mean(*args, **kws)

    def mode(self,*args, **kws):
        k210.image_mode(*args, **kws)

    def median(self,*args, **kws):
        k210.image_median(*args, **kws)

    def midpoint(self,*args, **kws):
        k210.image_midpoint(*args, **kws)

    def cartoon(self,*args, **kws):
        k210.image_cartoon(*args, **kws)

    def conv3(self,*args, **kws):
        k210.image_conv3(*args, **kws)

    def gaussian(self,*args, **kws):
        k210.image_gaussian(*args, **kws)

    def bilateral(self,*args, **kws):
        k210.image_bilateral(*args, **kws)

    def linpolar(self,*args, **kws):
        k210.image_linpolar(*args, **kws)

    def logpolar(self,*args, **kws):
        k210.image_logpolar(*args, **kws)
        
    def rotation_corr(self,*args, **kws):
        k210.image_rotation_corr(*args, **kws)

    def find_blobs(self,*args, **kws):
        return k210.image_find_blobs(*args, **kws)

    def skip_frames(self,*arg,**kw):
        k210.camera_skip_frames(*arg,**kw)


lcd = LCD()
camera = Camera()
model = Model()
image = Img()
