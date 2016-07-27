# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

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


def get_XAU_rate():
    try:
        index_url = 'http://www.investing.com/instruments/HistoricalDataAjax'

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.post(index_url, data={"action": "historical_data",
                                                  "curr_id": "68",
                                                  "st_date": "06/17/2011",
                                                  "end_date": "07/17/2016",
                                                  "interval_sec": "Daily"
                                                  }, timeout=TIMEOUT)

        response = request_content()
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        rate_data = []
        rate_list_tr = soup.find("div", class_="BOC_main publish").find_all("tr")

        for rates in rate_list_tr:
            r = rates.find_all("td")
            if len(r) == 8 and r[0].string.strip() == "美元":
                rate_data.append(['C10104',
                                  'BCHO',
                                  'USD',
                                  r[1].string.strip(),
                                  r[2].string.strip(),
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[6].string.strip(),
                                  format_datetime(r[7].string.strip())])
            elif len(r) == 8 and r[0].string.strip() == "英镑":
                rate_data.append(['C10104',
                                  'BCHO',
                                  'GBP',
                                  r[1].string.strip(),
                                  r[2].string.strip(),
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[6].string.strip(),
                                  format_datetime(r[7].string.strip())])
            elif len(r) == 8 and r[0].string.strip() == "欧元":
                rate_data.append(['C10104',
                                  'BCHO',
                                  'EUR',
                                  r[1].string.strip(),
                                  r[2].string.strip(),
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[6].string.strip(),
                                  format_datetime(r[7].string.strip())])
            elif len(r) == 8 and r[0].string.strip() == "澳大利亚元":
                rate_data.append(['C10104',
                                  'BCHO',
                                  'AUD',
                                  r[1].string.strip(),
                                  r[2].string.strip(),
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[6].string.strip(),
                                  format_datetime(r[7].string.strip())])
            elif len(r) == 8 and r[0].string.strip() == "日元":
                rate_data.append(['C10104',
                                  'BCHO',
                                  'JPY',
                                  r[1].string.strip(),
                                  r[2].string.strip(),
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[6].string.strip(),
                                  format_datetime(r[7].string.strip())])
            elif len(r) == 8 and r[0].string.strip() == "港币":
                rate_data.append(['C10104',
                                  'BCHO',
                                  'HKD',
                                  r[1].string.strip(),
                                  r[2].string.strip(),
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[6].string.strip(),
                                  format_datetime(r[7].string.strip())])
            elif len(r) == 8 and r[0].string.strip() == "加拿大元":
                rate_data.append(['C10104',
                                  'BCHO',
                                  'CAD',
                                  r[1].string.strip(),
                                  r[2].string.strip(),
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[6].string.strip(),
                                  format_datetime(r[7].string.strip())])

        # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10104'")
        # logger_local.info('BCHO ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""REPLACE INTO t_listing_rate
                          (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash, mid_rate,
                          publisher_mid_rate, publish_time, update_time)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        for r in rate_data:
            cursor.execute(add_product, r)

        logger_local.info('BCHO rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


class MyThread(threading.Thread):
    """docstring for MyThread"""

    def __init__(self, thread_id, name, counter) :
        super(MyThread, self).__init__()  #调用父类的构造函数
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name


def print_time(thread_name, delay, counter) :
    while counter :
        time.sleep(delay)
        print "%s %s" % (thread_name, time.ctime(time.time()))
        counter -= 1


def parse_rate(legal_group):
    call_func = eval("get_"+legal_group+"_rate")
    call_func()


def format_datetime(raw_datetime):
    pure_datetime = filter(unicode.isdigit, raw_datetime)

    if len(pure_datetime) == 8:
        return pure_datetime[:4] + '-' + pure_datetime[4:6] + '-' + pure_datetime[6:] + ' 00:00:00'
    elif len(pure_datetime) == 12:
        return pure_datetime[:4] + '-' + pure_datetime[4:6] + '-' + pure_datetime[6:8] + ' ' + \
           pure_datetime[8:10] + ':' + pure_datetime[10:] + ':00'
    elif len(pure_datetime) == 14:
        return pure_datetime[:4] + '-' + pure_datetime[4:6] + '-' + pure_datetime[6:8] + ' ' + \
           pure_datetime[8:10] + ':' + pure_datetime[10:12] + ':' + pure_datetime[12:]
    else:
        return '0000-00-00 00:00:00'


def currency_decoder(tenor_desc):
    result = decode(tenor_desc,
                           u'美元', 'USD',
                           u'澳元', 'AUD',
                           u'澳大利亚元', 'AUD',
                           u'欧元', 'EUR',
                           u'英镑', 'GBP',
                           u'日元', 'JPY',
                           u'港元', 'HKD',
                           u'港币', 'HKD',
                           u'加元', 'CAD',
                           u'加拿大元', 'CAD',
                           '')
    return result


# def main():
    # #创建新的线程
    # thread1 = MyThread(1, "Thread-1", 1)
    # thread2 = MyThread(2, "Thread-2", 2)
    #
    # #开启线程
    # thread1.start()
    # thread2.start()
    #
    #
    # thread1.join()
    # thread2.join()
    # print "Exiting Main Thread"


if __name__ == '__main__':
    logger_local.info('====================================================================================')
    logger_local.info('price parser started')
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
        issuer_list = {}

        query = """select issuer_code, en_short_name from t_issuer where en_short_name is not null"""
        cursor.execute(query)
        for (issuer_code, en_short_name) in cursor:
            issuer_list[issuer_code] = en_short_name
        logger_local.info(issuer_list)

        # pool = ThreadPool(8) # Sets the pool size to 4

        # results = pool.map(parse_rate, legal_groups)

        # close the pool and wait for the work to finish
        # pool.close()
        # pool.join()

        get_XAU_rate()

        cnx.commit()
        cursor.close()
        cnx.close()
        logger_local.info('All rates retrieved\n\n')
