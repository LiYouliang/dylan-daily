# -*- coding: utf-8 -*-
# session 单例类集合
# 当需要多连接时，通过new_session改变一下单例连接

import sys
import os
import logging.config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from impala.dbapi import connect
from hdfs.client import InsecureClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from conf import settings
from library.decorator import Singleton

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


@Singleton
class MyMySQL(object):
    def __init__(self, data_source='ads_db'):
        logger.info("Connecting to {}".format(data_source))
        self._data_source = data_source
        self._session = sessionmaker()
        self._session.configure(bind=self.db_engine, autoflush=self.connect_config['autoflush'],
                                autocommit=self.connect_config['autocommit'])
        self.__session = self._session()

    @property
    def connect_config(self):
        db_opts = settings.DATABASES[self._data_source]
        return db_opts

    @property
    def db_engine(self):
        engine = create_engine(
            'mysql+{driver}://{username}:{password}@{hostname}:{port}/{database}?charset={charset}'.format(
                driver=self.connect_config['driver'],
                username=self.connect_config['user'],
                password=self.connect_config['password'],
                hostname=self.connect_config['host'],
                port=self.connect_config['port'],
                database=self.connect_config['database'],
                charset=self.connect_config['charset']),
            echo=self.connect_config['echo'],
            pool_reset_on_return=None,
        )
        return engine

    @property
    def session(self):
        return self.__session

    def new_session(self, data_source):
        self._data_source = data_source
        self._session.configure(bind=self.db_engine, autoflush=self.connect_config['autoflush'],
                                autocommit=self.connect_config['autocommit'])
        self.__session = self._session()
        return self.__session


@Singleton
class MyHive(object):
    def __init__(self, data_source='hive'):
        self._data_source = data_source
        logger.info("Connecting to {}".format(data_source))
        self.conn = connect(**self.connect_config)
        self.__cursor = self.conn.cursor(user=self.connect_config['user'])

    @property
    def connect_config(self):
        db_opts = settings.DATABASES[self._data_source]
        return db_opts

    @property
    def cursor(self):
        return self.__cursor

    def new_cursor(self):
        return self.conn.cursor(user=self.connect_config['user'])


@Singleton
class MyImpala(object):
    def __init__(self, data_source='impala'):
        self._data_source = data_source
        logger.info("Connecting to {}".format(data_source))
        self.conn = connect(**self.connect_config)
        self.__cursor = self.conn.cursor(user=self.connect_config['user'])

    @property
    def connect_config(self):
        db_opts = settings.DATABASES[self._data_source]
        return db_opts

    @property
    def cursor(self):
        return self.__cursor

    def new_cursor(self):
        return self.conn.cursor(user=self.connect_config['user'])

    def close(self):
        self.conn.close()


@Singleton
class MyHdfs(object):

    @property
    def connect_config(self):
        return settings.HDFS

    @property
    def client(self):
        client = InsecureClient(
            url=self.connect_config['url'],
            timeout=self.connect_config['timeout'],
            user=self.connect_config['user'],
        )
        return client


@Singleton
class Sessions(object):
    def __init__(self):
        self.__mysql = MyMySQL()

    @property
    def mysql(self):
        return self.__mysql

    @mysql.setter
    def mysql(self, data_source):
        logger.debug(data_source)
        self.__mysql.new_session(data_source)

    @property
    def hive(self):
        return MyHive()

    @property
    def impala(self):
        return MyImpala()

    @property
    def hdfs(self):
        return MyHdfs()


if __name__ == '__main__':
    s1 = Sessions()
    s1.mysql = 'jc_db'
    logger.info([id(s1.mysql), s1.mysql.connect_config, id(s1.mysql.db_engine), id(s1.mysql.session)])
    s1.mysql = 'ads_db'  # 因为单例不能重新实例化，但能改变实例属性
    logger.info([id(s1.mysql), s1.mysql.connect_config, id(s1.mysql.db_engine), id(s1.mysql.session)])
    s2 = Sessions()
    s1.mysql = 'jc_db'  # 使用时要注意选择数据库连接，否则会沿用上次的连接
    logger.info([id(s1.mysql), s1.mysql.connect_config, id(s1.mysql.db_engine), id(s1.mysql.session)])
    exit()

    s = Sessions()
    # 验证HDFS单例
    my_hdfs = MyHdfs()
    logger.info([id(s.hdfs), id(my_hdfs)])

    # 验证Hive单例
    my_hive = MyHive()
    logger.info([id(s.hive), id(my_hive)])
    logger.info([id(s.hive.cursor), id(my_hive.cursor), id(my_hive.new_cursor())])

    # 验证impala单例
    my_impala = MyImpala()
    logger.info([id(s.impala), id(my_impala)])
    logger.info([id(s.impala.cursor), id(my_impala.cursor), id(my_impala.new_cursor())])

    # 验证MySQL单例
    mysql = MyMySQL()
    logger.info([id(s.mysql), id(mysql)])
    logger.info([id(s.mysql.session), id(mysql.session), id(s.mysql.new_session())])
