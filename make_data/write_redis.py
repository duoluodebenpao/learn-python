#!/usr/bin/env python
# encoding: utf-8
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/9/28 16:51
@desc:
"""

import os
import sys

sys.path.insert(0, os.getcwd())
from datetime import datetime
from utils import common, connection


def make_data(str_time):
    props = connection.get_props()
    conn = connection.get_redis_conn(props)

    hash_index = "hash_index"
    key = "key"
    count = 100
    conn.hincrby(hash_index, key, count)


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
