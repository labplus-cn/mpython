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

    def get_time():
        t = time.localtime()
        print("%d年%d月%d日 %d:%d:%d"%(t[0],t[1],t[2],t[3],t[4],t[5]))   
        oled.DispChar("{}年{}月{}日" .format(t[0],t[1],t[2]),20,8)
        oled.DispChar("{}:{}:{}" .format(t[3],t[4],t[5]),38,25)
        oled.show()
        oled.fill(0)

    tim1 = Timer(1)

    tim1.init(period=1000, mode=Timer.PERIODIC, callback=lambda _:get_time()) 








