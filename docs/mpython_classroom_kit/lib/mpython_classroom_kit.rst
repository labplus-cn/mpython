.. module:: mpython_classroom_kit
   :synopsis: 掌控板实验箱模块

:mod:`mpython_classroom_kit` --- 掌控板实验箱模块
==========================================================

``mpython_classroom_kit`` 模块提供实验箱上的传感器和输出设备的驱动函数,及人工智能应用的相关函数。

------------------------------------------------------------

.. contents::

------------------------------------------------------------

函数
---------


.. function:: get_distance()

获取超声波传感器测距值,单位cm。范围3~340CM


.. function:: set_motor(speed)

设置马达速度

-  ``speed`` - 马达速度,范围±100。正值表示正转,负值则反。


.. function:: get_key()

获取方向按键,返回已按下按键的集合。当单个或多个按键按下,可以集合(set)运算,判断按键状态。

集合所有元素如下: 
`{'left', 'right', 'up', 'down', 'ok'}`

.. literalinclude:: /../examples/mpython_classroom_kit/key_control_motor.py
    :caption: 方向按键控制马达
    :linenos:


.. method:: pir.value()

返回人体红外触发值。当为1时,表示已触发。

.. method:: slider_res.read()

返回滑杆电阻采样值。范围0~4095。

.. literalinclude:: /../examples/mpython_classroom_kit/slider_control_motor.py
    :caption: 滑杆控制马达
    :linenos:

------------------------------------------------------------

神经网络模型
------------

model支持yolov2和MobileNet卷积神经网络模型。内置人脸追踪,20类追踪,Mnist手写数字,1000分类器的应用模型。

.. method:: model.select_model(builtin)

内置神经网络模型加载

    - ``builtin`` 

        ========================= ======  ====================================  
        ``model.FACE_YOLO``          1      人脸追踪,yolov2
        ``model.CLASS_20_YOLO``      2      20类追踪,yolov2
        ``model.MNIST_NET``          3      手写数字(Mnist)图像分类器,MobileNet
        ``model.CLASS_1000_NET``     4      1000类图像分类器,MobileNet
        ========================= ======  ====================================  

.. Attention:: 1000分类器功能未实现,暂不开放。


.. figure:: https://arleyzhang.github.io/articles/1dc20586/1522997065951.png
    :align: center
    :width: 600

    PASCAL VOC挑战赛 20类别说明

.. method:: model.load_model(path, model_type, classes, anchor=None)

加载外部神经网络模型

    - ``path`` - 模型路径,字符串类型。模型应存放在SD卡中。
    - ``model_type`` - 神经网络模型类型

        - ``model.YOLO2`` - 1
        - ``model.MOBILENET`` - 2
    - ``classes`` - 分类标签,类型数组。计算得出结果将返回类别索引,对应该数组。
    - ``anchor`` - 在yolo模型上使用,锚点参数与模型参数一致。

.. method:: model.detect_yolo()

yolo追踪模型计算。返回已侦测到的物体数组,json数据包含物体所在的矩形 `x` , `y` , `w` , `h` 。`value` 为侦测物体的相似率。 `classid` 为识别物体的类别,类型为数字类型。
`index` 为侦测到物体的json数据索引。

.. method:: model.predict_net()

MobileNet模型计算。返回预测图形分类的概率数组。

.. method:: model.deinit_yolo()

使用yolo模型计算后,释放资源。

.. method:: model.deinit_net()

使用MobileNet模型计算后,释放资源。


.. literalinclude:: /../examples/mpython_classroom_kit/face_detect.py
    :caption: 人脸追踪
    :linenos:

.. literalinclude:: /../examples/mpython_classroom_kit/20classes_detect.py
    :caption: 20类的追踪
    :linenos:

.. literalinclude:: /../examples/mpython_classroom_kit/mnist.py
    :caption: 手写数字识别
    :linenos:

------------------------------------------------------------
    
摄像头
------------

.. method:: camera.reset()

重置并初始化摄像头


.. method:: camera.run()

启动/关闭芯片捕获图像。1表示开启，0 表示停止。

.. method:: camera.snapshot()

控制摄像头捕捉单帧图像

.. method:: camera.set_pixformat(format)

