import ntptime,network,time
from mpython import*
from machine import Timer
import analogClock


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
        pass
    print('WiFi Connection Successful,Network Config:%s' %str(wlan.ifconfig()))

connectWifi(SSID,PASSWORD)

ntptime.settime()

clock=analogClock.Clock(64,32,30)

def Refresh():
    clock.settime()
    clock.drawClock()
    display.show()
    clock.clear()
  
tim1 = Timer(1)

tim1.init(period=1000, mode=Timer.PERIODIC, callback=lambda _:Refresh()) 


