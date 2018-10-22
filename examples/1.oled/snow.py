from mpython import *
from time import sleep_ms
from random import randint
from collections import deque

class Ball():
    def __init__(self):
        self.x = randint(0,128)
        self.y = 0
        
        self.vx = 0
        self.vy = randint(1,5)
        
    def run(self):
        self.update()
        self.display()
        
    def update(self):
       
        
        self.x += self.vx
        self.y += self.vy
        if self.x > 128 or self.x < 0:
            self.x = randint(0,128)
        if self.y > 64 or self.y < 0:
            self.y = 0
            
    def display(self):
        display.pixel(self.x,self.y,1)

balls = []
for x in range(50):
    balls.append(Ball())


while True:
    sleep_ms(10)
    display.fill(0)
   
    for b in balls:
        b.run()
   
    display.show()
    
    