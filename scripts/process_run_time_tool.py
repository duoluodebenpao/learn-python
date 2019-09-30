#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import logging
import traceback

# logging.basicConfig(level=logging.INFO, filename="{}_log.txt".format(__file__[:-3]), filemode="w", format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s')

def init_logging(the_level=logging.INFO, the_filename="{}_log.txt".format(__file__[:-3]), the_filemode="a", the_format='%(asctime)s-%(filename)s[line:%(lineno)d]-%(levelname)s: %(message)s'):
    logging.basicConfig(level = the_level, filename= the_filename, filemode=the_filemode, format=the_format)

def record_time(fun_name):
    """记录程序执行时间工具"""
    def wrapper(fun):
        def inner(*fun_params):
            run_flag = False  # 标记作业是否正常执行
            start_time = time.time()
            logging.info("程序运行时间:{}  执行函数:{} ".format(time.strftime("%Y%m%d %H:%M:%S", time.localtime(start_time)), fun_name))

            try:
                fun(*fun_params)
                run_flag = True
            finally:
                run_result = "成功" if run_flag else "失败"
                logging.info("执行函数{}:   {}".format(fun_name, run_result) )

                # 统计单个作业运行时长
                end_time = time.time()
                run_time = end_time - start_time
                logging.info("开始时间:{}  结束时间:{}  耗时:{:.0f} 秒".format(time.strftime("%Y%m%d %H:%M:%S", time.localtime(start_time)),
                                                     time.strftime("%Y%m%d %H:%M:%S", time.localtime(end_time)), run_time))

        return inner
    return wrapper


@record_time("extract_data")
def test_fun():
    for i in range(5):
        logging.info("this is info message")
        time.sleep(1)
        if i == 1:
            1/0


if __name__ == '__main__':
    try:
        init_logging()
        test_fun()
    except Exception as e:
        logging.error("\033[35m  bug message:\n{}\n".format(traceback.format_exc()))
