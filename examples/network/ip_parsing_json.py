from mpython import*
import json
import urequests           # urequests模块是一个用于网络访问的模块

mywifi=wifi()
mywifi.connectWiFi('yourESSID', 'yourpassword')    #连接 WiFi 网络

url_ip ="http://ip-api.com/json/"                  #添加请求地址

rsp=urequests.get(url_ip)                          #发送get请求

ipJson=rsp.text

ipDict=json.loads(ipJson)

oled.DispChar('国家:%s' % ipDict['country'],0,5)     #将国家信息显示到OLED显示屏上
oled.show()

oled.DispChar('城市:%s' % ipDict['city'],0,25)       #将城市信息显示到OLED显示屏上
oled.show()

oled.DispChar('IP:%s' % ipDict['query'],0,45)        #将IP地址信息显示到OLED显示屏上
oled.show()