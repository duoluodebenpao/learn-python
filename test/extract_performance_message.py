#!/usr/bin python
# encoding: utf-8
"""
@author: fzj 
@license: (C) Copyright 2013-2017
@time: 2019/10/9 15:43
@desc: 采集服务器上的cpu，内存，硬盘等数据，然后上报

必填参数：
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


"""

import argparse
import datetime
import logging
import os
import subprocess


# import requests


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
        def inner():
            run_flag = False  # 标记作业是否正常执行
            start_time = datetime.datetime.now()
            logger.info("process [{}] start time:[{}]".format(process_desc, start_time.strftime("%Y%m%d %H:%M:%S")))

            try:
                fun()
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
        logger.info("cmd [{}]".format(cmd))
        output = str(subprocess.check_output(cmd, shell=True)).strip()
        logger.info("cmd [{}] is success, output is /n [{}]".format(cmd, output))
        return str(output)
    except Exception:
        logger.error("cmd [{}] is faild".format(cmd))


def get_disk_message(message_map):
    cmd = "df -m / |grep /"
    output = check_output(cmd)
    logger.info(output)
    words = output.split()
    message_map["disk_total"] = words[1]
    message_map["disk_used"] = words[2]
    message_map["disk_available"] = words[3]


def get_memery_message(message_map):
    """采集内存数据   每3秒采集一次，共采集5次"""
    count = 5
    cmd = "free -c {} -s 3 -m |grep '^Mem:'".format(count)
    output = check_output(cmd)
    memory_total = 0
    memory_used = 0
    memory_free = 0
    for line in str(output).split("\n"):
        if line is not None and len(line) < 4:
            continue
        words = line[4:].split()
        memory_total += int(words[0])
        memory_used += int(words[1])
        memory_free += int(words[2])

    message_map["memory_total"] = memory_total // count
    message_map["memory_used"] = memory_used // count
    message_map["memory_free"] = memory_free // count


def get_cpu_message(message_map):
    """采集cpu总核数"""
    # vmstat    https://zhangnq.com/1925.html
    # cmd = "vmstat 2  2|grep '[0-9]'"   #每3秒采集一次，共采集5次， 同时只 显示出数字开头的行
    cmd = "lscpu  |grep '^CPU(s):'"
    output = check_output(cmd)
    cpu_total = output.split(":")[1].strip()
    message_map["cpu_total"] = cpu_total


def get_memery_cpu_message(data_map):
    """使用top采集数据"""
    cmd = "top -bn 1 -i -c |grep -E  '^(%Cpu)|(KiB Mem)' "
    output = check_output(cmd)
    lines = output.split("\n")
    logger.info(lines[0])
    logger.info(lines[1])

    for word in lines[0].split(":", 2)[1].split(","):
        print("cpu =>[{}]".format(word))
    for word in lines[1].split(":", 2)[1].split(","):
        print("memory =>[{}]".format(word))


def parse_argus(message_map):
    """解析参数"""
    args = argparse.ArgumentParser(description="采集服务器上的cpu，内存，硬盘等数据，然后上报")
    # args.add_argument("--url", required=True, help="上报的url", default="xxx")
    args.add_argument("--log_path", required=False, help="log文件的路径", default="xxx")
    args.add_argument("--company_id", required=False, help="公司id", default="company_test")
    # args.add_argument("--company_name", required=False, help="公司名称", default="")
    params = args.parse_args()
    log_path = params.log_path
    print("input logPath [{}]".format(log_path))
    global logger
    logger = get_logger(file_path=log_path)

    for key, value in params.__dict__.items():
        logger.info("input param [{}]:[{}]".format(key, value))
        message_map[key] = value
    return params


def get_message(message_map):
    """采集服务器信息"""
    get_disk_message(message_map)
    get_cpu_message(message_map)
    get_memery_message(message_map)

    for key, value in message_map.items():
        logger.info("data [{}]:[{}]".format(key, value))


def send_message(message_map):
    """将采集到的数据发送出去"""
    url = message_map.get("url")
    # response = requests.post(url, data=message_map)
    # logger.info("requests.post(url=[{}], data=[{}]) => response [{}]".format(url, message_map, response.text))


@record_process_time(__file__)
def main():
    message_map = {}
    # 1. 解析参数 并 初始化logger
    param = parse_argus(message_map)

    # 2. 获取性能数据 (使用 psutil 模块采集机器信息   或者 使用linux的命令采集信息)
    get_message(message_map)

    # 3. 将数据上报
    send_message(message_map)


if __name__ == '__main__':
    main()
