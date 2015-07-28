__author__ = 'iceke'

import logging


class MyLog(object):
    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        logger.propagate = 0    # prevent repeat log
        logger.setLevel(logging.DEBUG)
        hdr = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
        hdr.setFormatter(formatter)
        logger.addHandler(hdr)
        return logger



