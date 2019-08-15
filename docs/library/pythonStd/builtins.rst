:mod:`Builtin` -- 内建函数和异常
================================

此处描述了所有内置函数和异常。它们也可通过 ``builtins`` 模块获取。



函数
-------------------

.. function:: abs()

返回一个数的绝对值。实参可以是整数或浮点数。如果实参是一个复数，返回它的模。




.. function:: all()

如果 `iterable` 的所有元素为真（或迭代器为空），返回 `True` 。

等价于::

    def all(iterable):
        for element in iterable:
            if not element:
                return False
        return True

.. function:: any()

如果 `iterable` 的任一元素为真则返回 `True` 。 如果迭代器为空，返回 `False` 。

等价于::

    def any(iterable):
        for element in iterable:
            if element:
                return True
        return False

.. function:: bin()

将一个整数转变为一个前缀为“0b”的二进制字符串。

::

    >>> bin(3)
    '0b11'
    >>> bin(-10)
    '-0b1010'

.. class:: bool()

用于将给定参数转换为布尔类型，如果没有参数，返回 `False` 。

::

    >>>bool()
    False
    >>> bool(0)
    False
    >>> bool(1)
    True
    >>> bool(None)
    False


.. class:: bytearray()

返回一个新的 bytes 数组。 bytearray 类是一个可变序列，包含范围为 0 <= x < 256 的整数。

::

    >>>bytearray()
    bytearray(b'')
    >>> bytearray([1,2,3])
    bytearray(b'\x01\x02\x03')
    >>> bytearray('mpython')
    bytearray(b'mpython')
    >>>

.. class:: bytes()

bytes 函数返回一个新的 bytes 对象，该对象是一个 0 <= x < 256 区间内的整数不可变序列。它是 bytearray 的不可变版本。参见CPython文档： `bytes <https://docs.python.org/3.5/library/functions.html#bytes>`_

::

    >>>a = bytes([1,2,3,4])
    >>> a
    b'\x01\x02\x03\x04'
    >>> type(a)
    <class 'bytes'>
    >>>
    >>> a = bytes('hello')
    >>>
    >>> a
    b'hello'
    >>> type(a)
    <class 'bytes'>
    >>>

.. function:: callable()

函数用于检查一个对象是否是可调用的。如果返回 True，object 仍然可能调用失败；但如果返回 False，调用对象 object 绝对不会成功。

::

    >>>callable(0)
    False
    >>> callable("mpython")
    False
    
    >>> def add(a, b):
    ...     return a + b
    ... 
    >>> callable(add)             # 函数返回 True
    True
    >>> class A:                  # 类
    ...     def method(self):
    ...             return 0
    ... 
    >>> callable(A)               # 类返回 True
    True
    >>> a = A()
    >>> callable(a)               # 没有实现 __call__, 返回 False
    False
    >>> class B:
    ...     def __call__(self):
    ...             return 0
    ... 
    >>> callable(B)
    True
    >>> b = B()
    >>> callable(b)               # 实现 __call__, 返回 True
    True

.. function:: chr()

返回 `Unicode` 码为整数 `i` 的字符的字符串格式。

::

    >>>chr(0x30)
    '0'
    >>> chr(97) 
    'a'
    >>> chr(8364)
    '€'

.. decorator:: classmethod()

把一个方法封装成类方法。

一个类方法把类自己作为第一个实参，就像一个实例方法把实例自己作为第一个实参。请用以下习惯来声明类方法::

    class C:
        @classmethod
        def f(cls, arg1, arg2, ...): ...

@classmethod 这样的形式称为函数的 decorator。类方法的调用可以在类上进行 (例如 C.f()) 也可以在实例上进行 (例如 C().f())。 
其所属类以外的类实例会被忽略。 如果类方法在其所属类的派生类上调用，则该派生类对象会被作为隐含的第一个参数被传入。

.. function:: compile(source, filename, mode[, flags[, dont_inherit]])

将一个字符串编译为字节代码。详细内容参见CPython文档： `compile <https://docs.python.org/zh-cn/3.7/library/functions.html#compile>`_

