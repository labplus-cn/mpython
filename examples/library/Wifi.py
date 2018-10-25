import network
import time

# wifi参数 
SSID="yourssid"            #wifi名称
PASSWORD="yourpsw"         #密码
wlan=None

# 本函数实现wifi连接 
def Connect(ssid=SSID,passwd=PASSWORD):
    global wlan
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid,passwd)
  
    while(wlan.ifconfig()[0]=='0.0.0.0'):
        time.sleep(1)
        print('Connecting to network...')
    print('WiFi Connection Successful,Network Config:%s' %str(wlan.ifconfig()))

def disConnect():
    wlan.disconnect()
    wlan.active(False)
    print('disconnect...')
