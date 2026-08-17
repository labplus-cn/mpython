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

from micropython import const


class IRQ(object):
    IRQ_CENTRAL_CONNECT = const(1)
    IRQ_CENTRAL_DISCONNECT = const(2)
    IRQ_GATTS_WRITE = const(3)
    IRQ_GATTS_READ_REQUEST = const(4)
    IRQ_SCAN_RESULT = const(5)
    IRQ_SCAN_DONE = const(6)
    IRQ_PERIPHERAL_CONNECT = const(7)
    IRQ_PERIPHERAL_DISCONNECT = const(8)
    IRQ_GATTC_SERVICE_RESULT = const(9)
    IRQ_GATTC_SERVICE_DONE = const(10)
    IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
    IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
    IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
    IRQ_GATTC_DESCRIPTOR_DONE = const(14)
    IRQ_GATTC_READ_RESULT = const(15)
    IRQ_GATTC_READ_DONE = const(16)
    IRQ_GATTC_WRITE_DONE = const(17)
    IRQ_GATTC_NOTIFY = const(18)
    IRQ_GATTC_INDICATE = const(19)
    IRQ_ALL = const(0xffff)


class ADType(object):
    """
    Advertising Data Type
    """

    AD_TYPE_FLAGS = const(0x01)  # Flags for discoverability.
    # ADV_TYPE_UUID16_MORE = const(0x02)  # Partial list of 16 bit service UUIDs.
    ADV_TYPE_UUID16_COMPLETE = const(0x03)  # Complete list of 16 bit service UUIDs.
    # ADV_TYPE_UUID32_MORE = const(0x04)  # Partial list of 32 bit service UUIDs.
    # ADV_TYPE_UUID32_COMPLETE = const(0x05)  # Complete list of 32 bit service UUIDs.
    # ADV_TYPE_UUID128_MORE = const(0x06)  # Partial list of 128 bit service UUIDs.
    ADV_TYPE_UUID128_COMPLETE = const(0x07)  # Complete list of 128 bit service UUIDs.
    AD_TYPE_SHORT_LOCAL_NAME = const(0x08)  # Short local device name.
    AD_TYPE_COMPLETE_LOCAL_NAME = const(0x09)  # Complete local device name.
    AD_TYPE_TX_POWER_LEVEL = const(0x0A)  # Transmit power level.
    AD_TYPE_APPEARANCE = const(0x19)  # Appearance.
    AD_TYPE_MANUFACTURER_SPECIFIC_DATA = const(0xFF) # Manufacturer Specific Data.

class AdvType(object):
    """
    Advertising Event Type
    """
    ADV_IND = const(0x00)
    ADV_DIRECT_IND = const(0x01)
    ADV_SCAN_IND = const(0x02)
    ADV_NONCONN_IND = const(0x03)
    SCAN_RSP  = const(0x04)