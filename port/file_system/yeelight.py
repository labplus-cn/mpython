import socket
import json

def discover_bulbs(timeout=2):
    """
    发现所有局域网内的Yeelight灯泡.

    :param int timeout: 等待回复需要多少秒。发现将总是要花这么长的时间，
                        因为它不知道当所有的灯泡都响应完毕时。
    :returns: 字典列表，包含网络中每个灯泡的IP，端口和功能。
    """
    msg = 'M-SEARCH * HTTP/1.1\r\n' \
          'ST:wifi_bulb\r\n' \
          'MAN:"ssdp:discover"\r\n'

    # Set up UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.settimeout(timeout)
    s.sendto(msg.encode(), ('239.255.255.250', 1982))
    read_buf = 1024
    bulbs = []
    bulb_ips = set()
    while True:
        try:
            data, addr = s.recvfrom(read_buf)
        except OSError:
            break

        capabilities = dict([x.strip("\r").split(": ")
                             for x in data.decode().split("\n") if ":" in x])
        parsed_url = capabilities["Location"].split("//")[1]

        bulb_ip = tuple(parsed_url.split(":"))
        if bulb_ip in bulb_ips:
            continue

        capabilities = {key: value for key,
                        value in capabilities.items() if key.islower()}
        bulbs.append(
            {"ip": bulb_ip[0], "port": bulb_ip[1], "capabilities": capabilities})
        bulb_ips.add(bulb_ip)

    return bulbs


class BulbException(Exception):
    """
    一般的 yeelight 异常类

    当灯泡通知错误时会引发此异常，例如，当尝试向灯泡发出不支持的命令时。
    """
    pass


