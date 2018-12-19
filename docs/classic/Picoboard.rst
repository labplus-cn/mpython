Picoboard-Scratch
==========
掌控板可以模拟Scratch中的传感板PicoBoard来使用。要使用掌控板模拟PicoBoard在Scratch中编程，首先需要把建立掌控板与Scratch之间的联系的程序刷入掌控板中。

刷入程序
+++++++

:: 

    # mPython掌控板模拟Scratch PicoBoard

    #------------------------------------------------------
    # Channel | PicoBoard       |  mPython                |
    #------------------------------------------------------
    # 4       | resistance-A    | press of the "A" button |
    # 2       | resistance-B    | accelerometer's x       |
    # 1       | resistance-C    | accelerometer's y       |
    # 0       | resistance-D    | ext                     |
    # 3       | button          | press of the "B" button |
    # 5       | light           | light                   |
    # 6       | Sound           | Sound                   |
    # 7       | Slider          | TouchPad                |
    # -----------------------------------------------------

    # 操作说明：正常启动默认进入scratch模式；退回到repl模式，同时按下复位和button b后，
    #          先松开复位按键2秒后再松开button b

    from mpython import *
    from machine import UART
    from machine import Pin,ADC

    scratchMode=True
    ext = MPythonPin(3,PinMode.ANALOG)

    #48*48
    scratchlogo= bytearray([
    0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
    0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
    0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X02,0X00,0X00,
    0X00,0X80,0X00,0X06,0X00,0X00,0X00,0XE0,0X00,0X0E,0X00,0X00,0X00,0XF0,0X00,0X1B,
    0X00,0X00,0X00,0X5C,0X00,0X33,0X00,0X00,0X00,0X46,0X7F,0XFD,0X00,0X00,0X00,0X5B,
    0XC0,0X7D,0X80,0X00,0X00,0X5C,0XFF,0XFB,0X80,0X00,0X00,0X5F,0X7F,0XF7,0XC0,0X00,
    0X00,0X5E,0X4F,0XE8,0X60,0X00,0X00,0X7D,0XF3,0XF8,0X30,0X00,0X00,0X6B,0X1D,0XF8,
    0X18,0X00,0X00,0X76,0X05,0XF8,0X0C,0X00,0X00,0XD4,0X02,0XE8,0X0C,0X00,0X00,0XB4,
    0X03,0XEC,0X0E,0X00,0X01,0XB4,0X01,0X74,0X6E,0X00,0X01,0X7E,0X11,0X76,0X0A,0X00,
    0X01,0X7A,0X11,0X03,0X01,0X00,0X23,0X7B,0X01,0X7E,0X60,0X02,0X0F,0XFD,0X82,0X3F,
    0X00,0X28,0X03,0X7F,0X6C,0X1E,0X00,0X30,0X03,0X7C,0X00,0X0C,0X00,0X10,0X03,0X78,
    0X00,0X00,0X00,0X10,0X3B,0X78,0X05,0X00,0X00,0X10,0X01,0X78,0X00,0X30,0X00,0X3C,
    0X01,0XB8,0X00,0X01,0X80,0X38,0X00,0XB8,0X00,0X00,0X20,0X38,0X00,0XDC,0X04,0X00,
    0X00,0X70,0X00,0X64,0X02,0X00,0X80,0XE0,0X00,0X3A,0X01,0X01,0X01,0XE0,0X00,0X1D,
    0X00,0X38,0X07,0XC0,0X00,0X0F,0X80,0X00,0X1F,0X00,0X00,0X03,0XF0,0X00,0XFE,0X00,
    0X00,0X01,0XFF,0XFF,0XF8,0X00,0X00,0X00,0X3F,0XFF,0XC0,0X00,0X00,0X00,0X00,0XE0,
    0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
    0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,0X00,
    ])

    if button_b.value()==0:               #启动检测 button b 按下进入repl
        scratchMode=False
        #print('replMode')
        oled.DispChar('replMode',30,20)
        oled.show()

    # 触摸按键扫描
    # 6个触摸按键按下，scratch依次分别反馈10、20、30、40、50、60

    def ScanTouchpad():
        if touchPad_P.read() <200:
            return int(1023/10)
        elif touchPad_Y.read()<200:
            return int(1023/10*2)
        elif touchPad_T.read()<200:
            return int(1023/10*3)
        elif touchPad_H.read()<200:
            return int(1023/10*4)
        elif touchPad_O.read()<200:
            return int(1023/10*5)
        elif touchPad_N.read()<200:
            return int(1023/10*6)
        else:
            return 0


    while scratchMode:
        oled.Bitmap(40,10,scratchlogo,48,48,1)
        oled.show()

        uart = UART(1, 38400, rx=3, tx=1)

        # Create and send Scratch data packet
        def convert(a, b):
            sensor = bytearray(2)
            upper = (b & 0x380) >> 7
            sensor[1] = b & 0x7f
            sensor[0] = (1 << 7) | a << 3 | upper
            uart.write(sensor)

        request = bytearray(1)

        while True:

            if uart.readinto(request) == 1 and request[0] == 0x01:       #当接收到scratch发来的0x01字节
                rgb.fill((0,20,0))
                rgb.write()
                convert(15, 0x04)
                sleep_us(10)
                extValue=int(ext.read_analog()/4)                              # Get ext
                convert(0,extValue)
                reading = accelerometer.get_y()*1000                    # Get accelerometer's y
                if reading >= 0:
                    reading = int(reading / 2) + 512
                    convert(1, reading)
                else:
                    reading = 512 - abs(int(reading / 2))
                    convert(1, reading)

                reading = accelerometer.get_x()*1000                    # Get accelerometer's x
                if reading >= 0:
                    reading = int(reading / 2) + 512
                    convert(2, reading)
                else:
                    reading = 512 - abs(int(reading / 2))
                    convert(2, reading)

                if button_b.value()==0:                                 # Get button B state
                    convert(3, 0)
                else:
                    convert(3, 1023)

                if button_a.value()==0:                                 #  Get button A state
                    convert(4, 1023)
                else:
                    convert(4, 0)

                convert(5, 1023-light.read())                            #  Get light senser

                convert(6, sound.read())                                 #  Get Sound senser

                convert(7, ScanTouchpad())                               #  Get TouchPad value

            else:
                rgb.fill((0,0,0))
                rgb.write()

