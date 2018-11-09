随机数
======================================

有时我们需要做些随机行为或生产随机数。这时你可以使用 :ref:`random<random>` 模块。

例如，以下是如何在oled显示屏上随机显示名称::

  from mpython import *
  import random

  names = ["Mary", "Yolanda", "Damien", "Alia", "Kushal", "Mei Xiu", "Zoltan" ]


  display.DispChar(random.choice(names),40,20)
  display.show()
  display.fill(0)

列表（names）包含七个定义为字符串的名称。random.choice方法将names列表作为参数并返回随机选择的项目。

你能修改列表以包含你自己的名字吗？

随机显示数字
---------

随机数非常有用。它们在游戏中很常见。为什么我们还有骰子？

MicroPython附带了几个有用的随机数方法。这是如何制作一个简单的骰子::

  from mpython import *
  import random

  display.DispChar(str(random.randint(1,6)),60,20)
  display.show()
  display.fill(0)

.. Note::

  每次重启掌控板时，它都会显示一个介于1和6之间的数字。``randint()`` 返回的是整形，我们需要使用 ``str()`` 将整形转为字符串(例如，6 -> "6")。
  ``display.DispChar()`` 将随机数写入oled。

假如你想设置随机范围或递增基数，你可以使用random.randrange()::

  from mpython import *
  import random

  display.DispChar(str(random.randrange(0,10,2)),60,20)
  display.show()
  display.fill(0)

.. Note::

  random.randrange(start, end, step)。``start`` 为随机数开始值，``end`` 为随机数结束值，step为递增基数。
  以上例子是随机显示(0,10)范围的偶数。

有时您需要带小数点的数字。你可以使用 ``random.random`` 方法生成0.0到1.0的随机浮点数。如果你需要较大的随机浮点数加的结果``random.uniform`` ::

  from mpython import *
  import random

  display.DispChar(str(random.random()),30,10)
  display.DispChar(str(random.uniform(1,20)),30,30)
  display.show()
  display.fill(0)

随机种子
-------

MicroPython中的随机数其实是一个稳定算法得出的稳定结果序列，而不是一个随机序列。 seed就是这个算法开始计算的第一个值。
所以就会出现只要seed是一样的，那么后续所有“随机”结果和顺序也都完全一致。

指定随机数种子，通常和其他随机数生成函数搭配使用

有时您希望具有可重复的随机行为：可重现的随机源。这就像说每次掷骰子时你需要相同的五个随机值。

示例::

  import random
  from mpython import *


  for i in range(0,2):
    random.seed(8)

    for j in range(8):
      display.DispChar(str(random.randint(1,10)),j*16,i*16)
      display.show()
      print(random.randint(1,10))

  display.fill(0)


