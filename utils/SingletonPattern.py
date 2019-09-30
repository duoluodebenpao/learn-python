

"""
设计模式:
设计模式 是 前人工作的总结和提炼，通常，被人们广泛流传的设计模式都是针对 某一特定问题 的成熟的解决方案
使用 设计模式 是为了可重用代码、让代码更容易被他人理解、保证代码可靠性


单例设计模式:
目的,让 类 创建的对象，在系统中 只有 唯一的一个实例
每一次执行 类名() 返回的对象，内存地址是相同的


__new__ 方法:
使用 类名() 创建对象时，Python 的解释器 首先会调用 __new__ 方法为对象分配空间
__new__ 是一个 由 object 基类提供的内置的静态方法，主要作用有两个：
1) 在内存中为对象分配空间
2) 返回对象的引用
Python 的解释器获得对象的引用后，将引用作为第一个参数，传递给 __init__ 方法

重写 __new__ 方法 一定要 return super().__new__(cls)
否则 Python 的解释器 得不到 分配了空间的 对象引用，就不会调用对象的初始化方法
注意：__new__ 是一个静态方法，在调用时需要 主动传递 cls 参数


"""


class SingletonPattern:
    # 记录第一个被创建对象的引用
    instance = None
    # 记录是否执行过初始化动作
    init_flag = False

    def __new__(cls, *args, **kwargs):
        # 1. 判断类属性是否是空对象
        if cls.instance is None:
            # 2. 调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
        # 3. 返回类属性保存的对象引用
        return cls.instance

    def __init__(self):
        if not SingletonPattern.init_flag:
            print("初始化实例对象")
            SingletonPattern.init_flag = True


# 创建多个对象
player1 = SingletonPattern()
print(player1)

player2 = SingletonPattern()
print(player2)