此程序是将掌控板与Scratch建立联系，当刷入该程序后，掌控板就与Scratch PicoBoard建立了联系，这样掌控板就能够模拟PicoBoard上的传感器来使用。
PicoBoard上的传感器与掌控板的一一对应，如下表：

==========  ====================================  
 PicoBoard  掌控板
==========  ====================================  
阻力A        按键A
阻力B        按键X
阻力C        按键Y
阻力D        ext(P3)
按键         按键B
光线         光线
声音         声音
滑杆         触摸按键
==========  ====================================  

.. admonition:: 提示

    当掌控板模拟PicoBoard在Scratch中使用时，注意掌控板的传感器的数值有所变化，如在mPython中，光线传感器的检测数值范围在0~4095之间，而在Scratch中，其数值范围为0~100。在Scratch中查看掌控板传感器参数的方法如下：在脚本栏“更多积木”下，点击相应的积木模块。以按键A为例，在按下与未按下两种条件下，点击“阻力A传感器的值”积木，未按下数值为0，按下数值为100，其他传感器查看方法同理。

掌控板与Scratch连接
+++++++

* 1、将上面的程序刷入掌控板，设为默认运行；
* 2、打开Scratch软件（这里使用2.0版本），单击脚本栏的“更多积木”中的“添加扩展”，添加“PicoBroad”硬件；
* 3、添加“PicoBroad”后，Scratch界面上会出现“PicoBoard”指令模块。当“PicoBoard”右边的黄色圆点变成绿色，同时掌控板上的三个RGB灯闪烁，此时表示掌控板与Scratch连接成功；
* 4、连接成功后，就可以在Scratch中做一些互动程序了。

.. image:: /images/classic/scratch.jpg
    :scale: 50%
    :align: center

Scratch软件编辑图形化程序
+++++++

示例下载 :download:`Scratch示例 </../docs/tools/Scratch.zip>` 。

.. image:: /images/classic/scratch.gif
    :scale: 50%
    :align: center

退出Scratch，返回repl模式
+++++++

掌握板在scratch模式时是无法读取文件和刷入程序的。如果想返回mPython2读取文件或刷入程序，必须使掌控板退出scratch模式，进入repl模式。方法如下：
* 同时按下复位键和button b后，先松开复位按键2秒后，当OLED显示屏上显示“replMode”字样时再松开button b，此时成功返回到repl模式，如图所示：

.. image:: /images/classic/replmode.jpg
    :scale: 35%
    :align: center



