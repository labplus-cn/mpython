# net_weather.py
# 天气信息提醒
# 功能：OLED显示当前从云端获取的天气信息

import urequests
import network
import socket
import time
import json
from labplus import *
 
# wifi参数 
SSID="fei"
PASSWORD="a1234567"
url = "http://www.weather.com.cn/data/sk/101020100.html"
wlan=None
s=None
oled = OLED() #定义一个oled实例

# 本函数实现wifi连接 
def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.disconnect()
  wlan.connect(ssid,passwd)
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)
  print("wifi connected......")
  return True
  
# 主程序入口  
# 1、wifi联网
  try:
    connectWifi(SSID,PASSWORD)
  except:
    wlan.disconnect()
    wlan.active(False) 
# 2、从网络获取天气信息  
rsp = urequests.get(url)
dict = rsp.json()  
print(dict)  #串口打印天气数据
# 3、OLED屏展示部分天气信息
oled.fill(0) #清屏
oled.show()
oled.drawStringAt("天气信息",35,0,1)
oled.drawStringAt("温度",0,20,1)
oled.drawStringAt("湿度",66,20,1)
oled.drawStringAt("气压",0,40,1)
oled.text(dict['weatherinfo']['temp'],35,27,1)
oled.text(dict['weatherinfo']['SD'] ,99,27,1) 
oled.text(dict['weatherinfo']['AP'],35,47,1) 
oled.show()
time.sleep(1)


