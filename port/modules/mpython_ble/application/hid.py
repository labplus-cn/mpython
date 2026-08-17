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
from ..descriptors import Descriptor
from .peripheral import Peripheral
from micropython import const
import struct

REPORT_MAP_DATA = (

    # HID 鼠标设备报告描述符
    # INPUT(report id = 1)
    #
    # byte0 buttons
    # byte1 X
    # byte2 Y
    # byte3 Wheel

    b"\x05\x01"  # Usage Page (Generic Desktop)
    b"\x09\x02"  # Usage (Mouse)
    b"\xA1\x01"  # Collection (Application)
    b"\x85\x01"  # Report Id (1)
    b"\x09\x01"  # Usage (Pointer)
    b"\xA1\x00"  # Collection (Physical)
    b"\x05\x09"  # Usage Page (Buttons)
    b"\x19\x01"  # Usage Minimum (01) - Button 1
    b"\x29\x03"  # Usage Maximum (03) - Button 3
    b"\x15\x00"  # Logical Minimum (0)
    b"\x25\x01"  # Logical Maximum (1)
    b"\x75\x01"  # Report Size (1)
    b"\x95\x03"  # Report Count (3)
    b"\x81\x02"  # Input (Data, Variable, Absolute) - Button states
    b"\x75\x05"  # Report Size (5)
    b"\x95\x01"  # Report Count (1)
    b"\x81\x01"  # Input (Constant) - Padding or Reserved bits
    b"\x05\x01"  # Usage Page (Generic Desktop)
    b"\x09\x30"  # Usage (X)
    b"\x09\x31"  # Usage (Y)
    b"\x09\x38"  # Usage (Wheel)
    b"\x15\x81"  # Logical Minimum (-127)
    b"\x25\x7F"  # Logical Maximum (127)
    b"\x75\x08"  # Report Size (8)
    b"\x95\x03"  # Report Count (3)
    b"\x81\x06"  # Input (Data, Variable, Relative) - X & Y coordinate
    b"\xC0"  # End Collection
    b"\xC0"        # End Collection

    # HID 键盘设备报告描述符
    # INPUT(report id = 2)
    #
    # byte0: Modified byte
    # byte1: reverse
    # byte2: key1
    # byte3: key2
    # byte4: key3
    # byte5: key4
    # byte6: key5
    # byte7: key6
    b"\x05\x01"  # Usage Pg (Generic Desktop)
    b"\x09\x06"  # Usage (Keyboard)
    b"\xA1\x01"  # Collection: (Application)
    b"\x85\x02"  # Report Id (2)
    b"\x05\x07"  # Usage Pg (Key Codes)
    b"\x19\xE0"  # Usage Min (224)
    b"\x29\xE7"  # Usage Max (231)
    b"\x15\x00"  # Log Min (0)
    b"\x25\x01"  # Log Max (1)
    #   Modifier byte
    b"\x75\x01"  # Report Size (1)
    b"\x95\x08"  # Report Count (8)
    b"\x81\x02"  # Input: (Data, Variable, Absolute)
    #   Reserved byte
    b"\x95\x01"  # Report Count (1)
    b"\x75\x08"  # Report Size (8)
    b"\x81\x01"  # Input: (Constant)
    #   LED report
    b"\x95\x05"  # Report Count (5)
    b"\x75\x01"  # Report Size (1)
    b"\x05\x08"  # Usage Pg (LEDs)
    b"\x19\x01"  # Usage Min (1)
    b"\x29\x05"  # Usage Max (5)
    b"\x91\x02"  # Output: (Data, Variable, Absolute)
    #   LED report padding
    b"\x95\x01"  # Report Count (1)
    b"\x75\x03"  # Report Size (3)
    b"\x91\x01"  # Output: (Constant)
    #   Key arrays (6 bytes)
    b"\x95\x06"  # Report Count (6)
    b"\x75\x08"  # Report Size (8)
    b"\x15\x00"  # Log Min (0)
    b"\x25\x65"  # Log Max (101)
    b"\x05\x07"  # Usage Pg (Key Codes)
    b"\x19\x00"  # Usage Min (0)
    b"\x29\x65"  # Usage Max (101)
    b"\x81\x00"  # Input: (Data, Array)
    b"\xC0"        # End Collection
    # HID 消费电子设备
    b"\x05\x0C"  # Usage Page (Consumer)
    b"\x09\x01"  # Usage (Consumer Control)
    b"\xA1\x01"  # Collection (Application)
    b"\x85\x03"  #   Report ID (3)
    b"\x75\x10"  #   Report Size (16)
    b"\x95\x01"  #   Report Count (1)
    b"\x15\x01"  #   Logical Minimum (1)
    b"\x26\x8C\x02"  #   Logical Maximum (652)
    b"\x19\x01"  #   Usage Minimum (Consumer Control)
    b"\x2A\x8C\x02"  #   Usage Maximum (AC Send)
    b"\x81\x00"  #   Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    b"\xC0"  # End Collection
)


