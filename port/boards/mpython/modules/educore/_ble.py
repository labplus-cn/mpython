from mpython_ble.hidcode import Mouse as _Mouse
from mpython_ble.hidcode import KeyboardCode as _KeyboardCode

class KeyboardCode():
    SPACE = 0
    CLICK = 1
    DCLICK = 2

class Mouse():
    SPACE = 0

class HID():
    def __init__(self, name='mpy_hid'):
        from mpython_ble.application import HID as _HID
        self.connection_state = False
        self._ble_hid = _HID(name=bytes(name, 'utf-8'), battery_level=100)
        self._ble_hid.hid_device.connection_callback(self._ble_hid_connect_callback)
        # 广播
        self._ble_hid.advertise(True)
    
    def _ble_hid_connect_callback(self, _1, _2, _3):
        self.connection_state = True

    def isconnected(self):
        return self.connection_state

    def keyboard_send(self,key):
        self._ble_hid.keyboard_send(_KeyboardCode.SPACE)

    def mouse_key(self,key):
        if(key==1):
            self._ble_hid.mouse_click(_Mouse.LEFT)
        elif(key==2):
            self._ble_hid.mouse_click(_Mouse.LEFT)
            time.sleep(0.1)
            self._ble_hid.mouse_click(_Mouse.LEFT)