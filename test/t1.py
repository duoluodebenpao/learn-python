# encoding: utf-8

"""
@author: fzj
@file: t1.py
@time: 2019/10/16 0016 0:33
desc:  

"""

import requests

def main():

    url = "http://172.16.3.87:7006/datachainstat/ftp_upload"
    images_id = "b18368d1af454038987d45aab60aba87"
    url = "http://172.17.7.24:9017/images/{}".format(images_id)
    print(url)
    r = requests.get(url)
    print(r.url)
    print(r.content)


if __name__ == "__main__":
    main()
