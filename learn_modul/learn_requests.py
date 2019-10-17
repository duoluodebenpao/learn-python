# encoding: utf-8

"""
@author: fzj
@file: learn_requests.py
@time: 2019/10/17 0017 1:19
desc:  

"""

import requests

# https://cloud.tencent.com/developer/article/1493120

def main():
    get = requests.get("http://www.baidu.com")
    print(get.content)
    print(get.text)

    pass


if __name__ == "__main__":
    main()
