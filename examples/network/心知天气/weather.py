from mpython import*
import json
import urequests                    #用于网络访问的模块
from seniverse import *             #天气图标模块
from machine import Timer           #定时器模块

API_KEY = 'yourkey'                 #心知天气API密钥（key）

url_now="https://api.seniverse.com/v3/weather/now.json"           #获取天气实况的请求地址
url_daily="https://api.seniverse.com/v3/weather/daily.json"       #获取多日天气预报的请求地址

oled.DispChar('联网中...',40,25)     #OLED屏显示联网提示
oled.show()

mywifi=wifi()
mywifi.connectWiFi('yourESSID','yourpassword')          #连接 WiFi 网络

def nowWeather(apikey,location='ip',language='zh-Hans',unit='c'):         #设置天气实况返回的数据
    nowResult = urequests.get(url_now, params={
        'key': apikey,
        'location': location,
        'language': language,
        'unit': unit
    })
    json=nowResult.json()
    nowResult.close()
    return json

def dailyWeather(apikey,location='ip',language='zh-Hans',unit='c',start='0',days='5'):        #设置多日天气，只返回今日的数据
    dailyResult = urequests.get(url_daily, params={
        'key': apikey,
        'location': location,
        'language': language,
        'start': start,
        'days': days
    })
    json=dailyResult.json()
    dailyResult.close()
    return  json


def refresh():
    nowRsp=nowWeather(API_KEY)                 #通过API密钥获取天气实况
    dailyRsp=dailyWeather(API_KEY)             #通过API密钥获取多日天气预报

    today=dailyRsp['results'][0]['daily'][0]['date'][-5:]         #当前日期，显示“月-日”
    todayHigh=dailyRsp['results'][0]['daily'][0]['high']          #最高温度
    todaylow=dailyRsp['results'][0]['daily'][0]['low']            #最低温度

    nowText=nowRsp['results'][0]['now']['text']                   #天气现象文字
    nowTemper=nowRsp['results'][0]['now']['temperature']          #温度
    todayIco=nowRsp['results'][0]['now']['code']                  #天气现象图标
    city=nowRsp['results'][0]['location']['name']                 #地理位置

    oled.fill(0)
    oled.Bitmap(10,23,ico[todayIco],38,38,1)                   #显示当前天气现象图标
    oled.DispChar("%s,天气实况" %city,0,0)
    oled.DispChar(today,90,0)
    oled.DispChar("%s℃/%s" %(nowTemper,nowText),70,25)        #显示当前温度
    oled.DispChar("%s~%s℃" %(todaylow,todayHigh),70,45)       #显示今日最低、最高气温
    oled.show()

refresh()          #数据更新

tim1 = Timer(1)
tim1.init(period=1800000, mode=Timer.PERIODIC,callback=lambda _:refresh())      #定时，每半个钟刷新一次