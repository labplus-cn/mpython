.. _glossary:
专业术语
========

.. glossary::

    baremetal
        没有（完全成熟的）OS的系统，例如基于 :term:`MCU` 的系统。
        在裸机系统上运行时，MicroPython通过命令解释器（REPL）有效地成为面向用户的操作系统。

    board
        A PCB board. Oftentimes, the term is used to denote a particular
        model of an :term:`MCU` system. Sometimes, it is used to actually
        refer to :term:`MicroPython port` to a particular board (and then
        may also refer to "boardless" ports like
        :term:`Unix port <MicroPython Unix port>`).

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
        Also known as a "file-like object". An object which provides sequential
        read-write access to the underlying data. A stream object implements
        a corresponding interface, which consists of methods like ``read()``,
        ``write()``, ``readinto()``, ``seek()``, ``flush()``, ``close()``, etc.
        A stream is an important concept in MicroPython, many I/O objects
        implement the stream interface, and thus can be used consistently and
        interchangeably in different contexts. For more information on
        streams in MicroPython, see `uio` module.

    upip
        （字面意思为"micro pip"）。MicroPython的包管理器，灵感来自 :term:`CPython`的pip，但是更小功能也更少。
        Upip可在 :term:`Unix port <MicroPython Unix port>` 和
        :term:`baremetal` 端口上运行（提供文件系统和网络支持）。
