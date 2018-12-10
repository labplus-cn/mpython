:mod:`btree` -- 简单的 BTree 数据库
=====================================

.. module:: btree
   :synopsis: 简单的 BTree 数据库

 ``btree`` 模块使用外部储存（磁盘文件，或在一般情况下为随机访问流）实现简单的键值数据库。
 键排序储存在数据库中，除对单个键值的有效检索外，数据库还支持高效的有序范围扫描（使用给定范围内的键来检索值）。
 在应用程序接口方面，B树数据库尽可能以与标准 `dict` 类型工作方式相似的方式运行，一个明显区别是键和值都须
 为 `bytes` 对象（因此，若您想要储存其他类型的对象，需首先将之序列化为 `bytes` ）。

该模块基于著名的BerkelyDB 库的1.xx版本。

示例::

    import btree

    # First, we need to open a stream which holds a database 首先，我们需要打开一个包含数据库的流
    # This is usually a file, but can be in-memory database 这通常是一个文件，也可能是一个内存数据库
    # using uio.BytesIO, a raw flash partition, etc. 使用uio.BytesIO，一个原始闪分区
    # Oftentimes, you want to create a database file if it doesn't
    # exist and open if it exists. Idiom below takes care of this.
    # 通常，若不存在数据库文件，则您需要创建一个；若已存在，则只需打开。以下的习语考虑到了这一点。
    # DO NOT open database with "a+b" access mode. 请勿打开带有"a+b"访问编码的数据库。

    try:
        f = open("mydb", "r+b")
    except OSError:
        f = open("mydb", "w+b")

    # Now open a database itself 现在打开一个数据库
    db = btree.open(f)

    # The keys you add will be sorted internally in the database 您添加的键将在数据库进行内部排序
    db[b"3"] = b"three"
    db[b"1"] = b"one"
    db[b"2"] = b"two"

    # Assume that any changes are cached in memory unless
    # explicitly flushed (or database closed). Flush database
    # at the end of each "transaction". 
    # 除非显式刷新（或数据库关闭），否则假设任何更改都缓存在内存中。在每次“处理”结束时都刷新数据库。
    db.flush()

    # Prints b'two'
    print(db[b"2"])

    # Iterate over sorted keys in the database, starting from b"2"
    # until the end of the database, returning only values. 
    # 在数据库中对已排序的键进行迭代，从b“2”开始到数据库结束，只返回值。
    # Mind that arguments passed to values() method are *key* values. 注意传递给values()方法的参数为*key*值
    # Prints:
    #   b'two'
    #   b'three'
    for word in db.values(b"2"):
        print(word)

    del db[b"2"]

    # No longer true, prints False 不正确，打印False
    print(b"2" in db)

    # Prints:
    #  b"1"
    #  b"3"
    for key in db:
        print(key)

    db.close()

    # Don't forget to close the underlying stream! 请一定记得关闭基础流！
    f.close()


函数
---------

.. function:: open(stream, \*, flags=0, cachesize=0, pagesize=0, minkeypage=0)

   从随机存取的 ``stream``（类似一个打开的文件）中打开一个数据库。所有其他的参数都是可选的，且都只为关键字，并允许对数据库操作的高级参数进行调整（大多数用户并不会需要这个）:

   * *flags* - 当前未使用的
   * *cachesize* - 以字节计的建议最大内存缓存大小。对于一个由充足内存的板而言，使用更大值或许可以提高性能。该值只是推荐值，若该值设置过低，则模块可能会占用更多内存。
   * *pagesize* - B树中用于节点的页面大小。可接受范围为512-65536。若为0，则会使用基础I/O块的大小（内存使用和性能之间的最佳协调）。
   * *minkeypage* - 每个页面存储的键的最小数量。默认值为0等于2。

   返回一个B树对象，该对象实现一个字典协议（方法集）和下述的一些附加方法。

方法
-------

.. method:: btree.close()

   关闭数据库。处理结束时关闭数据库是强制性的，因为某些未写入的数据可能仍留在缓存中。注意：这并不会关闭随数据库打开的基础流，基础流应单独关闭（这也是强制性的，以确保从缓冲区中刷新的数据进入底层储存）。

.. method:: btree.flush()

   将缓存中的任何数据刷新到底层流。

.. method:: btree.__getitem__(key)
            btree.get(key, default=None)
            btree.__setitem__(key, val)
            btree.__detitem__(key)
            btree.__contains__(key)

   标准字典方法。

.. method:: btree.__iter__()

   B树对象可被直接迭代（与字典相似）以按顺序访问所有键。

.. method:: btree.keys([start_key, [end_key, [flags]]])
            btree.values([start_key, [end_key, [flags]]])
            btree.items([start_key, [end_key, [flags]]])

   这些方法类似于标准字典方法，但也可使用可选参数来迭代一个键子范围，而不是整个数据库。
   注意：这三种方法中， *start_key* 和 *end_key* 参数都代表键值。例如， ``values()`` 方法将迭代与给定键范围对应的值。
   无 *start_key* 值即意为“从首个键”，无 *end_key* 值或其值为None则意为“直到数据库结束”。
   默认情况下，范围包括 *start_key* ，而不包括 *end_key* ，您可以通过传递 `btree.INCL` 的标记来将 *end_key* 包括在迭代中。
   您可以通过传递 `btree.DESC` 的标记来按照下行键方向进行迭代。标记值可同为ORed。

常量
---------

.. data:: INCL

    `keys()`, `values()`, `items()` 方法的标记, 指定扫描应该包含结束键。

.. data:: DESC

    `keys()`, `values()`, `items()` 方法的标记, 指定扫描应按照键的下行方向进行。