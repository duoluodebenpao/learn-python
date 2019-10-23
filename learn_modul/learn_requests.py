# encoding: utf-8

"""
@author: fzj
@file: learn_requests.py
@time: 2019/10/17 0017 1:19
desc:  

"""

import requests
import logging

logger = logging.getLogger()


# https://cloud.tencent.com/developer/article/1493120

def main():
    logger.setLevel(logging.DEBUG)
    r = requests.get("http://www.baidu.com")
    print(r.encoding)
    logger.error(r.text)
    r.encoding = "utf-8"
    logger.error(r.text)
    logger.error(r.content.decode("utf-8"))



if __name__ == "__main__":
    main()
