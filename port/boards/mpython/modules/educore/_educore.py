'''
educore
'''
import gc
from mpython import MPythonPin,PinMode,Pin,OLED,Image,i2c,I2C,wifi,button_a,button_b,sleep_ms,sleep,numberMap,Magnetic
from mpython import accelerometer as _accelerometer
from mpython import rgb as _rgb
from mpython import light as _light
from mpython import sound as _sound
import network
import neopixel
import machine
from bluebit import Scan_Rfid,Barometric
from servo import Servo
from umqtt.robust import MQTTClient as MQTT
import ubinascii
import time
from machine import Timer
from hcsr04 import HCSR04
import dht as _dht
import parrot as _parrot
from ds18x20 import DS18X20
import onewire
import math

gc.collect()



pins_esp32 = (33, 32, 35, 34, 39, 0, 16, 17, 26, 25, 36, 2, -1, 18, 19, 21, 5, -1, -1, 22, 23, -1, -1, 27, 14, 12, 13, 15, 4)
# global pins_state
pins_state = [None] * len(pins_esp32)
 
def set_dict_values_to_none(d):
    d = {key: None for key in d}

'''
输入输出引脚控制 pin类
MPythonPin,PinMode,Pin
'''
class pin():
    def __init__(self, pin):
        self.pin_num = pin
        self.mode = PinMode.IN
        self.pull = None
        self._event_change = None
        self._event_rising = None
        self._event_falling = None
        self._pin = MPythonPin(self.pin_num, PinMode.IN)
        self._iqr_func = None

    def read_digital(self):
        # if(pins_state[self.pin_num]!=PinMode.IN):
        pins_state[self.pin_num]=PinMode.IN
        self._pin = MPythonPin(self.pin_num, PinMode.IN)
        return self._pin.read_digital()
        # else:
        #     return self._pin.read_digital()

    def write_digital(self, value):
        # if(pins_state[self.pin_num]!=PinMode.OUT):
        pins_state[self.pin_num]=PinMode.OUT
        self._pin = MPythonPin(self.pin_num, PinMode.OUT, Pin.PULL_UP)
        return self._pin.write_digital(value)
        # else:
        #     return self._pin.write_digital(value)

    def read_analog(self):
        if self.pin_num not in [0, 1, 2, 3, 4, 10]:
            return self.read_digital()
        pins_state[self.pin_num]=PinMode.ANALOG
        self._pin = MPythonPin(self.pin_num, PinMode.ANALOG)
        return self._pin.read_analog()
        
    def write_analog(self, value=0, freq=5000):
        # if(pins_state[self.pin_num]!=PinMode.PWM):
        pins_state[self.pin_num]=PinMode.PWM
        self._pin = MPythonPin(self.pin_num, PinMode.PWM)
        return self._pin.write_analog(duty=value, freq=freq)
        # else:
        #     return self._pin.write_analog(duty=value, freq=freq)

    def irq(self, handler=None, trigger=Pin.IRQ_RISING):
        # if(pins_state[self.pin_num]!=PinMode.IN):
        pins_state[self.pin_num]=PinMode.IN
        self._pin = MPythonPin(self.pin_num, PinMode.IN)
        self._pin.irq(trigger=trigger, handler=handler)
        # else:
        #     self._pin.irq(trigger=trigger, handler=handler)
    
    @property
    def event_change(self):
        return self._event_change

    @event_change.setter
    def event_change(self, new_event_change):
        if new_event_change != self._event_change:
            self._event_change = new_event_change
            self._iqr_func = self._event_change
            self.irq(handler=self.func, trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING)

    @property
    def event_rising(self):
        return self._event_rising

    @event_rising.setter
    def event_rising(self, new_event_rising):
        if new_event_rising != self._event_rising:
            self._event_rising = new_event_rising
            self._iqr_func = self._event_rising
            self.irq(handler=self.func, trigger=Pin.IRQ_RISING)

    @property
    def event_falling(self):
        return self._event_falling

    @event_falling.setter
    def event_falling(self, new_event_falling):
        if new_event_falling != self._event_falling:
            self._event_falling = new_event_falling
            self._iqr_func = self._event_falling
            self.irq(handler=self.func, trigger=Pin.IRQ_FALLING)
    
    def func(self,_):
        self._iqr_func()

