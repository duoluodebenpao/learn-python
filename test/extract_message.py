# encoding: utf-8

"""
@author: fzj
@file: extract_message.py
@time: 2019/10/15 0015 23:39
desc:  

"""


import subprocess
import psutil

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
    print(output)
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


def main():
    data_map = {}
    get_disk_message(data_map)

    for key,value in data_map.items():
        print("{} : {}".format(key, value))


if __name__ == "__main__":
    main()
