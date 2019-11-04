# -*- coding: utf-8 -*-
# !/usr/bin python
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/10/25 14:36
@desc:

"""

import json

import requests


def get_session(url):
    """
    获取 某网站的登录session
    :param url:
    :return:
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Connection": "keep-alive"
    }
    data = {
        "password": "Zf/0Ytq0XD4Ne3SmiteMkw==",
        "username": "fengzhuojie"
    }
    s = requests.Session()
    r = s.post(url, json=data, headers=headers)
    print(r.status_code)
    print(r.text)
    print(r.headers["SOPHON-SAM-Auth-Token"])
    print(r.cookies)
    r_map = json.loads(r.text)
    if 200 == int(r.status_code) and 100000 == int(r_map["code"]):
        print("登录成功")
        return s, r.headers
    else:
        print("登录失败")
        raise Exception


def main():
    url_map = {
        "local":"http://localhost:9017/api/system/user/login",
        "dev": "http://dev.singer.lvwan-inc.com/api/system/user/login",
        "test": "http://test.singer.lvwan-inc.com/api/system/user/login",
        "demo": "http://singer.lvwan-inc.com/api/system/user/login"
    }
    url = url_map["dev"]

    s, response_headers = get_session(url)
    headers = {
        "SOPHON-SAM-Auth-Token": response_headers["SOPHON-SAM-Auth-Token"]
    }

    url = "http://dev.singer.lvwan-inc.com/api/data_api/system/user/list"
    r = s.get(url, headers=headers)
    print(r.text)

    pass


if __name__ == '__main__':
    main()
