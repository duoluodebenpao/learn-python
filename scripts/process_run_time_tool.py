#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
import logging
import time
import traceback
import os

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

logger = get_logger()


def record_process_time(process_desc):
    """记录程序执行时间工具"""

    def wrapper(fun):
        def inner(fun_params):
            run_flag = False  # 标记作业是否正常执行
            start_time = datetime.datetime.now()
            logging.info("process [{}] start time:[{}]".format(process_desc, start_time.strftime("%Y%m%d %H:%M:%S")))

            try:
                fun(fun_params)
                run_flag = True
            finally:
                process_status = "success" if run_flag else "fault"
                logging.info("process [{}] run [{}]".format(process_desc, process_status))

                # 统计单个作业运行时长
                end_time = datetime.datetime.now()
                run_time = end_time - start_time
                logging.info("process:[{}]  start_time:[{}]  end_time:[{}]  during(s):[{}]".format(process_desc,
                                                                                                   start_time.strftime(
                                                                                                       "%Y%m%d %H:%M:%S"),
                                                                                                   end_time.strftime(
                                                                                                       "%Y%m%d %H:%M:%S"),
                                                                                                   run_time.seconds))

        return inner

    return wrapper


@record_process_time(__file__)
def test_fun(param):
    for i in range(5):
        logging.info("this is info message")
        time.sleep(1)


if __name__ == '__main__':
    print("start")
    try:
        test_fun(5)
    except Exception as e:
        logging.error("bug message:[{}]".format(traceback.format_exc()))
