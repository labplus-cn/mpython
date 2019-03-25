算法指令
=======================

文件规范
--------------------

符号： ``Rd`` , ``Rm`` , ``Rn`` 表示ARM寄存器R0-R7。 ``immN`` 表示具有N位宽度的即时值，如 ``imm8`` 、 ``imm3``等。
``Carry`` 表示进位条件标志。 ``not(carry)`` 表示其补码。对于多于一个寄存器参数的指令，允许其相同。
例如，以下指令将把R0的内容添加到其自身，将结果置于R0中:

* add(r0, r0, r0)

除特殊说明的情况外，算法指令将会影响条件标志。

加
--------

* add(Rdn, imm8) ``Rdn = Rdn + imm8``
* add(Rd, Rn, imm3) ``Rd = Rn + imm3``
* add(Rd, Rn, Rm) ``Rd = Rn +Rm``
* adc(Rd, Rn) ``Rd = Rd + Rn + carry``

减
-----------

* sub(Rdn, imm8) ``Rdn = Rdn - imm8``
* sub(Rd, Rn, imm3) ``Rd = Rn - imm3``
* sub(Rd, Rn, Rm) ``Rd = Rn - Rm``
* sbc(Rd, Rn) ``Rd = Rd - Rn - not(carry)``

取反
--------

* neg(Rd, Rn) ``Rd = -Rn``

乘和除
---------------------------

* mul(Rd, Rn) ``Rd = Rd * Rn``

这会产生一个溢出丢失的32位结果。结果可能将根据操作数的定义被视为有符号或无符号。

* sdiv(Rd, Rn, Rm) ``Rd = Rn / Rm``
* udiv(Rd, Rn, Rm) ``Rd = Rn / Rm``

这些函数分别执行有符号和无符号的除法。条件标志不受影响。