# -*- coding: utf-8 -*-
"""
工具类：静态方法合集
"""
from datetime import datetime
import random
import string
import logging


class Utils(object):
    @staticmethod
    def generate_transaction_sn():
        """
        生成流水号
        :return: String
        """
        date_str = datetime.now().strftime('%y%m%d%H%M%S%f')[:-3]
        random_string = ''.join(random.sample(string.ascii_uppercase + string.digits, 4))
        return ''.join(['FO', date_str, random_string])

    @staticmethod
    def get_logger(name, log_dir='/tmp/record.log'):
        # Formatter
        formatter = logging.Formatter(
            '[{asctime}: {levelname}/{processName}/{name}/\033[1;35m{funcName}\033[0m/{lineno}] {message}',
            style='{')  # 定义日志输出格式
        # Handler
        ch = logging.StreamHandler()  # 日志输出到屏幕控制台
        ch.setFormatter(formatter)
        fh = logging.FileHandler(log_dir, encoding='utf-8')  # 创建一个文件流并设置编码utf8
        fh.setFormatter(formatter)

        # Logger
        logger = logging.getLogger(name)  # 获得一个logger对象，默认是root
        logger.setLevel(logging.INFO)  # 设置最低等级debug
        logger.addHandler(fh)  # 增加指定的handler
        logger.addHandler(ch)
        return logger


if __name__ == '__main__':
    utils = Utils()
    utils.generate_transaction_sn()
