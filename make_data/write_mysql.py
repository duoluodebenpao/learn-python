#!/usr/bin/env python
# encoding: utf-8
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/9/28 16:33
@desc:
"""
import os
import sys

sys.path.insert(0, os.getcwd())
from datetime import datetime
from utils import common, connection


def make_data(str_time):
    props = connection.get_props()
    conn = connection.get_mysql_conn(props)
    cursor = conn.cursor()
    table_name = "table_name"

    sql_delete = "delete from {} where stat_time='{}'".format(table_name, str_time)
    print(sql_delete)
    cursor.execute(sql_delete)
    conn.commit()

    sql_insert = """ insert into {}
    stat_time, a, b
    values 
    """.format(table_name)

    values = []  # values 用于存放所有的value值

    sql_insert += ",".join(values)
    print(sql_insert)
    cursor.execute(sql_insert)
    conn.commit()
    conn.close()
    print("success insert [{}] data, cont is [{}] ".format(table_name, len(values)))


if __name__ == '__main__':
    str_time_template = "%Y-%m-%d 12:00:00"
    if len(sys.argv) <= 1:
        str_time = datetime.now().strftime(str_time_template)
        make_data(str_time)
    else:
        start_time, end_time, datetime_format, hour_step = sys.argv[1:]
        str_time_list = common.get_str_time_list(start_time, end_time, datetime_format, hour_step)
        for stat_time in str_time_list:
            str_time = datetime.now().strftime(str_time_template)
            make_data(str_time)
