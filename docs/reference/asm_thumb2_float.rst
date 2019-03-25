浮点数指令
==============================

这些指令支持使用ARM浮点协同处理器（在诸如Python的平台上，此平台即配备了此处理器）。FPU有32个称为 ``s0-s31`` 的寄存器，
每个寄存器可容纳一个精度浮点。数据可通过 ``vmov`` 指令在FPU寄存器和ARM内核寄存器间传输。

注意：MicroPython不支持向汇编函数传输浮点，同样您与也不可将浮点置于 ``r0`` 中并期待合理值。解决方法有两种。
一种是使用数组，另一种是传输且/或返回整数并在代码中转化为浮点数。

文件规范
--------------------

符号： ``Sd, Sm, Sn`` 表示FPU寄存器， ``Rd, Rm, Rn`` 表示ARM核心寄存器。后者可为任何ARM核心寄存器，尽管寄存器 ``R13-R15`` 在此情况下并不适用。

算法
----------

* vadd(Sd, Sn, Sm) ``Sd = Sn + Sm``
* vsub(Sd, Sn, Sm) ``Sd = Sn - Sm``
* vneg(Sd, Sm) ``Sd = -Sm``
* vmul(Sd, Sn, Sm) ``Sd = Sn * Sm``
* vdiv(Sd, Sn, Sm) ``Sd = Sn / Sm``
* vsqrt(Sd, Sm) ``Sd = sqrt(Sm)``

寄存器可能相同： ``vmul(S0, S0, S0)`` 将执行 ``S0 = S0*S0``

在ARM和FPU寄存器间移动
---------------------------------------

* vmov(Sd, Rm) ``Sd = Rm``
* vmov(Rd, Sm) ``Rd = Sm``

FPU有一个称为FPSCR的寄存器，与ARM的核心APSR相似，储存条件代码及其他数据。以下指令提供对其的访问。

* vmrs(APSR\_nzcv, FPSCR)

将浮点N、Z、C、V标志移动到APSR N、Z、C、V标志中。

这是在诸如FPU比对之类的指令后完成的，从而使条件代码可由汇编代码进行测试。以下为该指令的一般形式。

* vmrs(Rd, FPSCR) ``Rd = FPSCR``

在FPU寄存器和内存间移动
------------------------------------

* vldr(Sd, [Rn, offset]) ``Sd = [Rn + offset]``
* vstr(Sd, [Rn, offset]) ``[Rn + offset] = Sd``

其中 ``[Rn + offset]`` 表示通过将Rn添加到偏移量获得的存储器地址。其单位为字节。由于每个浮点值占用一个32位字，因此在访问浮点数组时，偏移量须始终为4字节的倍数。

数据比对
---------------

* vcmp(Sd, Sm)

比对Sd和Sm中的值，并设定FPU N、C、Z、V标志。这之后通常有 ``vmrs(APSR_nzcv, FPSCR)`` 来启用待检测的结果。

整数和浮点间的转换
---------------------------------

* vcvt\_f32\_s32(Sd, Sm) ``Sd = float(Sm)``
* vcvt\_s32\_f32(Sd, Sm) ``Sd = int(Sm)``