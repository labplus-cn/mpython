import gc
import uos
from flashbdev import bdev
from neopixel import NeoPixel
import machine 
# 上电后立即关闭rgb,防止随机灯亮问题
_rgb = NeoPixel(machine.Pin(17, machine.Pin.OUT), 3, 3, 1,0.1)
_rgb.write()
del _rgb

try:
    if bdev:
        uos.mount(bdev, "/")
except OSError:
    import inisetup
    vfs = inisetup.setup()

gc.collect()
