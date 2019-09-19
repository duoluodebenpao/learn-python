# -*- coding: UTF-8-* -*-
# __author__ = 'fzj'
import configparser
import os
from datetime import datetime, timedelta

import pymysql
import redis

DEFAULT_ENV = "local"


def get_env(key="env"):
    """从系统环境中获取key的参数, 如果系统变量的值为空，返回默认值"""
    global DEFAULT_ENV
    try:
        value = os.environ.get(key)
    except Exception:
        value = os.environ.get(key.upper())

    if value:
        print("jenkens env has param, env is [{}]".format(value))
        return value
    else:
        print("jenkens env is None, so DEFAULT_ENV is [{}]".format(DEFAULT_ENV))
        return DEFAULT_ENV


def get_props(env=DEFAULT_ENV):
    """从db.ini 配置文件中获取参数,返回对应环境中的参数字典"""
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


def get_mysql_conn(env=DEFAULT_ENV):
    props = get_props(env)
    mysql_conn = pymysql.connect(props['mysql_host'], props['mysql_user'], props["mysql_password"], props["mysql_db"],
                                 charset="utf8")
    return mysql_conn


def get_redis_conn(env=DEFAULT_ENV):
    props = get_props(env)
    redis_conn = redis.Redis(host=props["redis_host"], port=int(props["redis_port"]))
    return redis_conn




if __name__ == '__main__':
    # get_props()

    # 测试redis
    r = get_redis_conn()
    r.set("key", "value")
    print("redis test value=[{}]".format(r.get("key")))
