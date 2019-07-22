from mpython import *    

myServo=Servo(0,min_us=500, max_us=2500)

while True:
    y=accelerometer.get_y()
    if y<=1 and y>=-1:
        angle=int(numberMap(y,1,-1,0,180))
    print(angle)
    myServo.write_angle(angle)
    oled.DispChar("angle:%d" %angle,40,25)
    oled.show()
    oled.fill(0)
    sleep_ms(10)



