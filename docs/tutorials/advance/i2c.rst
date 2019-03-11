I2C
===============

I²C（Inter-Integrated Circuit）字面上的意思是集成电路之间，它其实是I²C Bus简称。I2C总线类型是由飞利浦半导体公司在八十年代初设计出来的一种简单、双向、二线制、同步串行总线，主要是用来连接整体电路(ICS)

I2C协议是多个设备仅使用两条线（时钟和数据线）相互通信的一种方式。任何设备都可以是控制I2C时钟和数据线以与其他设备通信的主设备。
每个I2C器件都分配有一个唯一的地址，用于在读写操作期间识别它。当设备看到其在I2C总线上发送的地址时，它会响应请求，当它看到不同的地址时，它会忽略它。
使用唯一地址，许多设备可以共享相同的I2C总线而不会产生干扰。



sht20温湿度模块的示例::


    from mpython import *

    i2c = I2C(scl=Pin(Pin.P19), sda=Pin(Pin.P20),freq=100000)      
                                                                                            
    def temperature():
        i2c.writeto(0x40,b'\xf3',False)
        sleep_ms(70)
        t=i2c.readfrom(0x40, 2)
        return -46.86+175.72*(t[0]*256+t[1])/65535

    def humidity():
        i2c.writeto(0x40,b'\xf5',False)
        sleep_ms(25)
        t=i2c.readfrom(0x40, 2)
        return -6+125*(t[0]*256+t[1])/65535

