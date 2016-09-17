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


def import_csv(region, path):
    index = 1
    file_list = os.listdir(path)
    for filename in file_list:
        abs_file_path = "%s%s" % (path, filename)
        indicator_name = re.sub(r"^"+region+r"|\.csv$", "", filename).strip()
        print "#"+str(index)+",", indicator_name
        # print "import", abs_file_path

        with open(abs_file_path) as f:
            f_csv = csv.reader(f)
            headers = next(f_csv)
            for row in f_csv:
                if len(row) == 2:
                    indicator_date = datetime.strptime(row[0], '%Y-%m-%d')
                    add_product = ("""INSERT INTO indicator_db
                                   (region, indicator, date, value)
                                   VALUES (%s, %s, %s, %s)""")
                    cursor.execute(add_product, (region, indicator_name, indicator_date.strftime("%Y%m%d"), row[1]))

        index += 1


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

        import_csv("United States", "/Users/initialb/Projects/UCMS/indicator_download/United States/")

        #G20
        # get_trading_indicator('Argentina')
        # get_trading_indicator('Australia')
        # get_trading_indicator('Brazil')
        # get_trading_indicator('Canada')
        # get_trading_indicator('China')
        # get_trading_indicator('France')
        # get_trading_indicator('Germany')
        # get_trading_indicator('India')
        # get_trading_indicator('Indonesia')
        # get_trading_indicator('Italy')
        # get_trading_indicator('Japan')
        # get_trading_indicator('South-korea')
        # get_trading_indicator('Mexico')
        # get_trading_indicator('Russia')
        # get_trading_indicator('Saudi-arabia')
        # get_trading_indicator('South-africa')
        # get_trading_indicator('Turkey')
        # get_trading_indicator('United-kingdom')
        # get_trading_indicator('United-states')
        # download_trading_indicator('European Union')

        #other
        # get_trading_indicator('Spain')
        # get_trading_indicator('New-zealand')
        # get_trading_indicator('Thailand')
        # get_trading_indicator('Vietnam')
        # get_trading_indicator('Singapore')
        # get_trading_indicator('Malaysia')


        cnx.commit()
        cursor.close()
        cnx.close()
        logger_local.info('All indicators imported\n\n')