用于设置摄像头像素模式。

    - ``format`` - 帧格式

        - ``camera.GRAYSCALE`` - 4, 8-bits 每像素的灰度图
        - ``camera.RGB565`` - 2, 16-bits 每像素

.. method:: camera.set_contrast()

设置摄像头对比度,范围为[-2,+2]

.. method:: camera.set_brightness()

设置摄像头亮度,范围为[-2,+2]

.. method:: camera.set_saturation()

设置摄像头饱和度,范围为[-2,+2]

.. method:: camera.set_auto_gain(enable,gain_db)

设置摄像自动增益模式

    - ``enable`` - 1 表示开启自动增益 0 表示关闭自动增益
    - ``gain_db`` - 关闭自动增益时，设置的摄像头固定增益值，单位为db

.. method:: camera.set_auto_whitebal(enable)

设置摄像自动白平衡模式,默认打开。``True`` 为打开, ``False`` 为关闭自动白平衡。

.. Note:: 若您想追踪颜色，则需关闭白平衡。

.. method:: camera.set_windowing()

设置摄像头窗口大小。例如：你可以 ``set_windowing((224,224))`` ， 然后 ``snapshot()`` 以捕捉由摄像头输出的320*240分辨率的224x224中心像素。您可使用窗口来获得定制的分辨率。

.. method:: camera.set_hmirror()

设置摄像头水平镜像。1 表示开启水平镜像 0 表示关闭水平镜像。

.. method:: camera.set_vflip()

设置摄像头垂直翻转。1 表示开启垂直翻转 0 表示关闭垂直翻转。

------------------------------------------------------------

lcd显示屏
------------

.. method:: lcd.init(freq=15000000, color=lcd.BLACK)

初始化 `LCD` 屏幕显示。

    - ``freq`` - SPI 的通讯速率
    - ``color`` - LCD 初始化的颜色。默认 `lcd.BLACK` 。可以是16位的 RGB565 颜色值，比如 0xFFFF；或者RGB元组， 比如 (236, 36, 36)。或者以下定义的color常量；

        ========================= ==========  ==================================== 
        ``lcd.BLACK``               0           黑
        ``lcd.NAVY``                15          深蓝
        ``lcd.DARKGREEN``           992         深绿
        ``lcd.DARKCYAN``            1007        深青
        ``lcd.MAROON``              30720       褐红
        ``lcd.PURPLE``              30735       紫色
        ``lcd.OLIVE``               31712       橄榄绿
        ``lcd.LIGHTGREY``           50712       浅灰
        ``lcd.DARKGREY``            31727       深灰
        ``lcd.BLUE``                31          蓝
        ``lcd.GREEN``               2016        绿
        ``lcd.RED``                 63488       红
        ``lcd.MAGENTA``             63519       洋红
        ``lcd.YELLOW``              65504       黄
        ``lcd.WHITE``               65535       白
        ``lcd.ORANGE``              64800       橙
        ``lcd.GREENYELLOW``         45029       黄绿
        ``lcd.PINK``                63519       粉红
        ========================= ==========  ==================================== 
 
.. method:: lcd.display(roi)

在 `lcd` 屏上显示图片帧。 `roi` 居于屏幕中心，且不匹配像素不会显示（即液晶屏以窗口形态显示 `roi` 的中心）

    - ``roi`` - 感兴趣区域的矩形元组(x, y, w, h)。若未指定，即为图像矩形。

.. method:: lcd.clear()

将lcd屏清空为黑色或者指定的颜色。

.. method:: lcd.draw_string(x,y,text,color)

在lcd屏上绘制文本。从(x,y)位置开始绘制text文本, ``color`` 为文本的颜色,可以为16位的 `RGB565` 颜色值、RGB元组或者color常量。

------------------------------------------------------------

图像处理
------------

.. method:: image.load()

文件系统的图片加载。可以把图片存放至SD卡中,将对应图片文件路径作为该函数参数,将会创建该帧图片对象。支持bmp/pgm/ppm/jpg/jpeg格式的图像文件。

.. Attention:: 使用时需要注意图片分辨率大小,过大的话会导致内存错误！


.. method:: image.width()

返回当前图像帧的宽度。

.. method:: image.hight()

返回当前图像帧的高度。

