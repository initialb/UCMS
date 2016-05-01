# -*- coding: utf-8 -*-

import re
import logging
import time
import mysql.connector
import mysql.connector.errorcode
import butils

class Parser(object):

    def __init__(self,
                 timeout=None,
                 index_url=None,
                 paging=None
                 ):
        self._timeout = 10 if timeout is None else timeout


class PLogging(object):
    """
    Pre defined parser logger.
    """

    def __init__(self, *args, **kwargs):
        """
        initialize loggers.
        """
        _localtime = time.strftime('%Y%m%d', time.localtime(time.time()))
        _logname = 'log/' + args[0] + '_' + _localtime + '.log'

        logging.basicConfig(level=logging.DEBUG,
                            filename="log/" + args[0] + '_' + _localtime + ".verbose.log",
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # initialize a local logger
        self.logger = logging.getLogger(args[0])
        self.logger.setLevel(logging.DEBUG)

        # initialize a local logger file handler
        logger_local_fh = logging.FileHandler(_logname)
        logger_local_fh.setLevel(logging.INFO)
        logger_local_fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        # initialize a local logger console handler
        logger_local_ch = logging.StreamHandler()
        logger_local_ch.setLevel(logging.INFO)
        logger_local_ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        # add handler to local logger
        self.logger.addHandler(logger_local_fh)
        self.logger.addHandler(logger_local_ch)


class PConnectDB(object):
    """
    Parser DB ops
    """
    def __init__(self, hostname, dbname, username, password):
        try:
            self.cnx = mysql.connector.connect(host=hostname, user=username, password=password, database=dbname)
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            print('MYSQL connected.')


def tenor_decoder(tenor_desc):
    result = butils.decode(tenor_desc,
                    u'1个月', '30',
                    u'2个月', '60',
                    u'3个月', '90',
                    u'6个月', '180',
                    u'9个月', '270',
                    u'12个月', '360',
                    u'半年', '180',
                    u'1年', '360',
                    u'一年', '360',
                    u'2年', '720',
                    u'二年', '720',
                    u'3年', '1080',
                    u'三年', '1080',
                    u'5年', '1800',
                    u'五年', '1800',
                    '')
    return result


def currency_decoder(tenor_desc):
    result = butils.decode(tenor_desc,
                    u'美元', 'USD',
                    u'澳元', 'AUD',
                    '')
    return result


def repr_zh(obj):
    return re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())


