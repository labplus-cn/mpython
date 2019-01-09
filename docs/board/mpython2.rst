mPython2 IDE
====================

软件安装
-----------

目前有三个下载地址（for Windows 64位、Windows 32位、MacOS）：

http://static.steamaker.cn/files/mPython2_0.2.5_win64.exe

http://static.steamaker.cn/files/mPython2_0.2.5_win32.exe

http://static.steamaker.cn/files/mPython2_0.2.5_macos.zip


根据操作系统选择不同的版本下载，目前支持Win 7 / 8 / 10、MacOS，不支持XP系统。

.. Attention:: 

  因为Python调用路径的原因，程序不可以安装在中文目录下。
  程序默认会安装在Windows用户目录下，如：C:\\Users\\{用户名}\\AppData\\Local\\mPython2
  有的用户名为中文，使用默认路径会导致安装后的快捷方式无法正确打开
  请修改路径，如下图，修改为：D:\\mPython2


.. image:: /images/software/software_1.png
      :scale: 80 %

.. Hint::
  
  安装过程有可能被杀毒软件误报病毒，需要选择“允许程序所有操作”。


安装软件的最后一步，会自动安装CP210x的驱动，如果先前安装过则可以忽略。

.. image:: /images/software/software_2.png
    :scale: 70 %


接入硬件
-----------

点击桌面快捷方式mPython2，打开软件主界面。

.. image:: /images/software/software_3.png

用USB线接入掌控板。如果是初次接入，Windows可能要花费比较多的时间才能识别出掌控板，正确识别后，
软件会自动弹出提示，提示切换到：掌控（mPython）模式，如下图：

.. image:: /images/software/software_4.png


上述顺序可以颠倒，即：可以先接入掌控，再打开软件，一样会弹出提示。
如果软件已经是掌控模式，再接入掌控时，则只会在状态栏上提示。

浏览文件系统
-----------

点击菜单“文件”，打开掌控板上文件系统，目前为了确保掌控板文件系统能被正确打开，这个过程约需要3秒。

.. image:: /images/software/software_5.png

代码编辑区
-----------

代码提示功能：输入前两个字符，可以自动提示内容

.. image:: /images/software/software_6.png

打开本地文件，在电脑文件区右键菜单“在编辑区打开”

.. image:: /images/software/software_7.png

从Windows资源管理器拖动任意文件到编辑区

.. image:: /images/software/software_8.png

掌控板文件系统
-----------

界面左下是掌控板文件系统，初次使用掌控板，文件列表可能是空白的。
界面右下是本地文件系统，对应目录在 C:\\Users\\{用户名}\\mu_code

写入基础库
````````
掌控板文件区菜单自带基础库mpython.py，初次使用需要先把基础库写入掌控板。
如图，在掌控板文件区任意地方，鼠标右键点击“写入基础库(mpython.py)”

.. image:: /images/software/software_9.png

.. Note::

  写入基础库的目的是：以后在程序中可以使用 from mpython import * 的语句

向掌控板写入代码文件
````````

现在，可以向掌控板写入代码文件。

写入方式可以是：

1.通过菜单“刷入”，把当前编辑区的内容刷入掌控板

.. image:: /images/software/software_10.png

2.从电脑文件区拖动文件到掌控板

.. image:: /images/software/software_11.png


掌控板文件区菜单
````````

在编辑区打开
::::::::::


把掌控板上的文件内容读取到编辑区内，与电脑文件不同，来自掌控板的文件名称，会以中括号标起来。

.. image:: /images/software/software_12.png


运行指定代码
::::::::::

选定一个程序来实时运行。
若运行成功，在掌控板上可以看实时效果。

.. image:: /images/software/software_13.png



  由于micropython系统限制，超过40KB的源码（代码量500行以上），有可能无法实时运行，此时会在状态栏有提示。


停止
::::::::::

停止当前正在运行的程序（但无法停止main.py）。因为程序已经实现了连续运行不同代码，此功能现在较少用到。

设为默认运行
::::::::::

把某个代码设定为掌控板默认运行程序，在通电或者重启后立即运行。

.. Attention:: 

  部分不能实时运行的代码，有可能设置为默认程序后可以运行。

重命名
::::::::::

重命名某个文件。

删除
::::::::::

删除掌控板上某个文件。删除，不可撤销。


本地文件系统
-----------

界面右下是本地文件系统，对应目录在 C:\\Users\\{用户名}\\mu_code


本地文件区菜单
````````

在编辑区打开
::::::::::

把本地文件区的文件在IDE中打开。

刷新
::::::::::

手动刷新本地文件区文件。

在计算机中打开
::::::::::

调用计算机默认程序打开本地文件区文件，如*.txt对应的可能是记事本打开。

删除到回收站
::::::::::

把本地文件区文件删除到回收站。


在交互模式下进行调试
-----------

进入交互模式
````````

先关闭文件窗口，此时菜单栏原来灰掉的“交互”按钮变为可用，此时可以进入交互模式。

.. image:: /images/software/software_14.png

停止默认运行程序
````````

进入交互模式后，掌控板会软重启，默认会运行main.py，此时，先点击REPL区，并按下Ctrl+C，来打断main.py的运行。

.. image:: /images/software/software_15.png

准备粘贴代码
````````

鼠标焦点在REPL区的时候，按下Ctrl+E，进入代码粘贴模式。

.. image:: /images/software/software_16.png

粘贴代码
````````

用鼠标右键粘贴已有的代码，代码中若含有中文，将自动转换为Unicode格式。

.. image:: /images/software/software_17.png

退出粘贴模式，并调试代码
````````

按下Ctrl+D，退出粘贴模式，同时运行代码，此时可以同时查看调试信息。

.. image:: /images/software/software_18.png


恢复固件及写入基础库
-----------

固件异常表现
````````

接入掌控板时若有下图弹窗提示，先尝试重新插拔或更换接口、数据线。

.. image:: /images/software/software_19.png

固件异常时，掌控板上的文件处显示为空或...

固件异常时，交互模式显示为以下两种情况之一

.. image:: /images/software/software_30.png

.. image:: /images/software/software_31.png

恢复固件
````````

在掌控板文件区域的空白处右键，选择恢复固件，按照左下角提示信息操作。

.. image:: /images/software/software_20.png

.. image:: /images/software/software_21.png

.. image:: /images/software/software_22.png

.. image:: /images/software/software_23.png

.. image:: /images/software/software_24.png

文件系统出现boot.py及mpython.py即恢复固件成功。

.. image:: /images/software/software_25.png

写入基础库
````````

恢复固件成功后建议写入基础库，在掌控板文件区域的空白处右键，选择写入基础库。

.. image:: /images/software/software_26.png

.. image:: /images/software/software_27.png

写入成功即可见掌控板文件增加了mpython.py。

.. image:: /images/software/software_28.png
