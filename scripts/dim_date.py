# -*- coding: utf-8 -*-
# !/usr/bin python
"""
@author: fzj
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 20200320 11:13
@desc: 此脚本用于生成数据仓库中的日期维度表
"""

import logging
from datetime import datetime, timedelta

import pymysql


def get_console_logger(level=logging.INFO,
                       log_format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'):
    """python的log日志，此logger只会将日志打印到控制台"""
    logger = logging.getLogger()
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(log_format)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = get_console_logger()


def get_conn(host="127.0.0.1", user="root", password="root", db="mysql"):
    conn = pymysql.connect(host, user, password, db, charset="utf8")
    return conn


def create_table(conn):
    drop_table_sql = "DROP TABLE IF EXISTS `dim_date`"
    cursor = conn.cursor()
    logger.info(drop_table_sql)
    cursor.execute(drop_table_sql)
    create_table_sql = """
    CREATE TABLE `dim_date` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `ymd` varchar(25)  NOT NULL COMMENT 'yyyymmdd',
      `ymd_long_desc` varchar(25)  NOT NULL COMMENT 'yyyy年mm月dd日',
      `ymd_short_desc` varchar(25) NOT NULL COMMENT 'yyyy-mm-dd',
      `ymd_dt` timestamp NOT NULL COMMENT '时间戳类型',
      `ym` varchar(25)  NOT NULL COMMENT 'yyyymm',
      `y` varchar(25) NOT NULL COMMENT 'yyyy',
      `m` varchar(25) NOT NULL COMMENT 'mm',
      `d` varchar(25) NOT NULL COMMENT 'dd',
      `w_y` int(11) NOT NULL COMMENT '当年的第几周',
      `w` int(11) NOT NULL COMMENT '周几(周日=7)',
      `q` int(11) NOT NULL COMMENT '第几季度',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin COMMENT='日期维度表';
    """
    logger.info(create_table_sql)
    cursor.execute(create_table_sql)
    cursor.close()


def insert_date(conn, str_start_time="20100101", str_end_time="20351231", str_parse="%Y%m%d"):
    insert_sql = "insert into `dim_date` ( `ymd`,`ymd_long_desc`,`ymd_short_desc`, `ymd_dt` ,`ym` ,`y`,`m`,`d`,`w_y`,`w`,`q` ) values "
    values = []
    end_time = datetime.strptime(str_end_time, str_parse)
    start_time = datetime.strptime(str_start_time, str_parse)
    cursor = conn.cursor()
    while True:
        if start_time > end_time:
            break
        ymd = start_time.strftime("%Y%m%d")
        y = ymd[0:4]
        m = ymd[4:6]
        d = ymd[6:8]
        ymd_long_desc = f"{y}年{m}月{d}日"
        ymd_short_desc = f"{y}-{m}-{d}"
        ymd_dt = start_time.strftime("%Y-%m-%d %H:%M:%S")
        ym = y + m
        isocalendar = start_time.isocalendar()
        w_y = isocalendar[1]
        w = isocalendar[2]
        q = (start_time.month - 1) // 3 + 1
        value = f"('{ymd}', '{ymd_long_desc}','{ymd_short_desc}', '{ymd_dt}', '{ym}', '{y}', '{m}', '{d}', '{w_y}','{w}', '{q}')"
        values.append(value)
        start_time = start_time + timedelta(days=1)
        if len(values) > 1000:
            sql = insert_sql + ",".join(values)
            logging.info(sql)
            cursor.execute(sql)
            values = []
    sql = insert_sql + ",".join(values)
    logging.info(sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close()


if __name__ == '__main__':
    conn = get_conn(db="test")
    logger.info("获取mysql连接成功")
    create_table(conn)
    logger.info("创建日期维度表成功: dim_date")
    insert_date(conn)
    logger.info("填充数据成功")
    conn.close()
