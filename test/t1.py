# encoding: utf-8

"""
@author: fzj
@file: t1.py
@time: 2019/10/16 0016 0:33
desc:  

"""

import logging
def main():
    strip = "CPU(s):                48 ".split(":")[1].strip()
    print("[{}]".format(strip))

    logger = logging.getLogger()
    aa = {}
    aa["a"] = 11
    aa["b"] = 22

    for key,value in aa.items():
        print(key,value)


if __name__ == "__main__":
    main()
