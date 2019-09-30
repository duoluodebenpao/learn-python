#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import time
import threading

# 全局变量
local_tmp_folder = "/data/"

local_hdfs_source = "/user/"
local_hdfs_result = "/user"

local_hdfs_config_file = "/user"

current_time = time.time()
yesterday_time = current_time - 24 * 60 * 60
date_year = time.strftime("%Y", time.localtime(yesterday_time))
date_to_import = time.strftime("%Y%m%d", time.localtime(yesterday_time))
keep_source = 0  # 判断是否要使用历史保留的数据, 如果为0,不管是否有历史数据,肯定重新执行一遍, 如果为1,可以重用历史数据

user_password = dict()
user_password["a"] = "a"
db_host = ""

file_name = os.path.basename(sys.argv[0])
args = sys.argv[1:]


def clean():
    # listdir = os.listdir(local_tmp_folder)
    # for temp in listdir:
    #     if date_to_import > temp:
    #         temp_command="rm -rf {}".format(local_tmp_folder+temp)
    #         print(temp_command)
    #         os.system(temp_command)
    date_del = time.strftime("%Y%m%d",
                             time.localtime(time.mktime(time.strptime(date_to_import, "%Y%m%d")) - 24 * 60 * 60))
    path_del = os.path.join(local_tmp_folder, date_del)
    command_del = "rm -rf {}".format(path_del)
    print(command_del)
    os.system(command_del)


def parseParams():
    """解析参数"""
    try:
        if len(args) == 0:
            return
        elif len(args) == 1:
            if args[0] == "":
                keep_source = 1
            else:
                help()
                exit()
        elif len(args) == 2:
            time.strptime(args[0], "%Y%m%d")
            time.strptime(args[1], "%Y%m%d")
            date_year = args[0]
            date_to_import = args[1]
        elif len(args) == 3:
            time.strptime(args[0], "%Y%m%d")
            time.strptime(args[1], "%Y%m%d")
            date_year = args[0]
            date_to_import = args[1]
            if args[2] == "":
                keep_source = 1
            else:
                help()
                exit()
    except Exception as e:
        print("\nerror信息: {}".format(e))
        help()
        exit()


def dump_from_oracle(dump_date, dump_path, u_p):
    """从oracle数据库中导数据到本地"""
    # u_p=user_password.popitem()
    user = u_p[0]
    password = u_p[1]
    # print("args dump_date:{}, dump_path:{}, user:{}".format(dump_date,dump_path,user))
    sql = "select * from a where to_date(a)={}".format(dump_date)
    file = "{}/{}_{}.csv".format(dump_path, user, dump_date)
    command = "sqluldr2 {}/{}@db_host query=\"{}\" charset=AL32UTF8 text=csv head=no safe=yes file={}".format(user,
                                                                                                              password,
                                                                                                              sql, file)
    print("command: %s" % command)
    os.system(command)


def dump_main():
    print("3.从orcale中拉取数据到本地")
    dump_date = date_to_import
    dump_path = local_tmp_folder + date_to_import
    if not os.path.exists(dump_path):
        os.mkdir(dump_path)

    while True:

        u_p = user_password.popitem()
        # 设置最多6个线程并发
        while threading.activeCount() < 7:
            thread = threading.Thread(target=dump_from_oracle, args=(dump_date, dump_path, u_p))
            thread.setName(u_p[0])
            thread.start()
        if len(user_password) == 0:
            return
        time.sleep(1)


def running_time(fun):
    # 打印程序执行时间
    def inner():
        # 设置log输出位置
        # log_content = ""
        # log_path = "c://temp//log"

        flag = False  # 标记作业是否正常执行
        start_time = time.time()
        print("程序运行时间:%s  执行脚本:%s" % (time.strftime("%Y%m%d", time.localtime(start_time)), file_name))
        try:
            fun()
            flag = True
        finally:
            if flag:
                print("程序处理 正常 ")
            else:
                print("数据处理 异常 ")

            # 统计单个作业运行时长
            end_time = time.time()
            run_time = end_time - start_time
            print("开始时间:%s  结束时间:%s  耗时:%d 秒" % (time.strftime("%Y%m%d %H:%M:%S", time.localtime(start_time)),
                                                 time.strftime("%Y%m%d %H:%M:%S", time.localtime(end_time)), run_time))

    return inner


@running_time
def extract():
    """数据同步"""

    # 1.解析参数
    parseParams()

    # 2.检查hdfs上是否存在历史数据
    # 删除hdfs上历史数据,因为hdfs上没有加分区,不知道hdfs上的数据是否是其他日期的数据     感觉ods层应该按照日期进行分区
    command_remove_hdfs_data = "hdfs dfs -rm -r -skipTrash {}".format(local_hdfs_source)
    os.system(command_remove_hdfs_data)

    # 3.检查local是否存在历史数据, 如果存在,直接将数据同步到hdfs上
    local_data_path = local_tmp_folder + date_to_import
    if keep_source == 1 & os.path.exists(local_data_path) & len(os.listdir(local_data_path)) > 0:
        print("%s 目录下存在历史数据" % local_data_path)
        # os.system("rm -rf %s" %local_data_path)
    else:
        # 3.从orcale中拉取数据到本地
        dump_main()

    # 4.从本地拉取数据上传到hdfs上
    command_copy_data_to_hdfs = "export HADOOP_USER_NAME=abc && hdfs dfs -copyFromLocal {} {}".format(local_data_path,
                                                                                                        local_hdfs_source)
    print("4.从本地拉取数据上传到hdfs上: %s" % command_copy_data_to_hdfs)
    os.system(command_copy_data_to_hdfs)

    # 5.最后保留当天的数据,清除当天之前的历史数据  只删除一天
    clean()


if __name__ == '__main__':
    extract()
