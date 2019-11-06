# encoding: utf-8

"""
@author: fzj
@file: lear_logging.py
@time: 2019/9/30 0030 22:14
desc:  

"""

"""
1.日志级别
日志一共分成5个等级，从低到高分别是：
DEBUG  INFO   WARNING   ERROR   CRITICAL
这5个等级，也分别对应5种打日志的方法： debug 、info 、warning 、error 、critical。
默认的是WARNING，当在WARNING或之上时才被跟踪。

2. 日志格式说明
logging.basicConfig函数中，可以指定日志的输出格式format，这个参数可以输出很多有用的信息，如下:

%(levelno)s: 打印日志级别的数值
%(levelname)s: 打印日志级别名称
%(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s: 打印当前执行程序名
%(funcName)s: 打印日志的当前函数
%(lineno)d: 打印日志的当前行号
%(asctime)s: 打印日志的时间
%(thread)d: 打印线程ID
%(threadName)s: 打印线程名称
%(process)d: 打印进程ID
%(message)s: 打印日志信息

在工作中给的常用格式如下:
format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
这个格式可以输出日志的打印时间，是哪个模块输出的，输出的日志级别是什么，以及输入的日志内容。


注意，只要用过一次log功能再次设置格式时将失效，
实际开发中格式肯定不会经常变化，所以刚开始时需要设定好格式
"""

import logging
import os


def get_console_logger(level=logging.INFO,
                       log_format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'):
    """此logger只会将日志打印到控制台"""
    logger = logging.getLogger()
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(log_format)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def get_logger(level=logging.INFO, file_path="{}/default.log".format(os.getcwd()), mode="a", encoding="utf-8",
               log_format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'):
    """此logger会打印文件也打印到控制台"""
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


def main():
    logger = get_logger()
    logger.info('这是 loggging info message')
    logger.debug('这是 loggging debug message')
    logger.warning('这是 loggging a warning message')
    logger.error('这是 an loggging error message')
    logger.critical('这是 loggging critical message')
    logger.info("{}_log.txt".format(__file__[:-3]))


if __name__ == "__main__":
    main()