.. method:: image.format()

返回当前图像帧的格式。返回用于灰度图的 ``camera.GRAYSCALE`` 、用于RGB图像的 ``camera.RGB565`` 。

.. method:: image.size()

返回当前图像帧的大小,单位字节。

.. method:: image.get_pixel(x, y)

返回(x, y)位置的像素值。灰度图返回灰度值,RGB图返回rgb元组。

.. method:: image.set_pixel(x, y, pixel)

将(x, y) 位置的像素设置为pixel 。

.. method:: image.mean_pool(x_div, y_div)

在图像中找到 x_div * y_div 正方形的平均值，并返回由每个正方形的平均值组成的修改图像。

此方法允许您在原来图像上快速缩小图像。

.. method:: image.to_grayscale()

将图像转换为灰度图像。 

.. method:: image.to_rainbow()

将图像转换为彩虹图像。

.. method:: image.copy(roi)

复制 `roi` 感兴趣的矩形区域(x, y, w, h),来生产新的图像帧。

.. method:: image.save(path[, roi])

将图像的副本保存到 `path` 中的k210文件系统。

.. method:: image.clear()

将图像中的所有像素设置为零（非常快）。

.. method:: image.draw_line(x0, y0, x1, y1[, color[, thickness=1]])

在图像上绘制一条从(x0，y0)到(x1，y1)的线。 您可以单独传递x0，y0，x1，y1，也可以传递给元组(x0，y0，x1，y1)。

    - ``color`` -  是用于灰度或RGB565图像的元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
    - ``thickness`` -  控制线的粗细像素。

.. method:: image.draw_rectangle(x, y, w, h[, color[, thickness=1[, fill=False]]])


在图像上绘制一个矩形。 您可以单独传递x，y，w，h或作为元组(x，y，w，h)传递。

    - ``color`` -  是用于灰度或RGB565图像的元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
    - ``thickness`` -  控制线的粗细像素。
    - ``fill`` - 设置为True以填充矩形。

.. method:: image.draw_circle(x, y, radius[, color[, thickness=1[, fill=False]]])

在图像上绘制一个圆形。 您可以单独传递x，y，半径 或 作为元组(x，y，radius)传递。

    - ``color`` -  是用于灰度或RGB565图像的元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
    - ``thickness`` -  控制线的粗细像素。
    - ``fill`` - 设置为True以填充圆形。

