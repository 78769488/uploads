#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Created on 2016/1/4 10:07.

import logging
import sys
import time
from logging import Logger
from logging.handlers import TimedRotatingFileHandler


def init_logger(logger_name='mylog'):
    if logger_name not in Logger.manager.loggerDict:

        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        datefmt = '%Y-%m-%d %H:%M:%S'
        format_str = '[%(asctime)s]: %(name)s %(levelname)s %(lineno)s %(message)s'
        formatter = logging.Formatter(format_str, datefmt)

        # handler all
        handler = TimedRotatingFileHandler('./all.log', when='midnight', backupCount=7)
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)

        # handler error
        handler = TimedRotatingFileHandler('./error.log', when='midnight', backupCount=7)
        handler.setFormatter(formatter)
        handler.setLevel(logging.ERROR)
        logger.addHandler(handler)

        # logging.StreamHandler
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    logger = logging.getLogger(logger_name)
    return logger

logger = init_logger('mylog')

if __name__ == '__main__':
    logger = init_logger('mylog')
    logger.error('test-error')
    logger.info('test-info')
    logger.warn('test-warn')