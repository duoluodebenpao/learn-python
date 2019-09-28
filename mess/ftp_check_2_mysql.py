# -*- coding: utf-8 -*-

import os
import sys
import getopt
import datetime
import time
import logging
import requests
from logging.handlers import TimedRotatingFileHandler

RECEIVE_FTP_HOUR_STAT_URL = 'http://172.16.3.87:7006/datachainstat/ftp_upload'


def init_logger(level, log_file):
    log_formatter = logging.Formatter("%(asctime)s[%(levelname)s][%(module)s]%(lineno)d %(message)s")
    logger = logging.getLogger()
    file_handler = TimedRotatingFileHandler(log_file, 'midnight')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)
    logger.setLevel(level=level)


def getRecFileCount(ftp_dir):
    a_cmd = "".join(['find ', ftp_dir, ' -type f -mmin -60|wc -l'])
    logging.info("getRecFileCount cmd: %s", a_cmd)
    read_result = format_result(os.popen(a_cmd).read())
    logging.info("getRecFileCount cmd result: %s", read_result)
    return long(read_result)


def getRecFileSize(ftp_dir):
    # unit: M
    cmd_list = ["find ", ftp_dir,
                " -type f -mmin -60|xargs du -shm |awk -F' ' 'BEGIN {sum=0}; {sum+=$1};END {print sum}'"]
    a_cmd = "".join(cmd_list)
    logging.info("getRecFileSize cmd: %s", a_cmd)
    read_result = format_result(os.popen(a_cmd).read())
    logging.info("getRecFileSize cmd result: %s", read_result)
    return long(read_result) * 1024 * 1024


def get_df_size():
    # unit: kb
    disk_total, disk_ftp_use, disk_ftp_use_percent = 0, 0, 0
    try:
        stat_dir = "/Users/wuguowei/temp"
        cmd = "".join(["df -l ", stat_dir, "|tail -1|awk -F' ' '{print $2,$3,$5}' "])
        read_result = os.popen(cmd).read() or ''
        read_result = read_result.replace("\n", '')
        disk_total, disk_ftp_use, disk_ftp_use_percent = read_result.split(" ", 3)
        disk_ftp_use_percent = str(disk_ftp_use_percent).replace("%", "")
    except Exception as ex:
        logging.error(ex)
    return long(disk_total) * 1024, long(disk_ftp_use) * 1024, int(disk_ftp_use_percent)


def execute_check(ip, check_dir, data_origin_id, data_origin_name):
    process_count = get_process_coun()
    logging.info("process_count: %s", process_count)
    if process_count > 4:
        logging.warning("process_count=%s, stop stat <><><><><><><>", process_count)
        return

    execute_begin_time = int(time.time())
    now_time = datetime.datetime.now()
    end_time = "".join([now_time.strftime("%Y-%m-%d %H"), ':00:00'])
    start_time = (datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=-1)).strftime(
        '%Y-%m-%d %H:%M:%S')

    stat_time, busi_begin_time, busi_end_time = end_time, start_time, end_time
    execute_check_once(ip, check_dir, data_origin_id, data_origin_name, stat_time, busi_begin_time, busi_end_time)
    execute_end_time = int(time.time())
    logging.info("execute time: %s, user time: %s", now_time, (execute_end_time - execute_begin_time))


def execute_check_once(ip, check_dir, data_origin_id, data_origin_name, stat_time, busi_begin_time, busi_end_time):
    file_count = getRecFileCount(check_dir)
    file_size = getRecFileSize(check_dir)
    ftp_update_time = busi_end_time
    logging.info("file_count: %s", file_count)
    logging.info("file_size: %s", file_size)
    disk_total, disk_ftp_use, disk_ftp_use_percent = get_df_size()

    # send http request
    params = {
        'token': '1234567890',
        'ip': ip,
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
    logging.info("send ftp stat params: %s, resp: %s,content: %s", params, resp, resp.content if resp else "")


def format_result(_result):
    if not _result:
        return ''
    _result = _result.strip()
    _result = _result.replace(' ', '')
    _result = _result.replace("\r", '')
    _result = _result.replace("\n", '')
    return _result


def get_process_coun():
    cmd = "ps -ef|grep ftp_check_2_mysql.py|wc -l"
    read_result = format_result(os.popen(cmd).read())
    return int(read_result)


def main():
    long_opt_names = ['ip=', 'check_dir=', 'data_origin_id=', 'data_origin_name=', 'log_file=']
    optlist, args = getopt.getopt(sys.argv[1:], '', long_opt_names)
    ip = ""
    check_dir = ""
    data_origin_id = 2
    data_origin_name = "电围"
    log_file = 'ftp_check_2_mysql.log'
    for o, a in optlist:

        if o == '--ip':
            ip = a
        if o == '--check_dir':
            check_dir = a
        if o == '--data_origin_id':
            data_origin_id = int(a)
        if o == '--data_origin_name':
            data_origin_name = a
        if o == '--log_file':
            log_file = a

    ip = '192.168.1.2'
    check_dir = '/Users/wuguowei/temp'
    init_logger(logging.INFO, log_file)
    logging.info("begin ftp check 2 mysql...")
    logging.info("ip: %s", ip)
    logging.info("check_dir: %s", check_dir)
    logging.info("data_origin_id: %s", data_origin_id)
    logging.info("data_origin_name: %s", data_origin_name)

    execute_check(ip, check_dir, data_origin_id, data_origin_name)

    logging.info("end ftp check success")


if __name__ == '__main__':
    main()
