# The MIT License (MIT)
#
#  Ported from the Javascript library by Sam Curren
#  QRCode for Javascript
#  http://d-project.googlecode.com/svn/trunk/misc/qrcode/js/qrcode.js
#
#  Copyright (c) 2009 Kazuhiko Arase
#  URL: http://www.d-project.com/
#
#  Minimized for CircuitPython by ladyada for adafruit industries
#
#  Licensed under the MIT license:
#    http://www.opensource.org/licenses/mit-license.php
#
#  The word "QR Code" is registered trademark of
#  DENSO WAVE INCORPORATED
#    http://www.denso-wave.com/qrcode/faqpatent-e.html
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_miniqr`
====================================================

A non-hardware dependant miniature QR generator library. All native Python!

* Author(s): ladyada

Implementation Notes
--------------------

**Hardware:**

* Any!

**Software and Dependencies:**

* Python 3

"""

# imports
import math

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_miniQR.git"

# Consts!
M = 0
L = 1
H = 2
Q = 3

_MODE_8BIT_BYTE = 1 << 2
_PAD0 = 0xEC
_PAD1 = 0x11

# Optimized polynomial helpers

def _glog(n):
    """Lookup log(n) from pre-calculated byte table"""
    if n < 1:
        raise ValueError("glog(" + n + ")")
    return LOG_TABLE[n]

def _gexp(n):
    """Lookup exp(n) from pre-calculated byte table"""
    while n < 0:
        n += 255
    while n >= 256:
        n -= 255
    return EXP_TABLE[n]

#pylint: disable=line-too-long
EXP_TABLE = b'\x01\x02\x04\x08\x10 @\x80\x1d:t\xe8\xcd\x87\x13&L\x98-Z\xb4u\xea\xc9\x8f\x03\x06\x0c\x180`\xc0\x9d\'N\x9c%J\x945j\xd4\xb5w\xee\xc1\x9f#F\x8c\x05\n\x14(P\xa0]\xbai\xd2\xb9o\xde\xa1_\xbea\xc2\x99/^\xbce\xca\x89\x0f\x1e<x\xf0\xfd\xe7\xd3\xbbk\xd6\xb1\x7f\xfe\xe1\xdf\xa3[\xb6q\xe2\xd9\xafC\x86\x11"D\x88\r\x1a4h\xd0\xbdg\xce\x81\x1f>|\xf8\xed\xc7\x93;v\xec\xc5\x973f\xcc\x85\x17.\\\xb8m\xda\xa9O\x9e!B\x84\x15*T\xa8M\x9a)R\xa4U\xaaI\x929r\xe4\xd5\xb7s\xe6\xd1\xbfc\xc6\x91?~\xfc\xe5\xd7\xb3{\xf6\xf1\xff\xe3\xdb\xabK\x961b\xc4\x957n\xdc\xa5W\xaeA\x82\x192d\xc8\x8d\x07\x0e\x1c8p\xe0\xdd\xa7S\xa6Q\xa2Y\xb2y\xf2\xf9\xef\xc3\x9b+V\xacE\x8a\t\x12$H\x90=z\xf4\xf5\xf7\xf3\xfb\xeb\xcb\x8b\x0b\x16,X\xb0}\xfa\xe9\xcf\x83\x1b6l\xd8\xadG\x8e\x01'

LOG_TABLE = b'\x00\x00\x01\x19\x022\x1a\xc6\x03\xdf3\xee\x1bh\xc7K\x04d\xe0\x0e4\x8d\xef\x81\x1c\xc1i\xf8\xc8\x08Lq\x05\x8ae/\xe1$\x0f!5\x93\x8e\xda\xf0\x12\x82E\x1d\xb5\xc2}j\'\xf9\xb9\xc9\x9a\txM\xe4r\xa6\x06\xbf\x8bbf\xdd0\xfd\xe2\x98%\xb3\x10\x91"\x886\xd0\x94\xce\x8f\x96\xdb\xbd\xf1\xd2\x13\\\x838F@\x1eB\xb6\xa3\xc3H~nk:(T\xfa\x85\xba=\xca^\x9b\x9f\n\x15y+N\xd4\xe5\xacs\xf3\xa7W\x07p\xc0\xf7\x8c\x80c\rgJ\xde\xed1\xc5\xfe\x18\xe3\xa5\x99w&\xb8\xb4|\x11D\x92\xd9# \x89.7?\xd1[\x95\xbc\xcf\xcd\x90\x87\x97\xb2\xdc\xfc\xbea\xf2V\xd3\xab\x14*]\x9e\x84<9SGmA\xa2\x1f-C\xd8\xb7{\xa4v\xc4\x17I\xec\x7f\x0co\xf6l\xa1;R)\x9dU\xaa\xfb`\x86\xb1\xbb\xcc>Z\xcbY_\xb0\x9c\xa9\xa0Q\x0b\xf5\x16\xebzu,\xd7O\xae\xd5\xe9\xe6\xe7\xad\xe8t\xd6\xf4\xea\xa8PX\xaf'
#pylint: enable=line-too-long

