

:class:`machine.display/Image` --- 5x5点阵高级显示
=================================================


掌控实验箱上的rgb灯除了可使用 `neopixel` 库驱动，现在 ``machine`` 模块中新增模块 `display` 对象 和 `Image` 类 ，用于显示图片和文字。模块移植于 ``microbit`` 相应库，保持跟 `microbit` 库兼容，同时新增色彩控制相关特性。


---------------------------------------------------------------


display
--------------

该模块控制掌控板实验箱上的的5×5 LED点阵。它可用于显示图像，及文本。


.. method:: machine.display.get_pixel(x, y)

获取LED点阵 `x` 列 `y` 行像素点颜色值


.. method:: machine.display.set_pixel(x, y, value)

设置LED点阵 `x` 列 `y` 行像素点。当 `value` 为整形时,为1表示点亮,0则熄灭。当为元组类型时,格式(r,g,b)将以指定颜色点亮。


.. method:: machine.display.clear()

关闭所有LED点阵的像素点。

.. method:: machine.display.show(image)

显示 ``image`` 图像 。可用于显示内置图像或自定义图像。


.. method:: machine.display.show(value, delay=400, \*, wait=True, loop=False, clear=False)

如果value为字符串，浮点数或整数，则按顺序显示字母/数字。否则，如果value是可重复的图像序列，请依次显示这些图像。每个字母，数字或图像delay之间以毫秒为单位显示。可指定亮度和颜色，默认颜色红色。

    - ``value`` - 整形、字符串、`image` 图像
    - ``wait`` - 为True，则此功能将阻塞直到滚动结束，否则将后台一直滚动。
    - ``loop`` - 为True，则滚动将永远重复。
    - ``clear`` - 为True，则在完成后将清除显示

*请注意wait，loop和clear参数必须使用其关键字指定*


.. method:: machine.display.scroll(value, delay=150, \*, wait=True, loop=False, monospace=False)

在显示屏上水平滚动。如果value为整数或浮点数，则首先使用将其转换为字符串str()。该delay参数控制文本滚动的速度。

    - ``value`` - 整形、字符串、`image` 图像
    - ``wait`` - 为True，则此功能将阻塞直到滚动结束，否则将后台一直滚动。
    - ``loop`` - 为True，则滚动将永远重复。
    - ``clear`` - 为True，则在完成后将清除显示
    - ``monospace`` - 为True，则字符将全部占用5个像素列的宽度，否则在滚动时每个字符之间将恰好有1个空白像素列。


Image
--------------

.. class::
    machine.Image(string)
    machine.Image(width=None, height=None, buffer=None, value=None,color=(255,0,0))
    
    如果 `string` 使用，则它必须由排列成行的数字0,1组成，以描述图像，例如::

        image = Image("10001:"
                      "01010:"
                      "00100:"
                      "01010:"
                      "10001")

    将创建X的5×5图像。行的结尾用冒号表示。也可以使用换行符（n）指示行的结束，如下所示::

        image = Image("10001\n"
                      "01010\n"
                      "00100\n"
                      "01010\n"
                      "10001")

    另一种形式创建指定宽高的空图像。（可选）buffer为整数数组 以初始化图像::
   
        Image(2, 2, b'\x01\x01\x01\x01')


    指定颜色,以初始化图像::

        Image("01010:01010:01010:11111:01110",(0,50,0))

    .. method:: width()

    返回图像的宽度


    .. method:: height()

    返回图像的高度


    .. method:: set_pixel(x, y, value, color)

    设置 ``x`` 列  ``y`` 行 像素点。当 ``value`` 为1表示点亮, 0则熄灭。``color`` 参数可设置指定颜色。


    .. method:: get_pixel(x, y)

    返回设置 ``x`` 列  ``y`` 行 像素点颜色。返回为RGB颜色元组。


    .. method:: shift_left(n)

    返回通过将图片向左移动 `n` 列创建的新图像。


    .. method:: shift_right(n)

    与相同 ``image.shift_left(-n)``.

    .. method:: shift_up(n)

    返回通过将图片向上移动 `n` 行创建的新图像。


    .. method:: shift_down(n)

    与相同 ``image.shift_up(-n)``.

    .. method:: crop(x, y, w, h)

    通过将图片裁剪为宽度w和高度为来返回新图像h，从列x和行的像素开始y。

    .. method:: copy()

    返回图像的副本

    .. method:: fill(color)

    所有像素点填充指定颜色。


属性
------------

 ``Image`` 类 内置以下多种图像,与microbit一样。

    * ``Image.HEART``
    * ``Image.HEART_SMALL``
    * ``Image.HAPPY``
    * ``Image.SMILE``
    * ``Image.SAD``
    * ``Image.CONFUSED``
    * ``Image.ANGRY``
    * ``Image.ASLEEP``
    * ``Image.SURPRISED``
    * ``Image.SILLY``
    * ``Image.FABULOUS``
    * ``Image.MEH``
    * ``Image.YES``
    * ``Image.NO``
    * ``Image.CLOCK12``, ``Image.CLOCK11``, ``Image.CLOCK10``, ``Image.CLOCK9``,
      ``Image.CLOCK8``, ``Image.CLOCK7``, ``Image.CLOCK6``, ``Image.CLOCK5``,
      ``Image.CLOCK4``, ``Image.CLOCK3``, ``Image.CLOCK2``, ``Image.CLOCK1``
    * ``Image.ARROW_N``, ``Image.ARROW_NE``, ``Image.ARROW_E``,
      ``Image.ARROW_SE``, ``Image.ARROW_S``, ``Image.ARROW_SW``,
      ``Image.ARROW_W``, ``Image.ARROW_NW``
    * ``Image.TRIANGLE``
    * ``Image.TRIANGLE_LEFT``
    * ``Image.CHESSBOARD``
    * ``Image.DIAMOND``
    * ``Image.DIAMOND_SMALL``
    * ``Image.SQUARE``
    * ``Image.SQUARE_SMALL``
    * ``Image.RABBIT``
    * ``Image.COW``
    * ``Image.MUSIC_CROTCHET``
    * ``Image.MUSIC_QUAVER``
    * ``Image.MUSIC_QUAVERS``
    * ``Image.PITCHFORK``
    * ``Image.XMAS``
    * ``Image.PACMAN``
    * ``Image.TARGET``
    * ``Image.TSHIRT``
    * ``Image.ROLLERSKATE``
    * ``Image.DUCK``
    * ``Image.HOUSE``
    * ``Image.TORTOISE``
    * ``Image.BUTTERFLY``
    * ``Image.STICKFIGURE``
    * ``Image.GHOST``
    * ``Image.SWORD``
    * ``Image.GIRAFFE``
    * ``Image.SKULL``
    * ``Image.UMBRELLA``
    * ``Image.SNAKE``
    * ``Image.ALL_CLOCKS``
    * ``Image.ALL_ARROWS``

