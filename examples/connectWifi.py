import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
  print('connecting to network...')
  wlan.connect('SSID', 'PASSWORD')   #连接到AP
    #'SSID'： WiFi账号名
    #'PASSWORD'：WiFi密码
  while not wlan.isconnected():
    pass
print('network config:', wlan.ifconfig())

