
.. module:: bluetooth
   :synopsis: 提供无线蓝牙功能

:mod:`bluetooth` --- 提供无线蓝牙功能
==================================================

该模块提供ble蓝牙通讯、HID模拟设备功能。


ble类
-------

ble类, 支持客户端与主机端的BLE通讯及HID功能。HID功能,遵循BLE HID规范,可实现模拟无线蓝牙HID设备(如鼠标，键盘，游戏手柄等人机交互设备)。

.. class:: ble

BLE 通讯
~~~~~~~~~~~~

.. py:method:: ble.init(name="mpython")

    BLE客户端设备初始化。当不带参数时,默认客户端设备名为 `mpython` 。

        - ``name`` - 客户端设备名称,字符串类型。

.. py:method:: ble.bluetooth_start_advertising()

    BLE客户端设备开启广播。开启后,可被BLE主机设置搜索。

.. py:method:: ble.board_send(buf)

    BLE客户端向BLE主机端发送字节缓存


.. py:method:: ble.board_register_output_callback(f)

    接收BLE主机端的数据的回调函数, `f` 为回调函数,函数定义如下, ``f(bytearray)`` 。


.. py:method:: ble.bluetooth_stop_advertising()

    BLE客户端设备关闭广播

.. py:method:: ble.hidd_send_consumer(ble.HID_CONSUMER_xxx, True)

    模拟HID消费类设备的控制器。如,蓝牙遥控器。

    - ``第一参数`` - HID Consumer类的常用的按键ID。如你想控制电视机开机,则用 `ble.HID_CONSUMER_POWER`  。具体的按键常量详见 :ref:`HID Consumer ID表<HID Consumer Usage IDs>` 。 
    - ``第二参数``- 按键状态, `True` 为按下, `False` 为松开。



    电视遥控音量加减的示例::

        # 导入蓝牙ble类
        from bluetooth import ble       
        import time

        # ble初始化
        ble.init()  
        # 等待主机设备连接
        time.sleep(2)
        # 按下音量+
        ble.hidd_send_consumer(ble.HID_CONSUMER_VOLUME_UP,True)
        # 按下保持状态
        time.sleep(1)
        # 释放按键
        ble.hidd_send_consumer(ble.HID_CONSUMER_VOLUME_UP,False)

        # 按下音量-
        ble.hidd_send_consumer(ble.HID_CONSUMER_VOLUME_DOWN,True)
        # 按下保持状态
        time.sleep(1)
        # 释放按键
        ble.hidd_send_consumer(ble.HID_CONSUMER_VOLUME_DOWN,False)



.. py:method:: ble.hidd_send_keyboard(keys = [key1...], modifier = KEY_MASK_NONE)

    模拟HID键盘设备。

    - ``keys`` - 一个或多个按键的数组类型。当数组内成员表示为按下的按键,如要释放按键只需将数组内对应位置的值赋值为0。具体的按键常量详见 :ref:`HID Keyboard ID表<HID Keyboard Usage IDs>` 。 
    -  ``modifier`` - 键盘组合按键,默认为 `KEY_MASK_NONE` 表示为单按键 ,可以为以下值。如要用到2个组合按键,可使用 ``|`` 或逻辑运算,像 `Ctrl` + `Alt` 组合按键时为 `KEY_MASK_L_CTRL | KEY_MASK_L_ALT`

        - `KEY_MASK_NONE` - 0
        - `KEY_MASK_L_CTRL` - 1
        - `KEY_MASK_L_SHIFTL` - 2
        - `KEY_MASK_L_ALT` - 4
        - `KEY_MASK_L_GUI` - 8
        - `KEY_MASK_R_CTRL` - 16
        - `KEY_MASK_R_SHIFT` - 32
        - `KEY_MASK_R_ALT` - 64
        - `KEY_MASK_R_GUI` - 128

    键盘示例::

        # Ctrl + F组合按键
        ble.hidd_send_keyboard([ble.HID_KEY_F],ble.KEY_MASK_L_CTRL)
        # 释放按键
        ble.hidd_send_keyboard([0])

        # Ctrl + Alt + Del 组合按键
        ble.hidd_send_keyboard([ble.HID_KEYPAD_DOT],ble.KEY_MASK_L_CTRL | ble.KEY_MASK_L_ALT )
         # 释放按键
        ble.hidd_send_keyboard([0])

        # 单按键 A
        ble.hidd_send_keyboard([ble.HID_KEY_A])
        # 释放按键
        ble.hidd_send_keyboard([0])

