from simple import MQTTClient
from mpython import *
import time,network

# MQTT服务器地址域名为：183.230.40.39,不变
SERVER = "183.230.40.39"
#设备ID
CLIENT_ID = "deviceID"
#产品ID
username='productID'
#产品APIKey:
password='APIKey'


# wifi参数 
SSID="yourSSID"            #wifi名称
PASSWORD="yourPWD"         #密码
wlan=None

# 本函数实现wifi连接 
def ConnectWifi(ssid=SSID,passwd=PASSWORD):
    global wlan
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid,passwd)
  
    while(wlan.ifconfig()[0]=='0.0.0.0'):
        time.sleep(1)
        print('Connecting to network...')
    print('WiFi Connection Successful,Network Config:%s' %str(wlan.ifconfig()))


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
        
ConnectWifi()      
main()
