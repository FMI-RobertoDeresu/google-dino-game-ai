import logging
import sys
from config import config


class Logger:
    logger = logging.getLogger()

    @staticmethod
    def _init():
        Logger.logger.setLevel(config['log_level'])

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        Logger.logger.addHandler(handler)

    @staticmethod
    def info(msg):
        Logger.logger.info(msg)

    @staticmethod
    def warning(msg):
        Logger.logger.warning(msg)


Logger._init()