class Bulb(object):
    """
    YeeLight的控制类.

    :param str ip:       灯泡的IP.
    :param int port:     连接灯泡的端口号，默认55443.
    :param str effect:   效果类型."smooth" or "sudden".
    :param int duration: 效果的持续时间，以毫秒为单位.最小值为30.突然效果会忽略此值.
    :param bool auto_on: 是否 :py:meth:`ensure_on()
                            <yeelight.Bulb.ensure_on>` 在每次操作之前调用以自动打开灯泡，如果它已关闭。这会在每条消息之前更新灯泡的属性，
                            每个命令会花费一个额外的消息。 如果您担心速率限制，请将其关闭并自行检查。:py:meth:`get_properties()<yeelight.Bulb.get_properties()>`
                            或运行 :py:meth:`ensure_on() <yeelight.Bulb.ensure_on>`
    """

    def __init__(self, ip, port=55443, effect="smooth",
                 duration=300, auto_on=False):

        self._ip = ip
        self._port = port
        self._timeout = 5

        self.effect = effect
        self.duration = duration
        self.auto_on = auto_on

        self.__cmd_id = 0           # The last command id we used.
        self._last_properties = {}  # The last set of properties we've seen.
        self._music_mode = False    # Whether we're currently in music mode.
        self.__socket = None        # The socket we use to communicate.

    @property
    def _cmd_id(self):
        '''
        Get next command id in sequence

        :return: command id
        '''
        self.__cmd_id += 1
        return self.__cmd_id - 1

    @property
    def _socket(self):
        '''
        Get, optionally create, the communication socket
        
        :return: the communication socket
        '''
        if self.__socket is None:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.settimeout(self._timeout)
            self.__socket.connect((self._ip, self._port))

        return self.__socket

    def ensure_on(self):
        """Turn the bulb on if it is off."""
        if self._music_mode is True or self.auto_on is False:
            return

        self.get_properties()

        if self._last_properties["power"] != "on":
            self.turn_on()

    @property
    def music_mode(self):
        """
        Return whether the music mode is active.

        :rtype: bool
        :return: True if music mode is on, False otherwise.
        """
        return self._music_mode

    @property
    def last_properties(self):
        """
        The last properties we've seen the bulb have.

        This might potentially be out of date, as there's no background listener
        for the bulb's notifications. To update it, call
        :py:meth:`get_properties <yeelight.Bulb.get_properties()>`.
        """
        return self._last_properties

    def get_properties(self):
        """
        Retrieve and return the properties of the bulb.

        This method also updates ``last_properties`` when it is called.

        :returns: A dictionary of param: value items.
        :rtype: dict
        """
        # When we are in music mode, the bulb does not respond to queries
        # therefore we need to keep the state up-to-date ourselves
        if self._music_mode:
            return self._last_properties

        requested_properties = [
            "power", "bright", "ct", "rgb", "hue", "sat",
            "color_mode", "flowing", "delayoff", "flow_params",
            "music_on", "name"
        ]
        response = self.send_command("get_prop", requested_properties)
        properties = response["result"]
        properties = [x if x else None for x in properties]

        self._last_properties = dict(zip(requested_properties, properties))
        return self._last_properties

    def ensure_on(self):
        """Turn the bulb on if it is off."""
        if self._music_mode is True or self.auto_on is False:
            return

        self.get_properties()

        if self._last_properties["power"] != "on":
            self.turn_on()

    @property
    def bulb_type(self):
        """
        灯泡类型

        返回灯泡类型：White or Color.当尝试在属性已知之前访问时，灯泡类型是未知的。

        :return: 灯泡类型.
        """
        if not self._last_properties:
            return "BulbType.Unknown"
        if not all(name in self.last_properties for name in ['ct', 'rgb', 'hue', 'sat']):
            return "BulbType.White"
        else:
            return "BulbType.Color"

    def send_command(self, method, params=None):
        """
        请求信息并返回响应

        :param str method: control method id
        :param list params: list of params for the specified method
        :return: the command response
        """

        command = {'id': self._cmd_id, 'method': method, 'params': params}
        # print(command)
        try:
            self._socket.send((json.dumps(command) + '\r\n').encode('utf8'))
        except Exception as e:
            self.__socket.close()
            self.__socket = None
            raise BulbException(
                'A socket error occurred when sending the command.')

        if self._music_mode:
            # We're in music mode, nothing else will happen.
            return {"result": ["ok"]}

        # The bulb will send us updates on its state in addition to responses,
        # so we want to make sure that we read until we see an actual response.
        response = None
        while response is None:
            try:
                data = self._socket.recv(2 * 1024)
            except:
                self.__socket.close()
                self.__socket = None
                response = {'error': 'Bulb closed the connection.'}
                break

            for line in data.split(b'\r\n'):
                if not line:
                    continue

                try:
                    line = json.loads(line.decode('utf8'))
                except ValueError:
                    response = {'result': ['invalid command']}

                if line.get('method') != 'props':
                    response = line

                else:
                    self._last_properties.update(line["params"])

        if "error" in response:
            raise BulbException(response["error"])

        return response

    @property
    def name(self):
        '''
        设置或返回设备名字

        :return: 返回设备名字
        '''
        return self.send_command('get_prop', ['name'])['result']

    @name.setter
    def name(self, name):
        '''
        设置设备名字
        :param name: new name
        '''
        self.send_command('set_name', [name])

    @property
    def is_on(self):
        '''
        返回灯泡是否打开

        :return:打开则是'on',关闭侧'off'。
        '''
        return self.send_command('get_prop', ['power'])['result'][0] == 'on'

    def turn_on(self):
        '''
        打开灯泡
        '''
        self.send_command('set_power', ['on', self.effect, self.duration])

    def turn_off(self):
        '''
        关闭灯泡
        '''
        self.send_command('set_power', ['off', self.effect, self.duration])

    def toggle(self):
        """反转灯泡状态."""
        self.send_command('toggle', [])

    def set_rgb(self, red, green, blue):
        '''
        设置灯泡的RGB值

        :param int red: 红色范围 (0-255)
        :param int green: 绿色范围 (0-255)
        :param int blue: 蓝色范围 (0-255)
        '''

        self.ensure_on()

        red = max(0, min(255, red))
        green = max(0, min(255, green))
        blue = max(0, min(255, blue))

        self.send_command(
            'set_rgb', [red * 65536 + green * 256 + blue, self.effect, self.duration])


    def set_hsv(self, hue, saturation):
        """
        Set the bulb's HSV value.

        :param int hue:        The hue to set (0-359).
        :param int saturation: The saturation to set (0-100).
     
        """
        self.ensure_on()

        # We fake this using flow so we can add the `value` parameter.
        hue = max(0, min(359, hue))
        saturation = max(0, min(100, saturation))

        self.send_command('set_hsv', [hue, saturation,self.effect, self.duration])
        

    def set_color_temp(self, degrees):
        """
        设置灯泡色温

        :param int degrees: 色温范围(1700-6500).
        """
        self.ensure_on()

        degrees = max(1700, min(6500, degrees))
        self.send_command('set_ct_abx', [degrees, self.effect, self.duration])

    def set_adjust(self, action, prop):
        """
        该方法用于改变智能LED的亮度、CT或颜色，在不知道当前值的情况下.

        :param str action: 调整方向，可以的值是，'increase' : 增加指定属性；100'decrease': 减小指定属性；'circle': 增加指定的属性，当它达到最大值后，回到最小值.
        :param str prop:   属性调制. 可以是 "bright" 亮度调整， "ct" 色温调整， "color"
                           颜色调整. 
        """

        self.send_command('set_adjust',  [action, prop])

    def set_brightness(self, brightness):
        """
        设置灯泡亮度

        :param int brightness: 亮度范围 (1-100).
        """
        self.ensure_on()

        brightness = int(max(1, min(100, brightness)))
        self.send_command(
            'set_bright',  [brightness, self.effect, self.duration])

    def start_flow(self, flow):
        '''
        Start a flow

        :param yeelight.Flow flow: the Flow instance to start
        '''
        if not isinstance(flow, Flow):
            raise ValueError('Argument is not a Flow instance')
        self.ensure_on()
        self.send_command('start_cf', [
                          flow.count * len(flow.transitions), flow.action, flow.expression])


    def cron_add(self, event_type, value):
        """
        Add an event to cron.
        """
        self.send_command('cron_add', [event_type.value, value])

    def cron_get(self, event_type):
        """
        Retrieve an event from cron.
        """
        self.send_command('cron_get', [event_type])

    def cron_del(self, event_type):
        """
        Remove an event from cron.
        """
        self.send_command('cron_del', [event_type])