'''
声音值
'''
class sound():
    def __init__(self,pin=None): 
        self.pin_num = pin
        self.type = 1
        if(self.pin_num==None):
            self.type = 1
        else:
            self.type = 2
            self.pin = MPythonPin(self.pin_num, PinMode.ANALOG)

    def read(self):
        if(self.type == 1):
            return  _sound.read()
        elif(self.type == 2):
            return self.pin.read_analog()
            
    @staticmethod
    def read():
        return _sound.read()


'''
光线传感器
'''
class light():
    def __init__(self,pin=None): 
        self.pin_num = pin
        self.type = 1
        if(self.pin_num==None):
            self.type = 1
        else:
            self.type = 2
            self.pin = MPythonPin(self.pin_num, PinMode.ANALOG)

    def read(self):
        if(self.type == 1):
            return  _light.read()
        elif(self.type == 2):
            return self.pin.read_analog()
            
    @staticmethod
    def read():
        return _light.read()



'''
加速度计
'''
class Accelerometer():
    def __init__(self) :
        self.shake_status = False
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0

    def x(self):
        self.X = _accelerometer.get_x()
        return self.X

    def y(self):
        self.Y = _accelerometer.get_y()
        return self.Y

    def z(self):
        self.Z = _accelerometer.get_z()
        return self.Z

    def shake(self):
        return self.shake_status

'''
继承OLED
'''
class OLED(OLED):
    def print(self, _str):
        try:
            self.fill(0)
            _str = str(_str)
            if "\n" in _str:
                # print("字符串中包含换行符")
                _str = _str.split("\n") 
                if(len(_str)<4):
                    for i in range(len(_str)):
                        self.DispChar(str(_str[i]), 0, i*16, 1, False)
                else:
                    for i in range(4):
                        self.DispChar(str(_str[i]), 0, i*16, 1, False)
            elif "\:" in _str:
                # print("显示图像")
                _str = _str[2:]
                # print(_str)
                if(_str=='HAPPY'):
                    self.image_picture = Image()
                    self.blit(self.image_picture.load('face/4.pbm', 0), 32, 0)
                elif(_str=='SAD'):
                    self.image_picture = Image()
                    self.blit(self.image_picture.load('face/5.pbm', 0), 32, 0)
            else:
                # print("字符串中不包含换行符")
                self.DispChar(str(_str), 0, 0, 1, True)
            self.show()
        except Exception as e:
            print('oled print err:'+str(e))

    def clear(self):
        self.fill(0)
        self.show()

'''
电机控制
'''
class parrot():
    M1 = 1
    M2 = 2

    def __init__(self, *args, **kwargs):
        """
        Args:
            *args: 不定数量的位置参数，用位置参数占位符。
            **kwargs: 关键字参数，用于指定查询的其他配置。
                可能包含的键:
                    - in0: 
                    - in1: 
                    - speed: 
        """
        args_list = []
        self.in0 = kwargs.get('in0', None)
        self.in1 = kwargs.get('in1', None)
        # speed = kwargs.get('speed', None)

        if(self.in0==None):
            '''
            内置电机
            '''
            self.type = 1
            self.mode = True
            for arg in args:
                args_list.append(arg)
            if(self.in0 is None and len(args_list)!=1):
                print('位置参数数量错误')
            else:
                self.args_list = args_list
        else:
            '''
            外接电机
            '''
            self.type = 2
            self.mode = False
 
            if(self.in0==None or self.in1==None):
                print('关键字参数错误')
            self.out0 = MPythonPin(self.in0, PinMode.PWM)
            self.out1 = MPythonPin(self.in1, PinMode.PWM)
           
    def speed(self,speed):
        if(self.type==1):
            _parrot.set_speed(self.args_list[0],int(speed))
        elif(self.type==2):
            if(speed>=0):
                speed = int(numberMap(speed, 0, 100, 0, 1023))
                self.out0.write_analog(speed)
                sleep_ms(2)
                self.out1.write_analog(0)
                sleep_ms(2)
            elif(speed<0):
                speed = int(numberMap(math.fabs(speed), 0, 100, 0, 1023))
                self.out1.write_analog(speed)
                sleep_ms(2)
                self.out0.write_analog(0)
                sleep_ms(2)

