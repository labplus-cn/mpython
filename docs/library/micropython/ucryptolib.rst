:mod:`ucryptolib` -- 加密密码
==========================================

.. module:: ucryptolib
   :synopsis: 加密密码

类
-------

.. class:: aes

    .. classmethod:: __init__(key, mode, [IV])

        初始化密码对象，适用于加密/解密。注意：初始化后，密码对象只能用于加密或解密。不支持在encrypt()之后运行decrypt()操作，反之亦然。

        参数:

            * ``key`` 加密/解密密钥（类似字节）
            * ``mode`` :

                * ``1`` (或 ``ucryptolib.MODE_ECB`` 如果存在）电子代码簿(ECB)
                * ``2`` (ucryptolib.MODE_CBC如果存在）密码块链接(CBC)
                * ``6`` (或ucryptolib.MODE_CTR如果存在)用于计数器模式(CTR)

            * ``IV`` CBC模式的初始化矢量
            * 对于计数器模式，IV是计数器的初始值

    .. method:: encrypt(in_buf, [out_buf])

        加密in_buf。如果没有给出out_buf，则返回结果作为新分配的bytes对象。
        否则，结果被写入可变缓冲区out_buf。in_buf和out_buf也可以引用相同的可变缓冲区，在这种情况下，数据就地加密。

    .. method:: decrypt(in_buf, [out_buf])

        类似 `encrypt()` ，但是用于解密。