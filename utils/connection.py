# -*- coding: UTF-8-* -*-
# __author__ = 'fzj'
import configparser
import os
import sys

sys.path.insert(0, os.getcwd())

import pymysql
import redis


def get_props(env="dev"):
    """从db.ini 配置文件中获取参数,返回对应环境中的参数字典"""
    print("program's env is [{}]".format(env))
    conf_file_path = os.path.join(os.path.dirname(__file__), "db.ini")
    print("conf file path is [{}]".format(conf_file_path))
    config_parser = configparser.ConfigParser()
    config_parser.read(conf_file_path, encoding="utf-8")
    items = config_parser.items(env)
    props = {}
    for (key, value) in items.__iter__():
        print("key=[{}]  value=[{}]".format(key, value))
        props[key] = value
    return props


def get_mysql_conn(props=get_props()):
    conn = pymysql.connect(props['mysql_host'], props['mysql_user'], props["mysql_password"], props["mysql_db"],
                           charset="utf8")
    return conn


def get_redis_conn(props=get_props()):
    conn = redis.Redis(host=props["redis_host"], port=int(props["redis_port"]))
    return conn


if __name__ == '__main__':
    # get_props()

    # 测试redis
    r = get_redis_conn()
    r.set("key", "value")
    print("redis test value=[{}]".format(r.get("key")))
