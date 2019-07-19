
语音听写(IAT)
+++++++++++

基于 `讯飞TTS语音听写 <https://www.xfyun.cn/services/voicedictation>`_ ,将语音(≤60秒)转换成对应的文字信息，让机器能够“听懂”人类语言，相当于给机器安装上“耳朵”，使其具备“能听”的功能。


.. py:method:: audio.xunfei_iat_config(api_key, app_id)

| 讯飞iat配置,使用前须要用 ``audio.recorder_init()`` 录音初始化。由于该功能依赖讯飞API,在使用前需要先将掌控板连接至互联网,并设置RTC时钟至准确时间。
| 讯飞语音听写功能,使用该功能前需要在讯飞开发平台 https://www.xfyun.cn/ 注册账号,步骤如下：
|     
| 1. 注册账号(已有账号,略过)
| 2. 在产品中,选择“语音听写”服务。
| 3. 在IP白名单中添加网络的公网IP。

    - ``api_key`` (str): 讯飞应用的APIKey
    - ``app_id`` (str): 讯飞应用的APPID
   
.. py:method:: audio.xunfei_iat_record()

IAT录音,如要设置录音时长,带参数传入,单位为秒。不带参数默认为录音5秒。该函数为阻塞型,当录音结束后才释放,执行后续的命令。

.. py:method:: audio.xunfei_iat()

将iat录音传至讯飞平台处理,处理结束后,将返回语音转文字的json内容。