.. method:: image.draw_string(x, y, text[, color[, scale=1[, x_spacing=0[, y_spacing=0[, mono_space=True]]])

从图像中的(x, y)位置开始绘制8x10文本。您可以单独传递x，y，也可以作为元组(x，y)传递。

    - ``text`` -  是写入图像的字符串。 \n, \r, 和 \r\n 结束符将光标移至下一行。
    - ``color`` -  是用于灰度或RGB565图像的元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
    - ``scale`` - 增加图像上文本的大小,仅整数值。
    - ``x_spacing`` -  允许你在字符之间添加（如果是正数）或减去（如果是负数）x像素，设置字符间距。
    - ``y_spacing`` -  允许你在字符之间添加（如果是正数）或减去（如果是负数）y像素，设置行间距。
    - ``mono_space`` - 默认为True，强制文本间距固定。对于大文本，这看起来很糟糕。设置False以获得非固定宽度的字符间距。

.. method:: image.draw_cross(x, y[, color[, size=5[, thickness=1]]])

在图像上绘制一个十字。 您可以单独传递x，y或作为元组(x，y)传递。

    - ``color`` - 是用于灰度或RGB565图像的RGB元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
    - ``size`` -  控制十字线的延伸长度。
    - ``thickness`` - 控制边缘的像素厚度。

.. method:: image.draw_arrow(x0, y0, x1, y1[, color[, thickness=1]])

在图像上绘制一条从(x0，y0)到(x1，y1)的箭头。 您可以单独传递x0，y0，x1，y1，也可以传递给元组(x0，y0，x1，y1)。

    - ``color`` - 是用于灰度或RGB565图像的元组。默认为白色。但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。
    - ``thickness`` - 控制线的粗细像素。

.. method:: image.binary(thresholds[, invert=False[, zero=False[, mask=None[, to_bitmap=False[, copy=False]])

根据像素是否在阈值列表 `thresholds` 中的阈值内，将图像中的所有像素设置为黑色或白色。

`thresholds` 必须是元组列表。 [(lo, hi), (lo, hi), ..., (lo, hi)] 定义你想追踪的颜色范围。对于灰度图像，每个元组需要包含两个值 - 最小灰度值和最大灰度值。 仅考虑落在这些阈值之间的像素区域。
对于RGB565图像，每个元组需要有六个值(l_lo，l_hi，a_lo，a_hi，b_lo，b_hi) - 分别是LAB L，A和B通道的最小值和最大值。为方便使用，此功能将自动修复交换的最小值和最大值。此外，如果元组大于六个值，则忽略其余值。相反，如果元组太短，则假定其余阈值处于最大范围。



.. method:: image.invert()

将二进制图像0（黑色）变为1（白色），1（白色）变为0（黑色），非常快速地翻转二进制图像中的所有像素值。

.. method:: image.erode(size[, threshold[, mask=None]])

腐蚀效果,从分割区域的边缘删除像素。腐蚀是原图中的高亮区域被蚕食，效果图拥有比原图更小的高亮区域。

这一方法通过卷积图像上((size*2)+1)x((size*2)+1)像素的核来实现，如果相邻像素集的总和小于 `threshold` ，则对内核的中心像素进行归零。
若 `threshold` 未设定，这个方法的功能如标准腐蚀方法一样。若 `threshold` 设定，您就可以指定腐蚀的特定像素，例如：设置低于2个的像素周围阈值为2。`mask` 是另一个用作绘图操作的像素级掩码的图像。掩码应该是一个只有黑色或白色像素的图像，并且应该与你正在绘制的 image 大小相同。 仅掩码中设置的像素被修改。

.. method:: image.dilate(size[, threshold[, mask=None]])

膨胀效果,将像素添加到分割区域的边缘中。膨胀就是对图像高亮部分进行“领域扩张”，效果图拥有比原图更大的高亮区域。

这一方法通过卷积图像上((size*2)+1)x((size*2)+1)像素的核来实现，如果相邻像素集的总和大于 `threshold` ，则将内核的中心像素进行设置。若 `threshold` 未设定，这个方法的功能如标准腐蚀方法一样。
若threshold设定，您就可以指定腐蚀的特定像素，例如：设置低于2个的像素周围阈值为2。`mask` 是另一个用作绘图操作的像素级掩码的图像。掩码应该是一个只有黑色或白色像素的图像，并且应该与你正在绘制的 `image` 大小相同。仅掩码中设置的像素被修改。


.. method:: image.negate()

非常快速地翻转（数字反转）图像中的所有像素值。对每个颜色通道的像素值进行数值转换。例： (255 - pixel).

.. method:: image.mean(size, [threshold=False, [offset=0, [invert=False, [mask=None]]]]])

使用盒式滤波器的标准均值模糊滤波。

    - ``Size`` - 是内核的大小。取1 (3x3 内核)、2 (5x5 内核)或更高值。
    - ``threshold`` - 如果你想在滤波器的输出上自适应地设置阈值，你可以传递 threshold=True 参数来启动图像的自适应阈值处理， 他根据环境像素的亮度（核函数周围的像素的亮度有关），将像素设置为1或者0。 
    - ``offset`` 负数 offset 值将更多像素设置为1，而正值仅将最强对比度设置为1。 
    - ``invert`` -  以反转二进制图像的结果输出。
    - ``mask`` - 是另一个用作绘图操作的像素级掩码的图像。掩码应该是一个只有黑色或白色像素的图像，并且应该与你正在绘制的 `image` 大小相同。 仅掩码中设置的像素被修改。

.. method:: image.mode(size[, threshold=False, offset=0, invert=False, mask])

在图像上运行众数滤波，用相邻像素的模式替换每个像素。这一方法在灰度图上运行效果良好。但由于这一操作的非线性特性，会在RGB图像边缘上产生许多伪像。

    - ``Size`` -  是内核的大小。取1 (3x3 内核)、2 (5x5 内核)。
    - ``threshold`` - 如果你想在滤波器的输出上自适应地设置阈值，你可以传递 `threshold=True` 参数来启动图像的自适应阈值处理， 他根据环境像素的亮度（核函数周围的像素的亮度有关），将像素设置为1或者0。 
    - ``offset`` - 负数 offset 值将更多像素设置为1，而正值仅将最强对比度设置为1。 
    - ``invert`` - 设置 invert 以反转二进制图像的结果输出。
    - ``mask`` - 是另一个用作绘图操作的像素级掩码的图像。掩码应该是一个只有黑色或白色像素的图像，并且应该与你正在绘制的 image 大小相同。 仅掩码中设置的像素被修改。

.. method:: image.midpoint(size[, bias=0.5, threshold=False, offset=0, invert=False, mask])

在图像上运行中点滤波。此滤波器找到图像中每个像素邻域的中点((max-min)/2)。

    - ``size`` - 是内核的大小。取1 (3x3 内核)、2 (5x5 内核)或更高值。
    - ``bias`` - 控制图像混合的最小/最大程度。0只适用于最小滤波，1仅用于最大滤波。您可以通过 bias 对图像进行最小/最大化过滤。
    - ``threshold`` - 如果你想在滤波器的输出上自适应地设置阈值，你可以传递 threshold=True 参数来启动图像的自适应阈值处理， 他根据环境像素的亮度（核函数周围的像素的亮度有关），将像素设置为1或者0。 
    - ``offset`` - 负数 offset 值将更多像素设置为1，而正值仅将最强对比度设置为1。 
    - ``invert`` - 以反转二进制图像的结果输出。
    - ``mask`` - 是另一个用作绘图操作的像素级掩码的图像。掩码应该是一个只有黑色或白色像素的图像，并且应该与你正在绘制的 image 大小相同。 仅掩码中设置的像素被修改。


.. method:: image.cartoon(size[, seed_threshold=0.05[, floating_threshold=0.05[, mask=None]]])

使图像卡通化并使用flood-fills算法填充图像中的所有像素区域。 这通过使图像的所有区域中的颜色变平来有效地从图像中去除纹理。 为了获得最佳效果，图像应具有大量对比度，以使区域不会太容易相互渗透。

    - ``seed_threshold`` - 控制填充区域中的像素与原始起始像素的差异。
    - ``floating_threshold`` - 控制填充区域中的像素与任何相邻像素的差异。
    - ``mask`` - 是另一个用作绘图操作的像素级掩码的图像。掩码应该是一个只有黑色或白色像素的图像，并且应该与你正在绘制的 `image` 大小相同。 仅掩码中设置的像素被修改。

.. method:: image.conv3(kernel)

通过卷积内核对图像进行卷积。

    - ``kernel`` - 用来卷积图像的内核，可为一个元组或一个取值[-128:127]的列表。

.. method:: image.gaussian(size[, unsharp=False[, mul[, add=0[, threshold=False[, offset=0[, invert=False[, mask=None]]]]]]])

通过平滑高斯核对图像进行卷积。

    - ``size`` - 是内核的大小。取1 (3x3 内核)、2 (5x5 内核)或更高值。
    - ``unsharp`` - 如果 unsharp 设置为True，那么这种方法不会仅进行高斯滤波操作，而是执行非锐化掩模操作，从而提高边缘的图像清晰度。
    - ``mul`` - 用以与卷积像素结果相乘的数字。若不设置，则默认一个值，该值将防止卷积输出中的缩放。
    - ``add`` - 用来与每个像素卷积结果相加的数值。
    - ``mul`` - 可进行全局对比度调整，add可进行全局亮度调整。
    - ``threshold`` - 如果你想在滤波器的输出上自适应地设置阈值，你可以传递 threshold=True 参数来启动图像的自适应阈值处理， 他根据环境像素的亮度（核函数周围的像素的亮度有关），将像素设置为1或者0。
    - ``offset`` - 负数 offset 值将更多像素设置为1，而正值仅将最强对比度设置为1。
    - ``invert`` - 反转二进制图像的结果输出。
    - ``mask`` -  是另一个用作绘图操作的像素级掩码的图像。掩码应该是一个只有黑色或白色像素的图像，并且应该与你正在绘制的 image 大小相同。 仅掩码中设置的像素被修改。


.. method:: image.bilateral(size[, color_sigma=0.1[, space_sigma=1[, threshold=False[, offset=0[, invert=False[, mask=None]]]]]])


通过双边滤波器对图像进行卷积。 双边滤波器使图像平滑，同时保持图像中的边缘。

    - ``size`` - 是内核的大小。取1 (3x3 内核)、2 (5x5 内核)或更高值。
    - ``color_sigma`` - 控制使用双边滤波器匹配颜色的接近程度。增加此值可增加颜色模糊。
    - ``space_sigma`` - 控制像素在空间方面相互模糊的程度。增加此值可增加像素模糊。
    - ``threshold`` - 如果你想在滤波器的输出上自适应地设置阈值，你可以传递 `threshold=True` 参数来启动图像的自适应阈值处理， 他根据环境像素的亮度（核函数周围的像素的亮度有关），将像素设置为1或者0。 
    - ``offset`` - 负数 offset 值将更多像素设置为1，而正值仅将最强对比度设置为1。 
    - ``invert`` - 以反转二进制图像的结果输出。
    - ``mask`` - 是另一个用作绘图操作的像素级掩码的图像。掩码应该是一个只有黑色或白色像素的图像，并且应该与你正在绘制的 image 大小相同。 仅掩码中设置的像素被修改。


.. method:: image.linpolar([reverse=False])


图像从笛卡尔坐标到线性极坐标重新投影。线性极坐标重新投影将图像旋转转换为x平移。

    - ``reverse`` - 设置 `reverse = True` 可以在相反的方向重新投影。


.. method:: image.logpolar([reverse=False])

图像从笛卡尔坐标到对数极坐标重新投影。对数极坐标重新投影将图像的旋转转换为x平移和缩放到y平移。

    - ``reverse``- 设置 `reverse = True` 可以在相反的方向重新投影。

.. method:: image.rotation_corr([x_rotation=0.0[, y_rotation=0.0[, z_rotation=0.0[, x_translation=0.0[, y_translation=0.0[, zoom=1.0]]]]]])

通过执行帧缓冲区的3D旋转来纠正图像中的透视问题。

    - ``x_rotation`` - 围绕x轴在帧缓冲器中旋转图像的度数（这使图像上下旋转）。
    - ``y_rotation`` - 帧缓冲区中围绕y轴旋转图像的度数（即左右旋转图像）。
    - ``z_rotation`` - 围绕z轴在帧缓冲器中旋转图像的度数（即，使图像旋转到适当位置）。
    - ``x_translation`` - 旋转后将图像移动到左侧或右侧的单位数。因为这个变换是应用在三维空间的，单位不是像素…
    - ``y_translation`` - 是旋转后将图像上移或下移的单位数。因为这个变换是应用在三维空间的，单位不是像素…
    - ``zoom`` - 通过图像缩放的量。默认情况下1.0。


.. method:: image.find_blobs(thresholds[, invert=False[, roi[, x_stride=2[, y_stride=1[, area_threshold=10[, pixels_threshold=10[, merge=False[, margin=0[, threshold_cb=None[, merge_cb=None]]]]]]]]]])

查找图像中所有色块，并返回一个包括每个色块的色块对象的列表。请观察 ``blob`` 对象以获取更多信息。
   
   - ``thresholds`` - 必须是元组列表。
   - ``[(lo, hi), (lo, hi), ..., (lo, hi)]`` - 定义你想追踪的颜色范围。对于灰度图像，每个元组需要包含两个值-最小灰度值和最大灰度值。仅考虑落在这些阈值之间的像素区域。对于RGB565图像，每个元组需要有六个值(l_lo，l_hi，a_lo，a_hi，b_lo，b_hi) - 分别是LAB L，A和B通道的最小值和最大值。为方便使用，此功能将自动修复交换的最小值和最大值。此外，如果元组大于六个值，则忽略其余值。相反，如果元组太短，则假定其余阈值处于最大范围。
   - ``invert`` - 反转阈值操作，像素在已知颜色范围之外进行匹配，而非在已知颜色范围内。
   - ``roi`` - 感兴趣区域的矩形元组(x，y，w，h)。如果未指定，ROI即整个图像的图像矩形。操作范围仅限于 ``roi`` 区域内的像素。
   - ``x_stride`` - 查找某色块时需要跳过的x像素的数量。找到色块后，直线填充算法将精确像素。若已知色块较大，可增加 ``x_stride`` 来提高查找色块的速度。
   - ``y_stride`` - 查找某色块时需要跳过的y像素的数量。找到色块后，直线填充算法将精确像素。若已知色块较大，可增加 ``y_stride`` 来提高查找色块的速度。
   - ``area_threshold`` - 若一个色块的边界框区域小于 ``area_threshold`` ，则会被过滤掉。
   - ``pixel_threshold`` - 若一个色块的像素数小于 ``pixel_threshold`` ，则会被过滤掉。
   - ``merge`` - 若为True，则合并所有没有被过滤掉的色块，这些色块的边界矩形互相交错重叠。 
   - ``margin`` - 可在相交测试中用来增大或减小色块边界矩形的大小。例如：边缘为1、相互间边界矩形为1的色块将被合并。
   - ``threshold_cb`` - 可设置为用以调用阈值筛选后的每个色块的函数，以便将其从将要合并的色块列表中过滤出来。回调函数将收到一个参数：要被筛选的色块对象。然后回调函数需返回True以保留色块或返回False以过滤色块。
   - ``merge_cb`` - 可设置为用以调用两个即将合并的色块的函数，以禁止或准许合并。回调函数将收到两个参数—两个将被合并的色块对象。回调函数须返回True以合并色块，或返回False以防止色块合并。

   合并色块使颜色代码追踪得以实现。每个色块对象有一个代码值 ``code`` ，该值为一个位向量。
   例如：若您在 `image.find_blobs` 中输入两个颜色阈值，则第一个阈值代码为1，第二个代码为2（第三个代码为4，第四个代码为8，以此类推）。
   合并色块对所有的code使用逻辑或运算，以便您知道产生它们的颜色。这使得您可以追踪两个颜色，若您用两种颜色得到一个色块对象，则可能是一种颜色代码。

   若您使用严格的颜色范围，无法完全追踪目标对象的所有像素，您可能需要合并色块。最后，若您想要合并色块，但不想两种不同阈值颜色的色块被合并，只需分别两次调用 ``image.find_blobs`` ，不同阈值色块就不会被合并。


.. literalinclude:: /../examples/mpython_classroom_kit/find_max_blob.py
    :caption: 追踪色块
    :linenos:


------------------------------------------------------------

blob 类 -- 色块对象
--------------------

色块对象是由 :meth:`image.find_blobs` 返回的。

.. method:: blob.rect()

   返回一个矩形元组(x, y, w, h) ，用于如色块边界框的 `image.draw_rectangle` 等
   其他的 `image` 方法。

.. method:: blob.x()

   返回色块的边界框的x坐标(int)。


.. method:: blob.y()

   返回色块的边界框的y坐标(int)。


.. method:: blob.w()

   返回色块的边界框的w坐标(int)。


.. method:: blob.h()

   返回色块的边界框的h坐标(int)。


.. method:: blob.pixels()

   返回从属于色块(int)一部分的像素数量。

.. method:: blob.cx()

   返回色块(int)的中心x位置。

.. method:: blob.cy()

   返回色块(int)的中心x位置。

.. method:: blob.rotation()

   返回色块的旋转（单位：弧度）。如果色块类似铅笔或钢笔，那么这个值就是介于0-180之间的唯一值。
   如果这个色块圆的，那么这个值就没有效用。如果这个色块完全不具有对称性，您只能由此得到0-360度的旋转。


.. method:: blob.code()

   返回一个16位的二进制数字，其中为每个颜色阈值设置一个位，这是色块的一部分。
   例如，如果您通过 `image.find_blobs` 来寻找三个颜色阈值，这个色块可以设置为0/1/2位。

   注意：除非以 `merge=True` 调用 `image.find_blobs` ，否则每个色块只能设置一位。那么颜色阈值不同的多个色块就可以合并在一起了。您也可以用这个方法以及多个阈值来实现颜色代码跟踪。


.. method:: blob.count()

   返回合并为这一色块的多个色块的数量。只有您以 `merge=True`
   调用 `image.find_blobs` 时，这个数字才不是1。


