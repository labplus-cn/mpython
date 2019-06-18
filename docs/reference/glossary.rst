.. _glossary:
专业术语
========

.. glossary::

    baremetal
        没有（完全成熟的）OS的系统，例如基于 :term:`MCU` 的系统。
        在裸机系统上运行时，MicroPython通过命令解释器（REPL）有效地成为面向用户的操作系统。

    board
        PCB板。通常，该术语用于表示 :term:`MCU` 系统的特定模型。有时，它用于实际将 :term:`MicroPython port` 引用到特定板
        (然后也可能指 :term:`Unix port <MicroPython Unix port>`的 boardless ports)。
   
    callee-owned tuple
        由一些内置函数/方法返回的元组，包含在有限时间内有效的数据，通常直到下一次调用相同的函数（或一组相关函数）。
        下次调用后，可以更改元组中的数据。这导致对被调用者拥有的元组的使用进行以下限制 - 无法存储对它们的引用。
        唯一有效的操作是从中提取值（包括制作副本）。Callee拥有的元组是特定于MicroPython的构造（在通用Python语言中不可用），用于内存分配优化。
        这个想法是被调用者拥有的元组被分配一次并存储在被调用方。后续调用不需要分配，允许在无法分配时返回多个值（例如，在中断上下文中）或不可取（因为分配固有地导致内存碎片）。请注意，被调用者拥有的元组实际上是可变的元组，这使得Python的规则例外，即元组是不可变的。（可能有趣的是，为什么元组被用于这样的目的，而不是可变列表 - 原因是列表也可以从用户应用程序端变化，因此用户可以对被调用者拥有的列表执行操作不期望并且可能导致问题;元组受到保护。）而不是可变列表 - 原因是列表也可以从用户应用程序端变化，因此用户可以对被调用者拥有的列表执行操作，被调用者不期望并且可能导致问题; 一个元组受到保护。）而不是可变列表 - 原因是列表也可以从用户应用程序端变化，因此用户可以对被调用者拥有的列表执行操作，被调用者不期望并且可能导致问题; 一个元组受到保护。）


    CPython
        CPython是Python编程语言的参考实现，也是大多数人运行的最着名的编程语言。
        然而，它是众多实现中的一种（其中包括Jython，IronPython，PyPy等等，包括MicroPython）。
        由于没有正式的Python语言规范，只有CPython文档，因此在Python语言和CPython的特定实现之间划一条线并不总是很容易。
        然而，这为其他实现留下了更多的自由。例如，MicroPython做了很多与CPython不同的事情，同时仍然渴望成为Python语言实现。

    GPIO
        通用输入/输出。控制电信号的最简单方法。通过GPIO，用户可将硬件信号配置为输入或输出，
        并设置或获取其数字信号值（逻辑"0"或"1"）。MicroPython使用 :class:`machine.Pin`
        和 :class:`machine.Signal` 类提取访问GPIO权限。

    GPIO port
         一组 :term:`GPIO` 引脚，通常基于引脚的硬件特性（例如：可通过同一寄存器控制）。

    interned string

        由其（唯一）标识引用的字符串，而不是其地址。因此，可以通过标识符快速比较实习字符串，而不是按内容进行比较。
        实习字符串的缺点是实习操作需要时间（与现有实习字符串的数量成比例，即随时间变得越来越慢），并且用于实习字符串的空间不可回收。
        字符串实习由MicroPython编译器和runtimer自动完成，当实现需要它时（例如，函数关键字参数由实习字符串id表示）或认为是有益的（例如，对于足够短的字符串，有机会重复，因此实习）他们会在副本上节省内存）。
        由于上述缺点，大多数字符串和I / O操作不产生实际字符串。

    MCU

        微控制器。与完整的计算系统相比，微控制器的资源通常要少得多，但是也更小、价格更低且耗电更少。
        MicroPython的设计小而优化，可在一般的现代微控制器上运行。

    micropython-lib
        MicroPython（通常）作为一个单独的可执行/二进制文件分配，仅有很少的内置模块。
        与 :term:`CPython`相比，MicroPython无扩展标准库。但有一个相关但独立的项目
        `micropython-lib <https://github.com/micropython/micropython-lib>`_
        ，该项目提供许多来自标准库中模块的实现。但是，这些模块的较大子集需要类似POSIX的环境
        （部分支持Linux、MacOS、Windows），因此仅可在MicroPython Unix端口上运行。
        模块的某些子集在baremetal端口上也可用。

        与 :term:`CPython` 单片标准库不同，micropython-lib模块设计为手动复制或
        使用 :term:`upip`来单独安装。

    MicroPython port
        MicroPython支持不同的板（ :term:`boards <board>`），RTOS和OS可相对容易地适应新系统。
        支持特定系统的MicroPython被称为该系统的"端口"。不同端口的功能特性相差极大。此文档旨在为在
        不同端口（"MicroPython核心"）上可用的通用API提供参考。注意：一些端口可能删除此处所述的API
        （由于资源限制）。这类区别、以及超出MicroPython核心功能的特定于端口的扩展都将在但单独的、
        特定于端口的文件中进行介绍。

    MicroPython Unix port
        Unix端口是MicroPython（ :term:`MicroPython ports <MicroPython port>`）的主要端口之一。
        其设计为在与POSIX兼容的操作系统上运行，如Linux、MacOS、FreeBSD、Solaris等。
        该端口还可作为Windows端口的基础。端口的重要性在于在有许多不同板（ :term:`boards <board>`）时，
        任意两个用户不可能使用相同的板，几乎所有的现代操作系统都具有一定程度的POSIX兼容性，
        此时Unix端口可作为一种所有用户都可访问的"共同基础"。因此，Unix端口用于初始原型、不同种类
        的测试、开发独立于机器的特性等。我们建议所有MicroPython用户（甚至包括仅在 :term:`MCU` 系统中
        运行MicroPython的用户）都了解一下Unix（或Windows）端口，因为该端口可提高工作效率，且为MicroPython工作流的一部分。

    port
        :term:`MicroPython port` 或 :term:`GPIO port`。若您尚未理解上文，建议您使用如上述示例的完整规格。

    stream

        也称为“类文件对象”。一种对象，提供对底层数据的顺序读写访问。
        甲流对象实现对应的接口，它由类似的方法 ``read()`` ， ``write()`` ，``readinto()`` ，``seek()`` ，``flush()`` ，``close()`` ，等等流是在MicroPython一个重要的概念，
        许多I / O对象实现了流接口，因此可以在不同的被一致和互换地使用上下文。有关MicroPython中的流的更多信息，请参阅 :mod:`uio` 模块。 
     

    upip
        (字面意思为"micro pip")。MicroPython的包管理器，灵感来自 :term:`CPython` 的pip，但是更小功能也更少。
        upip可在 :term:`Unix port <MicroPython Unix port>` 和 :term:`baremetal` 端口上运行（提供文件系统和网络支持）。
      