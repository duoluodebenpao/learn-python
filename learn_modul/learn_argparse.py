#!/usr/bin/env python
# encoding: utf-8
"""
@author: fzj 
@license: (C) Copyright 2013-2017
@time: 2019/10/9 16:17
@desc:
"""

"""
如果要以命令行执行，那你需要解析一个命令行参数解析的模块来帮你做这个苦力活。
Python 本身就提供了三个命令行参数解析模块，我这里罗列一下它们的大致情况供你了解。

getopt，只能简单的处理命令行参数
optparse，功能强大，易于使用，可以方便地生成标准的、符合Unix/Posix 规范的命令行说明。
argparse，使其更加容易的编写用户友好的命令行接口。它所需的程序进程了参数定义，argparse将更好的解析sys.argv。同时argparse模块还能自动生成帮助及用户输入错误参数时的提示信息。

很多初学者可能会使用getopt，上手简单功能也简单。比如说optget无法解析一个参数多个值的情况，如 --file file1 file2 file3，而 optparse 实际上我没有用过，但是考虑到它在Python2.7后就已经弃用不再维护，我们通常也不会使用它。
接下来只剩下 argparse 这一神器，它几乎能满足我对命令解析器的所有需求。它支持解析一参数多值，可以自动生成help命令和帮助文档，支持子解析器，支持限制参数取值范围等等功能。


ArgumentParser类创建时的参数如下：

prog - 程序的名字（默认：sys.argv[0]）
usage - 描述程序用法的字符串（默认：从解析器的参数生成）
description - 参数帮助信息之前的文本（默认：空）
epilog - 参数帮助信息之后的文本（默认：空）
parents - ArgumentParser 对象的一个列表，这些对象的参数应该包括进去
formatter_class - 定制化帮助信息的类
prefix_chars - 可选参数的前缀字符集（默认：‘-‘）
fromfile_prefix_chars - 额外的参数应该读取的文件的前缀字符集（默认：None）
argument_default - 参数的全局默认值（默认：None）
conflict_handler - 解决冲突的可选参数的策略（通常没有必要）
add_help - 给解析器添加-h/–help 选项（默认：True）
add_argument函数的参数如下：

name or flags - 选项字符串的名字或者列表，例如foo 或者-f, –foo。
action - 在命令行遇到该参数时采取的基本动作类型。
nargs - 应该读取的命令行参数数目。
const - 某些action和nargs选项要求的常数值。
default - 如果命令行中没有出现该参数时的默认值。
type - 命令行参数应该被转换成的类型。
choices - 参数可允许的值的一个容器。
required - 该命令行选项是否可以省略（只针对可选参数）。
help - 参数的简短描述。
metavar - 参数在帮助信息中的名字。
dest - 给parse_args()返回的对象要添加的属性名称。



"""

import argparse


def cmd():
    args = argparse.ArgumentParser(description='Personal Information ', epilog='Information end ')
    # 必写属性,第一位
    args.add_argument("name", type=str, help="Your name")
    # 必写属性,第二位
    args.add_argument("birth", type=str, help="birthday")
    # 可选属性,默认为None
    args.add_argument("-r", '--race', type=str, dest="race", help=u"民族")
    # 可选属性,默认为0,范围必须在0~150
    args.add_argument("-a", "--age", type=int, dest="age", help="Your age", default=0, choices=range(150))
    # 可选属性,默认为male
    args.add_argument('-s', "--sex", type=str, dest="sex", help='Your sex', default='male', choices=['male', 'female'])
    # 可选属性,默认为None,-p后可接多个参数
    args.add_argument("-p", "--parent", type=str, dest='parent', help="Your parent", default="None", nargs='*')
    # 可选属性,默认为None,-o后可接多个参数
    args.add_argument("-o", "--other", type=str, dest='other', help="other Information", required=False, nargs='*')

    args = args.parse_args()  # 返回一个命名空间,如果想要使用变量,可用args.attr
    print("argparse.args=", args, type(args))
    print('name = %s' % args.name)
    d = args.__dict__
    for key, value in d.iteritems():
        print('%s = %s' % (key, value))


if __name__ == "__main__":
    cmd()

