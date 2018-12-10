from umqtt.simple import MQTTClient
from mpython import *

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
    c = MQTTClient(CLIENT_ID, server,6002,username,password)
    c.set_callback(sub_cb)
    c.connect()
    print("Connected to %s" % server)
    try:
        while 1:
            c.wait_msg()
    finally:
        c.disconnect()

mywifi.connectWiFi("ssid","password")
main()