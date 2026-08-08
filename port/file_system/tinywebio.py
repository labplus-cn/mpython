__version__ = "TinyWebIO v0.0.8"
__author__ = "roadlabs@gmail.com"
__license__ = "http://unlicense.org"

import mpython, music, socket, network, json, gc
from ubinascii import hexlify
from time import time
from urequests import request
from machine import Timer, unique_id


class Request:   
    def __init__(self, socket=None):
        self.client_socket = socket
        self.method = None
        self.path = None
        self.form = {"tag": None, "value": None, "fmt": None}

    def _unquote(self, str):
        res = []
        r = str.split('%')
        res = res + [ord(c) for c in r[0]]

        for i in range(1, len(r)):
            s = r[i]
            try:
                r_first = int(s[:2], 16)
                res.append(r_first)
                r_last = s[2:]
            except Exception:
                r_last = '%' + s     
            if len(r_last) > 0:
                res = res + [ord(c) for c in r_last]

        return bytes(res).decode()
    
    def parse(self):
        gc.collect()
        try:
            req_data = self.client_socket.recv(4096).decode().replace('+', ' ')   # .strip()
            if not req_data:
                raise Exception('no data')
            req_datas = req_data.split('\r\n')
            firstline = self._unquote(req_datas[0])
            lastline = self._unquote(req_datas[-1])
            if not lastline:
                for item in req_datas[1:]:
                    if item.lower().strip().startswith('content-length'):
                        size = int(item.split(':')[-1])
                        if size > 0:
                            lastline = self.client_socket.recv(size).decode().strip()
                            break
            cmd = firstline.split()
            self.method = cmd[0]
            _path = cmd[1].split('?', 1)
            if len(_path) > 1:
                self.method = 'POST'
                self._set_form(_path[-1])
            self.path = _path[0]
            if len(lastline) > 0:
                self._set_form(lastline)
        except Exception as e:
            print("request data parsed failure!:%s" % e)

    def _set_form(self, data):
        params = data.split('&')
        for p in params:
            k, v = p.split('=')
            self.form[k] = v.strip('"')


class Response:   
    def __init__(self, socket=None):
        self.client_socket = socket
        self.response_data = None
        self.response_state = b'HTTP/1.0 200 OK\r\n'
        self.data_type = None
    
    def make(self, data):
        gc.collect()
        firstline = self.response_state
        if self.data_type == 'html':
            header = b'Content-Type: text/html; charset=utf-8\r\n'
        else:
            header = b'Content-Type: application/jsonrequest\r\nAccess-Control-Allow-Origin: *\r\n'
        body = b'\r\n%s' % json.dumps(data)
        self.response_data = firstline + header + body

    def make_page(self, title=None, content=None):
        gc.collect()
        firstline = self.response_state
        header = b'Content-Type: text/html; charset=utf-8\r\n'
        template = b'''<html><head><title>{title}</title><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0"><meta charset='utf-8'><link rel="icon" href="data:;base64,=">
        <style>{style}</style></head><body class='c'><p><a href='/'>{home}</a></p>{content}</body></html>
        '''
        style = "*+*{box-sizing:border-box;margin:.5em 0}@media(min-width:35em){.col{display:table-cell}.row{display:table;border-spacing:1em 0}}.row,.w-100{width:100%}.card:focus,hr{outline:0;border:solid #fa0}.card,pre{padding:1em;border:solid #eee}.btn:hover,a:hover{opacity:.6}.c{max-width:60em;padding:1em;margin:auto;font:1em/1.6 nunito}a{color:#fa0;text-decoration:none}.btn.primary{color:#fff;background:#fa0;border:solid #fa0}pre{overflow:auto}td,th{padding:1em;text-align:left;border-bottom:solid #eee}.btn{cursor:pointer;padding:1em;letter-spacing:.1em;text-transform:uppercase;background:#fff;border:solid;font:.7em nunito}"
        data = template.format(title=title, style=style, home=__version__, content=content)
        body = b'\r\n%s' % data
        self.response_data = firstline + header + body

    def send(self):
        if self.response_data:
            try:
                self.client_socket.write(self.response_data)
            except Exception as e:
                print("response data sent failure!:%s" % e)
 

