:mod:`ure` -- 正则表达式
========================================

.. module:: ure
   :synopsis: 正则表达式

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `re <https://docs.python.org/3.5/library/re.html#module-re>`_

该模块实现了正则表达式操作。支持的正则表达式语法是CPython ``re`` 模块的子集（实际上是POSIX扩展正则表达式的子集）。

支持的运算符和特殊序列是:

``'.'``
   匹配任何角色。

``'[]'``
   匹配字符集。支持单个字符和范围，包括否定集（例​​如 ``[^a-c]`` ）。

``'^'``
   匹配字符串的开头。

``'$'``
   匹配字符串的结尾。

``'?'``
   匹配零个或前一个子模式之一。
   
``'*'``
   匹配前一个子模式的零个或多个。

``'+'``
   匹配前一个子模式中的一个或多个。

``'??'``
   非贪婪版本?，匹配零或一，偏好为零。

``'*?'``
   非贪婪版本*，匹配零或更多，与最短匹配的偏好。

``'+?'``
   非贪婪版本+，匹配一个或多个，与最短匹配的偏好。


``|``
   匹配此运算符的左侧或右侧子模式。

``(...)``
   分组。每个组都在捕获（它捕获的子字符串可以通过 `match.group()` 方法访问）。

``\d``
   匹配数字。相当于 ``[0-9]`` 。

``\D``
   匹配非数字。相当于 ``[^0-9]`` 。

``\s``
   匹配空白。相当于。``[ \t-\r]``

``\S``
   匹配非空白。相当于。``[^ \t-\r]``

``\w``
   匹配“单词字符”（仅限ASCII）。相当于 ``[A-Za-z0-9_]`` 。

``\W``
   匹配非“单词字符”（仅限ASCII）。相当于 ``[^A-Za-z0-9_]`` 。

``\``
   Escape character. Any other character following the backslash, except
   for those listed above, is taken literally. For example, ``\*`` is
   equivalent to literal ``*`` (not treated as the ``*`` operator).
   Note that ``\r``, ``\n``, etc. are not handled specially, and will be
   equivalent to literal letters ``r``, ``n``, etc. Due to this, it's
   not recommended to use raw Python strings (``r""``) for regular
   expressions. For example, ``r"\r\n"`` when used as the regular
   expression is equivalent to ``"rn"``. To match CR character followed
   by LF, use ``"\r\n"``.

   逃避角色。除了上面列出的那些之外，反斜杠后面的任何其他字符都是字面意思。例如，``\*`` 等同于文字 ``*``（不作为 ``*`` 运算符）。
   需要注意的是 ``\r`` ，``\n`` 等没有特殊处理，并且将相当于文字字母 ``r`` ，``n`` 等。由于这一点，不推荐使用（原始Python字符串 ``r""`` ）为正则表达式。
   例如，``r"\r\n"`` 当用作正则表达式时相当于 ``"rn"`` 。要匹配CR后跟LF的字符，请使用 ``"\r\n"`` 。

**不支持**:

* 计算重复次数 (``{m,n}``)
* 命名组 (``(?P<name>...)``)
* 非捕获组 (``(?:...)``)
* 更高级的断言 (``\b``, ``\B``)
* 特殊字符逃脱 ，例如 ``\r`` ，``\n`` 使用Python自己的转义
* 等等

示例::

    import ure

    # As ure doesn't support escapes itself, use of r"" strings is not
    # recommended.
    regex = ure.compile("[\r\n]")

    regex.split("line1\rline2\nline3\r\n")

    # Result:
    # ['line1', 'line2', 'line3', '', '']

函数
---------

.. function:: compile(regex_str)

   编译正则表达式，返回 `regex <regex>` 对象。

.. function:: match(regex_str, string)

   编译 *regex_str* 并匹配 *string* 。匹配始终从字符串中的起始位置开始。
 
.. function:: search(regex_str, string)

   Compile *regex_str* and search it in a *string*. Unlike `match`, this will search
   string for first position which matches regex (which still may be
   0 if regex is anchored).

   编译 `regex_str` 并在字符串中搜索它。与 ``match`` 此不同，这将搜索匹配正则表达式的第一个位置的字符串（如果正则表达式已锚定，则仍可能为0）。

.. data:: DEBUG

   标记值，显示有关已编译表达式的调试信息。


