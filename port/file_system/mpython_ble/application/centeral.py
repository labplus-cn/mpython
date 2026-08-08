# The MIT License (MIT)

# Copyright (c) 2020, Tangliufeng for labplus Industries

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import bluetooth
from bluetooth import UUID
from ..gatts import Profile
from ..services import Service
from ..characteristics import Characteristic
from ..advertising import decode_name, BLEError
from ..const import IRQ, AdvType
import time


class Centeral(object):
    """ 中央设备 """

    def __init__(self, name=b'mpy_centeral'):

        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.config(gap_name=name)
        print("BLE: activated!")
        self.ble.irq(self._irq)
        self._debug = False
        self._reset()

    def _reset(self):
        # self._conn_type = None
        self._name_param = b''
        self._addr_param = None
        self._conn_info = None
        self._conn_status = 0x00
        self.connected_handle = None
        self.profile = Profile()
        self._notify_cb = None
        self._read_buf = b''
        self._dicov_service_num = None
        self._dicov_charact_done = False
        self._READ_DONE = False
        # self._WRITE_DONE = None

    def _irq(self, event, data):
        if self._debug:
            print("Event: {}, Data: {}".format(event, data))
        if event == IRQ.IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            if self._conn_info is None:
                name = decode_name(adv_data)
                if name == self._name_param or addr == self._addr_param:
                    if adv_type in (AdvType.ADV_IND, AdvType.ADV_DIRECT_IND,):
                        self.ble.gap_scan(None)
                        # Note: The addr buffer is owned by modbluetooth, need to copy it.
                        self._conn_info = (addr_type, bytes(addr), name, adv_type, rssi)
                    else:
                        raise BLEError("{} BLE Device is unconnectable!" .format(name))

        elif event == IRQ.IRQ_SCAN_DONE:
            # find device
            if self._conn_info is not None:
                self.ble.gap_connect(self._conn_info[0], self._conn_info[1])
            else:
                print("BLE: Not found device!")
                self._conn_status = 0xff

        elif event == IRQ.IRQ_PERIPHERAL_CONNECT:
            print("BLE: connect successful!")
            # Connect successful.
            conn_handle, addr_type, addr, = data
            self.connected_handle = conn_handle
            self._conn_status = 0x01
            self.ble.gattc_discover_services(self.connected_handle)

        elif event == IRQ.IRQ_PERIPHERAL_DISCONNECT:
            # # Disconnect (either initiated by us or the remote end).
            conn_handle, _, _, = data
            if conn_handle == self.connected_handle:
                # If it was initiated by us, it'll already be reset.
                print("BLE: disconnected!")
                self._reset()

        elif event == IRQ.IRQ_GATTC_SERVICE_RESULT:
            # Connected device returned a service.
            conn_handle, start_handle, end_handle, uuid = data
            if conn_handle == self.connected_handle:
                service = Service(UUID(uuid))
                service.value_handle = (start_handle, end_handle)
                self.profile.add_services(service)

        elif event == IRQ.IRQ_GATTC_SERVICE_DONE:
            # Called once service discovery is complete.
            # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, status = data
            if conn_handle == self.connected_handle:
                if status == 0:
                    self._conn_status = 0x02
                else:
                    print("BLE: dicscovery services error.")
                    self.disconnect()

        elif event == IRQ.IRQ_GATTC_CHARACTERISTIC_RESULT:
            # Connected device returned a characteristic.
            conn_handle, def_handle, value_handle, properties, uuid = data
            if conn_handle == self.connected_handle:
                characteristic = Characteristic(UUID(uuid))
                characteristic._properties(properties)
                characteristic.value_handle = value_handle
                self.profile[self._service_num].add_characteristics(characteristic)

        elif event == IRQ.IRQ_GATTC_CHARACTERISTIC_DONE:
            # Called once service discovery is complete.
            # Note: Status will be zero on success, implementation-specific value otherwise.
            conn_handle, status = data
            self._dicov_charact_done = True

        elif event == IRQ.IRQ_GATTC_READ_RESULT:
            # A read completed successfully.
            conn_handle, value_handle, char_data = data
            if conn_handle == self.connected_handle:
                self._READ_DONE = True
                self._read_buf = char_data

        elif event == IRQ.IRQ_GATTC_WRITE_DONE:
            # A gattc_write() has completed.
            conn_handle, value_handle, status = data
            # if conn_handle == self.connected_handle and status == 0:
            #     self._WRITE_DONE = True
            # else:
            #     self._WRITE_DONE = False

        elif event == IRQ.IRQ_GATTC_NOTIFY:
            conn_handle, value_handle, notify_data = data
            if conn_handle == self.connected_handle:
                if self._notify_cb:
                    self._notify_cb(value_handle, notify_data)

    def connect(self, name=b'', addr=None):
        self._reset()
        if name != b'':
            self._name_param = name
        elif addr is not None:
            self._addr_param = addr
        self.ble.gap_scan(3000, 30000, 30000)
        # Waitting scan done
        while not (self._conn_info or self._conn_status == 0xff):
            pass
        # not found device
        if self._conn_status == 0xff:
            return None
        # Waitting connection
        while not self._conn_status == 0x01:
            pass
        # Waitting dicovery service done event
        while not self._conn_status == 0x02:
            # if disconnect
            if self._conn_status == 0x00:
                return None
        # poll discover_characteristics
        for num, service in enumerate(self.profile.services):
            self._service_num = num
            self.ble.gattc_discover_characteristics(self.connected_handle, service.value_handle[0], service.value_handle[1])
            # waitting dicscover characteristics done
            while not self._dicov_charact_done:
                pass
            self._dicov_charact_done = False
        self._conn_status = 0x03  # dicscover gatts profile done
        if self.is_connected():
            return self.profile
        else:
            return None

    def is_connected(self):
        return self.connected_handle is not None

    def connected_info(self):
        return self._conn_info

    def disconnect(self):
        if self.connected_handle is not None:
            self.ble.gap_disconnect(self.connected_handle)

    def characteristic_read(self, value_handle):
        if self.is_connected():
            self.ble.gattc_read(self.connected_handle, value_handle)
        else:
            return None
        while not self._READ_DONE:
            pass
        self._READ_DONE = False
        return self._read_buf

    def characteristic_write(self, value_handle, data):
        if self.is_connected():
            self.ble.gattc_write(self.connected_handle, value_handle, data)
        else:
            return False
        # while self._WRITE_DONE is None:
        #     pass
        # temp = self._WRITE_DONE
        # self._WRITE_DONE = None
        # return temp

    def notify_callback(self, callback):
        self._notify_cb = callback
