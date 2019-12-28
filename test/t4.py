# -*- coding: utf-8 -*-
# !/usr/bin python
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/12/27 16:41
@desc:

"""


props = {}
props["host"] = "abc"
props["user"] = ""
props["password"] = ""
props["database"] = ""


print(props["host"])

offset = 333
count = 1000
table_name = "name"
sql = f"select * from {table_name} where id > {offset} limit {count} "
print(sql)