.. py:method:: ble.hidd_send_mouse(button = 0 , x = 0,y = 0)

    模拟HID鼠标设备。

        - ``button`` - 鼠标按键, 可以为以下值:

            - ``0`` - 释放按键
            - ``ble.HID_MOUSE_LEFT`` - 鼠标左键
            - ``ble.HID_MOUSE_MIDDLE`` - 鼠标中键
            - ``ble.HID_MOUSE_RIGHT`` - 鼠标右键

        - ``x`` - 鼠标坐标x轴的相对位移,范围-1023 ~ 1023
        - ``y`` - 鼠标坐标y轴的相对位移,范围-1023 ~ 1023


    鼠标示例::

        # 按下鼠标左键
        ble.hidd_send_mouse(ble.HID_MOUSE_LEFT)
        # 释放鼠标按键
        ble.hidd_send_mouse(0)
        # 坐标x轴位移
        ble.hidd_send_mouse(x = 50 )
常量
-----

HID Consumer
~~~~~~~~~~~~~~

.. _HID Consumer Usage IDs:

======================================== ====== ====================================
HID Consumer Usage IDs                    数值    定义
======================================== ====== ====================================  
``ble.HID_CONSUMER_POWER``                48     Power
``ble.HID_CONSUMER_RESET``                49     Reset
``ble.HID_CONSUMER_SLEEP``                50     Sleep
``ble.HID_CONSUMER_MENU``                 64     Menu
``ble.HID_CONSUMER_SELECTION``            128    Selection
``ble.HID_CONSUMER_ASSIGN_SEL``           129    Assign Selection
``ble.HID_CONSUMER_MODE_STEP``            130    Mode Step
``ble.HID_CONSUMER_RECALL_LAST``          131    Recall Last
``ble.HID_CONSUMER_QUIT``                 148    Quit
``ble.HID_CONSUMER_HELP``                 149    Help
``ble.HID_CONSUMER_CHANNEL_UP``           156    Channel Increment
``ble.HID_CONSUMER_CHANNEL_DOWN``         157    Channel Decrement
``ble.HID_CONSUMER_PLAY``                 176    Play
``ble.HID_CONSUMER_PAUSE``                177    Pause
``ble.HID_CONSUMER_RECORD``               178    Record
``ble.HID_CONSUMER_FAST_FORWARD``         179    Fast Forward
``ble.HID_CONSUMER_REWIND``               180    Rewind
``ble.HID_CONSUMER_SCAN_NEXT_TRK``        181    Scan Next Track
``ble.HID_CONSUMER_SCAN_PREV_TRK``        182    Scan Previous Track
``ble.HID_CONSUMER_STOP``                 183    Stop
``ble.HID_CONSUMER_EJECT``                184    Eject
``ble.HID_CONSUMER_RANDOM_PLAY``          185    Random Play
``ble.HID_CONSUMER_SELECT_DISC``          186    Select Disk
``ble.HID_CONSUMER_ENTER_DISC``           187    Enter Disc
``ble.HID_CONSUMER_REPEAT``               188    Repeat
``ble.HID_CONSUMER_STOP_EJECT``           204    Stop/Eject
``ble.HID_CONSUMER_PLAY_PAUSE``           205    Play/Pause
``ble.HID_CONSUMER_PLAY_SKIP``            206    Play/Skip
``ble.HID_CONSUMER_VOLUME``               224    Volume
``ble.HID_CONSUMER_BALANCE``              225    Balance
``ble.HID_CONSUMER_MUTE``                 226    Mute
``ble.HID_CONSUMER_BASS``                 227    Bass
``ble.HID_CONSUMER_VOLUME_UP``            233    Volume Increment
``ble.HID_CONSUMER_VOLUME_DOWN``          234    Volume Decrement
======================================== ====== ==================================== 


