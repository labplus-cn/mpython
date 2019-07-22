from machine import Pin, SPI
import machine, sdcard, os

# 创建SPI对象,spi引脚如下述
spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(Pin.P13), mosi=Pin(Pin.P15), miso=Pin(Pin.P14))
# 构建SDCard对象
sd = sdcard.SDCard(spi, Pin(Pin.P16))
# 挂载sd到 '/sd' 路径
os.mount(sd, '/sd')

# 创建文件并写数据
with open("/sd/test.txt", "w") as f:
    f.write("Hello world!\r\n")
