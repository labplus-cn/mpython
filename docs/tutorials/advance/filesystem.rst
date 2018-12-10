储存
-------

有时你需要存储有用的信息。这些信息存储为数据：信息的表示（当存储在计算机上时以数字形式）。
如果您将数据存储在计算机上，即使您关闭再打开设备，它也应该保留。

microPython位允许您使用非常简单的文件系统来完成此操作。

什么是文件系统？

它是一种以持久方式存储和组织数据的方法 - 存储在文件系统中的任何数据都应该在设备重启后继续存在。
顾名思义，存储在文件系统中的数据被组织成文件。

.. image:: /images/tutorials/files.jpg

计算机文件是存储在文件系统上的命名数字资源。这些资源包含有用的信息作为数据。
这正是纸质文件的工作原理。它是一种包含有用信息的命名容器。通常，纸质和数字文件都会被命名以指示它们包含的内容。
在计算机上，通常使用 ``.xxx`` 后缀结束文件。通常，表示使用什么类型的数据来表示信息。
例如， ``.txt`` 表示文本文件， `` .jpg`` JPEG图像和 ``.mp3`` 编码为MP3的声音数据。

某些文件系统（例如笔记本电脑或PC上的文件系统）允许您将文件组织到目录中：命名容器将相关文件和子目录组合在一起。
但是，MicroPython提供的文件系统是一个平面文件系统。平面文件系统没有目录 - 所有文件都只存储在同一个地方。

Python编程语言包含易于使用且功能强大的方式来使用计算机的文件系统。mPython上的MicroPython实现了这些功能的有用子集
，使其易于在设备上读取和写入文件，同时还提供与其他Python版本的一致性。


打开文件
+++++++++++

有关更多的open()使用，可查阅 :term:`CPython` 文档:`open() <https://docs.python.org/3.5/library/functions.html#open>`_。

通过该 ``open`` 功能实现在文件系统上读取和写入文件。打开文件后，您可以使用它直到关闭它（类似于我们使用纸质文件的方式）。

确保这一点的最好方法是使用如下with语句::

    with open('story.txt') as my_file:
        content = my_file.read()
    print(content)

该 ``with`` 语句使用该 ``open`` 函数打开文件并将其分配给对象。在上面的示例中，该 ``open`` 函数打开调用的文件 ``story.txt``（显然是包含某种故事的文本文件）。
调用用于表示Python代码中的文件的对象`` my_file``。随后，在 ``with`` 语句下面缩进的代码块中，该 ``my_file`` 对象用于 ``read()`` 文件的内容并将其分配给 ``content`` 对象。

这是重要的一点，包含该 ``print`` 语句的下一行不是缩进的。与 ``with`` 语句关联的代码块只是读取文件的单行。
一旦与该 ``with`` 语句关联的代码块关闭，Python（和MicroPython）将自动为您关闭该文件。
这称为上下文处理，该 ``open`` 函数创建的对象是文件的上下文处理程序。

简而言之，与文件交互的范围由与with打开文件的语句关联的代码块定义。

困惑？

不要。我只是说你的代码应该是这样的::

    with open('some_file') as some_object:
        # 在这段代码块中完成文件的读写

    # 当块完成时，然后使用MicroPython
    # 自动为您关闭文件。

就像纸质文件一样，打开文件有两个原因：读取其内容（如上所示）或向文件写入内容。
默认模式是读取文件。如果要写入文件，则需要 ``open`` 按以下方式告诉函数::

    with open('hello.txt', 'w') as my_file:
        my_file.write("Hello, World!")

请注意，该 ``'w'`` 参数用于将 ``my_file`` 对象设置为写入模式。
您还可以传递一个 ``'r'`` 参数来将文件对象设置为读取模式，但由于这是默认设置，因此通常会将其保留。

将数据写入文件是通过（您猜对了） ``write`` 方法完成的，该方法将您要写入文件的字符串作为参数。
在上面的示例中，我将文本“Hello，World！”写入名为“hello.txt”的文件中。


.. note::

    当您打开文件并写入时（可能在文件处于打开状态时多次），如果文件已经存在，您将编写文件内容。

    如果要将数据附加到文件，则应首先将其读取，将内容存储在某处，关闭它，将数据附加到内容中，然后打开它以使用修改后的内容再次写入。

    虽然在MicroPython中就是这种情况，但“普通”Python可以打开文件以“附加”模式写入。我们不能在micro：bit上执行此操作是文件系统的简单实现的结果。

OS 
++++++

除了读写文件外，Python还可以操作它们。您当然需要知道文件系统中的文件，有时您也需要删除它们。

在常规计算机上，操作系统（如Windows，OSX或Linux）的角色是代表Python管理它。
Python中通过一个名为的模块提供了这样的功能os。
由于MicroPython 是操作系统，我们决定在os 模块中保持适当的功能以保持一致性，这样当您在笔记本电脑或Raspberry Pi等设备上使用“常规”Python时，您就会知道在哪里可以找到它们。

基本上，您可以执行与文件系统相关的三个操作：列出文件，删除文件并询问文件的大小。

要列出文件系统上的文件，请使用该listdir功能。它返回一个字符串列表，指示文件系统上文件的文件名::

    import os
    my_files = os.listdir()

要删除文件，请使用该remove功能。它需要一个字符串来表示要删除的文件的文件名作为参数，如下所示::

    import os
    os.remove('filename.txt')

最后，有时在读取文件之前了解文件的大小是有用的。要实现这个size功能。
与remove函数一样，它采用一个字符串来表示您想知道其大小的文件的文件名。
它返回一个整数（整数），告诉你文件占用的字节数::

    import os
    file_size = os.size('a_big_file.txt')


主程序 main.py
++++++++++++++

boot.py和main.py，这两个文件在启动时由MicroPython专门处理。 首先执行boot.py脚本（如果存在），然后在完成后执行main.py脚本。

此外，如果您将其他Python文件复制到文件系统上，那么 import就像其他任何Python模块一样。
例如，如果您有一个 ``hello.py`` 包含以下简单代码的文件::

    def say_hello(name="World"):
        return "Hello, {}!".format(name)

你可以导入并使用这样的 ``say_hello`` 函数::

    from mpython import *
    from hello import say_hello

    oled.DispChar(say_hello(),0,0)
    oled.show()

.. note::

    如果除了MicroPython运行时之外还在设备上刷过了一个脚本，那么MicroPython将忽略main.py并运行您的嵌入式脚本。

    要仅刷新MicroPython运行时，只需确保您在编辑器中编写的脚本中包含零个字符。一旦闪存，您就可以复制main.py文件。

.. footer:: The image of paper files is used under a Creative Commons License and is available here: https://www.flickr.com/photos/jenkim/2270085025