::

    >>>str = "for i in range(0,10): print(i)" 
    >>> c = compile(str,'','exec')   # 编译为字节代码对象 
    >>> c
    <code object <module> at 0x10141e0b0, file "", line 1>
    >>> exec(c)
    0
    1
    2
    3
    4
    5
    6
    7
    8
    9
    >>> str = "3 * 4 + 5"
    >>> a = compile(str,'','eval')
    >>> eval(a)
    17

.. class:: complex([real[, imag]])

返回值为 real + imag*1j 的复数，或将字符串或数字转换为复数。如果第一个形参是字符串，则它被解释为一个复数，并且函数调用时必须没有第二个形参。第二个形参不能是字符串。每个实参都可以是任意的数值类型（包括复数）。
如果省略了 imag，则默认值为零，构造函数会像 int 和 float 一样进行数值转换。如果两个实参都省略，则返回 0j。


::

    >>>complex(1, 2)
    (1 + 2j)
    
    >>> complex(1)    # 数字
    (1 + 0j)
    
    >>> complex("1")  # 当做字符串处理
    (1 + 0j)
    
    # 注意：这个地方在"+"号两边不能有空格，也就是不能写成"1 + 2j"，应该是"1+2j"，否则会报错
    >>> complex("1+2j")
    (1 + 2j)

.. function:: delattr(obj, name)

setattr() 相关的函数。实参是一个对象和一个字符串。该字符串必须是对象的某个属性。如果对象允许，该函数将删除指定的属性。
例如 delattr(x, 'foobar') 等价于 del x.foobar 。

::

    class Coordinate:
        x = 10
        y = -5
        z = 0
    
    point1 = Coordinate() 
    
    print('x = ',point1.x)
    print('y = ',point1.y)
    print('z = ',point1.z)
    
    delattr(Coordinate, 'z')
    
    print('--删除 z 属性后--')
    print('x = ',point1.x)
    print('y = ',point1.y)
    
    # 触发错误
    print('z = ',point1.z)

----------------------------------------------------------------

.. class:: dict(**kwarg)
.. class:: dict(mapping, **kwarg)
.. class:: dict(iterable, **kwarg)

- ``**kwargs`` -- 关键字
- ``mapping`` -- 元素的容器。
- ``iterable`` -- 可迭代对象。

dict() 函数用于创建一个字典

::

    >>>dict()                        # 创建空字典
    {}
    >>> dict(a='a', b='b', t='t')     # 传入关键字
    {'a': 'a', 'b': 'b', 't': 't'}
    >>> dict(zip(['one', 'two', 'three'], [1, 2, 3]))   # 映射函数方式来构造字典
    {'three': 3, 'two': 2, 'one': 1} 
    >>> dict([('one', 1), ('two', 2), ('three', 3)])    # 可迭代对象方式来构造字典
    {'three': 3, 'two': 2, 'one': 1}
    >>>


.. function:: dir(object)

dir() 函数不带参数时，返回当前范围内的变量、方法和定义的类型列表；带参数时，返回参数的属性、方法列表。
如果参数包含方法__dir__()，该方法将被调用。如果参数不包含__dir__()，该方法将最大限度地收集参数信息。

- ``object`` -- 对象、变量、类型。


.. function:: divmod()

