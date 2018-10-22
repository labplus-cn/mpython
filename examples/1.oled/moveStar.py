# 这个例子用来实现星星的水平移动
# by 964683112@qq.com
from mpython import *
from time import sleep_ms

# 定义星星的初始位置
x = 0
vx = 1 # 星星的水平速度x
while True:
    x += vx # 每次循环让水平位置增加1
    display.fill(0) # 清屏
    display.pixel(x,10,1)
    display.pixel(x,9,1)
    display.pixel(x,11,1)    
    display.pixel(x+1,10,1)
    display.pixel(x-1,10,1)
    # 以上代码用5个像素画了+形状的星星
    
    if x > 128: # 当星星移动到屏幕右侧
        x = 0 # 让星星重新从屏幕左侧移动
    display.show() # 显示
    sleep_ms(10) # 程序暂停10ms
    