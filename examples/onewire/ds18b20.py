from machine import Pin
import onewire 
import time, ds18x20
# 创建one wire总线,引脚为P0
ow = onewire.OneWire(Pin(Pin.P0)) 
# 实例DS18X20类
ds = ds18x20.DS18X20(ow)
# 扫描总线上的DS18B20，获取设备列表
roms = ds.scan()  

while True:
    # 转换温度值,每次获取温度前必须调用convert_temp，否则温度数据不会更新
    ds.convert_temp()
    # convert_temp后至少等待750ms
    time.sleep_ms(750)
    # 返回总线的上ds18b20设备的温度值
    for rom in roms:
        print('Device %s temperature is %d'%(bytes(rom),ds.read_temp(rom)))