HID Keyboard
~~~~~~~~~~~~~~~

.. _HID Keyboard Usage IDs:

======================================== ====== ====================================
HID Keyboard Usage IDs                    数值    定义
======================================== ====== ====================================  
``ble.HID_KEY_A``                         4      Keyboard A and a
``ble.HID_KEY_B``                         5      Keyboard B and b
``ble.HID_KEY_C``                         6      Keyboard C and c
``ble.HID_KEY_D``                         7      Keyboard D and d
``ble.HID_KEY_E``                         8      Keyboard E and e
``ble.HID_KEY_F``                         9      Keyboard F and f
``ble.HID_KEY_G``                         10     Keyboard G and g
``ble.HID_KEY_H``                         11     Keyboard H and h
``ble.HID_KEY_I``                         12     Keyboard I and i
``ble.HID_KEY_J``                         13     Keyboard J and j
``ble.HID_KEY_K``                         14     Keyboard K and k
``ble.HID_KEY_L``                         15     Keyboard L and l
``ble.HID_KEY_M``                         16     Keyboard M and m
``ble.HID_KEY_N``                         17     Keyboard N and n
``ble.HID_KEY_O``                         18     Keyboard O and o
``ble.HID_KEY_P``                         19     Keyboard P and p
``ble.HID_KEY_Q``                         20     Keyboard Q and q
``ble.HID_KEY_R``                         21     Keyboard R and r
``ble.HID_KEY_S``                         22     Keyboard S and s
``ble.HID_KEY_T``                         23     Keyboard T and t
``ble.HID_KEY_U``                         24     Keyboard U and u
``ble.HID_KEY_V``                         25     Keyboard V and v
``ble.HID_KEY_W``                         26     Keyboard W and w
``ble.HID_KEY_X``                         27     Keyboard X and x
``ble.HID_KEY_Y``                         28     Keyboard Y and y
``ble.HID_KEY_Z``                         29     Keyboard Z and z
``ble.HID_KEY_1``                         30     Keyboard 1
``ble.HID_KEY_2``                         31     Keyboard 2
``ble.HID_KEY_3``                         32     Keyboard 3
``ble.HID_KEY_4``                         33     Keyboard 4
``ble.HID_KEY_5``                         34     Keyboard 5
``ble.HID_KEY_6``                         35     Keyboard 6
``ble.HID_KEY_7``                         36     Keyboard 7
``ble.HID_KEY_8``                         37     Keyboard 8
``ble.HID_KEY_9``                         38     Keyboard 9
``ble.HID_KEY_0``                         39     Keyboard 0
``ble.HID_KEY_RETURN``                    40     Keyboard Return (ENTER)
``ble.HID_KEY_ESCAPE``                    41     Keyboard ESCAPE
``ble.HID_KEY_DELETE``                    42     Keyboard DELETE (Backspace)
``ble.HID_KEY_TAB``                       43     Keyboard Tab
``ble.HID_KEY_SPACEBAR``                  44     Keyboard Spacebar
``ble.HID_KEY_MINUS``                     45     Keyboard - and (underscore)
``ble.HID_KEY_EQUAL``                     46     Keyboard = and +
``ble.HID_KEY_LEFT_BRKT``                 47     Keyboard [ and {
``ble.HID_KEY_RIGHT_BRKT``                48     Keyboard ] and }
``ble.HID_KEY_BACK_SLASH``                49     Keyboard \ and |
``ble.HID_KEY_SEMI_COLON``                51     Keyboard ; and :
``ble.HID_KEY_SGL_QUOTE``                 52     Keyboard ' and "
``ble.HID_KEY_GRV_ACCENT``                53     Keyboard Grave Accent and Tilde
``ble.HID_KEY_COMMA``                     54     Keyboard , and <
``ble.HID_KEY_DOT``                       55     Keyboard . and >
``ble.HID_KEY_FWD_SLASH``                 56     Keyboard / and ?
``ble.HID_KEY_CAPS_LOCK``                 57     Keyboard Caps Lock
``ble.HID_KEY_F1``                        58     Keyboard F1
``ble.HID_KEY_F2``                        59     Keyboard F2
``ble.HID_KEY_F3``                        60     Keyboard F3
``ble.HID_KEY_F4``                        61     Keyboard F4
``ble.HID_KEY_F5``                        62     Keyboard F5
``ble.HID_KEY_F6``                        63     Keyboard F6
``ble.HID_KEY_F7``                        64     Keyboard F7
``ble.HID_KEY_F8``                        65     Keyboard F8
``ble.HID_KEY_F9``                        66     Keyboard F9
``ble.HID_KEY_F10``                       67     Keyboard F10
``ble.HID_KEY_F11``                       68     Keyboard F11
``ble.HID_KEY_F12``                       69     Keyboard F12
``ble.HID_KEY_PRNT_SCREEN``               70     Keyboard Print Screen
``ble.HID_KEY_SCROLL_LOCK``               71     Keyboard Scroll Lock
``ble.HID_KEY_PAUSE``                     72     Keyboard Pause
``ble.HID_KEY_INSERT``                    73     Keyboard Insert
``ble.HID_KEY_HOME``                      74     Keyboard Home
``ble.HID_KEY_PAGE_UP``                   75     Keyboard PageUp
``ble.HID_KEY_DELETE_FWD``                76     Keyboard Delete Forward
``ble.HID_KEY_END``                       77     Keyboard End
``ble.HID_KEY_PAGE_DOWN``                 78     Keyboard PageDown
``ble.HID_KEY_RIGHT_ARROW``               79     Keyboard RightArrow
``ble.HID_KEY_LEFT_ARROW``                80     Keyboard LeftArrow
``ble.HID_KEY_DOWN_ARROW``                81     Keyboard DownArrow
``ble.HID_KEY_UP_ARROW``                  82     Keyboard UpArrow
``ble.HID_KEY_NUM_LOCK``                  83     Keypad Num Lock and Clear
``ble.HID_KEY_DIVIDE``                    84     Keypad /
``ble.HID_KEY_MULTIPLY``                  85     Keypad *
``ble.HID_KEY_SUBTRACT``                  86     Keypad -
``ble.HID_KEY_ADD``                       87     Keypad +-
``ble.HID_KEY_ENTER``                     88     Keypad ENTER
``ble.HID_KEYPAD_1``                      89     Keypad 1 and End
``ble.HID_KEYPAD_2``                      90     Keypad 2 and Down Arrow
``ble.HID_KEYPAD_3``                      91     Keypad 3 and PageDn
``ble.HID_KEYPAD_4``                      92     Keypad 4 and Lfet Arrow
``ble.HID_KEYPAD_5``                      93     Keypad 5
``ble.HID_KEYPAD_6``                      94     Keypad 6 and Right Arrow
``ble.HID_KEYPAD_7``                      95     Keypad 7 and Home
``ble.HID_KEYPAD_8``                      96     Keypad 8 and Up Arrow
``ble.HID_KEYPAD_9``                      97     Keypad 9 and PageUp
``ble.HID_KEYPAD_0``                      98     Keypad 0 and Insert
``ble.HID_KEYPAD_DOT``                    99     Keypad . and Delete
``ble.HID_KEY_MUTE``                      127    Keyboard Mute
``ble.HID_KEY_VOLUME_UP``                 128    Keyboard Volume up
``ble.HID_KEY_VOLUME_DOWN``               129    Keyboard Volume down
======================================== ====== ====================================                                                                                                                                                                                                                            


HID Mouse
~~~~~~~~~~~~~~~

.. _HID Mouse Usage IDs:

======================================== ====== ====================================
HID Mouse Usage IDs                       数值    定义
======================================== ====== ====================================  
``ble.HID_MOUSE_LEFT``                    253     Mouse Left
``ble.HID_MOUSE_MIDDLE``                  254     Mouse Middle
``ble.HID_MOUSE_RIGHT``                   255     Mouse Right
======================================== ====== ==================================== 



.. literalinclude:: /../examples/bluetooth/hid_ppt_Remote_Control.py
    :caption: PPT 翻页遥控器
    :linenos: