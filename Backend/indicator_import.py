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

        # import_csv("Argentina", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Argentina/")
        # import_csv("Australia", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Australia/")
        # import_csv("Brazil", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Brazil/")
        # import_csv("Canada", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Canada/")
        # import_csv("China", "/Users/initialb/Projects/UCMS/Backend/indicator_output/China/")
        # import_csv("France", "/Users/initialb/Projects/UCMS/Backend/indicator_output/France/")
        # import_csv("Germany", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Germany/")
        # import_csv("India", "/Users/initialb/Projects/UCMS/Backend/indicator_output/India/")
        # import_csv("Indonesia", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Indonesia/")
        # import_csv("Italy", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Italy/")
        # import_csv("Japan", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Japan/")
        # import_csv("South Korea", "/Users/initialb/Projects/UCMS/Backend/indicator_output/South Korea/")
        # import_csv("Mexico", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Mexico/")
        # import_csv("Russia", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Russia/")
        # import_csv("Saudi Arabia", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Saudi Arabia/")
        # import_csv("South Africa", "/Users/initialb/Projects/UCMS/Backend/indicator_output/South Africa/")
        # import_csv("Turkey", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Turkey/")
        # import_csv("United Kingdom", "/Users/initialb/Projects/UCMS/Backend/indicator_output/United Kingdom/")
        # import_csv("United States", "/Users/initialb/Projects/UCMS/Backend/indicator_output/United States/")
        # import_csv("European Union", "/Users/initialb/Projects/UCMS/Backend/indicator_output/European Union/")
        # import_csv("Euro Area", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Euro Area/")

        import_csv("Spain", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Spain/")
        import_csv("New Zealand", "/Users/initialb/Projects/UCMS/Backend/indicator_output/New Zealand/")
        import_csv("Thailand", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Thailand/")
        import_csv("Vietnam", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Vietnam/")
        import_csv("Singapore", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Singapore/")
        import_csv("Malaysia", "/Users/initialb/Projects/UCMS/Backend/indicator_output/Malaysia/")

        #G20
        # download_indicator('Argentina')
        # download_indicator('Australia')
        # download_indicator('Brazil')
        # download_indicator('Canada')
        # download_indicator('China')
        # download_indicator('France')
        # download_indicator('Germany')
        # download_indicator('India')
        # download_indicator('Indonesia')
        # download_indicator('Italy')
        # download_indicator('Japan')
        # download_indicator('South Korea')
        # download_indicator('Mexico')
        # download_indicator('Russia')
        # download_indicator('Saudi Arabia')
        # download_indicator('South Africa')
        # download_indicator('Turkey')
        # download_indicator('United Kingdom')
        # download_indicator('United States')
        # download_indicator('European Union')
        # download_indicator("Euro Area")

        # other
        # download_indicator('Spain')
        # download_indicator('New Zealand')
        # download_indicator('Thailand')
        # download_indicator('Vietnam')
        # download_indicator('Singapore')
        # download_indicator('Malaysia')

        cnx.commit()
        cursor.close()
        cnx.close()
        logger_local.info('All indicators imported\n\n')