class Board:
    def __init__(self):
        self.scope = {}
        self.error = None
        self.id = hexlify(unique_id()).decode()

    def _get_real_tag(self, raw_tag):
        real_tag = raw_tag
        raw_tag_lower = raw_tag.lower().strip()
        for tag_name in ['button_a', 
                         'button_b', 
                         'touchPad_P', 
                         'touchPad_Y', 
                         'touchPad_T', 
                         'touchPad_H', 
                         'touchPad_O', 
                         'touchPad_N']:
            real_tag_lower = tag_name.lower().replace('_', '')
            if real_tag_lower == raw_tag_lower:
                real_tag = tag_name
                return real_tag
        if raw_tag_lower.startswith('pin'):
            pin_name = 'MPythonPin'
            pin_mode = 'digital' if raw_tag_lower[3] == 'd' else 'analog'
            pin_num = raw_tag_lower[4:]
            real_tag = '%s_%s_%s' % (pin_name, pin_mode, pin_num)
        return real_tag

    def read(self, raw_tag):
        gc.collect()
        tag = self._get_real_tag(raw_tag)
        value = ''
        try:
            if tag in ['button_a', 
                       'button_b', 
                       'touchPad_P', 
                       'touchPad_Y', 
                       'touchPad_T', 
                       'touchPad_H', 
                       'touchPad_O', 
                       'touchPad_N', 
                       'light', 
                       'sound']:
                sensor = getattr(mpython, tag)
                method = 'read' if hasattr(sensor, 'read') else 'value'         
                value = '%d' % getattr(sensor, method)()
            elif tag == 'accelerometer':
                accelerometer = getattr(mpython, 'accelerometer')           
                value = '%f,%f,%f' % (accelerometer.get_x(), 
                                      accelerometer.get_y(), 
                                      accelerometer.get_z())
            elif tag.startswith('MPythonPin'):
                pname, pmode, pnum = tag.split('_')
                pfun = getattr(mpython, pname)
                n = int(pnum)
                if pmode == 'digital':
                    pin = pfun(n, 1)
                    value = '%d' % pin.read_digital()
                elif pmode == 'analog':
                    pin = pfun(n, 4)
                    value = '%d' % pin.read_analog()
            elif tag.startswith('id'):
                value = self.id
            elif tag.startswith('time'):
                value = time()
        except Exception as e:
            print("error for board data reading!:%s" % e)
        return ["VALUE", raw_tag, value]    
    
    def write(self, raw_tag, raw_value):
        gc.collect()
        tag = self._get_real_tag(raw_tag)
        value = raw_value.strip()
        try:
            if tag.startswith('rgb'):
                led = getattr(mpython, 'rgb')
                num = 0 if tag[3:] == '' else int(tag[3:])
                n = num if num < 3 and num >= 0 else 2
                r, g, b = value.split(',')          
                led[n] = tuple([int(r), int(g), int(b)])
                led.write()
            elif tag.startswith('display') or tag.startswith('oled'):
                oled = getattr(mpython, tag.strip())
                values = value.split(':', 1)
                method = values[0].strip()
                vdata = values[-1].strip()
                if method == 'show':
                    content, x, y = vdata.split(',')
                    oled.DispChar(content, int(x.strip()), int(y.strip()))
                elif method == 'fill':
                    oled.fill(int(vdata))
                else:
                    oled.DispChar(values[0].strip(), 0, 0)
                oled.show()
            elif tag.startswith('buzz'):
                bz = getattr(mpython, 'buzz')
                method = value.strip()
                if method.startswith('on'):
                    param = method.split(':', 1)[-1].strip()
                    freq = 500 if param == 'on' else int(param)
                    bz.on(freq) 
                elif method.startswith('off'):
                    bz.off()
                else:
                    freq = method.split(':', 1)[0].strip()
                    bz.on(int(freq))
            elif tag.startswith('music'):
                method = value.strip()
                if method.startswith('pitch'):
                    param = method.split(':', 1)[-1].strip()
                    freq, duration = param.split(',')
                    music.pitch(int(freq), int(duration))
                else:
                    tune = value.upper().split(',')
                    if len(tune) == 1:
                        tune_builtin = tune[0].strip()
                        if hasattr(music, tune_builtin):
                            tune = getattr(music, tune_builtin)
                    music.play(tune)
            elif tag.startswith('servo'):
                servo = getattr(mpython, 'Servo')
                pin = int(tag[5:])
                param = value.strip()
                servo(pin).write_angle(int(param))
            elif tag.startswith('MPythonPin'):
                pname, pmode, pnum = tag.split('_')
                pfun = getattr(mpython, pname)
                n = int(pnum)
                val = int(value)
                if pmode == 'digital':
                    pin = pfun(n, 2)
                    pin.write_digital(val)
                elif pmode == 'analog':
                    pin = pfun(n, 3)
                    pin.write_analog(val)
            elif tag.startswith('client'):
                cmd = getattr(appclient, value.strip())
                cmd()                
        except Exception as e:
            print(" error for board data writing!:%s" % e)
        return ["STORED", raw_tag, value]


