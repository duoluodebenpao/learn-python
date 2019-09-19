#!/usr/bin/env python
# encoding: utf-8
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/9/19 15:32
@desc:
"""

import logging
import os
from datetime import datetime, timedelta


def get_file_logger(the_level=logging.INFO, the_filename="./logs/python_default_log", the_filemode="a",
                    the_format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'):
    """python的log日志，打印文件也打印到控制台"""
    logger = logging.getLogger()
    logger.setLevel(the_level)
    fh = logging.FileHandler(the_filename, mode=the_filemode)
    fh.setLevel(the_level)
    ch = logging.StreamHandler()
    ch.setLevel(the_level)
    formatter = logging.Formatter(the_format)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def fun_run_time(function):
    # 打印程序执行时间
    def fun(command):
        run_flag = False  # 标记作业是否正常执行
        start_time = datetime.now()
        try:
            function(command)
            run_flag = True
        finally:
            run_result = "success" if run_flag else "fault"
            # 统计单个作业运行时长
            end_time = datetime.now()
            run_time = (end_time - start_time).total_seconds()
            print("[{}] run status is [{}]".format(command, run_result))
            print(
                "start time:[{}]  end time:[{}]  during:[{}] second".format(start_time.strftime("%Y%m%d %H:%M:%S"),
                                                                            end_time.strftime("%Y%m%d %H:%M:%S"), run_time))

    return fun


def get_str_times(str_start_time, str_end_str, str_parse="%Y-%m-%d %H:%M:%S", hours=24):
    """传入 str_start_time 开始时间的字符串，str_end_str 结束时间的字符串，str_parse 字符串格式， hours 步长，   返回此时间范围内的日期列表 """
    str_times = []
    str_times.append(str_start_time)
    while True:
        # strptime = datetime.strptime(str_start_time, "%Y-%m-%d %H:%M:%S")
        stat_datetime = datetime.strptime(str_start_time, str_parse)
        str_time = (stat_datetime + timedelta(hours=int(hours))).strftime(str_parse)
        if str_end_str < str_time:
            break
        str_times.append(str_time)
        str_start_time = str_time
    return str_time


@fun_run_time
def cmd_exec(cmd):
    print("cmd [{}]".format(cmd))
    status = os.system(cmd)
    if status == 0:
        print("success... status [{}]  cmd [{}]".format(status, cmd))
    else:
        print("fault... status [{}]  cmd [{}]".format(status, cmd))


if __name__ == '__main__':
    cmd_exec("dir ./")
