
贝壳物联
==============

贝壳物联是一个让你与智能设备沟通更方便的物联网云平台，你可以通过互联网以对话、遥控器等形式与你的智能设备聊天、发送指令，查看实时数据， 
跟实际需求设置报警条件，通过APP、邮件、短信、微博、微信等方式通知用户。

.. figure:: https://www.bigiot.net/Public/upload/UEditor/image/20181024/1540363897144665.jpg
    :width: 550
    :align: center

    贝壳物联架构

- 贝壳物联平台通讯协议：https://www.bigiot.net/help/1.html

掌控板连接贝壳物联
-----------------

准备工作
+++++++++

* 在使用前,需要先到贝壳物联 https://www.bigiot.net 注册账号,并增加智能设备。

* 程序中,需要用到bigiot的mPython库,你可以到 https://github.com/labplus-cn/mPython-lib 获取。 将 bigiot.py 上传到文件系统中。
  或者你也可以用 upip.install("mPython-bigiot") 的方法获取pypi包。


设备间通讯
++++++++++++

bigiot简单通讯示例::

    from mpython import *
    import bigiot

    my_wifi = wifi()
    my_wifi.connectWiFi("youruser", "yourpassword")

    ID = ""                             # 设备ID
    API_KEY = ""                        # 设备APIKEY


    def say_cb(msg):                    # say回调函数
        print(msg)


    device = bigiot.Device(ID, API_KEY)         # 构建bigiot 设备

    device.say_callback(say_cb)                 # 设置say通讯的回调函数

程序开始要首先连接至

语音助手
---------

https://www.bigiot.net/talk/359.html