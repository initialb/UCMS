# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import errno
import math
import codecs
import argparse
import logging
import re
import requests
import bs4
import json
import urllib
import threading, thread
import time
import xml.dom.minidom
import mysql.connector
from mysql.connector import errorcode
from multiprocessing import Pool
from decimal import *

import csv
import random
from retrying import retry


from datetime import datetime
from xml.dom.minidom import parse
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

# import from BUtils
import butils.finutils
from butils import decode
from butils import fix_json
from butils import ppprint
from butils.pprint import pprint

# pp = pprint.PrettyPrinter(indent=4)
TIMEOUT = 10
LOCALDATE = time.strftime('%Y%m%d', time.localtime(time.time()))
LOGNAME = 'log/price_parser_' + LOCALDATE + '.log'

# initialize root logger to write verbose log file
logging.basicConfig(level=logging.DEBUG,
                    filename="log/price_parser_" + LOCALDATE + ".verbose.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# initialize a local logger
logger_local = logging.getLogger("ucms.birdie.parser.price")
logger_local.setLevel(logging.DEBUG)

# initialize a local logger file handler
logger_local_fh = logging.FileHandler(LOGNAME)
logger_local_fh.setLevel(logging.INFO)
logger_local_fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# initialize a local logger console handler
logger_local_ch = logging.StreamHandler()
logger_local_ch.setLevel(logging.INFO)
logger_local_ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# add handler to local logger
logger_local.addHandler(logger_local_fh)
logger_local.addHandler(logger_local_ch)


def export_csv():
    indicator = []
    query = """SELECT distinct indicator from indicator_db"""

    # cursor.execute(query, (hire_start, hire_end))
    cursor.execute(query)

    for (idc,) in cursor:
        indicator.append(idc)

    # print indicator

    hist_indicator = []

    for idc in indicator:
        query1 = """SELECT indicator,value,date FROM indicator_db
                   WHERE indicator=%s order by date desc limit 1"""
        cursor.execute(query1, (idc,))
        for (indicator,value,date) in cursor:
            hist_indicator.append([indicator, value, date])

    for hi in hist_indicator:
        query2 = """SELECT wm_data.value, wm_data.reference
                    FROM wm_data, t_indicator
                    WHERE wm_data.indicator=t_indicator.dasb_name and t_indicator.hist_name=%s
                    and region='United states'"""
        cursor.execute(query2, (hi[0],))
        print hi[0]
        for (v2, d2) in cursor:
            pass
            # print hi[0], hi[1], v2, hi[2], d2

    # for hi in hist_indicator:
    #     print i, v, d
    #     query2 = """SELECT wm_data.value, wm_data.reference
    #                 FROM wm_data, t_indicator
    #                 WHERE wm_data.indicator=t_indicator.dasb_name and t_indicator.hist_name=%s
    #                 and region='United states'"""
    #     cursor.execute(query2, (i,))
    #     for (v2, d2) in cursor:
    #         print i, v, v2, d, d2


if __name__ == '__main__':
    logger_local.info('====================================================================================')
    logger_local.info('indicator parser started')
    logger_local.info('====================================================================================')

    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')

        cursor = cnx.cursor()

        export_csv()


        # pool = ThreadPool(8) # Sets the pool size to 4
        # results = pool.map(parse_rate, legal_groups)
        # close the pool and wait for the work to finish
        # pool.close()
        # pool.join()

        # indicator_urls = get_indicator_link_by_country()
        #
        # pprint(indicator_urls)
        #
        # for i in indicator_urls:
        #     get_trading_indicator(i[0], i[1])

        # import_csv("United States", "/Users/initialb/Projects/UCMS/indicator_download/United States/")

        cnx.commit()
        cursor.close()
        cnx.close()
        logger_local.info('All indicators imported\n\n')
