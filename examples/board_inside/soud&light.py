from mpython import *

while True:
    print('light:%d,Sound:%d' % (light.read(),sound.read()))
    sleep_ms(5)
