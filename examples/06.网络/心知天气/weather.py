import json
from mpython import*
import urequests
import seniverse
from machine import Timer

API_KEY = '4w06fmyn1gxuvy88'


url_now="https://api.seniverse.com/v3/weather/now.json"
url_daily="https://api.seniverse.com/v3/weather/daily.json"

oled.DispChar('联网中...',40,25)
oled.show()

mywifi=wifi()
mywifi.connectWiFi('ssid','password')

def nowWeather(apikey,location='ip',language='zh-Hans',unit='c'):
    nowResult = urequests.get(url_now, params={
        'key': apikey,
        'location': location,
        'language': language,
        'unit': unit
    }) 
    return nowResult.json()

def dailyWeather(apikey,location='ip',language='zh-Hans',unit='c',start='0',days='5'):
    dailyResult = urequests.get(url_daily, params={
        'key': apikey,
        'location': location,
        'language': language,
        'start': start,
        'days': days
    })
    return  dailyResult.json()


def refresh():
    nowRsp=nowWeather(API_KEY)
    dailyRsp=dailyWeather(API_KEY)

    today=dailyRsp['results'][0]['daily'][0]['date'][-5:]
    todayHigh=dailyRsp['results'][0]['daily'][0]['high']
    todaylow=dailyRsp['results'][0]['daily'][0]['low']

    nowText=nowRsp['results'][0]['now']['text']
    nowTemper=nowRsp['results'][0]['now']['temperature']
    todayIco=nowRsp['results'][0]['now']['code']
    city=nowRsp['results'][0]['location']['name']

    oled.fill(0)
    oled.Bitmap(10,23,ico[todayIco],38,38,1)
    oled.DispChar("%s,天气实况" %city,0,0)
    oled.DispChar(today,90,0)
    oled.DispChar("%s℃/%s" %(nowTemper,nowText),70,25)
    oled.DispChar("%s~%s℃" %(todaylow,todayHigh),70,45)
    oled.show()
    print('refresh Weather!')

refresh()

tim1 = Timer(1)               
tim1.init(period=1800000, mode=Timer.PERIODIC,callback=lambda _:refresh())       