'''
继承Servo
'''
class servo(Servo):
    def __init__(self,pin):
        super().__init__(pin)
    
    def angle(self, value):
        value = int(value)
        if(value<0):
            value = 0
        if(value>180):
            value = 180
        self.write_angle(value)
    

'''继承Scan_Rfid'''
class rfid(Scan_Rfid):
    def __init__(self,sda,scl):
        _sda = pins_esp32[sda]
        _scl = pins_esp32[scl]
        if(sda==20 or scl==19):
            self.i2c_1 = i2c
        else:
            self.i2c_1 = I2C(1, scl=Pin(_scl), sda=Pin(_sda), freq=400000)
        # print(self.i2c_1.scan())
        super().__init__()
    
    def scanning(self,wait=True):
        rf = None
        if(isinstance(wait, bool)):
            if(wait):
                while True:
                    rf = super().scanning(i2c=self.i2c_1)
                    if rf:
                        return rf
                    else:
                        time.sleep_ms(200)
            else:
                rf = super().scanning(i2c=self.i2c_1)
                if rf:
                    return rf
                else:
                    return None
        elif(isinstance(wait, int)):
            time_start = time.time()
            while True:
                if (int(time.time()-time_start) > wait):
                    return None
                rf = super().scanning(i2c=self.i2c_1)
                if rf:
                    return rf
                else:
                    time.sleep_ms(200)


'''继承wifi'''
class WiFi(wifi):
    def __init__(self):
        super().__init__()

    def connect(self, ssid, psd, timeout=10000):
        self.connectWiFi(ssid, psd, int(timeout/1000))
    
    def status(self):
        return self.sta.isconnected()

    def info(self):
        return str(self.sta.ifconfig())


'''MQTT'''
class MqttClient():
    def __init__(self):
        self.client = None
        self.server = None
        self.port = None
        self.client_id = None
        self.user = None
        self.passsword = None
        self.topic_msg_dict = {}
        self.topic_callback = {}
        self.tim_count = 0
        self._connected = False
        self.lock = False

    def connect(self, **kwargs):
        server = kwargs.get('server',"iot.mpython.cn" )
        port = kwargs.get('port',1883 )
        client_id = kwargs.get('client_id',"" )
        user = kwargs.get('user',"" )
        psd = kwargs.get('psd',None)
        password = kwargs.get('password',None)
        if(psd==None and password==None):
            psd = ""
        elif(password!=None):
            psd = password
        try:
            self.client = MQTT(client_id, server, port, user, psd, 0)
            self.client.connect()
            self.server = server
            self.port = port
            self.client_id = client_id
            self.user = user
            self.passsword = psd
            print('Connected to MQTT Broker "{}"'.format(self.server))
            self._connected = True
            self.client.set_callback(self.on_message)
            time.sleep(0.5)
            self.tim = Timer(15)
            self.tim.init(period=100, mode=Timer.PERIODIC, callback=self.mqtt_heartbeat)
            gc.collect()
        except Exception as e:
            print('Connected to MQTT Broker error:{}'.format(e))

    def connected(self):
        return self._connected

    def publish(self, topic, content):
        try:
            self.lock = True
            self.client.publish(str(topic),str(content).encode("utf-8"))
            self.lock = False
        except Exception as e:
            print('publish error:{}'.format(e))

    def message(self, topic):
        topic = str(topic)
        if(not topic in self.topic_msg_dict):
            # self.topic_msg_dict[topic] = None
            self.topic_callback[topic] = False 
            self.subscribe(topic, self.default_callbak)
            return self.topic_msg_dict[topic]
        else:
            return self.topic_msg_dict[topic]
        
    def received(self, topic, callback):
        self.subscribe(topic, callback)

    def subscribe(self, topic, callback):
        self.lock = True
        try:
            topic = str(topic)
            if(not topic in self.topic_msg_dict):
                global _callback
                _callback = callback
                self.topic_msg_dict[topic] = None
                self.topic_callback[topic] = True
                exec('global mqtt_topic_' + bytes.decode(ubinascii.hexlify(topic)),globals())
                exec('mqtt_topic_' + bytes.decode(ubinascii.hexlify(topic)) + ' = _callback',globals())
                self.client.subscribe(topic)
                time.sleep(0.1)
            elif(topic in self.topic_msg_dict and self.topic_callback[topic] == False):
                global _callback
                _callback = callback
                self.topic_callback[topic] = True
                exec('global mqtt_topic_' + bytes.decode(ubinascii.hexlify(topic)),globals())
                exec('mqtt_topic_' + bytes.decode(ubinascii.hexlify(topic)) + ' = _callback',globals())
                time.sleep(0.1)
            else:
                print('Already subscribed to the topic:{}'.format(topic))
            self.lock = False
        except Exception as e:
            print('MQTT subscribe error:'+str(e))

    def on_message(self, topic, msg):
        try:
            gc.collect()
            topic = topic.decode('utf-8', 'ignore')
            msg = msg.decode('utf-8', 'ignore')
            # print("Received '{payload}' from topic '{topic}'\n".format(payload = msg, topic = topic))
            if(topic in self.topic_msg_dict):
                self.topic_msg_dict[topic] = msg
                if(self.topic_callback[topic]):
                    exec('global mqtt_topic_' + bytes.decode(ubinascii.hexlify(topic)),globals())
                    eval('mqtt_topic_' + bytes.decode(ubinascii.hexlify(topic))+'()',globals())
        except Exception as e:
            print('MQTT on_message error:'+str(e))
    
    def default_callbak(self):
        pass
    
    def mqtt_check_msg(self):
        try:
            self.client.check_msg()
        except Exception as e:
            print('MQTT check msg error:'+str(e))

    def mqtt_heartbeat(self,_):
        self.tim_count += 1 
        if(not self.lock):
            self.mqtt_check_msg()
        if(self.tim_count==200):
            self.tim_count = 0
            try:
                self.client.ping() # 心跳消息
                self._connected = True
            except Exception as e:
                print('MQTT keepalive ping error:'+str(e))
                self._connected = False
   

