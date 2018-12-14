from mpython import *
import music


music.play(music.PYTHON,wait=False)
loc = 0
width = 42
high = 4

X = 10
Y = 48
rad=5

a = 1
b = 1

start_flag = False
Start = True
END = False

while True:
  if Start:
    if button_a.value() == 0 and  button_b.value() == 1 :
      start_flag = True
      loc = loc - 2
      if loc < 0:
        loc = 0
    if button_a.value() == 1 and  button_b.value() == 0 :
      start_flag = True
      loc = loc + 2
      if loc > 128-width:
        loc = 128-width
    if start_flag:
      X = X + a
      Y = Y + b
      if X >= 128-rad:
        a = a * -1
      if X <= rad:
        a = a * -1
      if Y >= 50:
        b = b * -1
      if Y <= rad:
        b = b * -1
      if Y >= 49:
        if X > loc + (width+rad) or X < loc-rad:
          music.play(music.BADDY,wait=False)
          start_flag = False
          Start = False
          END = True
    oled.fill(0)
    oled.fill_rect(loc,55,width,high,1)
    oled.fill_circle(X,Y,rad,1)
    oled.show()
  if END:
    oled.fill(0)
    oled.DispChar("失败!",50,25)
    oled.show()













