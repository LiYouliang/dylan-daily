# -*- coding: utf-8 -*-
import os
import sys
import youtube_dl
import logging.config

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from conf import settings

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(__name__)


def handle_finished(d):
    filename = d['filename']
    logger.info('[video file]:{0}'.format(filename))


def my_hook(d):
    if d['status'] == 'downloading':
        process_bar = '[downloading]:filename {0} percent {1} speed {2}'.format(d['filename'],
                                                                                d['_percent_str'],
                                                                                d['_speed_str'])
        # logger.info(process_bar)

    if d['status'] == 'finished':
        logger.info("[finished]:filename {0} elapsed {1} downloaded_bytes {2}".format(d['filename'],
                                                                                      d['elapsed'],
                                                                                      d['downloaded_bytes']))
        handle_finished(d)

    if d['status'] == 'error':
        logger.info('[download error]')
        logger.info(d)


ydl_opts = {
    'progress_hooks': [my_hook],
    'format': 'best[ext=mp4]',  # Video format code, see the "FORMAT SELECTION" for all the info
    'outtmpl': os.path.join(settings.DATA_PATH, 'mp4s', '%(title)s.%(alt_title)s.%(id)s.f%(format_id)s.%(ext)s'),
    # Output filename template, see the "OUTPUT TEMPLATE" for all the info
    'download_archive': os.path.join('/data/download/', 'mp4s', 'archive.txt'),
    # Download only videos not listed in the archive file. Record the IDs of all downloaded videos in it.
    'restrictfilenames': False,  # Restrict filenames to only ASCII characters, and avoid "&" and spaces in filenames
    'no_check_certificate': True,  # Suppress HTTPS certificate validation
    'writethumbnail': False,  # Write thumbnail image to disk
    # 'proxy': 'http://127.0.0.1:1080', # Use the specified HTTP/HTTPS/SOCKS proxy.
    'ignoreerrors': True,  # Continue on download errors, for example to skip unavailable videos in a playlist
    'print_json': False,  # Be quiet and print the video information as JSON (video is still being downloaded).
    'dump_single_json': False,
    # Simulate, quiet but print JSON information for each command-line argument. If the URL refers to a playlist, dump the whole playlist information in a single line.
}


def run(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        logger.info("download url: {}".format(url))
        # ydl.download([url])
        info_dict = ydl.extract_info(url, download=True)
        # print(info_dict)
        filename = ydl.prepare_filename(info_dict)
        logger.info(filename)


if __name__ == '__main__':
    run('https://www.youtube.com/watch?v=Ejd00Vi2eV0')
