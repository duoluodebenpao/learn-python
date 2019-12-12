# -*- coding: utf-8 -*-
# !/usr/bin python
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/12/12 14:36
@desc:

"""


def contain_str():
    """a字符串是否包含b字符串"""
    one = "abc"
    print(one.__contains__("a"))
    print(one.__contains__("ac"))


def split_str():
    """字符串切片"""
    other = "abcdef"
    print(other[-1])
    print(other[:3])
    print(other[1:])
    print(other[::-1])


def build_str():
    """构建字符串的两种方式"""
    v1 = "aaa"
    line1 = f"ni hao a, {v1}"
    line2 = "ni hao a, {}".format(v1)
    print(line1)
    print(line2)


def practice1():
    """
    str = ’X-DSPAM-Confidence:  0.8475’
    使用find方法和字符串切片，提取出字符串中冒号后面的部分，
    然后使用float函数，将提取出来的字符串转换为浮点数
    """
    words = "X-DSPAM-Confidence:  0.8475"
    sub = words[words.find(":") + 1:]
    print(sub)

    value = float(sub.strip())
    print(value)


if __name__ == '__main__':
    split_str()
    build_str()
    practice1()
    pass
