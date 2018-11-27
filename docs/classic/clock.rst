数字模拟时钟
==========

掌控板上集成1.3英寸OLED显示屏，支持显示文字、图案等内容。除此之外，掌控板板载ESP-WROOM-32双核芯片，支持WiFi通信。我们可以将OLED显示屏结合WiFi功能制作数字模拟时钟，通过WiFi连接网络来获取国际标准时间，将时间显示在OLED显示屏上。

数字时钟
+++++++

:: 

    import ntptime,network     # 导入国际标准时间、网络模块
    from mpython import*
    from machine import Timer  # 导入计时模块

    mywifi=wifi()
    mywifi.connectWiFi("ssid","password")  # ssid 指WiFi网络名称，password指WiFi密码

    try:
        ntptime.settime()
    except OSError :
        oled.DispChar("ntp链接超时,请重启!",0,20)    #当服务器获取时间超时，在坐标（0,20）位置显示相关内容予以提醒
        oled.show()
    else:

        def get_time(_):   #定义时钟刷屏时间
            t = time.localtime()
            print("%d年%d月%d日 %d:%d:%d"%(t[0],t[1],t[2],t[3],t[4],t[5]))  
            oled.DispChar("{}年{}月{}日" .format(t[0],t[1],t[2]),20,8)
            oled.DispChar("{}:{}:{}" .format(t[3],t[4],t[5]),38,25)
            oled.show()
            oled.fill(0)  #清除时钟，否则时间会重叠显示在OLED显示屏上

        tim1 = Timer(1) 

        tim1.init(period=1000, mode=Timer.PERIODIC, callback=get_time)  

数字时钟是取代模拟表盘而以数字显示的钟表，它用数字显示此时的时间，案例中的数字时钟能同时显示时，分，秒。
显示时间，需要先连接网络，因此需要设置WiFi名称及其密码：
::

    mywifi=wifi()
    mywifi.connectWiFi("ssid","password")

.. admonition:: 提示

 “ssid”指可连接的WiFi名称，“password”指所连接WiFi的密码，您可以根据实际情况来设置WiFi连接。关于WiFi连接，可参见 :mod:`network` 模块了解更多使用方法。为了更加清晰地了解网络连接的情况，您可以设置当连接网络出现超时时，显示一些提示语：

::

    except OSError :
        oled.DispChar("ntp链接超时,请重启!",0,20)    #当服务器获取时间超时，在坐标（0,20）位置显示提示语予以提醒
        oled.show()


设置时间显示格式：
::
    time.localtime([secs])

将一个以秒计的时间转换为一个包含下列内容的8元组：年、月、日、小时、分钟、秒、一周中某日、一年中某日。若未提供秒或为None，则使用RTC时间。

* 年包括世纪（例如2018）
* 月为 1-12 
* 日为 1-31 
* 小时为 0-23 
* 分钟为 0-59 
* 秒钟 0-59 
* 周中某日为 0-6 （对应周一到周日） 
* 年中某日为 1-366 

时间显示：
::
    oled.DispChar("{}年{}月{}日" .format(t[0],t[1],t[2]),20,8)
    oled.DispChar("{}:{}:{}" .format(t[3],t[4],t[5]),38,25)
在坐标（20,8）位置显示年、月、日：t[0]对应年、t[1]对应月，t[2]对应日；在坐标（38,25）位置显示时、分、秒：t[3]对应时，t[4]对应分，t[5]对应秒。

计时模式：
::
    tim1.init(period=1000, mode=Timer.PERIODIC, callback=get_time)  
将时间初始化为以1000毫秒为单位的计时模式，并返回所获取的时间。

模拟时钟
+++++++

::
    
    import ntptime,network   
    from mpython import*
    from machine import Timer

    mywifi=wifi()
    mywifi.connectWiFi("ssid","password")

    try:
        ntptime.settime()
    except OSError :
        oled.DispChar("ntp链接超时,请重启!",0,20)
        oled.show()
    else:
        clock=UI.Clock(64,32,30)      # UI 中的clock类 x、y、r

        def Refresh(_):
            clock.settime()
            clock.drawClock()
            display.show()
            clock.clear()
        
        tim1 = Timer(1)

        tim1.init(period=1000, mode=Timer.PERIODIC, callback=Refresh) 

.. Hint:: 维护中,敬请期待！

.. admonition:: 编辑备忘

    案例大致说明：分数字时钟和模拟钟表时钟两部分。结合结构,可将掌控板拓展为智能手表。