'''
ble 模拟键盘鼠标
'''

'''
超声波
'''
# class Ultrasonic(HCSR04):
#     def __init__(self, trig=1, echo=0):
#         self._trig = pins_esp32[trig]
#         self._echo = pins_esp32[echo]
#         super().__init__(trigger_pin=self._trig, echo_pin=self._echo)

#     def distance(self):
#         return self.distance_cm()

class ultrasonic(object):
    """
    超声波模块控制类
    """
    def __init__(self, sda=20, scl=19):
        _sda = pins_esp32[sda]
        _scl = pins_esp32[scl]
        if(sda==20 or scl==19):
            self.i2c = i2c
        else:
            self.i2c = I2C(1, scl=Pin(_scl), sda=Pin(_sda), freq=400000)

    def distance(self):
        """
        获取超声波测距
        :return: 返回测距,单位cm
        """
        self.i2c.writeto(0x0b, bytearray([1]))
        sleep_ms(2)
        temp = self.i2c.readfrom(0x0b, 2)
        distanceCM = int((temp[0] + temp[1] * 256) / 10)
        return distanceCM

'''
DHT11
'''
class _dht11():
    def __init__(self, pin):
        self._pin = pins_esp32[pin]
        self.dht11 = _dht.DHT11(Pin(self._pin))
        self.tim = Timer(16)
        self.tim.init(period=1000, mode=Timer.PERIODIC, callback=self.timer_tick)
        time.sleep(1.5)
        self.dht11.measure()

    def timer_tick(self,_):
        try: 
            self.dht11.measure()
        except: 
            pass

    def read(self):
        return self.dht11.temperature(),self.dht11.humidity()

dht11_old_pin = None
dht11_thing = None

def dht(pin):
    global dht11_old_pin,dht11_thing
    if dht11_old_pin != pin:
        dht11_thing = _dht11(pin)
        dht11_old_pin = pin
    return dht11_thing


