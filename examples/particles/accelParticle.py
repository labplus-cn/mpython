'''
基于加速度计的读数实时改变发射点位置的粒子系统
感觉粒子系统的读数和板子的方向似乎有点问题
同时使用pixel和DispChar会导致显示巨卡
'''
from mpython import *
from time import sleep_ms
from random import randint
from collections import deque


class Ball():
    '''
    粒子类
    '''

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.vx = randint(-6, 6)
        self.vy = randint(-6, 6)

    def run(self):
        self.update()
        self.display()

    def update(self):

        self.x += self.vx
        self.y += self.vy

    def isDead(self):

        if self.x > 128 or self.x < 0 or self.y > 64 or self.y < 0:
            return True
        else:
            return False

    def display(self):
        display.pixel(self.x, self.y, 1)


class ParticleSystem():
    '''
    粒子系统类
    '''

    def __init__(self, x, y):
        self.particles = []
        self.x = x
        self.y = y
        for i in range(200):
            self.particles.append(Ball(self.x, self.y))

    def run(self):
        for p in self.particles:
            if p.isDead():
                p.x = self.x
                p.y = self.y
            p.run()


# 初始化粒子系统
ps = ParticleSystem(0, 0)

while True:

    sleep_ms(20)

    display.fill(0)

    x = accelerometer.get_y()
    y = accelerometer.get_x()
    ps.x = 128-int(x*64+64)
    ps.y = int(y*32+32)
    ps.run()
    # 把加速度计的读数

    display.show()
