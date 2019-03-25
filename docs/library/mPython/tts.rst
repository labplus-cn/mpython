.. _tts:

tts 模块
==========

基于讯飞TTS语音合成API的文字转语音功能,将文字信息转化为声音信息，给掌控板配上“嘴巴”。其合成音在音色、自然度等方面的表现均接近甚至超过了人声。目前应用于掌控拓展板。



TTS类
----------

讯飞文字转语音功能,使用该功能前需要在讯飞开发平台 https://www.xfyun.cn/ 注册账号,步骤如下：
    
1. 注册账号
2. 新建产品,选择“在线语音合成”服务。
3. 在IP白名单中添加网络的公网IP。

.. py:class:: TTS( appid, api_key, voice_name="aisxping", engine_type="intp65")

构建对象

    - ``appid`` (str): 讯飞应用的APPID
    - ``api_key`` (str): 讯飞应用的APIKey
    - ``voice_name`` (str): 发音人,默认"aisxping";可选有"xiaoyan","aisjiuxu","aisjinger","aisbabyxu"
    - ``engine_type`` (str): 引擎类型，可选值：aisound（普通效果），intp65（中文），intp65_en（英文），mtts（小语种，需配合小语种发音人使用），x（优化效果），默认为intp65


.. py:method:: TTS.translate(text)

 文字转语音

    - ``text`` (str): 转换的文本,支持中英文。