class HID(object):
    """BLE HID Device"""

    def __init__(self, name=b'mpy_hid', battery_level=100):
        # Human Interface Device
        humman_interface_service = Service(UUID(0x1812))

        hid_information = Characteristic(UUID(0x2A4A), properties='-r')
        hid_control_point = Characteristic(UUID(0x2A4C), properties='-r')
        self._report_map = Characteristic(UUID(0x2A4B), properties='-r')

        # Report input: Report Reference
        self._report_mouse_char = Characteristic(UUID(0x2A4D), properties='-rn')
        self._report_keyboard_char = Characteristic(UUID(0x2A4D), properties='-rn')
        self._report_consumer_char = Characteristic(UUID(0x2A4D), properties='-rn')

        self._report_mouse_char.add_descriptors(Descriptor(UUID(0x2908), properties='-r'))
        self._report_keyboard_char.add_descriptors(Descriptor(UUID(0x2908), properties='-r'))
        self._report_consumer_char.add_descriptors(Descriptor(UUID(0x2908), properties='-r'))

        humman_interface_service.add_characteristics(hid_information, hid_control_point, self._report_map,
                                                     self._report_mouse_char, self._report_keyboard_char, self._report_consumer_char)

        # Battery Service
        battery_service = Service(UUID(0x180F))
        battery_service.add_characteristics(Characteristic(UUID(0x2A19), properties='-rn'))

        # gatt profile
        self.profile = Profile()
        self.profile.add_services(humman_interface_service, battery_service)
        # Instantiation ble peripheral

        self.hid_device = Peripheral(profile=self.profile, name=name, appearance=const(960),
                                     adv_services=self.profile.services_uuid)
        self._debug = self.hid_device._debug
        # write battery level
        self.battery_level = battery_level
        self._init_value()
        self.hid_device.advertise(True)

        self._report_mouse_buf = bytearray(4)

        self._report_kb_buf = bytearray(8)
        self._report_kb_modifier = memoryview(self._report_kb_buf)[0:1]
        self._report_kb_keys = memoryview(self._report_kb_buf)[2:]
        
        self._report_consumer_buf = bytearray(2)

    def _init_value(self):
        # write report map
        self.hid_device.attrubute_write(self._report_map.value_handle, bytes(REPORT_MAP_DATA))
        # hid information
        self.hid_device.attrubute_write(self.profile[0][0].value_handle, struct.pack("<Hbb", 0x0111, 0x00, 0b0001))
        # write report reference: <report_id,report_type_input>
        self.hid_device.attrubute_write(self.profile[0][3][0].value_handle, struct.pack("<BB", 0x01, 0x01))
        self.hid_device.attrubute_write(self.profile[0][4][0].value_handle, struct.pack("<BB", 0x02, 0x01))
        self.hid_device.attrubute_write(self.profile[0][5][0].value_handle, struct.pack("<BB", 0x03, 0x01))

    @property
    def battery_level(self):
        return struct.unpack("<B", self.hid_device.attrubute_read(self.profile[1][0].value_handle))[0]

    @battery_level.setter
    def battery_level(self, level):
        self.hid_device.attrubute_write(self.profile[1][0].value_handle, struct.pack('<B', level), notify=True)

    def advertise(self, toggle=True):
        self.hid_device.advertise(toggle)

    def disconnect(self):
        self.hid_device.disconnect()

    # Mouse device

    def mouse_click(self, buttons):
        self.mouse_press(buttons)
        self.mouse_release(buttons)

    def mouse_press(self, buttons):
        self._report_mouse_buf[0] |= buttons
        self._mouse_send_no_move()

    def mouse_release(self, buttons):
        self._report_mouse_buf[0] &= ~buttons
        self._mouse_send_no_move()

    def mouse_release_all(self):
        self._report_mouse_buf[0] = 0x00
        self._mouse_send_no_move()

    def _mouse_send_no_move(self):
        self._report_mouse_buf[1:] = b'\x00' * 3
        self.hid_device.attrubute_write(self._report_mouse_char.value_handle, self._report_mouse_buf, notify=True)

    def mouse_move(self, x=0, y=0, wheel=0):
        while x != 0 or y != 0 or wheel != 0:
            partial_x = self._limit(x)
            partial_y = self._limit(y)
            partial_wheel = self._limit(wheel)
            self._report_mouse_buf[1] = partial_x & 0xff
            self._report_mouse_buf[2] = partial_y & 0xff
            self._report_mouse_buf[3] = partial_wheel & 0xff
            self.hid_device.attrubute_write(self._report_mouse_char.value_handle, self._report_mouse_buf, notify=True)
            x -= partial_x
            y -= partial_y
            wheel -= partial_wheel

    @staticmethod
    def _limit(dist):
        return min(127, max(-127, dist))

    # Keyboard device

    def keyboard_press(self, *keycodes):
        for keycode in keycodes:
            self._kyeboard_add_keycode_to_report(keycode)
        self.hid_device.attrubute_write(self._report_keyboard_char.value_handle, self._report_kb_buf, notify=True)

    def keyboard_release(self, *keycodes):
        for keycode in keycodes:
            self._keyboard_remove_keycode_from_report(keycode)
        self.hid_device.attrubute_write(self._report_keyboard_char.value_handle, self._report_kb_buf, notify=True)

    def keyboard_release_all(self):
        """Release all pressed keys."""
        for i in range(8):
            self._report_kb_buf[i] = 0
        self.hid_device.attrubute_write(self._report_keyboard_char.value_handle, self._report_kb_buf, notify=True)

    def keyboard_send(self, *keycodes):
        self.keyboard_press(*keycodes)
        self.keyboard_release_all()

    @staticmethod
    def _modifier_bit(keycode):
        return 1 << (keycode - 0xE0) if 0xE0 <= keycode <= 0xE7 else 0

    def _kyeboard_add_keycode_to_report(self, keycode):
        """Add a single keycode to the USB HID report."""
        modifier = self._modifier_bit(keycode)
        if modifier:
            # Set bit for this modifier.
            self._report_kb_modifier[0] |= modifier
        else:
            # Don't press twice.
            # (I'd like to use 'not in self.report_keys' here, but that's not implemented.)
            for i in range(6):
                if self._report_kb_keys[i] == keycode:
                    # Already pressed.
                    return
            # Put keycode in first empty slot.
            for i in range(6):
                if self._report_kb_keys[i] == 0:
                    self._report_kb_keys[i] = keycode
                    return

    def _keyboard_remove_keycode_from_report(self, keycode):
        """Remove a single keycode from the report."""
        modifier = self._modifier_bit(keycode)
        if modifier:
            # Turn off the bit for this modifier.
            self._report_kb_modifier[0] &= ~modifier
        else:
            # Check all the slots, just in case there's a duplicate. (There should not be.)
            for i in range(6):
                if self._report_kb_keys[i] == keycode:
                    self._report_kb_keys[i] = 0

    # Consumer Device

    def consumer_send(self, consumer_code):
        struct.pack_into("<H", self._report_consumer_buf, 0, consumer_code)
        self.hid_device.attrubute_write(self._report_consumer_char.value_handle, self._report_consumer_buf, notify=True)
        self._report_consumer_buf[0] = self._report_consumer_buf[1] = 0x0
        self.hid_device.attrubute_write(self._report_consumer_char.value_handle, self._report_consumer_buf, notify=True)
