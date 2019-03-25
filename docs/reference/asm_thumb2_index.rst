.. _asm_thumb2_index:

Thumb2架构的内联汇编
=========================================

本文件假定您熟悉汇编语言编程，故您应在学习教程（ :ref:`tutorial <pyboard_tutorial_assembler>`）后阅读本文件。
有关指令集的详细说明，请参阅《体系结构参考手册》。内联汇编器支持此处介绍的ARM Thumb-2指令集的一个子集。
该语法尝试尽可能接近上述ARM手册中定义的转换为Python函数调用的语法。

除非另作说明，否则指令对32位有符号整数数据进行操作。大多数支持的指令仅在寄存器 ``R0-R7`` 上运行：
若支持 ``R8-R15`` ，则作说明。从函数返回前，寄存器 ``R8-R12`` 必须恢复到其初始值。寄存器 ``R13-R15`` 分别构成链接寄存器、堆栈指针和程序计数器。

文件规范
--------------------

在可能情况下，每条指令的行为都在Python中进行介绍，例如

* add(Rd, Rn, Rm) ``Rd = Rn + Rm``

这支持在Python中演示指令的效果。在某些情况下，这并不具有可行性，因为Python不支持间接法等概念。在相关页面中介绍了在此情况下使用的虚拟程序代码。

指令分类
----------------------

以下部分详细介绍了MicroPython支持的ARM Thumb-2指令集的子集。

.. toctree::
   :maxdepth: 1
   :numbered:

   asm_thumb2_mov.rst
   asm_thumb2_ldr.rst
   asm_thumb2_str.rst
   asm_thumb2_logical_bit.rst
   asm_thumb2_arith.rst
   asm_thumb2_compare.rst
   asm_thumb2_label_branch.rst
   asm_thumb2_stack.rst
   asm_thumb2_misc.rst
   asm_thumb2_float.rst
   asm_thumb2_directives.rst

用法示例
--------------

这部分提供使用汇编程序的更多代码示例和提示。

.. toctree::
   :maxdepth: 1
   :numbered:

   asm_thumb2_hints_tips.rst

参考目录
----------

-  汇编程序教程 :ref:`Assembler Tutorial <pyboard_tutorial_assembler>`
-  `Wiki提示与技巧
   <http://wiki.micropython.org/platforms/boards/pyboard/assembler>`__
-  `uPy内联汇编源代码，
   emitinlinethumb.c <https://github.com/micropython/micropython/blob/master/py/emitinlinethumb.c>`__
-  `ARM Thumb2指令集快速参考卡 <http://infocenter.arm.com/help/topic/com.arm.doc.qrc0001l/QRC0001_UAL.pdf>`__
-  `RM0090参考指南 <http://www.google.ae/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&sqi=2&ved=0CBoQFjAA&url=http%3A%2F%2Fwww.st.com%2Fst-web-ui%2Fstatic%2Factive%2Fen%2Fresource%2Ftechnical%2Fdocument%2Freference_manual%2FDM00031020.pdf&ei=G0rSU66xFeuW0QWYwoD4CQ&usg=AFQjCNFuW6TgzE4QpahO_U7g3f3wdwecAg&sig2=iET-R0y9on_Pbflzf9aYDw&bvm=bv.71778758,bs.1,d.bGQ>`__
-  ARM v7-M 构造参考手册（在ARM网站简单注册即可获取，也可在学术网站上获取，请注意过期版本）