它将两个（非复数）数字作为实参，并在执行整数除法时返回一对商和余数。对于混合操作数类型，适用双目算术运算符的规则。
对于整数，结果和 (a // b, a % b) 一致。对于浮点数，结果是 (q, a % b) ，q 通常是 math.floor(a / b) 但可能会比 1 小。
在任何情况下， q * b + a % b 和 a 基本相等；如果 a % b 非零，它的符号和 b 一样，并且 0 <= abs(a % b) < abs(b) 。

::

    >>> divmod(7, 2)
    (3, 1)
    >>> divmod(8, 2)
    (4, 0)
    >>> divmod(8, -2)
    (-4, 0)
    >>> divmod(3, 1.3)
    (2.0, 0.4000001)

.. function:: enumerate(sequence, [start=0])

enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。

- ``sequence`` -- 一个序列、迭代器或其他支持迭代对象。
- ``start`` -- 下标起始位置。

::

    >>>seq = ['one', 'two', 'three']
    >>> for i, element in enumerate(seq):
    ...     print i, element
    ... 
    0 one
    1 two
    2 three

.. function:: eval(expression[, globals[, locals]])

eval() 函数用来执行一个字符串表达式，并返回表达式的值。

- ``expression`` -- 表达式。
- ``globals`` -- 变量作用域，全局命名空间，如果被提供，则必须是一个字典对象。
- ``locals`` -- 变量作用域，局部命名空间，如果被提供，可以是任何映射对象。


::

    >>>x = 7
    >>> eval( '3 * x' )
    21
    >>> eval('pow(2,2)')
    4
    >>> eval('2 + 2')
    4
    >>> n=81
    >>> eval("n + 4")
    85

.. function:: exec(object[, globals[, locals]])

exec 执行储存在字符串或文件中的 Python 语句，相比于 eval，exec可以执行更复杂的 Python 代码。

- ``object``：必选参数，表示需要被指定的Python代码。它必须是字符串或code对象。如果object是一个字符串，该字符串会先被解析为一组Python语句，然后在执行（除非发生语法错误）。如果object是一个code对象，那么它只是被简单的执行。
- ``globals``：可选参数，表示全局命名空间（存放全局变量），如果被提供，则必须是一个字典对象。
- ``locals``：可选参数，表示当前局部命名空间（存放局部变量），如果被提供，可以是任何映射对象。如果该参数被忽略，那么它将会取与globals相同的值。

::

    >>>exec('print("Hello World")')
    Hello World
    # 单行语句字符串
    >>> exec("print ('runoob.com')")
    runoob.com
    
    #  多行语句字符串
    >>> exec ("""for i in range(5):
    ...     print ("iter time: %d" % i)
    ... """)
    iter time: 0
    iter time: 1
    iter time: 2
    iter time: 3
    iter time: 4

.. function:: filter(function, iterable)

用于过滤序列，过滤掉不符合条件的元素，返回一个迭代器对象，如果要转换为列表，可以使用 list() 来转换

- ``function`` -- 判断函数。
- ``iterable`` -- 可迭代对象。

过滤出列表中的所有奇数::
 
    def is_odd(n):
        return n % 2 == 1
    
    tmplist = filter(is_odd, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    newlist = list(tmplist)
    print(newlist)


.. class:: float([x])

float() 函数用于将整数和字符串转换成浮点数。

::

    >>>float(1)
    1.0
    >>> float(112)
    112.0
    >>> float(-123.6)
    -123.6
    >>> float('123')     # 字符串
    123.0

.. function:: format(value[, format_spec])

格式化字符串的函数 str.format()，它增强了字符串格式化的功能。format 函数可以接受不限个参数，位置可以不按顺序。基本语法是通过 {} 和 : 来代替以前的 % 。更详细的语法,请查阅CPython `格式字符串语法 <https://docs.python.org/zh-cn/3.7/library/string.html#format-specification-mini-language>`_

::

    >>>"{} {}".format("hello", "world")    # 不设置指定位置，按默认顺序
    'hello world'
    
    >>> "{0} {1}".format("hello", "world")  # 设置指定位置
    'hello world'
    
    >>> "{1} {0} {1}".format("hello", "world")  # 设置指定位置
    'world hello world

.. class:: frozenset([iterable])

返回一个冻结的集合，冻结后集合不能再添加或删除任何元素。

- ``iterable`` -- 可迭代的对象，比如列表、字典、元组等等。


.. function:: getattr(object, name[, default])

用于返回一个对象属性值。

::

    >>>class A(object):
    ...     bar = 1
    ... 
    >>> a = A()
    >>> getattr(a, 'bar')        # 获取属性 bar 值
    1
    >>> getattr(a, 'bar2')       # 属性 bar2 不存在，触发异常
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    AttributeError: 'A' object has no attribute 'bar2'
    >>> getattr(a, 'bar2', 3)    # 属性 bar2 不存在，但设置了默认值


.. function:: globals()

globals() 函数会以字典类型返回当前位置的全部全局变量。

.. function:: hasattr(object, name)

判断对象是否包含对应的属性。

- ``object`` -- 对象。
- ``name`` -- 字符串，属性名。

::

    class Coordinate:
        x = 10
        y = -5
        z = 0
    
    point1 = Coordinate() 
    print(hasattr(point1, 'x'))
    print(hasattr(point1, 'y'))
    print(hasattr(point1, 'z'))
    print(hasattr(point1, 'no'))  # 没有该属性

输出结果::

    True
    True
    True
    False

.. function:: hash(object)

返回该对象的哈希值（如果它有的话）。哈希值是整数。它们在字典查找元素时用来快速比较字典的键。相同大小的数字变量有相同的哈希值


----------------------------------------------------------------


.. function:: help([object])

查看函数或模块用途的详细说明


.. function:: hex(x)

将整数转换为以“0x”为前缀的小写十六进制字符串。

::

    >>> hex(255)
    '0xff'
    >>> hex(-42)
    '-0x2a'

.. function:: id([object])

获取对象的内存地址。

.. function:: input([prompt])

接收一个标准输入数据，返回为 string 类型


.. class:: int([x])
.. class:: int(x,base=10)

将一个字符串或数字转换为整型。

- ``x`` -- 字符串或数字。
- ``base`` -- 进制数，默认十进制

.. function:: isinstance(object, classinfo)

如果 object 实参是 classinfo 实参的实例，或者是（直接、间接或 虚拟）子类的实例，则返回 true。
如果 object 不是给定类型的对象，函数始终返回 false。如果 classinfo 是对象类型（或多个递归元组）的元组，如果 object 是其中的任何一个的实例则返回 true。 
如果 classinfo 既不是类型，也不是类型元组或类型的递归元组，那么会触发 TypeError 异常。

.. admonition:: isinstance() 与 type() 区别

    - `type()` 不会认为子类是一种父类类型，不考虑继承关系。
    - `isinstance()` 会认为子类是一种父类类型，考虑继承关系。

    *如果要判断两个类型是否相同推荐使用 isinstance()。*


.. function:: issubclass(class, classinfo)

如果 class 是 classinfo 的子类（直接、间接或 虚拟 的），则返回 true。classinfo 可以是类对象的元组，此时 classinfo 中的每个元素都会被检查。
其他情况，会触发 TypeError 异常。

::

    class A:
        pass
    class B(A):
        pass
        
    print(issubclass(B,A))    # 返回 True

    

.. function:: iter(object[, sentinel])

用来生成迭代器。

- ``object`` -- 支持迭代的集合对象。
- ``sentinel`` -- 如果传递了第二个参数，则参数 object 必须是一个可调用的对象（如，函数），此时，iter 创建了一个迭代器对象，每次调用这个迭代器对象的__next__()方法时，都会调用 object。

::

    >>>lst = [1, 2, 3]
    >>> for i in iter(lst):
    ...     print(i)
    ... 
    1
    2
    3

.. function:: len()

返回对象（字符、列表、元组等）长度或项目个数。

::

    >>>str = "runoob"
    >>> len(str)             # 字符串长度
    6
    >>> l = [1,2,3,4,5]
    >>> len(l)               # 列表元素个数
    5

.. class:: list()

用于将元组或字符串转换为列表。

::

    aTuple = (123, 'Google', 'baidu', 'Taobao')
    list1 = list(aTuple)
    print ("列表元素 : ", list1)

    str="Hello World"
    list2=list(str)
    print ("列表元素 : ", list2)

输出结果::

    列表元素 :  [123, 'Google', 'Runoob', 'Taobao']
    列表元素 :  ['H', 'e', 'l', 'l', 'o', ' ', 'W', 'o', 'r', 'l', 'd']

.. function:: locals()

以字典类型返回当前位置的全部局部变量。

::

    >>>def runoob(arg):    # 两个局部变量：arg、z
    ...     z = 1
    ...     print (locals())
    ... 
    >>> runoob(4)
    {'z': 1, 'arg': 4}      # 返回一个名字/值对的字典
    >>>

.. function:: map(function, iterable, ...)

map() 会根据提供的函数对指定序列做映射。返回一个将 function 应用于 iterable 中每一项并输出其结果的迭代器。 
如果传入了额外的 iterable 参数，function 必须接受相同个数的实参并被应用于从所有可迭代对象中并行获取的项。 
当有多个可迭代对象时，最短的可迭代对象耗尽则整个迭代就将结束。

::

    >>>def square(x) :            # 计算平方数
    ...     return x ** 2
    ... 
    >>> map(square, [1,2,3,4,5])   # 计算列表各个元素的平方
    [1, 4, 9, 16, 25]
    >>> map(lambda x: x ** 2, [1, 2, 3, 4, 5])  # 使用 lambda 匿名函数
    [1, 4, 9, 16, 25]
    
    # 提供了两个列表，对相同位置的列表数据进行相加
    >>> map(lambda x, y: x + y, [1, 3, 5, 7, 9], [2, 4, 6, 8, 10])
    [3, 7, 11, 15, 19]


.. function:: max()

返回给定参数的最大值，参数可以为序列

::

    print ("max(80, 100, 1000) : ", max(80, 100, 1000))
    print ("max(-20, 100, 400) : ", max(-20, 100, 400))
    print ("max(-80, -20, -10) : ", max(-80, -20, -10))
    print ("max(0, 100, -400) : ", max(0, 100, -400))

输出结果::

    max(80, 100, 1000) :  1000
    max(-20, 100, 400) :  400
    max(-80, -20, -10) :  -10
    max(0, 100, -400) :  100

.. class:: memoryview()

返回给定参数的内存查看对象(Momory view)。所谓内存查看对象，是指对支持缓冲区协议的数据进行包装，在不需要复制对象基础上允许Python代码访问。

::

    >>>v = memoryview(bytearray("abcefg"))
    >>> v[1]
    98
    >>> v[-1]
    103
    >>> v[1:4]
    <memoryview>
    >>> bytes(v[1:4)
    b'bce'
    >>>


---------------------------------------------------------

.. function:: min()

返回给定参数的最小值，参数可以为序列。

::

    print ("min(80, 100, 1000) : ", min(80, 100, 1000))
    print ("min(-20, 100, 400) : ", min(-20, 100, 400))
    print ("min(-80, -20, -10) : ", min(-80, -20, -10))
    print ("min(0, 100, -400) : ", min(0, 100, -400))

输出结果::

    min(80, 100, 1000) :  80
    min(-20, 100, 400) :  -20
    min(-80, -20, -10) :  -80
    min(0, 100, -400) :  -400



.. function:: next(iterator[, default])


返回迭代器的下一个项目。通过调用 iterator 的 __next__() 方法获取下一个元素。如果迭代器耗尽，则返回给定的 default，如果没有默认值则触发 StopIteration。

::

    # 首先获得Iterator对象:
    it = iter([1, 2, 3, 4, 5])
    # 循环:
    while True:
        try:
            # 获得下一个值:
            x = next(it)
            print(x)
        except StopIteration:
            # 遇到StopIteration就退出循环
            break

.. class:: object()

.. function:: oct()

将一个整数转换成8进制字符串。

::

    >>>oct(10)
    '012'
    >>> oct(20)
    '024'
    >>> oct(15)
    '017'
    >>>

.. function:: open()

open() 方法用于打开一个文件，并返回文件对象，在对文件进行处理过程都需要使用到这个函数，如果该文件无法被打开，会抛出 OSError。
注意：使用 open() 方法一定要保证关闭文件对象，即调用 close() 方法

open() 函数常用形式是接收两个参数：文件名(file)和模式(mode)::

    open(file, mode='r')

mode 是一个可选字符串，用于指定打开文件的模式。默认值是 'r' ，这意味着它以文本模式打开并读取。其他常见模式有：写入 'w' （截断已经存在的文件）；
排它性创建 'x' ；追加写 'a' （在 一些 Unix 系统上，无论当前的文件指针在什么位置，所有 写入都会追加到文件末尾）。可用的模式有:

=========  =================================
模式        描述
'r'        读取（默认）
'w'        写入，并先截断文件
'x'        排它性创建，如果文件已存在则失败
'a'        写入，如果文件存在则在末尾追加
'a'        写入，如果文件存在则在末尾追加
'b'        二进制模式
't'        文本模式（默认）
'+'        更新磁盘文件（读取并写入）
=========  =================================

默认的模式是 'r' （打开并读取文本，同 'rt' ）。对于二进制写入， 'w+b' 模式打开并把文件截断成 0 字节； 'r+b' 则不会截断。


.. function:: ord(c)

这是 chr() 的逆函数。。它以一个字符串（Unicode 字符）作为参数,返回代表对应 Unicode 的整数。

::

    >>>ord('a')
    97
    >>> ord('€')
    8364
    >>>

.. function:: pow(x, y[, z])

返回 xy（x的y次方） 的值。

::

    print ("pow(100, 2) : ", pow(100, 2))
    print ("pow(100, -2) : ", pow(100, -2))
    print ("pow(2, 4) : ", pow(2, 4))
    print ("pow(3, 0) : ", pow(3, 0))

输出结果::

    pow(100, 2) :  10000
    pow(100, -2) :  0.0001
    pow(2, 4) :  16
    pow(3, 0) :  1

.. function:: print(*objects, sep=' ', end='\n', file=sys.stdout)

用于打印输出，最常见的一个函数。

    - ``objects`` ：复数，表示可以一次输出多个对象。输出多个对象时，需要用 , 分隔。
    - ``sep`` ：用来间隔多个对象，默认值是一个空格。
    - ``end`` ：用来设定以什么结尾。默认值是换行符 \n，我们可以换成其他字符串。
    - ``file`` ：要写入的文件对象。

::

    >>> print(1)
    1
    >>> print("Hello World")
    Hello World
    >>> a = 1
    >>> b = 'w3cschool'
    >>> print(a,b)
    1 w3cschool
    >>> print("aaa""bbb")
    aaabbb
    >>> print("aaa","bbb")
    aaa bbb
    >>>
    >>> print("www","w3cschool","cn",sep=".") # 设置间隔符
    www.w3cschool.cn


.. decorator:: property()

property() 函数的作用是在新式类中返回属性值。将 `property` 函数用作装饰器可以很方便的创建只读属性：

property 的 getter，setter 和 deleter 方法同样可以用作装饰器::

    class C(object):
        def __init__(self):
            self._x = None
    
        @property
        def x(self):
            """I'm the 'x' property."""
            return self._x
    
        @x.setter
        def x(self, value):
            self._x = value
    
        @x.deleter
        def x(self):
            del self._x


.. function:: range()

range() 函数返回的是一个可迭代对象（类型是对象），而不是列表类型， 所以打印的时候不会打印列表。

函数语法:

    - ``range(stop)``
    - ``range(start, stop[, step])``

::

    >>>range(5)
    range(0, 5)
    >>> for i in range(5):
    ...     print(i)
    ... 
    0
    1
    2
    3
    4
    >>> list(range(5))
    [0, 1, 2, 3, 4]
    >>> list(range(0))
    []
    >>>

有两个参数或三个参数的情况（第二种构造方法）::

    >>>list(range(0, 30, 5))
    [0, 5, 10, 15, 20, 25]
    >>> list(range(0, 10, 2))
    [0, 2, 4, 6, 8]
    >>> list(range(0, -10, -1))
    [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
    >>> list(range(1, 0))
    []
    >>>
    >>>


.. function:: repr()

返回包含一个对象的可打印表示形式的字符串。

::

    >>>s = 'baidu'
    >>> repr(s)
    "'baidu'"
    >>> dict = {'baidu': 'baidu.com', 'google': 'google.com'}
    >>> repr(dict)
    "{'google': 'google.com', 'baidu': 'baidu.com'}"
    >>>

.. function:: reversed(seq)

返回一个反转的迭代器。

::

    # 字符串
    seqString = 'Runoob'
    print(list(reversed(seqString)))
    
    # 元组
    seqTuple = ('R', 'u', 'n', 'o', 'o', 'b')
    print(list(reversed(seqTuple)))
    
    # range
    seqRange = range(5, 9)
    print(list(reversed(seqRange)))
    
    # 列表
    seqList = [1, 2, 4, 3, 5]
    print(list(reversed(seqList)))

输出结果::

    ['b', 'o', 'o', 'n', 'u', 'R']
    ['b', 'o', 'o', 'n', 'u', 'R']
    [8, 7, 6, 5]
    [5, 3, 4, 2, 1]


.. function:: round(x [, n])

返回浮点数x的四舍五入值。

    - ``x`` - 数字表达式。
    - ``n`` - 表示从小数点位数，其中 x 需要四舍五入，默认值为 0

::

    print ("round(70.23456) : ", round(70.23456))
    print ("round(56.659,1) : ", round(56.659,1))
    print ("round(80.264, 2) : ", round(80.264, 2))
    print ("round(100.000056, 3) : ", round(100.000056, 3))
    print ("round(-100.000056, 3) : ", round(-100.000056, 3))

输出结果::

    round(70.23456) :  70
    round(56.659,1) :  56.7
    round(80.264, 2) :  80.26
    round(100.000056, 3) :  100.0
    round(-100.000056, 3) :  -100.0

.. class:: set([iterable])

set() 函数创建一个无序不重复元素集，可进行关系测试，删除重复数据，还可以计算交集、差集、并集等。

    >>> x = set('runoob')
    >>> y = set('google')
    >>> x, y
    ({'b', 'u', 'n', 'o', 'r'}, {'e', 'l', 'g', 'o'})     # 重复的被删除
    >>> x & y         # 交集
    {'o'}
    >>> x | y         # 并集
    {'e', 'u', 'o', 'n', 'r', 'l', 'g', 'b'}
    >>> x - y         # 差集
    {'b', 'u', 'n', 'r'}
    >


------------------------------------------------


.. function:: setattr(object, name, value)

setattr() 函数对应函数 getattr()，用于设置属性值，该属性不一定是存在的。

对已存在的属性进行赋值::

    >>>class A(object):
    ...     bar = 1
    ... 
    >>> a = A()
    >>> getattr(a, 'bar')          # 获取属性 bar 值
    1
    >>> setattr(a, 'bar', 5)       # 设置属性 bar 值
    >>> a.bar
    5

如果属性不存在会创建一个新的对象属性，并对属性赋值::

    >>>class A():
    ...     name = "runoob"
    ... 
    >>> a = A()
    >>> setattr(a, "age", 28)
    >>> print(a.age)
    28
    >>>


.. class:: slice()


.. function:: sorted(iterable, *, key=None, reverse=False)

对所有可迭代的对象进行排序操作

- ``iterable`` -- 可迭代对象。
- ``key`` -- 主要是用来进行比较的元素，只有一个参数，具体的函数的参数就是取自于可迭代对象中，指定可迭代对象中的一个元素来进行排序。
- ``reverse`` -- 排序规则，reverse = True 降序 ， reverse = False 升序（默认）。

sorted 的最简单的使用方法::

    >>>sorted([5, 2, 3, 1, 4])
    [1, 2, 3, 4, 5]                      # 默认为升序

利用key进行倒序排序::

    >>>example_list = [5, 0, 6, 1, 2, 7, 3, 4]
    >>> result_list = sorted(example_list, key=lambda x: x*-1)
    >>> print(result_list)
    [7, 6, 5, 4, 3, 2, 1, 0]
    >>>

要进行反向排序，也通过传入第三个参数 reverse=True::

    >>>example_list = [5, 0, 6, 1, 2, 7, 3, 4]
    >>> sorted(example_list, reverse=True)
    [7, 6, 5, 4, 3, 2, 1, 0]

.. decorator:: staticmethod()

将方法转换为静态方法。

静态方法不会接收隐式的第一个参数。要声明一个静态方法，请使用此语法::

    class C:
        @staticmethod
        def f(arg1, arg2, ...): ...

静态方法的调用可以在类上进行 (例如 C.f()) 也可以在实例上进行 (例如 C().f())。


.. class:: str()

函数将对象转化为str对象。

::

    >>>s = 'w3cschool'
    >>> str(s)
    'W3Cschool'
    >>> dict = {'w3cschool': 'w3cschool', 'google': 'google.com'};
    >>> str(dict)
    "{'google': 'google.com', 'w3cschool': 'w3cschool.cn'}"
    >>>


.. function:: sum(iterable[, start])

::

    >>>sum([0,1,2])
    3
    >>> sum((2, 3, 4), 1) # 元组计算总和后再加 1
    10
    >>> sum([0,1,2,3,4], 2) # 列表计算总和后再加 2
    12


.. function:: super()

super() 函数是用于调用父类(超类)的一个方法。

::

    class A:
        def add(self, x):
            y = x+1
            print(y)
    class B(A):
        def add(self, x):
            super().add(x)
    b = B()
    b.add(2)  # 3

.. class:: tuple()

将列表转换为元组。

::

    >>>list1= ['Google', 'Taobao', 'Runoob', 'Baidu']
    >>> tuple1=tuple(list1)
    >>> tuple1
    ('Google', 'Taobao', 'Runoob', 'Baidu')


.. function:: type()

type() 函数如果你只有第一个参数则返回对象的类型，三个参数返回新的类型对象。

- ``type(object)``
- ``type(name, bases, dict)``

    - ``name`` -- 类的名称。
    - ``bases`` -- 基类的元组。
    - ``dict`` -- 字典，类内定义的命名空间变量。

.. Hint:: isinstance() 与 type() 区别

    - type() 不会认为子类是一种父类类型，不考虑继承关系。
    - isinstance() 会认为子类是一种父类类型，考虑继承关系。

    **如果要判断两个类型是否相同推荐使用 isinstance()。**

::

    >>> type(1)
    <type 'int'>
    >>> type('runoob')
    <type 'str'>
    >>> type([2])
    <type 'list'>
    >>> type({0:'zero'})
    <type 'dict'>
    >>> x = 1          
    >>> type( x ) == int    # 判断类型是否相等
    True
    
    # 三个参数
    >>> class X(object):
    ...     a = 1
    ...
    >>> X = type('X', (object,), dict(a=1))  # 产生一个新的类型 X
    >>> X
    <class '__main__.X'>

type() 与 isinstance()区别::

    class A:
        pass
    s
    class B(A):
        pass
    
    isinstance(A(), A)    # returns True
    type(A()) == A        # returns True
    isinstance(B(), A)    # returns True
    type(B()) == A        # returns False


.. function:: zip([iterable, ...])

zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象，这样做的好处是节约了不少的内存。

我们可以使用 list() 转换来输出列表。如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同，利用 * 号操作符，可以将元组解压为列表。

::

    >>>a = [1,2,3]
    >>> b = [4,5,6]
    >>> c = [4,5,6,7,8]
    >>> zipped = zip(a,b)     # 返回一个对象
    >>> zipped
    <zip object at 0x103abc288>
    >>> list(zipped)  # list() 转换为列表
    [(1, 4), (2, 5), (3, 6)]
    >>> list(zip(a,c))              # 元素个数与最短的列表一致
    [(1, 4), (2, 5), (3, 6)]
    
    >>> a1, a2 = zip(*zip(a,b))          # 与 zip 相反，zip(*) 可理解为解压，返回二维矩阵式
    >>> list(a1)
    [1, 2, 3]
    >>> list(a2)
    [4, 5, 6]
    >>>


异常
----------

.. exception:: AssertionError

.. exception:: AttributeError

.. exception:: Exception

.. exception:: ImportError

.. exception:: IndexError

.. exception:: KeyboardInterrupt

.. exception:: KeyError

.. exception:: MemoryError

.. exception:: NameError

.. exception:: NotImplementedError

.. _OSError:

.. exception:: OSError

    参见CPython文档： ``OSError`` . MicroPython不实现 ``errno``  属性，而是使用标准方式访问异常参数： ``exc.args[0]`` .

.. exception:: RuntimeError

.. exception:: StopIteration

.. exception:: SyntaxError

.. exception:: SystemExit

   参见CPython文档： ``SystemExit`` .

.. exception:: TypeError

    参见CPython文档： ``SystemExit`` .

.. exception:: ValueError

.. exception:: ZeroDivisionError