'''
DS18b20
'''
class ds18b20():
    def __init__(self, pin):
        self._pin = pins_esp32[pin]
        self.dat = Pin(self._pin)
   
    def read(self):
        # create the onewire object
        self.ds = DS18X20(onewire.OneWire(self.dat))
        # scan for devices on the bus
        roms = self.ds.scan()
        # print('found devices:', roms)
        self.ds.convert_temp()
        sleep_ms(750)
        temp = self.ds.read_temp(roms[0])
        # print(temp,end='℃\n ')
        return temp


'''
字典生成器
从txt文本生成字典
'''
def get_dict_from_file(dict_file):
    with open(dict_file) as f:
        d = dict(x.rstrip().split(None, 1) for x in f)
        return d 

# d = get_dict_from_file("dict.txt")

'''
根据字符串生成字典
'''
def get_dict_from_str(s):
    _str = str(s)
    d = {}
    if "\n" in _str:
        _str = _str.split("\n")
        for i in _str:
            tmp = i.strip().split(' ')
            key = tmp[0]
            value = tmp[1]
            d[key] = value
        return d
    elif ";" in _str:
        _str = _str.split(";")
        for i in _str:
            tmp = i.strip().split(' ')
            key = tmp[0]
            value = tmp[1]
            d[key] = value
        return d
    else:
        return d

# s = "001 张三; 002 李四"
# d = get_dict_from_file(s)
# print(d["001"])

"""
uuid
"""
def uuid():
    return ubinascii.hexlify(machine.unique_id()).decode().upper()


'''
六轴 educore定时器
'''
class accelerometer():
    def __init__(self):
        self.tim_count = 0
        self.tim = Timer(17)
        self.tim.init(period=100, mode=Timer.PERIODIC, callback=self.educore_callback)
        self._is_shaked = False
        self._last_x = 0
        self._last_y = 0
        self._last_z = 0
        self._count_shaked = 0
        self.accelerometer = Accelerometer()

    def educore_callback(self,_):
        self.tim_count += 1 
        try:
            self.accelerometer_callback()
            gc.collect()
        except Exception as e:
            print(str(e))
        if(self.tim_count==200):
            self.tim_count = 0

    def accelerometer_callback(self):
        '''加速度计'''
        if self._is_shaked:
            self._count_shaked += 1
            if self._count_shaked == 5: 
                self._count_shaked = 0
                self.accelerometer.shake_status = False
        x=self.accelerometer.x(); y=self.accelerometer.y();z=self.accelerometer.z()
        if self._last_x == 0 and self._last_y == 0 and self._last_z == 0:
            self._last_x = x; 
            self._last_y = y; 
            self._last_z = z; 
            self.accelerometer.shake_status = False
            return
        diff_x = x - self._last_x; diff_y = y - self._last_y; diff_z = z - self._last_z
        self._last_x = x; self.last_y = y; self._last_z = z
        if self._count_shaked > 0: 
            return
        self._is_shaked = (diff_x * diff_x + diff_y * diff_y + diff_z * diff_z > 1)
        if self._is_shaked: 
            self.accelerometer.shake_status = True
        
    def X(self):
        return self.accelerometer.x()
    
    def Y(self):
        return self.accelerometer.y()
    
    def Z(self):
        return self.accelerometer.z()
    
    def shake(self):
        return self.accelerometer.shake()




'''Webcamera'''
class FCR:
    def __init__(self):
        self.id = None
        self.blinks = None
        self.mouth = None
        self.status = 0

class webcamera():
    def __init__(self): 
        self.fcr = FCR()
    
    def connect(self, id):
        self.id = str(id)
        self.topic = str(id)
        self._MQTTClient = MqttClient()
        self._MQTTClient.connect(server='8.135.108.214',  port=1883,  client_id=self.id,  user=self.id, psd=self.id)
        self._MQTTClient.Received(self.topic, self.callbackFunction)
    
    def result(self):
        d = {"blink":self.fcr.blinks,"mouth_open":self.fcr.mouth,"status":self.fcr.status}
        return d

    def callbackFunction(self):
        try:
            msg = self._MQTTClient.receive(topic=self.topic)
            # print(msg)
            if(msg):
                msg = eval(msg)
                self.fcr.blinks = msg[0]
                self.fcr.mouth = msg[1]
                self.fcr.status = 1
            else:
                self.fcr.blinks = None
                self.fcr.mouth = None
                self.fcr.status = 0
        except Exception as e:
            self.fcr.blinks = 0
            self.fcr.mouth = 0
            self.fcr.status = 0


