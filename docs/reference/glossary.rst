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
        General-purpose input/output. The simplest means to control
        electrical signals. With GPIO, user can configure hardware
        signal pin to be either input or output, and set or get
        its digital signal value (logical "0" or "1"). MicroPython
        abstracts GPIO access using :class:`machine.Pin` and :class:`machine.Signal`
        classes.

    GPIO port
        A group of :term:`GPIO` pins, usually based on hardware
        properties of these pins (e.g. controllable by the same
        register).

    MCU

        微控制器。微控制器通常比完整的计算系统具有更少的资源，但更小，更便宜并且需要更少的功率。
        MicroPython设计小巧，经过优化，足以在普通的现代微控制器上运行。

    micropython-lib
        MicroPython is (usually) distributed as a single executable/binary
        file with just few builtin modules. There is no extensive standard
        library comparable with :term:`CPython`. Instead, there is a related, but
        separate project
        `micropython-lib <https://github.com/micropython/micropython-lib>`_
        which provides implementations for many modules from CPython's
        standard library. However, large subset of these modules require
        POSIX-like environment (Linux, MacOS, Windows may be partially
        supported), and thus would work or make sense only with
        `MicroPython Unix port`. Some subset of modules is however usable
        for `baremetal` ports too.

        Unlike monolithic :term:`CPython` stdlib, micropython-lib modules
        are intended to be installed individually - either using manual
        copying or using :term:`upip`.

    MicroPython port
        MicroPython supports different :term:`boards <board>`, RTOSes,
        and OSes, and can be relatively easily adapted to new systems.
        MicroPython with support for a particular system is called a
        "port" to that system. Different ports may have widely different
        functionality. This documentation is intended to be a reference
        of the generic APIs available across different ports ("MicroPython
        core"). Note that some ports may still omit some APIs described
        here (e.g. due to resource constraints). Any such differences,
        and port-specific extensions beyond MicroPython core functionality,
        would be described in the separate port-specific documentation.

    MicroPython Unix port
        Unix port is one of the major :term:`MicroPython ports <MicroPython port>`.
        It is intended to run on POSIX-compatible operating systems, like
        Linux, MacOS, FreeBSD, Solaris, etc. It also serves as the basis
        of Windows port. The importance of Unix port lies in the fact
        that while there are many different :term:`boards <board>`, so
        two random users unlikely have the same board, almost all modern
        OSes have some level of POSIX compatibility, so Unix port serves
        as a kind of "common ground" to which any user can have access.
        So, Unix port is used for initial prototyping, different kinds
        of testing, development of machine-independent features, etc.
        All users of MicroPython, even those which are interested only
        in running MicroPython on :term:`MCU` systems, are recommended
        to be familiar with Unix (or Windows) port, as it is important
        productivity helper and a part of normal MicroPython workflow.

    port
        Either :term:`MicroPython port` or :term:`GPIO port`. If not clear
        from context, it's recommended to use full specification like one
        of the above.

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
        (Literally, "micro pip"). A package manage for MicroPython, inspired
        by :term:`CPython`'s pip, but much smaller and with reduced functionality.
        upip runs both on :term:`Unix port <MicroPython Unix port>` and on
        :term:`baremetal` ports (those which offer filesystem and networking
        support).
