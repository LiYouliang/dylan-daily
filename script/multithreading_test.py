# -*- coding: utf-8 -*-
"""
多线程
"""
import sys
import os
import logging.config
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from conf import settings

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)
thread_max = threading.BoundedSemaphore(5)


def run(n):
    logger.info("task {} start".format(n))
    time.sleep(2)
    logger.info("task {} end".format(n))
    thread_max.release()


def main():
    start_time = time.time()
    for i in range(20):
        thread_max.acquire()
        t = threading.Thread(target=run, args=("t-%s" % i,))
        t.start()

    while threading.active_count() > 1:
        logger.debug("----threads count {}---".format(threading.active_count()))
    else:
        logger.info('----all threads done---')
        logger.info("cost  : {}".format(time.time() - start_time))


if __name__ == '__main__':
    main()

