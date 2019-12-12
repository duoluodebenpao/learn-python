# -*- coding: utf-8 -*-
# !/usr/bin python
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/12/12 14:51
@desc:

loads 方法是 将json格式的字符串转化成 python对象的过程
dumps 方法是 将python对象转化成 json格式的字符串

load 方法是 将文件对象转化成 python对象的过程
dump 方法是 将python对象转化成 文件对象的过程

"""

import json


if __name__ == '__main__':
    json_str = '{"a":"1","b":"bbb"}'
    loads = dict(json.loads(json_str))
    print(loads.get("b"))

    people = {"name":"frank", "age":18}
    dumps = json.dumps(people)
    print(dumps)

    with open("./../json_file") as a:
        # print(a.read())
        load = list(json.load(a))
        print(dict(load[1]).get("c"))

    with open("./../json_dump_file", "w+") as dump_file:
        cat = {"name": "frank", "age": 18}
        json.dump(cat, dump_file)

    pass

