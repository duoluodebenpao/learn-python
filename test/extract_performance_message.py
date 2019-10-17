#!/usr/bin/env python
# encoding: utf-8
"""
@author: fzj 
@license: (C) Copyright 2013-2017
@time: 2019/10/9 15:43
@desc: 采集服务器上的cpu，内存，硬盘等数据，然后上报
"""

import argparse
import datetime
import logging
import os
import subprocess

import requests


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


def record_process_time(process_desc):
    """记录程序执行时间工具"""

    def wrapper(fun):
        def inner(fun_params):
            run_flag = False  # 标记作业是否正常执行
            start_time = datetime.datetime.now()
            logger.info("process [{}] start time:[{}]".format(process_desc, start_time.strftime("%Y%m%d %H:%M:%S")))

            try:
                fun(fun_params)
                run_flag = True
            finally:
                process_status = "success" if run_flag else "fault"
                logger.info("process [{}] run [{}]".format(process_desc, process_status))

                # 统计单个作业运行时长
                end_time = datetime.datetime.now()
                run_time = end_time - start_time
                logger.info("process:[{}]  start_time:[{}]  end_time:[{}]  during(s):[{}]".format(process_desc,
                                                                                                   start_time.strftime(
                                                                                                       "%Y%m%d %H:%M:%S"),
                                                                                                   end_time.strftime(
                                                                                                       "%Y%m%d %H:%M:%S"),
                                                                                                   run_time.seconds))

        return inner

    return wrapper


def import_model():
    # https://blog.csdn.net/woho778899/article/details/91875408
    # 使用psutil 模块采集集群信息
    pass

def check_output(cmd):
    """用于python2.7 版本"""
    try:
        print("cmd [{}]".format(cmd))
        output = subprocess.check_output(cmd, shell=True)
        print("run [{}] is success".format(cmd))
        return output
    except Exception:
        print("run [{}] is faild".format(cmd))

def get_disk_message(data_map):
    cmd = "df -m / |grep /"
    output = check_output(cmd)
    logger.info(output)
    words = str(output).split()

    data_map["disk_all"] = words[1]
    data_map["disk_used"] = words[2]
    data_map["disk_available"] = words[3]
    data_map["disk_used_percent"] = words[4]

def get_memery_message(data_map):
    cmd = "free -c 5 -s 2 |grep Mem:"
    output = check_output(cmd)

def get_cpu_message(data_map):
    # vmstat    https://zhangnq.com/1925.html
    cmd = "vmstat 2  2|grep '[0-9]'"   #每3秒采集一次，共采集5次， 同时只 显示出数字开头的行

    # sar 命令需要linux安装
    cmd = "sar -u 1 5 |grep Average:"    #每秒采集一次，共采集5次
    output = check_output(cmd)

def get_memery_cpu_message(data_map):
    # vmstat    https://zhangnq.com/1925.html
    cmd = "vmstat 3  5|grep '[0-9]'"   #每3秒采集一次，共采集5次， 同时只 显示出数字开头的行
    cmd = "top -n 1 |head 5"




def parse_argus():
    args = argparse.ArgumentParser(description="采集服务器上的cpu，内存，硬盘等数据，然后上报")
    args.add_argument("--url", required=True, help="上报的url", default="xxx")

    return args.parse_args()




def send_message(data_map):
    """将采集到的数据发送出去"""
    RECEIVE_FTP_HOUR_STAT_URL = ""
    params = {
        'token': '1234567890',
        'ip': "",
        'data_origin_id': data_origin_id,
        'data_origin_name': data_origin_name,
        'stat_time': stat_time,
        'busi_begin_time': busi_begin_time,
        'busi_end_time': busi_end_time,
        'ftp_update_time': ftp_update_time,
        'file_count': file_count,
        'file_size': file_size,
        'disk_total': disk_total,
        'disk_ftp_use': disk_ftp_use,
        'disk_ftp_use_percent': disk_ftp_use_percent,
        'company_id': 1,
        'company_name': "绿湾",
    }
    resp = requests.post(RECEIVE_FTP_HOUR_STAT_URL, data=params)
    logger.info("send ftp stat params: [{}], resp: [{}], content: [{}]".format(params, resp, resp.content if resp else ""))


def get_message(data_map):
    get_disk_message(data_map)

    for key,value in data_map.items():
        logger.info("{} : {}".format(key, value))



@record_process_time(__file__)
def main():
    data_map = {}
    # 1. 解析参数 并 初始化logger
    argus = parse_argus()
    logger.info(argus.url)

    # 2. 获取性能数据 (使用 psutil 模块采集机器信息   或者 使用linux的命令采集信息)
    get_message(data_map)

    # 3. 将数据上报
    send_message(data_map)



if __name__ == '__main__':
    main()
