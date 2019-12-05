#!/usr/bin/python3


"""
User defined exceptions
"""


__author__  = 'Zsolt Forray'
__license__ = 'MIT'
__version__ = '0.0.1'
__date__    = '05/12/2019'
__status__  = 'Development'


class NoTradeFoundError(Exception):
    pass


class InvalidStrategyError(Exception):
    pass


class InvalidDataError(Exception):
    pass
