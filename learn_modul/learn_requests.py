# encoding: utf-8

"""
@author: fzj
@file: learn_requests.py
@time: 2019/10/17 0017 1:19
desc:  

"""

import requests
import logging
import json
import os

logger = logging.getLogger()


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
        "username": "fzj"
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
        return r.headers["token"]
    else:
        print("登录失败")
        raise Exception


def get_token(env="dev"):
    token_file = "./token"
    if os.path.isfile(token_file):
        with open(token_file, "r") as f:
            token = f.readline()

        url = ""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Connection": "keep-alive",
            "SOPHON-SAM-Auth-Token": token,
            "Content-Type": "multipart/form-data",
            "Accept": "application/json"
        }
        r = requests.get(url, headers=headers)
        print(r.text)
        r_map = json.loads(r.text)
        try:
            if 200 == int(r.status_code) and 100000 == int(r_map["code"]):
                print("使用历史保存的token")
                return token
        except Exception:
            print("重新获取token")

    url_map = {
        "local":"",
        "env":"",
        "test":"",
        "prod":""
    }
    url = url_map[env]
    token = get_session(url, token_file)
    print("token >>>{}".format(token))
    with open(token_file, "w") as f:
        f.write(token)
    return token

def main():
    logger.setLevel(logging.DEBUG)
    token = get_token("dev")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Connection": "keep-alive",
        "SOPHON-SAM-Auth-Token": token,
        "Content-Type": "multipart/form-data",
        "Accept": "application/json"
    }
    url = "http://www.baidu.com"
    file_path = "D:\share\LW_Standard.zip"
    files = {"file": open(file_path, "rb")}
    r = requests.get(url, headers=headers, filees=files)

    print(r.encoding)
    logger.error(r.text)
    r.encoding = "utf-8"
    logger.error(r.text)
    logger.error(r.content.decode("utf-8"))



if __name__ == "__main__":
    main()
