:mod:`framebuf` --- 帧缓冲操作
=============================================

.. module:: framebuf
   :synopsis: 帧缓冲操作

该模块提供了一个通用的帧缓冲区，可用于创建位图图像，然后可以将其发送到显示器。

类 FrameBuffer
-----------------

FrameBuffer类提供了一个像素缓冲区，可以使用像素，线条，矩形，文本甚至其他FrameBuffer来绘制。在为显示生成输出时很有用。

例子::

    import framebuf

    # FrameBuffer needs 2 bytes for every RGB565 pixel
    buffer=bytearray(10 * 100 * 2)
    fbuf = framebuf.FrameBuffer(buffer, 10, 100, framebuf.RGB565)

    fbuf.fill(0)
    fbuf.text('MicroPython!', 0, 0, 0xffff)

构建函数
------------

.. class:: FrameBuffer(buffer, width, height, format, stride=width)

    构造一个FrameBuffer对象。参数是:

        - *buffer* 是一个具有缓冲协议的对象，该协议必须足够大，以包含由FrameBuffer的宽度，高度和格式定义的每个像素。
        - *width*  是FrameBuffer的宽度（以像素为单位）
        - *height* 是FrameBuffer的高度（以像素为单位）
        - *format* 指定FrameBuffer中使用的像素类型; 允许值列在下面的常量下。这些设置用于编码颜色值的位数以及缓冲区中这些位的布局。在将颜色值c传递给方法的情况下，c是一个小整数，其编码取决于FrameBuffer的格式。
        - *stride* 是FrameBuffer中每个水平像素线之间的像素数。默认为宽度，但在另一个较大的FrameBuffer或屏幕中实现FrameBuffer时可能需要进行调整。
        所述缓冲器的大小必须容纳增加的步长大小。

    必须指定有效的 *buffer* , *width*, *height*, *format*  和可选 *stride*.。无效的缓冲区大小或尺寸可能会导致意外错误。

绘制原始形状
------------------------

以下方法在FrameBuffer上绘制形状。

.. method:: FrameBuffer.fill(c)

    使用指定的颜色填充整个FrameBuffer。

.. method:: FrameBuffer.pixel(x, y[, c])

   如果未给出c，则获取指定像素的颜色值。如果给出c，则将指定的像素设置为给定的颜色。

.. method:: FrameBuffer.hline(x, y, w, c)
.. method:: FrameBuffer.vline(x, y, h, c)
.. method:: FrameBuffer.line(x1, y1, x2, y2, c)

    使用给定颜色和1个像素的厚度从一组坐标中绘制一条线。该 ``line`` 方法将线条绘制到第二组坐标，而 ``hline`` 和 ``vline``  方法分别绘制水平线和垂直线，直到给定长度。

.. method:: FrameBuffer.rect(x, y, w, h, c)
.. method:: FrameBuffer.fill_rect(x, y, w, h, c)

    在给定的位置，大小和颜色绘制一个矩形。该 ``rect`` 方法仅绘制1像素轮廓，而该 ``fill_rect`` 方法绘制轮廓和内部。

绘制文字
------------

.. method:: FrameBuffer.text(s, x, y[, c])

    使用坐标作为文本的左上角将文本写入 `FrameBuffer` 。文本的颜色可以通过可选参数定义，但默认值为1.所有字符的尺寸均为8x8像素，目前无法更改字体。


其他方法
-------------

.. method:: FrameBuffer.scroll(xstep, ystep)

   按给定的向量移动 `FrameBuffer` 的内容。这可能会在 `FrameBuffer` 中留下以前颜色的足迹。

.. method:: FrameBuffer.blit(fbuf, x, y[, key])

 

    在给定坐标处的当前一个上绘制另一个 `FrameBuffer` 。如果指定了*key*，那么它应该是一个颜色整数，并且相应的颜色将被视为透明：将不会绘制具有该颜色值的所有像素。

    此方法在使用不同格式的 `FrameBuffer` 实例之间起作用，但由于颜色格式不匹配，所得到的颜色可能是意外的。

常数
---------

.. data:: framebuf.MONO_VLSB

    单色（1bit）颜色格式这定义了一种映射，其中字节中的位垂直映射，位0最接近屏幕顶部。
    因此，每个字节占据8个垂直像素。后续字节出现在连续的水平位置，直到到达最右边。
    在从最左边开始的位置处渲染另外的字节，低8个像素。

.. data:: framebuf.MONO_HLSB

    单色（1位）颜色格式这定义了一个字节中的位被水平映射的映射。每个字节占据8个水平像素，其中第0位是最左边的。
    后续字节出现在连续的水平位置，直到到达最右边。在下一行上渲染更多字节，一个像素更低。

.. data:: framebuf.MONO_HMSB

    单色（1bit）颜色格式这定义了一个字节中的位被水平映射的映射。每个字节占据8个水平像素，其中第0位是最左边的。
    后续字节出现在连续的水平位置，直到到达最右边。在下一行上渲染更多字节，一个像素更低。

.. data:: framebuf.RGB565

    红绿蓝（16bit，5 + 6 + 5）颜色格式

.. data:: framebuf.GS2_HMSB

    灰度（2位bit）颜色格式

.. data:: framebuf.GS4_HMSB

    灰度（4位bit）颜色格式


.. data:: framebuf.GS8

    灰度（8bit）颜色格式
