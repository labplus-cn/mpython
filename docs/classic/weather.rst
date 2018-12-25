获取网络气象
==========


例：通过网络获取气象信息，并将气象信息反馈到oled屏上。
::
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



.. image:: /images/classic/weather.jpg
    :align: center
    :scale: 60 %

使用前，导入mpython、json、urequests、Timer和天气图标seniverse模块（:download:`seniverse模块 </../examples/06.网络/心知天气/seniverse.py>`，将seniverse模块文件导入掌控板文件根目录）::

    from mpython import*
    import json
    import urequests
    from seniverse import *
    from machine import Timer

使用心知天气的免费天气API，您须先在心知天气官网注册一个账号，您将获得一个API密钥（key），API密钥（key）是用来验证API请求合法性的一个唯一字符串，通过API请求中的key参数传入::

    API_KEY = 'yourkey'

添加天气实况和多日天气预报的请求地址（更多请求可参考心知天气官网提供的天气数据选项）::

    url_now="https://api.seniverse.com/v3/weather/now.json"           #获取天气实况的请求地址
    url_daily="https://api.seniverse.com/v3/weather/daily.json"       #获取多日天气预报的请求地址

连接您的 WiFi 网络，需要设置您的WiFi名称和密码::

    mywifi=wifi()
    mywifi.connectWiFi('yourESSID','yourpassword')

定义天气实况和多日天气预报返回的结果::

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

.. Note::

    参数：``unit`` 为温度单位， ``c`` 为摄氏度℃。``start`` 为起始时间，如 ``-2`` 前天，``-1`` 昨天，``0`` 今天，``1`` 明天。``days`` 为天数，返回从start算起days天的结果。更多参数可参考心知天气官网。
    https://www.seniverse.com/doc


对返回的所有结果有选择性的输出，元组可以使用下标索引来访问元组中的值::

    today=dailyRsp['results'][0]['daily'][0]['date'][-5:]         #当前日期，显示“月-日”
    todayHigh=dailyRsp['results'][0]['daily'][0]['high']          #最高温度
    todaylow=dailyRsp['results'][0]['daily'][0]['low']            #最低温度

    nowText=nowRsp['results'][0]['now']['text']                   #天气现象文字
    nowTemper=nowRsp['results'][0]['now']['temperature']          #温度
    todayIco=nowRsp['results'][0]['now']['code']                  #天气现象图标
    city=nowRsp['results'][0]['location']['name']                 #地理位置


.. Note::

    元组的具体使用方法参考Python的元组。