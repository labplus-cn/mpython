逻辑&位运算指令
==============================

文件规范
--------------------

符号：除使用R0-R15的特殊指令的情况外， ``Rd, Rn`` 表示ARM寄存器R0-R7。 ``Rn<a-b>`` 表示内容介于 ``a <= contents <= b`` 范围的ARM寄存器。
对于有两个寄存器参数的指令，允许二者相同。例如，无论初始内容如何，以下指令都将把R0归零（Python  ``R0 ^= R0`` ）。

* eor(r0, r0)

除特殊说明外，这些指令会影响条件标志。

逻辑指令
--------------------

* and\_(Rd, Rn) ``Rd &= Rn``
* orr(Rd, Rn) ``Rd |= Rn``
* eor(Rd, Rn) ``Rd ^= Rn``
* mvn(Rd, Rn) ``Rd = Rn ^ 0xffffffff`` i.e.  Rd = Rn的1的补码
* bic(Rd, Rn) ``Rd &= ~Rn``  bit 使用Rn中掩码清除Rd

注意：使用"and\_"而非"and"，因为"and"在Python中是保留关键字。

转换和旋转指令
-------------------------------

* lsl(Rd, Rn<0-31>) ``Rd <<= Rn``
* lsr(Rd, Rn<1-32>) ``Rd = (Rd & 0xffffffff) >> Rn`` 逻辑右移
* asr(Rd, Rn<1-32>) ``Rd >>= Rn`` 算术右移
* ror(Rd, Rn<1-31>) ``Rd = rotate_right(Rd, Rn)`` Rd右转Rn位。

三位旋转运行如下。若Rd初始就包含位 ``b31 b30..b0`` ，则旋转后将包含 ``b2 b1 b0 b31 b30..b3`` 。

特殊指令
--------------------

条件代码不受这些指令的影响。

* clz(Rd, Rn) ``Rd = count_leading_zeros(Rn)``

count_leading_zeros(Rn) 返回Rn中第一个二进制位之前的二进制零位数。

* rbit(Rd, Rn) ``Rd = bit_reverse(Rn)``

bit_reverse(Rn) 返回Rn的位反转内容。若Rn包含位 ``b31 b30..b0`` ，则Rd将设置为 ``b0 b1 b2..b31`` 。

在执行clz之前，可通过执行一次位反转来计算尾部零点。