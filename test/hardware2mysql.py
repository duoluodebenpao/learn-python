#!/usr/bin/env python
# encoding: utf-8
"""
@author: fzj 
@license: (C) Copyright 2013-2017
@time: 2019/10/9 15:43
@desc: 采集服务器上的cpu，内存，硬盘等数据，然后上报
"""

import argparse
import logging
import os
import subprocess


def get_logger(level=logging.INFO, file_path="{}.log".format(__file__), mode="a", encoding="utf-8",
               log_format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'):
    """python的log日志，打印文件也打印到控制台"""
    if not os.path.exists(file_path):
        with open(file_path, "w+") as f:
            print("[{}] is not exists, so create file".format(file_path))
    else:
        print("[{}] is exists".format(file_path))

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


logger = get_logger()


def parse_argus():
    args = argparse.ArgumentParser(description="采集服务器上的cpu，内存，硬盘等数据，然后上报")
    args.add_argument("--url", required=True, help="上报的url", default="xxx")

    return args.parse_args()

def extract_message():

    pass


def send_message():

    pass


def main():
    # 1. 解析参数
    argus = parse_argus()
    print(argus.url)

    # 2. 获取性能数据


    # 3. 将数据上报
    send_message()

    pass


if __name__ == '__main__':
    logger.info("=======================================start")
    main()
