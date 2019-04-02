# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import time
import re
import urllib.request
import random
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)


def mp3():
    my_dir = 'D:\\Videos\\小白10天入門Python全能實戰開發'
    files = os.listdir(my_dir)
    for file in files:
        if 'mp4' in file:
            logging.debug(file)
            mp4_file = os.path.join(my_dir, file)
            mp3_file = os.path.join(my_dir, file.split('.')[0] + '.mp3')
            if os.path.isfile(mp3_file):
                continue

            command = ["D:\\Software\\ffmpeg-4.1.1-win64-static\\bin\\ffmpeg.exe", "-i", mp4_file, "-f", "mp3", "-vn",
                       mp3_file]
            logging.debug(command)
            ps = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
            # for c in iter(lambda: ps.stdout.read(1), ''):  # replace '' with b'' for Python 3
            #     sys.stdout.write(c)
            # exit()


def generate_gid():
    gids = []
    for number in range(100000, 10000000):
        gids.append(number)
    for gid in gids:
        index0 = random.randint(0, len(gids) - 1)
        index1 = len(gids) - 1
        tmp = gids[index0]
        gids[index0] = gids[index1]
        gids[index1] = tmp
    return gids.pop()


if __name__ == '__main__':
    logging.info(generate_gid())
