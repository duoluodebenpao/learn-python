# encoding: utf-8

"""
@author: fzj
@file: fanyi.py
@time: 2019/10/27 0027 16:55
desc:  

"""

import sys

import requests

url = "https://fanyi.baidu.com/basetrans"
headers = {
"user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}

data = {
"from":"zh",
"to":"en",
"query":"你好"
}

def main(sentence):
    print("input argument [{}]".format(sentence))
    r = requests.post(url, data=data, headers=headers)
    print(r.status_code)
    print(r.content.decode())
    pass


if __name__ == "__main__":
    sentence = sys.argv[1] if len(sys.argv) > 1 else "no"
    main(sentence)
