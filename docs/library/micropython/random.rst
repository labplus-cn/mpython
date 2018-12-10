.. _random:
:mod:`random` --- 生成随机数
=========================================

该模块基于Python标准库中的 ``random`` 模块。它包含用于生成随机数的函数。

函数
---------

.. method:: random.randint(start, end)

随机生成一个start到end之间的整数。

  - ``start``:指定范围内的开始值，包含在范围内。
  - ``stop``：指定范围内的结束值，包含在范围内。

示例::

  >>> import random
  >>> print(random.randint(1, 4))
  4
  >>> print(random.randint(1, 4))
  2

.. method:: random.random()

随机生成一个0到1之间的浮点数。 

示例::

  >>> print(random.random())
  0.7111824
  >>> print(random.random())
  0.3168149


.. method:: random.unifrom(start, end)

随机生成start到end之间的浮点数。

  - ``start``：指定范围内的开始值，包含在范围内。
  - ``stop``：指定范围内的结束值，包含在范围内。

示例::

  >>> print(random.uniform(2, 4))
  2.021441
  >>> print(random.uniform(2, 4))
  3.998012


.. method:: random.getrandbits(size)

随机生成 0 到 size 个位二进制数范围内的正整数。 

  - ``size`` :位大小。例如，size = 4，那么便是从 0 到0b1111中随机一个正整数；size = 8，那么便是从 0 到 0b11111111中随机一个正整数。

示例::

  >>> print( random.getrandbits(1))  #1位二进制位，范围为0~1（十进制：0~1）
  1
  >>> print(random.getrandbits(1))
  0
  >>> print(random.getrandbits(8))  #8位二进制位，范围为0000 0000~1111 11111（十进制：0~255）
  224
  >>> print(random.getrandbits(8))
  155

.. method:: random.randrange(start, end, step)

随机生成start到end并且递增为 step 的范围内的正整数。例如，randrange(0, 8, 2)中，随机生成的数为0、2、4、6中任一个。

  - ``start``：指定范围内的开始值，包含在范围内
  - ``stop``：指定范围内的结束值，包含在范围内
  - ``step``：递增基数

示例::

  >>> print(random.randrange(2, 8, 2))
  4
  >>> print(random.randrange(2, 8, 2))
  6
  >>> print(random.randrange(2, 8, 2))
  2

.. method:: random.seed(sed)

指定随机数种子，通常和其他随机数生成函数搭配使用。

.. 注意::

   MicroPython中的随机数其实是一个稳定算法得出的稳定结果序列，而不是一个随机序列。
   seed就是这个算法开始计算的第一个值。所以就会出现只要seed是一样的，那么后续所有“随机”结果和顺序也都完全一致。

示例::

  import random

  for j in range(0, 2):
    random.seed(13)  #指定随机数种子
    for i in range(0, 10):  #生成0到10范围内的随机序列
      print(random.randint(1, 10))
    print("end")

运行结果::

  5
  2
  3
  2
  3
  4
  2
  5
  8
  2
  end
  5
  2
  3
  2
  3
  4
  2
  5
  8
  2
  end

从上面可以看到生成两个随机数列表是一样的，你也可以多生成几个随机数列表看看。
另外当我们不用seed(sed)函数时，相当于没有指定随机种子，这样就是随机生成的。

.. method:: random.choice(obj)

函数说明：随机生成对象obj中的元数。

  - ``obj``：元数列表

示例::

  >>> print(random.choice("mPython"))
  m
  >>> print(random.choice("mPython"))
  n
  >>> print(random.choice([0, 2, 4, 3]))
  3
  >>> print(random.choice([0, 2, 4, 3]))
  3
  >>> print(random.choice([0, 2, 4, 3]))
  2