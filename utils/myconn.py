# -*- coding: UTF-8-* -*-
# __author__ = 'fzj'


my_dict = {}


if my_dict.__contains__("aa"):
    print("11")
else:
    print("22")




def set_status(stats_map, data_origin_id, status):
    str_id = str(data_origin_id)
    str_status = str(status)
    if stats_map.__contains__(str_id):
        stats = stats_map.get(str_id)
        stats.add(str_status)

    else:
        stats = {str_id}

        stats_map[str_id] = stats

set_status(my_dict, 1, "a")
print(my_dict)
set_status(my_dict, 1, "b")
print(my_dict)
set_status(my_dict, 1, "b")
print(my_dict)

set_status(my_dict, 2, "b")
print(my_dict)

a = {'1','1','2'}
a.add('a')
print(a)

dict()

my = {}
my['a']='aa'
print(my)
b = any({1: 2, 3: 4})
print("----")

print(type(b))

dict()

import uuid

uuid_ = str(uuid.uuid1()).replace("-","")
print(uuid_)
import datetime
print(    datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

print((datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y%m%d%H%M%S"))

print(  "/home/admin/fengzhuojie/mysql_{}".format("abc"))

import os
print(os.path.join("a","b","c"))

strptime = datetime.datetime.strptime("20190909 090909", "%Y%m%d %H%M%S")
print(strptime)
strptime2 = datetime.datetime.strptime("20190909 091011", "%Y%m%d %H%M%S")
print((strptime2-strptime).total_seconds())



