# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34777773/typeerror-object-takes-no-parameters-after-defining-new

class Foo(object):
    def __new__(cls, *args, **kwargs):
        # __new__是类方法，在对象创建的时候调用
        print('excute __new__')
        return super(Foo, cls).__new__(cls)

    def __init__(self, value):
        # __init__是一个实例方法，在对象创建后调用，对实例属性做初始化
        print('excute __init__')
        self.value = value


f1 = Foo(1)
print(f1.value)
f2 = Foo(2)
print(f2.value)