class Server:
    def __init__(self):
        self.handlers = {}
        self.server_socket = None
        self.client_socket = None

    def _start_server(self, port=8888, accept_handler=None):
        self.stop()
        gc.collect()
        try:
            s = socket.socket()
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            ai = socket.getaddrinfo("0.0.0.0", port)
            server_addr = ai[0][-1]
            s.bind(server_addr)
            s.listen(5)
            if accept_handler:
                s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)
            self.server_socket = s
            for i in (network.AP_IF, network.STA_IF):
                iface = network.WLAN(i)
                if iface.active():
                    suc_info = 'tinywebio started on http://'
                    print("%s%s:%d" % (suc_info, iface.ifconfig()[0], port))
        except Exception as e:
            print("appserver error occurred!:%s" % e)
        return self.server_socket
   
    def start(self, port=8888):
        self._start_server(port, self.connect_client)

    def start_foreground(self, port=8888):
        socket = self._start_server(port, None)
        if socket:
            while True:
                self.connect_client(socket)

    def route(self, url):
        def wrapper(func):
            self.handlers[url] = func
            return func
        return wrapper
    
    def connect_client(self, socket):
        csock, caddr = socket.accept()
        self.client_socket = csock
        request = Request(csock)
        response = Response(csock)
        board = Board()

        try:
            self.process_data(request, response, board)
        except Exception as e:
            print("client connection failure!:%s" % e)
        finally:
            self.client_socket.close()
            csock.close()
    
    def process_data(self, request, response, board):
        request.parse()
        path = request.path
        if path:
            handler = self.get_handler(path)
            if handler:
                handler(request, response, board)
    
    def get_handler(self, path):
        if path in self.handlers.keys():
            return self.handlers[path]
        else:
            return None
    
    def stop(self):
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()


class Remote:
    def __init__(self, url, lasttask):
        self.lasttask = lasttask
        self.method = 'POST'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.puburl = '%s/storeavalue' % url
        self.suburl = '%s/getvalue' % url

    def pub(self, tag, value):
        _val = value[-1]
        _data = 'tag=%s&value=%s' % (tag, _val)
        request(self.method, self.puburl, data=_data, headers=self.headers)

    def sub(self, tag):
        _data = 'tag=%s' % tag
        _res = request(self.method, self.suburl, data=_data, headers=self.headers)
        _val = json.loads(_res.text)[-1].strip('"')
        value = None
        if not _val == self.lasttask[tag]:
            self.lasttask[tag] = _val
            value = _val.split('_')[0]
        return value

