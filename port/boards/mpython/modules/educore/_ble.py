from mpython_ble.hidcode import Mouse as _Mouse
from mpython_ble.hidcode import KeyboardCode as _KeyboardCode
from micropython import const
import time

class keycode():
    # SPACE = 0
    CLICK = 1
    DCLICK = 2
    A = _KeyboardCode.A
    B = _KeyboardCode.B
    C = _KeyboardCode.C
    D = _KeyboardCode.D
    E = _KeyboardCode.E
    F = _KeyboardCode.F
    G = _KeyboardCode.G
    H = _KeyboardCode.H
    I = _KeyboardCode.I
    J = _KeyboardCode.J
    K = _KeyboardCode.K
    L = _KeyboardCode.L
    M = _KeyboardCode.M
    N = _KeyboardCode.N
    O = _KeyboardCode.O
    P = _KeyboardCode.P
    Q = _KeyboardCode.Q
    R = _KeyboardCode.R
    S = _KeyboardCode.S
    T = _KeyboardCode.T
    U = _KeyboardCode.U
    V = _KeyboardCode.V
    W = _KeyboardCode.W
    X = _KeyboardCode.X
    Y = _KeyboardCode.Y
    Z = _KeyboardCode.Z

    a = const(0x04)
    """``a`` and ``A``"""
    b = const(0x05)
    """``b`` and ``B``"""
    c = const(0x06)
    """``c`` and ``C``"""
    d = const(0x07)
    """``d`` and ``D``"""
    e = const(0x08)
    """``e`` and ``E``"""
    f = const(0x09)
    """``f`` and ``F``"""
    g = const(0x0A)
    """``g`` and ``G``"""
    h = const(0x0B)
    """``h`` and ``H``"""
    i = const(0x0C)
    """``i`` and ``I``"""
    j = const(0x0D)
    """``j`` and ``J``"""
    k = const(0x0E)
    """``k`` and ``K``"""
    l = const(0x0F)
    """``l`` and ``L``"""
    m = const(0x10)
    """``m`` and ``M``"""
    n = const(0x11)
    """``n`` and ``N``"""
    o = const(0x12)
    """``o`` and ``O``"""
    p = const(0x13)
    """``p`` and ``P``"""
    q = const(0x14)
    """``q`` and ``Q``"""
    r = const(0x15)
    """``r`` and ``R``"""
    s = const(0x16)
    """``s`` and ``S``"""
    t = const(0x17)
    """``t`` and ``T``"""
    u = const(0x18)
    """``u`` and ``U``"""
    v = const(0x19)
    """``v`` and ``V``"""
    w = const(0x1A)
    """``w`` and ``W``"""
    x = const(0x1B)
    """``x`` and ``X``"""
    y = const(0x1C)
    """``y`` and ``Y``"""
    z = const(0x1D)
    """``z`` and ``Z``"""

    _1 = const(0x1E)
    """``1`` and ``!``"""
    _2 = const(0x1F)
    """``2`` and ``@``"""
    _3 = const(0x20)
    """``3`` and ``#``"""
    _4 = const(0x21)
    """``4`` and ``$``"""
    _5 = const(0x22)
    """``5`` and ``%``"""
    _6 = const(0x23)
    """``6`` and ``^``"""
    _7 = const(0x24)
    """``7`` and ``&``"""
    _8 = const(0x25)
    """``8`` and ``*``"""
    _9 = const(0x26)
    """``9`` and ``(``"""
    _0 = const(0x27)
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
    RIGHT = RIGHT_ARROW
    """Move the cursor right"""
    LEFT_ARROW = const(0x50)
    LEFT = LEFT_ARROW
    """Move the cursor left"""
    DOWN_ARROW = const(0x51)
    DOWN = DOWN_ARROW
    """Move the cursor down"""
    UP_ARROW = const(0x52)
    UP = UP_ARROW
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
    CTRL = CONTROL
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

class Mouse():
    SPACE = 0

class hid():
    def __init__(self, name='mpython_hid'):
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
        if(isinstance(key,list)):
            if(len(key)==2):
                self._ble_hid.keyboard_send(key[0],key[1])
            else:
                print('组合键有误')
        else:
            self._ble_hid.keyboard_send(key)

    def mouse_key(self,key):
        if(key==1):
            self._ble_hid.mouse_click(_Mouse.LEFT)
        elif(key==2):
            self._ble_hid.mouse_click(_Mouse.LEFT)
            time.sleep(0.05)
            self._ble_hid.mouse_click(_Mouse.LEFT)