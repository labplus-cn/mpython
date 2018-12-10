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
    clock=UI.Clock(64,32,30)

    def Refresh():
        clock.settime()
        clock.drawClock()
        display.show()
        clock.clear()
    
    tim1 = Timer(1)

    tim1.init(period=1000, mode=Timer.PERIODIC, callback=lambda _:Refresh()) 


