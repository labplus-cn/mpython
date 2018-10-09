
from machine import Pin, ADC, PWM, I2C,TouchPad,SPI,Timer,UART
from mpython import *
import machine
import time,ubinascii

# analog 
ext   = ADC(Pin(34))
P2   = ADC(Pin(35))
P1   = ADC(Pin(32))
P0   = ADC(Pin(33))

# Pin test

pwm_P8=PWM(Pin(26), freq = 20,duty = 512) 
pwm_P9=PWM(Pin(25), freq = 20,duty = 512)   
pwm_P13=PWM(Pin(18),freq = 20, duty = 512) 
pwm_P16=PWM(Pin(5), freq = 20,duty = 512)   
pwm_P14=PWM(Pin(19),freq = 20, duty = 512)   
pwm_P15=PWM(Pin(21),freq = 20, duty = 512)


# touchPad
touchPad_Y = TouchPad(Pin(14))
touchPad_T = TouchPad(Pin(12))
touchPad_H = TouchPad(Pin(13))
touchPad_O = TouchPad(Pin(15))
touchPad_N = TouchPad(Pin(4))

def btn_A_irq(_):
  if button_a.value() == 0:
    buzz.on()
  else:
    buzz.off()

def btn_B_irq(_):
  if button_b.value() == 0:
    buzz.on()
  else:
    buzz.off()
    
	
def testdrawline():
 
  for i in range(0,64):
    display.line(0,0,i*2,63,1)
    display.show()
  for i in range(0,32):
    display.line(0,0,127,i*2,1)
    display.show()
  time.sleep_ms(50)
  display.fill(0)
  display.show()
  for i in range(0,32):
    display.line(0,63,i*4,0,1)
    display.show()
  for i in range(0,16):
    display.line(0,63,127,(64-4*i)-1,1)
    display.show()
  time.sleep_ms(50)
  display.fill(0)
  display.show()
  for i in range(1,32):
    display.rect(2*i,2*i,(128-4*i)-1,(64-2*i)-1,1)
    display.show()

  
def Print_Serial_num():
  u = UART(2, baudrate=115200, bits=8, parity=None, stop=1, rx=26, tx=25, timeout = 10)
  display.fill(1)
  display.show()
  while True:
    
    if u.readline()=='COM:Give me string'.encode():
      
      time.sleep_ms(50)
      u.write(machine_id[:6]+'\n')
      u.write(machine_id[6:]+'\n\r')
      u.write(machine_id[:6]+'\n')
      u.write(machine_id[6:]+'\n\r')
 

button_a.irq(btn_A_irq)
button_b.irq(btn_B_irq)


tim1 = Timer(1)

# pixles

color_index = 0
color = ((32, 0, 0), (0, 32, 0), (0, 0, 32))

def Rgb_Neopixel():
  global color_index,color
  for i in range(0, 3):
    rgb[i] = color[color_index]
  rgb.write()
  color_index = color_index + 1
  color_index = color_index % 3
  
machine_id = ubinascii.hexlify(machine.unique_id()).decode().upper()

 # pixles timer
tim1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:Rgb_Neopixel()) 


#oled full pixel test
testdrawline()
display.fill(0)
display.show()


while True:
  if ext.read()==0:
    time.sleep_ms(1000)
    if ext.read()==0:
      Print_Serial_num()
      
  print('Y:%d, T:%d, H:%d, O:%d, N:%d' % (touchPad_Y.read(),touchPad_T.read(),touchPad_H.read(),touchPad_O.read(),touchPad_N.read()))
  print('P0:%d, P1:%d ,P2:%d, P3/ext:%d' % (P0.read(),P1.read(),P2.read(),ext.read()))
  print('light:%d,Sound:%d' % (light.read(),sound.read()))
  print('x = %.2f, y = %0.2f, z = %.2f ' % (accelerometer.get_x(), accelerometer.get_y(), accelerometer.get_z()))
  display.rect(0,0,128,64,1)
  display.DispChar('声音:%d,光线:%d' % (sound.read(),light.read()), 3, 3)
  display.DispChar('加速度:%.1f,%.1f,%.1f' %(accelerometer.get_x(), accelerometer.get_y(), accelerometer.get_z()),3,16)
  display.DispChar('id:%s' %machine_id,3,42)
  display.show()
  display.fill(0)












































