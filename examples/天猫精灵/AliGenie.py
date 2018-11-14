import network
import time
from mpython import *
# wifi参数 
SSID="yourSSID"            #wifi名称
PASSWORD="yourPSW"         #密码
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

def disConnectWifi():
    wlan.disconnect()
    wlan.active(False)
    print('disconnect...')

ConnectWifi()

import bigiot

from bigiot import Device

a = Device()

while not a.isCheckin():
    a.checkin('7947','ace154787')
    time.sleep(1)

display.DispChar('连接成功！',0,0)
display.show()

def say_cb(msg):
    if msg=='play':
        rgb.fill((50,0,0))      #掌控板开灯
        rgb.write()
        
    if msg=='stop':          #掌控板关灯
        rgb.fill((0,0,0))    
        rgb.write()
        
a.say_callback(say_cb)







