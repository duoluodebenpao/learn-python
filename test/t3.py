# -*- coding: utf-8 -*-
# !/usr/bin python
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/11/5 16:06
@desc:

"""

import random

def create():
    xing = "12345"
    ming = "你好啊陌生人".encode("utf-8")
    x = random.choice(xing)
    m = "".join(random.choice(ming) for i in range(2))
    return str(x+m)

print(create())

