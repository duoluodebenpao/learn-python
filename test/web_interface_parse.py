# -*- coding: utf-8 -*-
# !/usr/bin python
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/12/27 14:45
@desc:
通过调用网络接口，解析数据
"""

import argparse
import logging
import os
import sys

import pymysql

sys.path.insert(0, os.getcwd())

props = {}
props["host"] = ""
props["user"] = ""
props["password"] = ""
props["database"] = ""
props["table"] = ""


def get_logger(level=logging.INFO, file_path="{}/default.log".format(os.getcwd()), mode="a", encoding="utf-8",
               log_format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'):
    """python的log日志，打印文件也打印到控制台"""
    if not os.path.exists(file_path):
        with open(file_path, "w+") as f:
            print("log file [{}] is not exists, so create file".format(file_path))
    else:
        print("log file [{}] is exists".format(file_path))
    logger = logging.getLogger()
    logger.setLevel(level)
    fh = logging.FileHandler(file_path, mode=mode, encoding=encoding)
    fh.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


logger = logging.getLogger()


def get_mysql_conn(props):
    conn = pymysql.connect(props['host'], props['user'], props["password"], props["database"], charset="utf8")
    return conn


def parse_argus(argus_map):
    """解析参数"""
    args = argparse.ArgumentParser(description="")
    args.add_argument("--host", required=True, help="")
    args.add_argument("--user", required=True, help="账号")
    args.add_argument("--password", required=True, help="密码")
    args.add_argument("--database", required=True, help="数据库名称")
    args.add_argument("--table", required=True, help="表名")
    params = args.parse_args()
    log_file = params.logFile
    global logger
    if log_file:
        print("input logFile [{}]".format(log_file))
        logger = get_logger(file_path=log_file)
    else:
        logger = get_logger()

    for key, value in params.__dict__.items():
        logger.info("input param [{}]:[{}]".format(key, value))
        argus_map[key] = value
    return params


def get_offset(file_path="{}/offset"):
    try:
        with open(file_path, "a") as f:
            offset = int(f.readline())
            logger.info("offset is [{}]".format(offset))
            return offset
    except Exception as e:
        return 0


def run(conn, table_name, file_path="{}/offset"):
    """将数据库中的基站信息通过web接口获取地理位置"""
    offset = get_offset()
    count = 1000
    sql = f"select * from {table_name} where id > {offset} limit {count} "
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    pass


if __name__ == '__main__':
    global props
    # 1. 获取mysql连接
    conn = get_mysql_conn(props)
    # 2. 从myslq中加载一批数据
    run(conn, props["table"])
    # 3. 调用接口获取数据，之后将数据保存

    # 4. 更新offset值

    pass
