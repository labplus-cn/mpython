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
from ..advertising import advertising_payload
from ..const import IRQ


class Peripheral(object):
    """ 外围设备 """

    def __init__(self, profile, name=b'mpy_ble', appearance=None, adv_services=None, resp_services=None, interval_us=500000, connectable=True):
        self.interval_us = interval_us
        self.connectable = connectable
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.config(gap_name=name)
        print("BLE: activated!")
        self.ble.irq(handler=self._irq)
        self.connections = set()
        profile.handles = self.ble.gatts_register_services(profile.definition)
        self._adv_payload = advertising_payload(name=name, appearance=appearance, services=adv_services)
        self._resp_payload = advertising_payload(services=resp_services)
        self._write_cb = None
        self._connection_cb = None
        # self.advertise(True)
        self._debug = False

    @property
    def mac(self):
        return self.ble.config('mac')

    def write_callback(self, callback):
        self._write_cb = callback

    def connection_callback(self, callback):
        self._connection_cb = callback

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if self._debug:
            print("Event: {}, Data: {}".format(event, data))
        if event == IRQ.IRQ_CENTRAL_CONNECT:
            conn_handle, addr_type, addr = data
            self.connections.add(conn_handle)
            print("BLE: connect successful!")
            if self._connection_cb:
                self._connection_cb(conn_handle, addr_type, addr)
        elif event == IRQ.IRQ_CENTRAL_DISCONNECT:
            conn_handle, addr_type, addr = data
            if conn_handle in self.connections:
                print("BLE: disconnected!")
                self.connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self.advertise(True)
        elif event == IRQ.IRQ_GATTS_WRITE:
            conn_handle, attr_handle = data
            if conn_handle in self.connections:
                if self._write_cb:
                    self._write_cb(conn_handle, attr_handle, self.attrubute_read(attr_handle))

    def advertise(self, toggle=True):
        if toggle:
            self.ble.gap_advertise(self.interval_us, adv_data=self._adv_payload,
                                   resp_data=self._resp_payload, connectable=self.connectable)
        else:
            self.ble.gap_advertise(interval_us=None)

    def attrubute_write(self, value_handle, data, notify=False):
        self.ble.gatts_write(value_handle, data)
        if notify:
            for conn_handle in self.connections:
                # Notify connected centrals to issue a read.
                self.ble.gatts_notify(conn_handle, value_handle)

    def attrubute_read(self, value_handle):
        return self.ble.gatts_read(value_handle)

    def disconnect(self):
        for conn_handle in self.connections:
            self.ble.gap_disconnect(conn_handle)
        self.connections.clear()