class button:
    a = 'a'
    b = 'b'
    def __init__(self,_type='a'): 
        self.button_a = button_a
        self.button_b = button_b
        self.type = _type
        self.func_event_change = None
        if(self.type not in ['a','b']):
             self.pin = MPythonPin(self.type, PinMode.IN)

    def func(self,_):
        self.func_event_change()

    @property
    def event_pressed(self):
        return self.func_event_change

    @event_pressed.setter
    def event_pressed(self, new_event_change):
        if new_event_change != self.func_event_change:
            self.func_event_change = new_event_change
            if(self.type=='a'):
                self.button_a.event_pressed = self.func
            elif(self.type=='b'):
                self.button_b.event_pressed = self.func
            else:
                print('Not supported')


    def status(self):
        if(self.type=='a'):
            return self.button_a.status()
        elif(self.type=='b'):
            return self.button_b.status()
        else:
            val = self.pin.read_digital()
            return val
'''
麦克风
'''          
import music

class speaker():
    def __init__(self,pin=None): 
        self.pin = pin
        self.type = 1
        if(pin==None):
            self.type = 1
        else:
            self.type = 2

    def tone(self,freq=1000,durl=None):
        if(isinstance(freq,list)):
            freq = freq[0]

        if(self.type == 1):
            if(durl==None):
                music.pitch(int(freq))
            else:
                music.pitch(int(freq), int(durl))
        elif(self.type == 2):
            if(durl==None):
                music.pitch(int(freq), pin=pins_esp32[self.pin])
            else:
                music.pitch(int(freq), int(durl), pin=pins_esp32[self.pin])

    def stop(self):
        if(self.type == 1):
            music.stop()
        elif(self.type == 2):
            music.stop(pins_esp32[self.pin])



'''
rgb
'''
class rgb():
    def __init__(self,pin=None): 
        self.pin_num = pin
        self.type = 1
        if(self.pin_num==None):
            self.type = 1
        else:
            self.type = 2
            self.pin = pins_esp32[self.pin_num]
            self.my_rgb = neopixel.NeoPixel(Pin(self.pin), n=10, bpp=3, timing=1)

    def write(self,index=[0,1,2],r=0,g=0,b=0):
        if(self.type == 1):
            for i in index:
                _rgb[i]=(r,g,b)
                _rgb.write()
                sleep_ms(1)
        elif(self.type == 2):
            for i in index:
                self.my_rgb[i]=(r,g,b)
                self.my_rgb.write()
                sleep_ms(1)
            
        
    def clear(self):
        if(self.type == 1):
            _rgb.fill((0,0,0))
            _rgb.write()
            sleep_ms(1)
        elif(self.type == 2):
            self.my_rgb.fill((0,0,0))
            self.my_rgb.write()
            sleep_ms(1)


'''
人体红外
'''
class tsd():
    def __init__(self,pin=None): 
        self.pin_num = pin
        self.type = 1
        self.pin = MPythonPin(self.pin_num, PinMode.IN)

    def read(self):
        return  self.pin.read_digital()
    
'''
气压
'''
class pressure(object):
    def __init__(self, sda=20, scl=19):
        _sda = pins_esp32[sda]
        _scl = pins_esp32[scl]
        if(sda==20 or scl==19):
            self.i2c = i2c
            self.dev = Barometric(self.i2c)
            print(self.i2c)
        else:
            self.i2c = I2C(1, scl=Pin(_scl), sda=Pin(_sda), freq=400000)
            time.sleep(0.1)
            self.dev = Barometric(self.i2c)

    def read(self):
        # 百帕
        return self.dev.pressure()/100


'''
地磁
'''
class compass(object):
    def __init__(self):
        if 48 in i2c.scan():
            self.type = 1
            self.magnetic = Magnetic()
        else:
            self.type = -1
            print('Not supported')
        
    def adjust(self):
        self.magnetic.calibrate()

    def direction(self):
        return self.magnetic.get_heading()