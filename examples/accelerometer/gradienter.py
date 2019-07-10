from mpython import *    #导入mpython模块

Center_x=63           #设定中心点（原点）x的坐标
Center_y=31           #设定中心点（原点）y的坐标

while True:
    
    x=accelerometer.get_x()         #获取X轴的加速度
    y=accelerometer.get_y()         #获取Y轴的加速度

    if y<=1 and y>=-1:
        offsetX=int(numberMap(y,1,-1,-64,64))   #映射Y轴偏移值
    if x<=1 and x>=-1:
        offsetY=int(numberMap(x,1,-1,32,-32))   #映射X轴偏移值
    move_x=Center_x+offsetX                 #水平球在X坐标上的移动
    move_y=Center_y+offsetY                 #水平球在Y坐标上的移动

    oled.circle(Center_x,Center_y,6,1)      #画中心固定圆：空心
    oled.fill_circle(move_x,move_y,4,1)     #画移动的水平球：实心
    oled.DispChar("%0.1f,%0.1f" %(x,y),85,0)    #显示水平球在X、Y轴的加速度值

    if offsetX==0 and offsetY==0:
        rgb.fill((0,10,0))          #水平球在中心位置亮绿灯，亮度为10
        rgb.write()
    else:
        rgb.fill((0,0,0))           #水平球不在中心位置灭灯
        rgb.write()
    oled.show()
    oled.fill(0)