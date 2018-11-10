import time,ntptime,network
from mpython import*
from machine import Timer

# wifi参数 
SSID="yourSSID"            #wifi名称
PASSWORD="yourPSW"         #密码

# 本函数实现wifi连接 
def connectWifi(ssid,passwd):
    global wlan
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid,passwd)
    print('connecting to network...')
    while(wlan.ifconfig()[0]=='0.0.0.0'):
        time.sleep(1)
        print('Connecting to network...')
    print('WiFi Connection Successful,Network Config:%s' %str(wlan.ifconfig()))

connectWifi(SSID,PASSWORD)

ntptime.settime()
def get_time():
    t = time.localtime()
    print("%d年%d月%d日 %d:%d:%d"%(t[0],t[1],t[2],t[3],t[4],t[5]))   
    display.DispChar("{}年{}月{}日" .format(t[0],t[1],t[2]),20,8)
    display.DispChar("{}:{}:{}" .format(t[3],t[4],t[5]),38,25)
    display.show()
    display.fill(0)

tim1 = Timer(1)

tim1.init(period=1000, mode=Timer.PERIODIC, callback=lambda _:get_time()) 








