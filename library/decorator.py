# -*- coding: utf-8 -*-
# 装饰器集合
import sys
import os
import logging.config
from functools import wraps

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from conf import settings

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


class Singleton(object):
    """
    类型：类装饰器
    功能：单例
    """

    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self, *args, **kw):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(*args, **kw)
            return self._instance[self._cls]
        logger.debug("call {} again".format(self._cls))
        return self._instance[self._cls]


class Logit(object):
    def __init__(self, logfile='out.log'):
        self.logfile = logfile

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            # 打开logfile并写入
            with open(self.logfile, 'a') as opened_file:
                # 现在将日志打到指定的文件
                opened_file.write(log_string + '\n')
            # 现在，发送一个通知
            self.notify()
            return func(*args, **kwargs)

        return wrapped_function

    def notify(self):
        # logit只打日志，不做别的
        pass


class EmailLogit(Logit):
    """
    一个logit的实现版本，可以在函数调用时发送email给管理员
    """

    def __init__(self, email='admin@myproject.com', *args, **kwargs):
        self.email = email
        super(EmailLogit, self).__init__(*args, **kwargs)

    def notify(self):
        # 发送一封email到self.email
        # 这里就不做实现了
        pass


class Transaction(object):
    """
    类型：类装饰器
    功能：事务
    """

    def __init__(self, cls):
        self._cls = cls
        self._instance = {}


if __name__ == '__main__':
    @Logit(logfile='a.log')
    def addition_func(x):
        """Do some math."""
        return x + x


    result = addition_func(4)
    # Output: addition_func was called
