import network
import time

# wifi参数 
SSID="yourSSID"            #wifi名称
PASSWORD="yourPASSWORD"         #密码


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