class Client:
    def __init__(self):
        self.url = None
        self.topic = {'pub': [], 'sub': []}
        self.interval = 1000
        self.tim = None
        self.lasttask = {}
        self.currtask = None
        self.tasks = {}

    def task(self, name):
        def wrapper(func):
            self.tasks[name] = func
            return func
        return wrapper

    def setup(self, url=None, pub='', sub='', interval=1000):
        self.url = 'http://%s' % url
        self.topic['pub'] = pub.split(',')
        self.topic['sub'] = sub.split(',')
        for _topic in self.topic['sub']:
            self.lasttask[_topic.strip()] = None
        self.interval = interval
        print('TinywebDB server address:%s/%s' % (self.url, hexlify(unique_id()).decode()))

    def exec(self):
        _board = Board()
        _url = '%s/%s' % (self.url, _board.id)
        _remote = Remote(_url, self.lasttask)
        _topic = self.topic
        _tasks = self.tasks
        while True:
            try:
                for _id in _tasks.keys():
                    _task = _tasks[_id]
                    if _task:
                        _task(_remote, _topic, _board)
            except Exception as e:
                print('executing task failure:%s' % e)

            gc.collect()
            yield

    def start(self):
        self.stop()
        try:
            # settime()
            self.tim = Timer(1)
            self.currtask = self.exec()
            next(self.currtask)
            if len(self.url) > 0 and (len(self.topic['pub']) > 0 or len(self.topic['sub']) > 0):
                self.tim.init(period=self.interval, mode=Timer.PERIODIC, callback=lambda t: self.currtask.send(None))
        except Exception as e:
            print('starting client failure:%s' % e)

    def stop(self):
        if self.currtask:
            self.currtask.close()
        if self.tim:
            self.tim.deinit()
        gc.collect()

appclient = Client()
appserver = Server()
gc.collect()

@appserver.route('/')
def index(request, response, board):
    title = '%s' % __version__
    content = '''
    <p>\u529f\u80fd\u5217\u8868
      <ul>
        <li><a href="/storeavalue">/storeavalue</a>: \u5199\u5165\u6570\u636e</li>
        <li><a href="/getvalue">/getvalue</a>: \u8bfb\u53d6\u6570\u636e</li>
      </ul>
    </p>
    '''
    response.make_page(title, content)
    response.send()

@appserver.route('/getvalue')
def getValue(request, response, board):
    if request.method == 'POST':
        tag = request.form['tag']
        fmt = request.form['fmt']
        result = board.read(tag)
        response.data_type = fmt
        response.make(result)
        response.send()
    elif request.method == 'GET':
        title = '\u8bfb\u53d6\u6570\u636e'
        content = '''
        <form action="/getvalue" method="post" enctype=application/x-www-form-urlencoded target="result">
            <label for="tag">\u6807\u7b7e</label><input type="text" name="tag" class="card w-100" />
            <input type="hidden" name="fmt" value="html">
            <input type="submit" value="\u8bfb\u53d6" class="btn primary">
        </form>
        <div class='row'>
            <iframe name='result' frameborder='0' scrolling='no' class='col c12'></iframe>
        </div>
        '''
        response.make_page(title, content)
        response.send()

@appserver.route('/storeavalue')
def storeAValue(request, response, board):
    if request.method == 'POST':
        tag = request.form['tag']
        value = request.form['value']
        fmt = request.form['fmt']
        result = board.write(tag, value)
        response.data_type = fmt
        response.make(result)
        response.send()
    elif request.method == 'GET':
        title = '\u5199\u5165\u6570\u636e'
        content = '''
        <form action="/storeavalue" method="post" enctype=application/x-www-form-urlencoded target="result">
            <label for="tag">\u6807\u7b7e</label><input type="text" name="tag" class="card w-100" />
            <label for="value">\u6570\u503c</label><input type="text" name="value" class="card w-100" />
            <input type="hidden" name="fmt" value="html">
            <input type="submit" value="\u5199\u5165" class="btn primary">
        </form>
        <div class='row'>
            <iframe name='result' frameborder='0' scrolling='no' class='col c12'></iframe>
        </div>
        '''
        response.make_page(title, content)
        response.send()

@appclient.task('publish')
def publishTask(remote, topic, board):
    for _tag in topic['pub']:
        tag = _tag.strip()
        val = board.read(tag)
        remote.pub(tag, val)

@appclient.task('subscribe')
def subscribeTask(remote, topic, board):
    for _tag in topic['sub']:
        tag = _tag.strip()
        val = remote.sub(tag)
        if val:
            board.write(tag, val)

if __name__ == "__main__":
    appserver.start()