# fork by http://www.1zlab.com/wiki/micropython-esp32/timer/

from machine import Timer, Pin
import utime


def toggle_led(led_pin):
    '''
    LED状态反转
    '''
    led_pin.value(not led_pin.value())


def led_blink_timed(timer, led_pin, freq=10):
    '''
    led 按照特定的频率进行闪烁
    LED闪烁周期 = 1000ms / 频率
    状态变换间隔（period） = LED闪烁周期/ 2 
    '''
    # 计算状态变换间隔时间 ms
    period = int(0.5 * 1000 / freq)
    # 初始化定时器
    # 这里回调是使用了lambada表达式，因为回调函数需要传入led_pin
    timer.init(period=period, mode=Timer.PERIODIC, callback=lambda t: toggle_led(led_pin))


# 声明引脚 D2 作为LED的引脚
led_pin = Pin(2, Pin.OUT)
timer = Timer(1)  # 创建定时器对象
led_blink_timed(timer, led_pin, freq=20)