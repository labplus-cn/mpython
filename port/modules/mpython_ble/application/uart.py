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

from bluetooth import UUID
from ..gatts import Profile
from ..services import Service
from ..characteristics import Characteristic
from .peripheral import Peripheral
from .centeral import Centeral, BLEError


class BLEUART():
    """ UART (Transmit transparently) """

    """role"""
    SLAVE = 0
    MASTER = 1
    
    def __init__(self, name=b'ble_uart', appearance=0, rxbuf=100, role=0, slave_mac=None):
        self.role = role
        UART_SERVICE = Service(UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E'))
        UART_TX = Characteristic(UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), properties='-n')
        UART_RX = Characteristic(UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), properties='-w')
        self._rx_cb = None
        connected = False
        if self.role == 0:
            profile = Profile()
            profile.add_services(UART_SERVICE.add_characteristics(UART_TX, UART_RX))
            self.ble = Peripheral(name=name, profile=profile, resp_services=profile.services_uuid, appearance=appearance)
            self._rx_handle, self._tx_handle = UART_RX.value_handle, UART_TX.value_handle
            self.ble.ble.gatts_set_buffer(self._rx_handle, rxbuf, True)
            self.ble.write_callback(self._uart_cb_s)
            self.ble.advertise(True)
        else:
            self.ble = Centeral()
            while not connected:
                self.profile = self.ble.connect(name=name) if slave_mac is None else self.ble.connect(addr=slave_mac)
                if self.profile:
                    connected = True
            # discovery rx,tx value_handle
            for service in self.profile:
                if service.uuid == UART_SERVICE.uuid:
                    for characteristics in service:
                        if characteristics.uuid == UART_TX.uuid:
                            self._rx_handle = characteristics.value_handle
                        elif characteristics.uuid == UART_RX.uuid:
                            self._tx_handle = characteristics.value_handle
            self.ble.notify_callback(self._uart_cb_m)

        self.rx_buffer = bytearray()

    def _uart_cb_s(self, conn_handle, attr_handle, data):
        if attr_handle == self._rx_handle:
            self.rx_buffer += data
            if self._rx_cb:
                self._rx_cb()

    def _uart_cb_m(self, attr_handle, data):
        if attr_handle == self._rx_handle:
            self.rx_buffer += data
            if self._rx_cb:
                self._rx_cb()

    def is_connected(self):
        if self.role == self.SLAVE:
            return True if self.ble.connections != set() else False
        elif self.role == self.MASTER:
            return self.ble.is_connected()


    def irq(self, handler):
        self._rx_cb = handler

    def any(self):
        return len(self.rx_buffer)

    def read(self, size=None):
        if not size:
            size = len(self.rx_buffer)
        result = self.rx_buffer[0:size]
        self.rx_buffer = self.rx_buffer[size:]
        return result

    def write(self, data):
        if self.role == self.SLAVE:
            self.ble.attrubute_write(self._tx_handle, data, notify=True)
        else:
            self.ble.characteristic_write(self._tx_handle, data)
      
    def close(self):
        self.ble.disconnect()
