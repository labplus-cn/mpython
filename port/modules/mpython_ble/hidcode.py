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


class Mouse(object):
    """
    HID mouse button code
    """
    LEFT = const(1)
    RIGHT = const(2)
    MIDDLE = const(4)



class KeyboardCode:
    """USB HID Keycode constants.

    This list is modeled after the names for USB keycodes defined in
    https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf#page=53.
    This list does not include every single code, but does include all the keys on
    a regular PC or Mac keyboard.

    Remember that keycodes are the names for key *positions* on a US keyboard, and may
    not correspond to the character that you mean to send if you want to emulate non-US keyboard.
    For instance, on a French keyboard (AZERTY instead of QWERTY),
    the keycode for 'q' is used to indicate an 'a'. Likewise, 'y' represents 'z' on
    a German keyboard. This is historical: the idea was that the keycaps could be changed
    without changing the keycodes sent, so that different firmware was not needed for
    different variations of a keyboard.
    """
    A = const(0x04)
    """``a`` and ``A``"""
    B = const(0x05)
    """``b`` and ``B``"""
    C = const(0x06)
    """``c`` and ``C``"""
    D = const(0x07)
    """``d`` and ``D``"""
    E = const(0x08)
    """``e`` and ``E``"""
    F = const(0x09)
    """``f`` and ``F``"""
    G = const(0x0A)
    """``g`` and ``G``"""
    H = const(0x0B)
    """``h`` and ``H``"""
    I = const(0x0C)
    """``i`` and ``I``"""
    J = const(0x0D)
    """``j`` and ``J``"""
    K = const(0x0E)
    """``k`` and ``K``"""
    L = const(0x0F)
    """``l`` and ``L``"""
    M = const(0x10)
    """``m`` and ``M``"""
    N = const(0x11)
    """``n`` and ``N``"""
    O = const(0x12)
    """``o`` and ``O``"""
    P = const(0x13)
    """``p`` and ``P``"""
    Q = const(0x14)
    """``q`` and ``Q``"""
    R = const(0x15)
    """``r`` and ``R``"""
    S = const(0x16)
    """``s`` and ``S``"""
    T = const(0x17)
    """``t`` and ``T``"""
    U = const(0x18)
    """``u`` and ``U``"""
    V = const(0x19)
    """``v`` and ``V``"""
    W = const(0x1A)
    """``w`` and ``W``"""
    X = const(0x1B)
    """``x`` and ``X``"""
    Y = const(0x1C)
    """``y`` and ``Y``"""
    Z = const(0x1D)
    """``z`` and ``Z``"""

    ONE = const(0x1E)
    """``1`` and ``!``"""
    TWO = const(0x1F)
    """``2`` and ``@``"""
    THREE = const(0x20)
    """``3`` and ``#``"""
    FOUR = const(0x21)
    """``4`` and ``$``"""
    FIVE = const(0x22)
    """``5`` and ``%``"""
    SIX = const(0x23)
    """``6`` and ``^``"""
    SEVEN = const(0x24)
    """``7`` and ``&``"""
    EIGHT = const(0x25)
    """``8`` and ``*``"""
    NINE = const(0x26)
    """``9`` and ``(``"""
    ZERO = const(0x27)
    """``0`` and ``)``"""
    ENTER = const(0x28)
    """Enter (Return)"""
    ESCAPE = const(0x29)
    """Escape"""
    BACKSPACE = const(0x2A)
    """Delete backward (Backspace)"""
    TAB = const(0x2B)
    """Tab and Backtab"""
    SPACEBAR = const(0x2C)
    """Spacebar"""
    SPACE = SPACEBAR
    """Alias for SPACEBAR"""
    MINUS = const(0x2D)
    """``-` and ``_``"""
    EQUALS = const(0x2E)
    """``=` and ``+``"""
    LEFT_BRACKET = const(0x2F)
    """``[`` and ``{``"""
    RIGHT_BRACKET = const(0x30)
    """``]`` and ``}``"""
    BACKSLASH = const(0x31)
    """``\`` and ``|``"""
    POUND = const(0x32)
    """``#`` and ``~`` (Non-US keyboard)"""
    SEMICOLON = const(0x33)
    """``;`` and ``:``"""
    QUOTE = const(0x34)
    """``'`` and ``"``"""
    GRAVE_ACCENT = const(0x35)
    """:literal:`\`` and ``~``"""
    COMMA = const(0x36)
    """``,`` and ``<``"""
    PERIOD = const(0x37)
    """``.`` and ``>``"""
    FORWARD_SLASH = const(0x38)
    """``/`` and ``?``"""

    CAPS_LOCK = const(0x39)
    """Caps Lock"""

    F1 = const(0x3A)
    """Function key F1"""
    F2 = const(0x3B)
    """Function key F2"""
    F3 = const(0x3C)
    """Function key F3"""
    F4 = const(0x3D)
    """Function key F4"""
    F5 = const(0x3E)
    """Function key F5"""
    F6 = const(0x3F)
    """Function key F6"""
    F7 = const(0x40)
    """Function key F7"""
    F8 = const(0x41)
    """Function key F8"""
    F9 = const(0x42)
    """Function key F9"""
    F10 = const(0x43)
    """Function key F10"""
    F11 = const(0x44)
    """Function key F11"""
    F12 = const(0x45)
    """Function key F12"""

    PRINT_SCREEN = const(0x46)
    """Print Screen (SysRq)"""
    SCROLL_LOCK = const(0x47)
    """Scroll Lock"""
    PAUSE = const(0x48)
    """Pause (Break)"""

    INSERT = const(0x49)
    """Insert"""
    HOME = const(0x4A)
    """Home (often moves to beginning of line)"""
    PAGE_UP = const(0x4B)
    """Go back one page"""
    DELETE = const(0x4C)
    """Delete forward"""
    END = const(0x4D)
    """End (often moves to end of line)"""
    PAGE_DOWN = const(0x4E)
    """Go forward one page"""

    RIGHT_ARROW = const(0x4F)
    """Move the cursor right"""
    LEFT_ARROW = const(0x50)
    """Move the cursor left"""
    DOWN_ARROW = const(0x51)
    """Move the cursor down"""
    UP_ARROW = const(0x52)
    """Move the cursor up"""

    KEYPAD_NUMLOCK = const(0x53)
    """Num Lock (Clear on Mac)"""
    KEYPAD_FORWARD_SLASH = const(0x54)
    """Keypad ``/``"""
    KEYPAD_ASTERISK = const(0x55)
    """Keypad ``*``"""
    KEYPAD_MINUS = const(0x56)
    """Keyapd ``-``"""
    KEYPAD_PLUS = const(0x57)
    """Keypad ``+``"""
    KEYPAD_ENTER = const(0x58)
    """Keypad Enter"""
    KEYPAD_ONE = const(0x59)
    """Keypad ``1`` and End"""
    KEYPAD_TWO = const(0x5A)
    """Keypad ``2`` and Down Arrow"""
    KEYPAD_THREE = const(0x5B)
    """Keypad ``3`` and PgDn"""
    KEYPAD_FOUR = const(0x5C)
    """Keypad ``4`` and Left Arrow"""
    KEYPAD_FIVE = const(0x5D)
    """Keypad ``5``"""
    KEYPAD_SIX = const(0x5E)
    """Keypad ``6`` and Right Arrow"""
    KEYPAD_SEVEN = const(0x5F)
    """Keypad ``7`` and Home"""
    KEYPAD_EIGHT = const(0x60)
    """Keypad ``8`` and Up Arrow"""
    KEYPAD_NINE = const(0x61)
    """Keypad ``9`` and PgUp"""
    KEYPAD_ZERO = const(0x62)
    """Keypad ``0`` and Ins"""
    KEYPAD_PERIOD = const(0x63)
    """Keypad ``.`` and Del"""
    KEYPAD_BACKSLASH = const(0x64)
    """Keypad ``\\`` and ``|`` (Non-US)"""
    KEYPAD_EQUALS = const(0x67)
    """Keypad ``=`` (Mac)"""
    F13 = const(0x68)
    """Function key F13 (Mac)"""
    F14 = const(0x69)
    """Function key F14 (Mac)"""
    F15 = const(0x6A)
    """Function key F15 (Mac)"""
    F16 = const(0x6B)
    """Function key F16 (Mac)"""
    F17 = const(0x6C)
    """Function key F17 (Mac)"""
    F18 = const(0x6D)
    """Function key F18 (Mac)"""
    F19 = const(0x6E)
    """Function key F19 (Mac)"""

    LEFT_CONTROL = const(0xE0)
    """Control modifier left of the spacebar"""
    CONTROL = LEFT_CONTROL
    """Alias for LEFT_CONTROL"""
    LEFT_SHIFT = const(0xE1)
    """Shift modifier left of the spacebar"""
    SHIFT = LEFT_SHIFT
    """Alias for LEFT_SHIFT"""
    LEFT_ALT = const(0xE2)
    """Alt modifier left of the spacebar"""
    ALT = LEFT_ALT
    """Alias for LEFT_ALT; Alt is also known as Option (Mac)"""
    OPTION = ALT
    """Labeled as Option on some Mac keyboards"""
    LEFT_GUI = const(0xE3)
    """GUI modifier left of the spacebar"""
    """Labeled as Command on Mac keyboards, with a clover glyph"""
    RIGHT_CONTROL = const(0xE4)
    """Control modifier right of the spacebar"""
    RIGHT_SHIFT = const(0xE5)
    RIGHT_ALT = const(0xE6)
    RIGHT_GUI = const(0xE7)


class ConsumerCode:
    POWER = const(0x30)
    CHANNEL_UP = const(0X9C)
    CHANNEL_DOWN = const(0X9D)
    RECORD = const(0xB2)
    FAST_FORWARD = const(0xB3)
    REWIND = const(0xB4)
    SCAN_NEXT_TRACK = const(0xB5)
    SCAN_PREVIOUS_TRACK = const(0xB6)
    STOP = const(0xB7)
    EJECT = const(0xB8)
    PLAY_PAUSE = const(0xCD)
    MUTE = const(0xE2)
    VOLUME_DECREMENT = const(0xEA)
    VOLUME_INCREMENT = const(0xE9)