class QRCode:
    """The generator class for QR code matrices"""
    def __init__(self, *, qr_type=None, error_correct=L):
        """Initialize an empty QR code. You can define the `qr_type` (size)
        of the code matrix, or have the libary auto-select the smallest
        match. Default `error_correct` is type L (7%), but you can select M,
        Q or H."""
        self.type = qr_type
        self.ECC = error_correct  #pylint: disable=invalid-name
        self.matrix = None
        self.module_count = 0
        self.data_cache = None
        self.data_list = []

    def add_data(self, data):
        """Add more data to the QR code, must be bytestring stype"""
        self.data_list.append(data)
        datalen = sum([len(x) for x in self.data_list])
        if not self.type:
            for qr_type in range(1, 6):
                rs_blocks = _get_rs_blocks(qr_type, self.ECC)
                total_data_count = 0
                for block in rs_blocks:
                    total_data_count += block['data']
                if total_data_count > datalen:
                    self.type = qr_type
                    break
        self.data_cache = None

    def make(self, *, test=False, mask_pattern=0):
        """Perform the actual generation of the QR matrix. To keep things
        small and speedy we don't generate all 8 mask patterns and pick
        the best. Instead, please pass in a desired mask_pattern, the
        default mask is 0."""
        self.module_count = self.type * 4 + 17
        self.matrix = QRBitMatrix(self.module_count, self.module_count)

        self._setup_position_probe_pattern(0, 0)
        self._setup_position_probe_pattern(self.module_count - 7, 0)
        self._setup_position_probe_pattern(0, self.module_count - 7)
        self._setup_position_adjust_pattern()
        self._setup_timing_pattern()
        self._setup_type_info(test, mask_pattern)

        if self.type >= 7:
            self._setup_type_number(test)

        if self.data_cache is None:
            self.data_cache = QRCode._create_data(self.type, self.ECC, self.data_list)
        self._map_data(self.data_cache, mask_pattern)

    def _setup_position_probe_pattern(self, row, col):
        """Add the positition probe data pixels to the matrix"""
        for r in range(-1, 8):
            if (row + r <= -1 or self.module_count <= row + r):
                continue
            for c in range(-1, 8):   #pylint: disable=invalid-name
                if (col + c <= -1 or self.module_count <= col + c):
                    continue
                test = ((r >= 0 and r <= 6 and (c == 0 or c == 6))
                        or (c >= 0 and c <= 6 and (r == 0 or r == 6))
                        or (r >= 2 and r <= 4 and c >= 2 and c <= 4))
                self.matrix[row+r, col+c] = test
    def _setup_timing_pattern(self):
        """Add the timing data pixels to the matrix"""
        for r in range(8, self.module_count-8):
            if (self.matrix[r, 6] != None):
                continue
            self.matrix[r, 6] = (r % 2 == 0)

        for c in range(8, self.module_count-8): #pylint: disable=invalid-name
            if (self.matrix[6, c] != None):
                continue
            self.matrix[6, c] = (c % 2 == 0)

    def _setup_position_adjust_pattern(self):
        """Add the position adjust data pixels to the matrix"""
        pos = QRUtil.get_pattern_position(self.type)

        for row in pos:
            for col in pos:
                if (self.matrix[row, col] != None):
                    continue

                for r in range(-2, 3):
                    for c in range(-2, 3):  #pylint: disable=invalid-name
                        test = (abs(r) == 2 or abs(c) == 2 or
                                (r == 0 and c == 0))
                        self.matrix[row+r, col+c] = test

    def _setup_type_number(self, test):
        """Add the type number pixels to the matrix"""
        bits = QRUtil.get_BCH_type_number(self.type)

        for i in range(18):
            mod = not test and ((bits >> i) & 1) == 1
            self.matrix[i // 3, i % 3 + self.module_count - 8 - 3] = mod

        for i in range(18):
            mod = not test and ((bits >> i) & 1) == 1
            self.matrix[i % 3 + self.module_count - 8 - 3, i // 3] = mod

    def _setup_type_info(self, test, mask_pattern):
        """Add the type info pixels to the matrix"""
        data = (self.ECC << 3) | mask_pattern
        bits = QRUtil.get_BCH_type_info(data)

        #// vertical
        for i in range(15):
            mod = not test and ((bits >> i) & 1) == 1
            if i < 6:
                self.matrix[i, 8] = mod
            elif i < 8:
                self.matrix[i + 1, 8] = mod
            else:
                self.matrix[self.module_count - 15 + i, 8] = mod

        #// horizontal
        for i in range(15):
            mod = not test and ((bits >> i) & 1) == 1
            if i < 8:
                self.matrix[8, self.module_count - i - 1] = mod
            elif i < 9:
                self.matrix[8, 15 - i - 1 + 1] = mod
            else:
                self.matrix[8, 15 - i - 1] = mod

        #// fixed module
        self.matrix[self.module_count - 8, 8] = (not test)

    def _map_data(self, data, mask_pattern):
        """Map the data onto the QR code"""
        inc = -1
        row = self.module_count - 1
        bit_idx = 7
        byte_idx = 0

        for col in range(self.module_count - 1, 0, -2):
            if col == 6:
                col -= 1

            while True:
                for c in range(2):  #pylint: disable=invalid-name
                    if self.matrix[row, col - c] is None:
                        dark = False
                        if byte_idx < len(data):
                            dark = ((data[byte_idx] >> bit_idx) & 1) == 1
                        mask = QRUtil.get_mask(mask_pattern, row, col - c)
                        if mask:
                            dark = not dark
                        self.matrix[row, col-c] = dark
                        bit_idx -= 1
                        if bit_idx == -1:
                            byte_idx += 1
                            bit_idx = 7
                row += inc
                if row < 0 or self.module_count <= row:
                    row -= inc
                    inc = -inc
                    break

    @staticmethod
    def _create_data(qr_type, ecc, data_list):
        """Check and format data into bit buffer"""
        rs_blocks = _get_rs_blocks(qr_type, ecc)

        buffer = QRBitBuffer()

        for data in data_list:
            buffer.put(_MODE_8BIT_BYTE, 4)
            buffer.put(len(data), 8)
            for byte in data:
                buffer.put(byte, 8)

        #// calc num max data.
        total_data_count = 0
        for block in rs_blocks:
            total_data_count += block['data']

        if buffer.get_length_bits() > total_data_count * 8:
            raise RuntimeError("Code length overflow: %d > %d" %
                               (buffer.get_length_bits(), total_data_count*8))

        #// end code
        if buffer.get_length_bits() + 4 <= total_data_count * 8:
            buffer.put(0, 4)

        #// padding
        while buffer.get_length_bits() % 8 != 0:
            buffer.put_bit(False)

        #// padding
        while True:
            if buffer.get_length_bits() >= total_data_count*8:
                break
            buffer.put(_PAD0, 8)
            if buffer.get_length_bits() >= total_data_count*8:
                break
            buffer.put(_PAD1, 8)

        return QRCode._create_bytes(buffer, rs_blocks)

    #pylint: disable=too-many-locals,too-many-branches
    @staticmethod
    def _create_bytes(buffer, rs_blocks):
        """Perform error calculation math on bit buffer"""
        offset = 0
        max_dc_count = 0
        max_ec_count = 0

        dcdata = [0] * len(rs_blocks)
        ecdata = [0] * len(rs_blocks)

        for r, block in enumerate(rs_blocks):

            dc_count = block['data']
            ec_count = block['total'] - dc_count

            max_dc_count = max(max_dc_count, dc_count)
            max_ec_count = max(max_ec_count, ec_count)

            dcdata[r] = [0] * dc_count

            for i in range(len(dcdata[r])):
                dcdata[r][i] = 0xff & buffer.buffer[i + offset]
            offset += dc_count

            rs_poly = QRUtil.get_error_correct_polynomial(ec_count)
            mod_poly = QRPolynomial(dcdata[r], rs_poly.get_length() - 1)

            while True:
                if mod_poly.get_length() - rs_poly.get_length() < 0:
                    break
                ratio = _glog(mod_poly.get(0)) - _glog(rs_poly.get(0))
                num = [0 for x in range(mod_poly.get_length())]
                for i in range(mod_poly.get_length()):
                    num[i] = mod_poly.get(i)
                for i in range(rs_poly.get_length()):
                    num[i] ^= _gexp(_glog(rs_poly.get(i)) + ratio)
                mod_poly = QRPolynomial(num, 0)

            ecdata[r] = [0 for x in range(rs_poly.get_length()-1)]
            for i in range(len(ecdata[r])):
                mod_index = i + mod_poly.get_length() - len(ecdata[r])
                if mod_index >= 0:
                    ecdata[r][i] = mod_poly.get(mod_index)
                else:
                    ecdata[r][i] = 0

        total_code_count = 0
        for block in rs_blocks:
            total_code_count += block['total']

        data = [None] * total_code_count
        index = 0

        for i in range(max_dc_count):
            for r in range(len(rs_blocks)):
                if i < len(dcdata[r]):
                    data[index] = dcdata[r][i]
                    index += 1

        for i in range(max_ec_count):
            for r in range(len(rs_blocks)):
                if i < len(ecdata[r]):
                    data[index] = ecdata[r][i]
                    index += 1

        return data
#pylint: enable=too-many-locals,too-many-branches

class QRUtil(object):
    """A selection of bit manipulation tools for QR generation and BCH encoding"""
    PATTERN_POSITION_TABLE = [b'', b'\x06\x12', b'\x06\x16', b'\x06\x1a',
                              b'\x06\x1e', b'\x06"', b'\x06\x16&',
                              b'\x06\x18*', b'\x06\x1a.', b'\x06\x1c2']

    G15 = 0b10100110111
    G18 = 0b1111100100101
    G15_MASK = 0b101010000010010
#pylint: disable=invalid-name
    @staticmethod
    def get_BCH_type_info(data):
        """Encode with G15 BCH mask"""
        d = data << 10
        while QRUtil.get_BCH_digit(d) - QRUtil.get_BCH_digit(QRUtil.G15) >= 0:
            d ^= QRUtil.G15 << (QRUtil.get_BCH_digit(d) - QRUtil.get_BCH_digit(QRUtil.G15))

        return ((data << 10) | d) ^ QRUtil.G15_MASK
    @staticmethod
    def get_BCH_type_number(data):
        """Encode with G18 BCH mask"""
        d = data << 12
        while QRUtil.get_BCH_digit(d) - QRUtil.get_BCH_digit(QRUtil.G18) >= 0:
            d ^= QRUtil.G18 << (QRUtil.get_BCH_digit(d) - QRUtil.get_BCH_digit(QRUtil.G18))
        return (data << 12) | d
    @staticmethod
    def get_BCH_digit(data):
        """Count digits in data"""
        digit = 0
        while data != 0:
            digit += 1
            data >>= 1
        return digit
#pylint: enable=invalid-name
    @staticmethod
    def get_pattern_position(qr_type):
        """The mask pattern position array for this QR type"""
        return QRUtil.PATTERN_POSITION_TABLE[qr_type - 1]
    @staticmethod
    def get_mask(mask, i, j):
        """Perform matching calculation on two vals for given pattern mask"""
        #pylint: disable=multiple-statements, too-many-return-statements
        if mask == 0: return (i + j) % 2 == 0
        if mask == 1: return i % 2 == 0
        if mask == 2: return j % 3 == 0
        if mask == 3: return (i + j) % 3 == 0
        if mask == 4: return (math.floor(i / 2) + math.floor(j / 3)) % 2 == 0
        if mask == 5: return (i * j) % 2 + (i * j) % 3 == 0
        if mask == 6: return ((i * j) % 2 + (i * j) % 3) % 2 == 0
        if mask == 7: return ((i * j) % 3 + (i + j) % 2) % 2 == 0
        raise ValueError("Bad mask pattern:" + mask)
        #pylint: enable=multiple-statements, too-many-return-statements
    @staticmethod
    def get_error_correct_polynomial(ecc_length):
        """ Generate a ecc polynomial"""
        poly = QRPolynomial([1], 0)
        for i in range(ecc_length):
            poly = poly.multiply(QRPolynomial([1, _gexp(i)], 0))
        return poly

class QRPolynomial:
    """Structure for creating and manipulating error code polynomials"""
    def __init__(self, num, shift):
        """Create a QR polynomial"""
        if not num:
            raise Exception(num.length + "/" + shift)
        offset = 0
        while offset < len(num) and num[offset] == 0:
            offset += 1
        self.num = [0 for x in range(len(num)-offset+shift)]
        for i in range(len(num) - offset):
            self.num[i] = num[i + offset]

    def get(self, index):
        """The exponent at the index location"""
        return self.num[index]
    def get_length(self):
        """Length of the poly"""
        return len(self.num)
    def multiply(self, e): #pylint: disable=invalid-name
        """Multiply two polynomials, returns a new one"""
        num = [0 for x in range(self.get_length() + e.get_length() - 1)]

        for i in range(self.get_length()):
            for j in range(e.get_length()):
                num[i + j] ^= _gexp(_glog(self.get(i)) + _glog(e.get(j)))

        return QRPolynomial(num, 0)

_QRRS_BLOCK_TABLE = (b'\x01\x1a\x10', b'\x01\x1a\x13', b'\x01\x1a\t', b'\x01\x1a\r', b'\x01,\x1c', b'\x01,"', b'\x01,\x10', b'\x01,\x16', b'\x01F,', b'\x01F7', b'\x02#\r', b'\x02#\x11', b'\x022 ', b'\x01dP', b'\x04\x19\t', b'\x022\x18', b'\x02C+', b'\x01\x86l', b'\x02!\x0b\x02"\x0c', b'\x02!\x0f\x02"\x10', b'\x04+\x1b', b'\x02VD', b'\x04+\x0f', b'\x04+\x13', b'\x041\x1f', b'\x02bN', b"\x04'\r\x01(\x0e", b'\x02 \x0e\x04!\x0f', b"\x02<&\x02='", b'\x02ya', b'\x04(\x0e\x02)\x0f', b'\x04(\x12\x02)\x13', b'\x03:$\x02;%', b'\x02\x92t', b'\x04$\x0c\x04%\r', b'\x04$\x10\x04%\x11') #pylint: disable=line-too-long

def _get_rs_blocks(qr_type, ecc):
    rs_block = _QRRS_BLOCK_TABLE[(qr_type - 1) * 4 + ecc]

    length = len(rs_block) // 3
    blocks = []
    for i in range(length):
        count = rs_block[i * 3 + 0]
        total = rs_block[i * 3 + 1]
        data = rs_block[i * 3 + 2]
        block = {'total' : total, 'data' : data}
        for _ in range(count):
            blocks.append(block)
    return blocks

class QRBitMatrix:
    """A bit-packed storage class for matrices"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        if width > 60:
            raise ValueError("Max 60 bits wide:", width)
        self.buffer = [0] * self.height * 2
        self.used = [0] * self.height * 2

    def __repr__(self):
        b = ""
        for y in range(self.height):
            for x in range(self.width):
                if self[x, y]:
                    b += 'X'
                else:
                    b += '.'
            b += '\n'
        return b

    def __getitem__(self, key):
        x, y = key
        if y > self.width:
            raise ValueError()
        i = 2*x + (y // 30)
        j = y % 30
        if not self.used[i] & (1 << j):
            return None
        return self.buffer[i] & (1 << j)

    def __setitem__(self, key, value):
        x, y = key
        if y > self.width:
            raise ValueError()
        i = 2*x + (y // 30)
        j = y % 30
        if value:
            self.buffer[i] |= 1 << j
        else:
            self.buffer[i] &= ~(1 << j)
        self.used[i] |= 1 << j # buffer item was set

class QRBitBuffer:
    """Storage class for a length of individual bits"""
    def __init__(self):
        self.buffer = []
        self.length = 0

    def __repr__(self):
        return ".".join([str(n) for n in self.buffer])

    def get(self, index):
        """The bit value at a location"""
        i = index // 8
        return self.buffer[i] & (1 << (7 - index % 8))

    def put(self, num, length):
        """Add a number of bits from a single integer value"""
        for i in range(length):
            self.put_bit(num & (1 << (length - i - 1)))

    def get_length_bits(self):
        """Size of bit buffer"""
        return self.length

    def put_bit(self, bit):
        """Insert one bit at the end of the bit buffer"""
        i = self.length // 8
        if len(self.buffer) <= i:
            self.buffer.append(0)
        if bit:
            self.buffer[i] |= (0x80 >> (self.length % 8))
        self.length += 1
