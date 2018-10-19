# net_weather.py
# 天气信息提醒
# 功能：OLED显示当前从云端获取的天气信息

import upip
import network
import socket
import time
import json
from mpython import*
    
# wifi参数 
SSID="fei"
PASSWORD="a1234567"
url = "http://www.weather.com.cn/data/sk/101020100.html"
wlan=None
s=None


# 本函数实现wifi连接 
def connectWifi(ssid,passwd):
    global wlan
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid,passwd)
    print('connecting to network...')
    while(wlan.ifconfig()[0]=='0.0.0.0'):
        time.sleep_ms(1000)
        print('.',end="")
    print('WiFi Connection Successful,Network Config:%s' %str(wlan.ifconfig()))


connectWifi(SSID,PASSWORD)

#upip.install('micropython-urequests')
import urequests
# 2、从网络获取天气信息  
rsp = urequests.get(url)
dict = rsp.json()  
print(dict)  #串口打印天气数据
# 3、OLED屏展示部分天气信息

# 3、OLED屏展示部分天气信息
display.fill(0) #清屏
display.show()
display.DispChar("天气信息",35,0,1)
display.DispChar("温度",0,20,1)
display.DispChar("湿度",66,20,1)
display.DispChar("气压",0,40,1)
display.DispChar(dict['weatherinfo']['temp'],35,27,1)
display.DispChar(dict['weatherinfo']['SD'] ,99,27,1) 
display.DispChar(dict['weatherinfo']['AP'],35,47,1) 
display.show()
time.sleep(1)


