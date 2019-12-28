# -*- coding: utf-8 -*-
# !/usr/bin python
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/12/28 11:04
@desc:
命名空间是从名称到对象的映射，大部分的命名空间都是通过python字典来实现的；
命名空间提供了在项目中避免名字冲突的一种方法，各个命名空间是独立的，没有任何关系的，所以一个命名空间中不能有重名，但不同的命名空间是可以崇明而没有任何影响；

一般有三种命名空间：
内置名称（built-in names）， Python 语言内置的名称，比如函数名 abs、char 和异常名称 BaseException、Exception 等等。
全局名称（global names），模块中定义的名称，记录了模块的变量，包括函数、类、其它导入的模块、模块级的变量和常量。
局部名称（local names），函数中定义的名称，记录了函数的变量，包括函数的参数和局部定义的变量。（类中定义的也是）

命名空间查找顺序:
假设我们要使用变量 runoob，则 Python 的查找顺序为：局部的命名空间去 -> 全局命名空间 -> 内置命名空间。
如果找不到变量 runoob，它将放弃查找并引发一个 NameError 异常:



变量的作用域决定了在哪一部分程序可以访问哪个特定的变量名称。Python的作用域一共有4种，分别是：
有四种作用域：
L（Local）：最内层，包含局部变量，比如一个函数/方法内部。
E（Enclosing）：包含了非局部(non-local)也非全局(non-global)的变量。比如两个嵌套函数，一个函数（或类） A 里面又包含了一个函数 B ，那么对于 B 中的名称来说 A 中的作用域就为 nonlocal。
G（Global）：当前脚本的最外层，比如当前模块的全局变量。
B（Built-in）： 包含了内建的变量/关键字等。，最后被搜索
规则顺序： L –> E –> G –>gt; B。
在局部找不到，便会去局部外的局部找（例如闭包），再找不到就会去全局找，再者去内置中找。

"""

num = 1

def alter_global():
    """
    修改全局变量
    :return:
    """
    global num  # 需要使用 global 关键字声明
    print(num)
    num = 123
    print(num)

def alter_local():
    """
    修改局部变量
    :return:
    """
    num = 10
    def inner():
        nonlocal num   # nonlocal关键字声明
        num = 100
        print(num)
    inner()
    print(num)

pass
