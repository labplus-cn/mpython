
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

# Helpers for generating BLE advertising payloads.

from micropython import const
import struct
import bluetooth
from ..const import ADType

# Advertising payloads are repeated packets of the following form:
#   1 byte data length (N + 1)
#   1 byte type (see constants below)
#   N bytes type-specific data


class BLEError(Exception):
    pass

class AD_Structure:
    """ AD Structure """
    def __init__(self,ad_type,ad_data):
        self.ad_type = ad_type
        self.ad_data = ad_data


# Generate a payload to be passed to gap_advertise(adv_data=...).


def advertising_payload(limited_disc=False, br_edr=False, name=None, services=None, appearance=None, ad_structure=None):
    payload = bytearray()
    # AD Structure

    def _append(adv_type, value):
        nonlocal payload
        payload += struct.pack('BB', len(value) + 1, adv_type) + value
    # AD Type: flags
    _append(ADType.AD_TYPE_FLAGS, struct.pack('B', (0x01 if limited_disc else 0x02) + (0x18 if br_edr else 0x04)))
    # AD Type: local name
    if name:
        _append(ADType.AD_TYPE_COMPLETE_LOCAL_NAME, name)
    # AD Type: uuid servers
    if services:
        for uuid in services:
            b = bytes(uuid)
            if len(b) == 2:
                _append(ADType.ADV_TYPE_UUID16_COMPLETE, b)
            elif len(b) == 16:
                _append(ADType.ADV_TYPE_UUID128_COMPLETE, b)

    # AD Type: appearance
    if appearance:
        _append(ADType.AD_TYPE_APPEARANCE, struct.pack('<h', appearance))
    # custom expand ad structre
    if ad_structure:
        for ad in ad_structure:
            if isinstance(ad,AD_Structure):
                _append(ad.ad_type,ad.ad_data)
            else:
                raise BLEError('Muse be AD_Structure obj.')
    # Check Adv payload length
    if len(payload) > 31:
        raise BLEError('Avd payload length must not exceed {} Bytes,but now {} Btyes'.format(31, len(payload)))
    return payload


def decode_field(payload, adv_type):
    i = 0
    result = []
    while i + 1 < len(payload):
        if payload[i + 1] == adv_type:
            result.append(payload[i + 2:i + payload[i] + 1])
        i += 1 + payload[i]
    return result


def decode_name(payload):
    n = decode_field(payload, ADType.AD_TYPE_COMPLETE_LOCAL_NAME)
    return n[0] if n else None


def decode_services(payload):
    services = []
    for u in decode_field(payload, ADType.ADV_TYPE_UUID16_COMPLETE):
        services.append(bluetooth.UUID(struct.unpack('<h', u)[0]))
    for u in decode_field(payload, ADType.ADV_TYPE_UUID128_COMPLETE):
        services.append(bluetooth.UUID(u))
    return services


def demo():
    payload = advertising_payload(name='micropython', services=[bluetooth.UUID(
        0x181A), bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')])
    print(payload)
    print(decode_name(payload))
    print(decode_services(payload))


if __name__ == '__main__':
    demo()
