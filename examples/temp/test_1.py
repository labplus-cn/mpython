from machine import Pin, ADC, PWM, I2C, SPI, Timer, TouchPad
from handPy import *
import time

light = ADC(Pin(39))
sound = ADC(Pin(36))
ext   = ADC(Pin(34))

lightVal = "%d" % (light.read())
soundVal = "%d" % (sound.read())
extVal = "%d" % (ext.read())

while True:
  print('light:%d,Sound:%d' % (light.read(),sound.read()))
  display.DispChar('light = %d' % (light.read()), 0, 0)
  display.DispChar('Sound = %d' % (sound.read()), 0, 20)
  display.show()
  #print('T = %0.1f, P = %0.1fKPa, H = %0.1f' % (weather.temperature(), weather.pressure()/100, weather.humidity()))
  #print('x = %0.1f, y = %0.1f, z = %0.1f\n' % (acc.getX()*1000, acc.getY()*1000, acc.getZ()*1000))
  time.sleep_ms(20)











'''
def print_tem():  #定时器中断执行程序
  #print(temp)    #也可以这么写
  print('T = %0.1f' % (weather.temperature()))
  print('S = %d'%(sound.read()))
  print('x = %0.1f, y = %0.1f, z = %0.1f\n' % (acc.getX()*1000, acc.getY()*1000, acc.getZ()*1000))

# touchPad
touchPad_Y = TouchPad(Pin(14))
touchPad_T = TouchPad(Pin(12))
touchPad_H = TouchPad(Pin(13))
touchPad_O = TouchPad(Pin(4))
#light sound ext sensor
light = ADC(Pin(39))
sound = ADC(Pin(36))
ext   = ADC(Pin(34))
# weather sensor温湿度气压
weather = BME280()
# accelerator sensor
acc = MMA8653()
#打开定时器中断
tim1 = Timer(1)
#tim2 = Timer(2)

tim1.init(period=3000, mode=Timer.PERIODIC, callback=lambda t:print_tem())    #定时器1中断入口


#tim2.init(period=500, mode=Timer.PERIODIC, callback=lambda t:Rgb_Neopixel()) #定时器2中断入口

while True:
  oled.fill(0)
  oled.show()
#  buzz.freq(1000)
  buzz.duty(512)
  temp = "%0.1f" % (weather.temperature())
  hum = "%0.1f" % (weather.humidity())
  press = "%0.1f" % (weather.pressure()/100)
  lightVal = "%d" % (light.read())
  soundVal = "%d" % (sound.read())
  extVal = "%d" % (ext.read())

  oled.text("tem",0,0,1)
  oled.text(temp,32,0,1)
  oled.text("hum",0,10,1)
  oled.text(hum,32,10,1)
  oled.text("pre",0,20,1)
  oled.text(press,32,20,1)
  oled.text("lig",0,30,1)
  oled.text(lightVal,32,30,1)
  oled.text("sou",0,40,1)
  oled.text(soundVal,32,40,1)
  oled.text("ext",0,50,1)
  oled.text(extVal,32,50,1)
  buzz.duty(0)
  oled.show()
  time.sleep_ms(500)
'''












