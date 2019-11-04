# -*- coding: utf-8 -*-
# !/usr/bin python
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/10/29 14:38
@desc:

configparser 解析配置文件，可以通过环境，获取不同的数据

"""

import configparser

def main(env):
    """
    configparser 解析配置文件，可以通过环境，获取不同的数据
    :param env:  确定参数的范围
    :return:
    """
    conf_file_path = "配置文件路径"

    config_parser = configparser.ConfigParser()
    config_parser.read(conf_file_path, encoding="utf-8")
    items = config_parser.items(env)
    pass


if __name__ == '__main__':
    # 获取 test 环境下的参数
    main("test")

