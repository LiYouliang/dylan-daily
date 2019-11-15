import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
PROJECT_NAME = os.path.basename(BASE_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime} {levelname} {processName}:{process:d} {threadName}:{thread:d} {module}:{funcName}:{lineno}] {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{asctime} \033[1;35m{levelname}\033[0m {processName}:{threadName}:{module}:{funcName}:{lineno}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'simple',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "dylan-daily.log",
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {  # root logger 默认日志
            'handlers': ['console', 'file'],
            'level': 'DEBUG',  # logging.lastResort: root 默认level是WARNING, 输入到stderr
            'propagate': True
        },
        '__main__': {
            'handlers': ['console', 'file'],
            # 'level': 'DEBUG',  # logger 优先级高于handlers的level
            'propagate': False   # propagate会把当前的logger设置为其parent, 并将record传入parent的Handler
        },
    }
}
