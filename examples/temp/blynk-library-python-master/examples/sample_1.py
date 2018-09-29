import BlynkLib
import network
import time

WIFI_SSID  = 'fei'
WIFI_PW  = 'a1234567'
BLYNK_AUTH = '58ad927f148d4adfa1498e7a1f6b93df'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
  print('connecting to network...')
  wlan.connect(WIFI_SSID,WIFI_PW)   #连接到AP
     #'SSID'： WiFi账号名
     #'PASSWORD'：WiFi密码
  while not wlan.isconnected():
    pass
print('network config:', wlan.ifconfig())



# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Register virtual pin handler
@blynk.VIRTUAL_WRITE(3)
def v3_write_handler(value):
    print('Current slider value: {}'.format(value))

# Start Blynk (this call should never return)
blynk.run()
