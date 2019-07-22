import parrot
from mpython import sleep_ms,sleep

# 可设置速度范围为-100到100。
# 当值为正值时,电机正转；为负值时,电机反转；


while True:

    # 设置正转速度100
    parrot.set_speed(parrot.MOTOR_1,100)   
    parrot.set_speed(parrot.MOTOR_2,100)   
    print("current motor speend: %d,%d" %(parrot.get_speed(parrot.MOTOR_1),parrot.get_speed(parrot.MOTOR_2)))    #获取电机速度
    sleep(5)
    # 设置反转速度100
    parrot.set_speed(parrot.MOTOR_1,-100)   
    parrot.set_speed(parrot.MOTOR_2,-100)   
    print("current motor speend: %d,%d" %(parrot.get_speed(parrot.MOTOR_1),parrot.get_speed(parrot.MOTOR_2)))    #获取电机速度
    sleep(5)
    # 停止  
    parrot.set_speed(parrot.MOTOR_1,0)   
    parrot.set_speed(parrot.MOTOR_2,0)   
    print("current motor speend: %d,%d" %(parrot.get_speed(parrot.MOTOR_1),parrot.get_speed(parrot.MOTOR_2)))    #获取电机速度
    sleep(2)