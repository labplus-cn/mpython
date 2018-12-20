from umqtt.simple import MQTTClient
from mpython import *
from machine import Timer

# MQTT服务器地址域名为：183.230.40.39,不变
SERVER = "183.230.40.39"
#设备ID
CLIENT_ID = "deviceID"
#产品ID
username='productID'
#产品APIKey:
password='APIKey'

mywifi=wifi()

def sub_cb(topic, msg):

    print((topic, msg))
    if msg == b"on":
        rgb.fill((50,0,0))       #点亮红灯
        rgb.write()
    elif msg == b"off":        #灭灯
        rgb.fill((0,0,0))
        rgb.write()


def main(server=SERVER):
    #端口号为：6002
    c = MQTTClient(CLIENT_ID, server,6002,username,password,keepalive=10)    # 保持连接时间间隔设置10秒
    c.set_callback(sub_cb)
    c.connect()
    tim1 = Timer(1)           #创建定时器1
    tim1.init(period=2000, mode=Timer.PERIODIC,callback=lambda n:c.ping())   #  发送心跳包 ,保持连接  
    print("Connected to %s" % server)
    try:
        while 1:
            c.wait_msg()
    finally:
        c.disconnect()

mywifi.connectWiFi("ssid","password")
main()