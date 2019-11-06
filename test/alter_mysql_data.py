# -*- coding: utf-8 -*-
# !/usr/bin python
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/11/6 11:13
@desc:
此脚本用于保证 logic_db 中的初始化状态是正确的，即原始库，资源库等6大库的状态正确

"""

import logging
import os
import sys

import pymysql

sys.path.insert(0, os.getcwd())


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

host = "172.16.1.58"
user = "sam_dev"
password = "123456"
db = "sam_dev"
table_logic_db = "logic_db"
table_logic_db = "logic_db_copy"
table_logic_table = "logic_table"
table_logic_table = "logic_table_copy"

def show_data(conn):
    """用于判断环境中的数据是否正确"""
    cursor = conn.cursor()
    sql_check_id = "select id,db_name,db_desc,db_level,parent_id,status from {} where id >=1 and id <=6".format(table_logic_db)
    logger.info(sql_check_id)
    cursor.execute(sql_check_id)
    beans = cursor.fetchall()
    logger.info("id在1-6之间的数量有[{}]条".format(len(beans)))
    for bean in beans:
        logger.info(bean)
    db_names = "'原始库','资源库','主题库','业务要素索引库','业务库','知识库'"
    sql_check_name = "select id,db_name,db_desc,db_level,parent_id,status from {} where db_name in ({}) ".format(table_logic_db, db_names)
    logger.info(sql_check_name)
    cursor.execute(sql_check_name)
    beans = cursor.fetchall()
    logger.info("db_name in [{}] 的数量有[{}]条".format(db_names, len(beans)))
    for bean in beans:
        logger.info(bean)
    # 如果数据库中没有6大库的情况下才会继续执行脚本
    return len(beans) <= 0


def init_job(conn):
    """初始化mysql中的环境，确保1-6位置空余"""
    logger.info("插入数据前的初始化工作...")
    global table_logic_db
    global table_logic_table
    cursor = conn.cursor()
    sql_get_top_id = "select max(id) id from {}".format(table_logic_db)
    logger.info(sql_get_top_id)
    cursor.execute(sql_get_top_id)
    top_id = int(cursor.fetchone()[0])
    logger.info("[{}] max id [{}] ".format(table_logic_db, top_id))
    sql_get_old_data = "select id,db_name,db_desc,db_level,parent_id,status from {} where id >=1 and id <=6".format(table_logic_db)
    logger.info(sql_get_old_data)
    cursor.execute(sql_get_old_data)
    beans = cursor.fetchall()
    try:
        for bean in beans:
            logger.info(bean)
            bean_id = int(bean[0])
            sql_update_table = "update {} set logic_db_id={} where logic_db_id={}".format(table_logic_table,
                                                                                          top_id + bean_id, bean_id)
            logger.info(sql_update_table)
            cursor.execute(sql_update_table)
            sql_update_db = "update {} set id={} where id={}".format(table_logic_db, top_id + bean_id, bean_id)
            logger.info(sql_update_db)
            cursor.execute(sql_update_db)
        conn.commit()
        logger.info("插入数据前的初始化工作完成...")
    except Exception:
        conn.rollback()
        logger.info("程序异常，数据库已经回滚")
        logger.info(Exception)
        raise Exception


def insert_data(conn):
    """将数据插入到mysql"""
    logger.info("插入6大库数据到mysql...")
    sql_insert = [
        ""
        , ""
        , ""
        , ""
        , ""
        , ""
    ]
    cursor = conn.cursor()
    try:
        for sql in sql_insert:
            logger.info(sql)
            cursor.execute(sql)
        conn.commit()
    except Exception:
        conn.rollback()
        logger.info("程序异常，数据库已经回滚")
        logger.info(Exception)
        raise Exception


if __name__ == '__main__':
    conn = pymysql.connect(host, user, password, db, charset="utf8")
    logger.info("获取mysql连接成功")
    flag = show_data(conn)
    if flag:
        logger.info("判断[{}]未初始化，程序继续".format(table_logic_table))
        init_job(conn)
        insert_data(conn)
        conn.close()
        logger.info("success...")
    else:
        logger.info("判断[{}]已初始化，程序退出".format(table_logic_table))


