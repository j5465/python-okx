import logging
import time
import sys
import logging.config as log_config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': './logs/log',
            'when': 'd',  # 分割单位，秒
            'encoding': 'utf-8',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': sys.stdout,
        },
    },
    'loggers':{
        "okxlogger": {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        }
    }
    # 'root': {
    #     'handlers': ['file'],
    #     'level': 'DEBUG',
    # },
}

def initLoggingConfig():
    log_config.dictConfig(LOGGING)

initLoggingConfig()


def get_my_logger(log_name):
    # 1、创建一个logger
    logger = logging.getLogger("okxlogger")
    
    logger.setLevel(logging.DEBUG)
    return logger