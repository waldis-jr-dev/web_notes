import logging
from abc import ABC, abstractmethod


class AbstractLogger(ABC):
    pass


class Logger(AbstractLogger):
    def __init__(self, logger_config):
        # TODO
        pass


if __name__ == '__main__':
    test = Logger('test')
