#!/usr/bin/env python
# encoding: utf-8
"""
@author: fzj 
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@time: 2019/9/29 16:08
@desc:

那么我们到底该用哪个模块、哪个函数来执行命令与系统及系统进行交互呢？下面我们来做个总结：

首先应该知道的是，Python2.4版本引入了subprocess模块用来替换os.system()、os.popen()、os.spawn*()等函数以及commands模块；也就是说如果你使用的是Python 2.4及以上的版本就应该使用subprocess模块了。
如果你的应用使用的Python 2.4以上，但是是Python 3.5以下的版本，Python官方给出的建议是使用subprocess.call()函数。Python 2.5中新增了一个subprocess.check_call()函数，Python 2.7中新增了一个subprocess.check_output()函数，这两个函数也可以按照需求进行使用。
如果你的应用使用的是Python 3.5及以上的版本（目前应该还很少），Python官方给出的建议是尽量使用subprocess.run()函数。
当subprocess.call()、subprocess.check_call()、subprocess.check_output()和subprocess.run()这些高级函数无法满足需求时，我们可以使用subprocess.Popen类来实现我们需要的复杂功能。


"""
import subprocess


def check_output(cmd):
    """用于python2.7 版本"""
    try:
        output = subprocess.check_output(cmd, shell=True)
        print("run [{}] is success".format(cmd))
        return output
    except Exception:
        print("run [{}] is faild".format(cmd))


def run(cmd):
    """用于python3.5以上版本 output对象中存储状态信息，及返回内容"""
    output = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    print("returncode [{}], stdout [{}]".format(output.returncode, output.stdout))
    return output


if __name__ == '__main__':
    run("ls -al")
    run("pwd")
