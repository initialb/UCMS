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


def get_CMHO_rate():
    try:
        index_url = 'http://fx.cmbchina.com/hq/'
        publisher_code = 'C10308'

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get(index_url, timeout=TIMEOUT)

        response = request_content()

        # while True:
        #     try:
        #         response = requests.get(index_url, timeout=TIMEOUT)
        #     except requests.exceptions.ConnectionError, e:
        #         print e
        #         continue
        #     except requests.exceptions.Timeout, e:
        #         print e
        #         continue
        #     break
        #
        # response = requests.get(index_url)

        soup = bs4.BeautifulSoup(response.text, "html.parser")
        publish_date = filter(unicode.isdigit, soup.find(text=re.compile(u"当前日期")))

        rate_data = []

        rate_list_tr = soup.find("table", class_="data").find_all("tr")

        for rates in rate_list_tr:
            r = rates.find_all("td")
            if r[0].string.strip() == "美元":
                rate_data.append(['C10308',
                                  'CMHO',
                                  'USD',
                                  r[6].string.strip(),
                                  r[7].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[3].string.strip(),
                                  format_datetime(publish_date + r[8].string.strip())])
            elif r[0].string.strip() == "英镑":
                rate_data.append(['C10308',
                                  'CMHO',
                                  'GBP',
                                  r[6].string.strip(),
                                  r[7].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[3].string.strip(),
                                  format_datetime(publish_date + r[8].string.strip())])
            elif r[0].string.strip() == "欧元":
                rate_data.append(['C10308',
                                  'CMHO',
                                  'EUR',
                                  r[6].string.strip(),
                                  r[7].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[3].string.strip(),
                                  format_datetime(publish_date + r[8].string.strip())])
            elif r[0].string.strip() == "澳大利亚元":
                rate_data.append(['C10308',
                                  'CMHO',
                                  'AUD',
                                  r[6].string.strip(),
                                  r[7].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[3].string.strip(),
                                  format_datetime(publish_date + r[8].string.strip())])
            elif r[0].string.strip() == "日元":
                rate_data.append(['C10308',
                                  'CMHO',
                                  'JPY',
                                  r[6].string.strip(),
                                  r[7].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[3].string.strip(),
                                  format_datetime(publish_date + r[8].string.strip())])

        # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10308'")
        # logger_local.info('CMHO ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""REPLACE INTO t_listing_rate
                          (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash,
                          publisher_mid_rate, publish_time, update_time)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        for r in rate_data:
            cursor.execute(add_product, r)

        logger_local.info('CMHO rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def get_ICBC_rate():
    try:
        """
        update USD rate
        """
        index_url = 'http://www.icbc.com.cn/ICBCDynamicSite/Optimize/Quotation/QuotationListIframe.aspx?variety=2' \
                    '&beginDate=' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '&endDate=' \
                    + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '&currency=USD&ppublishDate='

        for ccy_desc in [u'美元(USD)', u'英镑(GBP)', u'欧元(EUR)', u'澳大利亚元(AUD)', u'日元(JPY)']:
            @retry(stop_max_attempt_number=10, wait_fixed=2000)
            def request_content():
                return requests.get(index_url, timeout=TIMEOUT)

            response = request_content()
            soup = bs4.BeautifulSoup(response.text, "html.parser")

            rate_data = []
            rate_list_tr = soup.find("table", class_="tableDataTable").find_all("tr")

            for rates in rate_list_tr:
                r = rates.find_all("td")
                if len(r) == 6 and r[0].string.strip() == ccy_desc:
                    rate_data = ['C10102',
                                 'ICBC',
                                 ccy_desc[-4:-1],
                                 r[2].string.strip(),
                                 r[3].string.strip(),
                                 r[4].string.strip(),
                                 r[4].string.strip(),
                                 format_datetime(r[1].string.strip() + r[5].string.strip())]

                    # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10102' AND currency='USD'")

                    add_product = ("""REPLACE INTO t_listing_rate
                                      (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash,
                                      publish_time, update_time)
                                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
                    cursor.execute(add_product, rate_data)
                    break

        logger_local.info('ICBC rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))
        logger_local.exception('EXCEPTION:')


def get_BCHO_rate():
    try:
        index_url = 'http://srh.bankofchina.com/search/whpj/search.jsp'

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.post(index_url, data={"pjname": "1316,1314,1325,1326,1323"}, timeout=TIMEOUT)

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


def get_ABCI_rate():
    try:
        index_url = 'http://app.abchina.com/rateinfo/RateSearch.aspx?id=1'

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get(index_url, timeout=TIMEOUT)

        response = request_content()
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        publish_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"更新日期")))

        rate_data = []

        rate_list_tr = soup.find("table", class_="DataList").find_all("tr")

        for rates in rate_list_tr:
            r = rates.find_all("td")
            if len(r) == 4 and r[0].string.strip() == "美元(USD)":
                rate_data.append(['C10103',
                                  'ABCI',
                                  'USD',
                                  r[1].string.strip(),
                                  r[3].string.strip(),
                                  r[2].string.strip(),
                                  r[2].string.strip(),
                                  format_datetime(publish_datetime)])
            elif len(r) == 4 and r[0].string.strip() == "英磅(GBP)":
                rate_data.append(['C10103',
                                  'ABCI',
                                  'GBP',
                                  r[1].string.strip(),
                                  r[3].string.strip(),
                                  r[2].string.strip(),
                                  r[2].string.strip(),
                                  format_datetime(publish_datetime)])
            elif len(r) == 4 and r[0].string.strip() == "欧元(EUR)":
                rate_data.append(['C10103',
                                  'ABCI',
                                  'EUR',
                                  r[1].string.strip(),
                                  r[3].string.strip(),
                                  r[2].string.strip(),
                                  r[2].string.strip(),
                                  format_datetime(publish_datetime)])
            elif len(r) == 4 and r[0].string.strip() == "澳大利亚元(AUD)":
                rate_data.append(['C10103',
                                  'ABCI',
                                  'AUD',
                                  r[1].string.strip(),
                                  r[3].string.strip(),
                                  r[2].string.strip(),
                                  r[2].string.strip(),
                                  format_datetime(publish_datetime)])
            elif len(r) == 4 and r[0].string.strip() == "日元(JPY)":
                rate_data.append(['C10103',
                                  'ABCI',
                                  'JPY',
                                  r[1].string.strip(),
                                  r[3].string.strip(),
                                  r[2].string.strip(),
                                  r[2].string.strip(),
                                  format_datetime(publish_datetime)])

        # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10103'")
        # logger_local.info('ABCI ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""REPLACE INTO t_listing_rate
                       (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash,
                       publish_time, update_time)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
        for r in rate_data:
            cursor.execute(add_product, r)

        logger_local.info('ABCI rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def get_CCBH_rate():
    try:
        index_url = 'http://forex.ccb.com/cn/home/news/jshckpj.xml'

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.post(index_url, timeout=TIMEOUT)

        response = request_content()
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        publish_datetime = unicode(soup.timestamp.string)

        rate_data = []

        rt_data_array = soup.find_all("referencepricesettlement")

        for rt_data in rt_data_array:
            if rt_data.cm_curr_cod.string == '14':
                rate_data.append(['C10105',
                             'CCBH',
                             'USD',
                             '%.2f' % (float(rt_data.fxr_xch_buyin.string)*100),
                             '%.2f' % (float(rt_data.fxr_cur_buyin.string)*100),
                             '%.2f' % (float(rt_data.fxr_xch_sellout.string)*100),
                             '%.2f' % (float(rt_data.fxr_cur_sellout.string)*100),
                             '%.2f' % (float(rt_data.mid_rate.string)*100),
                             format_datetime(publish_datetime)])
            elif rt_data.cm_curr_cod.string == '12':
                rate_data.append(['C10105',
                             'CCBH',
                             'GBP',
                             '%.2f' % (float(rt_data.fxr_xch_buyin.string)*100),
                             '%.2f' % (float(rt_data.fxr_cur_buyin.string)*100),
                             '%.2f' % (float(rt_data.fxr_xch_sellout.string)*100),
                             '%.2f' % (float(rt_data.fxr_cur_sellout.string)*100),
                             '%.2f' % (float(rt_data.mid_rate.string)*100),
                             format_datetime(publish_datetime)])
            elif rt_data.cm_curr_cod.string == '33':
                rate_data.append(['C10105',
                             'CCBH',
                             'EUR',
                             '%.2f' % (float(rt_data.fxr_xch_buyin.string)*100),
                             '%.2f' % (float(rt_data.fxr_cur_buyin.string)*100),
                             '%.2f' % (float(rt_data.fxr_xch_sellout.string)*100),
                             '%.2f' % (float(rt_data.fxr_cur_sellout.string)*100),
                             '%.2f' % (float(rt_data.mid_rate.string)*100),
                             format_datetime(publish_datetime)])
            elif rt_data.cm_curr_cod.string == '29':
                rate_data.append(['C10105',
                             'CCBH',
                             'AUD',
                             '%.2f' % (float(rt_data.fxr_xch_buyin.string)*100),
                             '%.2f' % (float(rt_data.fxr_cur_buyin.string)*100),
                             '%.2f' % (float(rt_data.fxr_xch_sellout.string)*100),
                             '%.2f' % (float(rt_data.fxr_cur_sellout.string)*100),
                             '%.2f' % (float(rt_data.mid_rate.string)*100),
                             format_datetime(publish_datetime)])
            elif rt_data.cm_curr_cod.string == '27':
                rate_data.append(['C10105',
                             'CCBH',
                             'JPY',
                             '%.4f' % (float(rt_data.fxr_xch_buyin.string)*100),
                             '%.4f' % (float(rt_data.fxr_cur_buyin.string)*100),
                             '%.4f' % (float(rt_data.fxr_xch_sellout.string)*100),
                             '%.4f' % (float(rt_data.fxr_cur_sellout.string)*100),
                             '%.4f' % (float(rt_data.mid_rate.string)*100),
                             format_datetime(publish_datetime)])

        # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10105'")
        # logger_local.info('CCBH ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""REPLACE INTO t_listing_rate
                          (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash,
                          publisher_mid_rate, publish_time, update_time)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        for r in rate_data:
            cursor.execute(add_product, r)

        logger_local.info('CCBH rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def get_CTIB_rate():
    try:
        index_url = 'http://www.ecitic.com/xml/ftp.txt'

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get(index_url, timeout=TIMEOUT)

        response = request_content()
        rate_data = []

        rt_data_list = response.text.split()
        for rt_data in rt_data_list:
            if rt_data[15:17] == '14':
                rate_data.append(['C10302',
                                  'CTIB',
                                  'USD',
                                  rt_data[33:36] + '.' + rt_data[36:38],
                                  rt_data[21:24] + '.' + rt_data[24:26],
                                  rt_data[45:48] + '.' + rt_data[48:50],
                                  rt_data[69:72] + '.' + rt_data[72:74],
                                  rt_data[57:60] + '.' + rt_data[60:62],
                                  format_datetime(rt_data[1:9] + rt_data[9:15])])
            elif rt_data[15:17] == '12':
                rate_data.append(['C10302',
                                  'CTIB',
                                  'GBP',
                                  rt_data[33:36] + '.' + rt_data[36:38],
                                  rt_data[21:24] + '.' + rt_data[24:26],
                                  rt_data[45:48] + '.' + rt_data[48:50],
                                  rt_data[69:72] + '.' + rt_data[72:74],
                                  rt_data[57:60] + '.' + rt_data[60:62],
                                  format_datetime(rt_data[1:9] + rt_data[9:15])])
            elif rt_data[15:17] == '51':
                rate_data.append(['C10302',
                                  'CTIB',
                                  'EUR',
                                  rt_data[33:36] + '.' + rt_data[36:38],
                                  rt_data[21:24] + '.' + rt_data[24:26],
                                  rt_data[45:48] + '.' + rt_data[48:50],
                                  rt_data[69:72] + '.' + rt_data[72:74],
                                  rt_data[57:60] + '.' + rt_data[60:62],
                                  format_datetime(rt_data[1:9] + rt_data[9:15])])
            elif rt_data[15:17] == '29':
                rate_data.append(['C10302',
                                  'CTIB',
                                  'AUD',
                                  rt_data[33:36] + '.' + rt_data[36:38],
                                  rt_data[21:24] + '.' + rt_data[24:26],
                                  rt_data[45:48] + '.' + rt_data[48:50],
                                  rt_data[69:72] + '.' + rt_data[72:74],
                                  rt_data[57:60] + '.' + rt_data[60:62],
                                  format_datetime(rt_data[1:9] + rt_data[9:15])])
            elif rt_data[15:17] == '27':
                rate_data.append(['C10302',
                                  'CTIB',
                                  'JPY',
                                  rt_data[32:33] + '.' + rt_data[33:37],
                                  rt_data[20:21] + '.' + rt_data[21:25],
                                  rt_data[44:45] + '.' + rt_data[45:49],
                                  rt_data[68:69] + '.' + rt_data[69:73],
                                  rt_data[56:57] + '.' + rt_data[57:61],
                                  format_datetime(rt_data[1:9] + rt_data[9:15])])


        # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10302'")
        # logger_local.info('CTIB ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""REPLACE INTO t_listing_rate
                        (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash,
                        publisher_mid_rate, publish_time, update_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        for r in rate_data:
            cursor.execute(add_product, r)

        logger_local.info('CTIB rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def get_BCOH_rate():
    try:
        index_url = 'http://www.bankcomm.com/BankCommSite/simple/cn/whpj/queryExchangeResult.do?type=simple'

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get(index_url, timeout=TIMEOUT)

        response = request_content()
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        publish_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"更新时间")))

        rate_data = []

        rate_list_tr = soup.find("table", class_="exchangeTab").find_all("tr", class_="data")

        for rates in rate_list_tr:
            r = rates.find_all("td")
            if r[0].string.strip() == "美元(USD/CNY)":
                rate_data.append(['C10301',
                                  'BCOH',
                                  'USD',
                                  r[2].string.strip(),
                                  r[4].string.strip(),
                                  r[3].string.strip(),
                                  r[5].string.strip(),
                                  format_datetime(publish_datetime)])
            elif r[0].string.strip() == "英镑(GBP/CNY)":
                rate_data.append(['C10301',
                                  'BCOH',
                                  'GBP',
                                  r[2].string.strip(),
                                  r[4].string.strip(),
                                  r[3].string.strip(),
                                  r[5].string.strip(),
                                  format_datetime(publish_datetime)])
            elif r[0].string.strip() == "欧元(EUR/CNY)":
                rate_data.append(['C10301',
                                  'BCOH',
                                  'EUR',
                                  r[2].string.strip(),
                                  r[4].string.strip(),
                                  r[3].string.strip(),
                                  r[5].string.strip(),
                                  format_datetime(publish_datetime)])
            elif r[0].string.strip() == "澳大利亚元(AUD/CNY)":
                rate_data.append(['C10301',
                                  'BCOH',
                                  'AUD',
                                  r[2].string.strip(),
                                  r[4].string.strip(),
                                  r[3].string.strip(),
                                  r[5].string.strip(),
                                  format_datetime(publish_datetime)])
            elif r[0].string.strip() == "日元(JPY/CNY)":
                rate_data.append(['C10301',
                                  'BCOH',
                                  'JPY',
                                  round(float(r[2].string.strip())/1000, 4),
                                  round(float(r[4].string.strip())/1000, 4),
                                  round(float(r[3].string.strip())/1000, 4),
                                  round(float(r[5].string.strip())/1000, 4),
                                  format_datetime(publish_datetime)])

        # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10301'")
        # logger_local.info('BCOH ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""REPLACE INTO t_listing_rate
                       (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash,
                       publish_time, update_time)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
        for r in rate_data:
            cursor.execute(add_product, r)

        logger_local.info('BCOH rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def get_EBBC_rate():
    try:
        index_url = 'http://www.cebbank.com/eportal/ui?pageId=477257'

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get(index_url, timeout=TIMEOUT)

        response = request_content()
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        publish_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"更新时间")))

        rate_data = []

        rate_list_tr = soup.find("table", class_="lczj_box").find_all("tr")

        for rates in rate_list_tr:
            r = rates.find_all("td")
            if r[0].string.strip() == "美元(USD)":
                rate_data.append(['C10303',
                                  'EBBC',
                                  'USD',
                                  r[3].string.strip(),
                                  r[1].string.strip(),
                                  r[4].string.strip(),
                                  r[2].string.strip(),
                                  r[5].string.strip(),
                                  format_datetime(publish_datetime)])
            elif r[0].string.strip() == "英镑(GBP)":
                rate_data.append(['C10303',
                                  'EBBC',
                                  'GBP',
                                  r[3].string.strip(),
                                  r[1].string.strip(),
                                  r[4].string.strip(),
                                  r[2].string.strip(),
                                  r[5].string.strip(),
                                  format_datetime(publish_datetime)])
            elif r[0].string.strip() == "欧元(EUR)":
                rate_data.append(['C10303',
                                  'EBBC',
                                  'EUR',
                                  r[3].string.strip(),
                                  r[1].string.strip(),
                                  r[4].string.strip(),
                                  r[2].string.strip(),
                                  r[5].string.strip(),
                                  format_datetime(publish_datetime)])
            elif r[0].string.strip() == "澳大利亚元(AUD)":
                rate_data.append(['C10303',
                                  'EBBC',
                                  'AUD',
                                  r[3].string.strip(),
                                  r[1].string.strip(),
                                  r[4].string.strip(),
                                  r[2].string.strip(),
                                  r[5].string.strip(),
                                  format_datetime(publish_datetime)])
            elif r[0].string.strip() == "日元(JPY)":
                rate_data.append(['C10303',
                                  'EBBC',
                                  'JPY',
                                  r[3].string.strip(),
                                  r[1].string.strip(),
                                  r[4].string.strip(),
                                  r[2].string.strip(),
                                  r[5].string.strip(),
                                  format_datetime(publish_datetime)])

        # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10303'")
        # logger_local.info('EBBC ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""REPLACE INTO t_listing_rate
                       (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash,
                       publisher_mid_rate, publish_time, update_time)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        for r in rate_data:
            cursor.execute(add_product, r)

        logger_local.info('EBBC rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def get_IBCN_rate():
    try:
        entry = 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery.do'
        index_url = 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery!list.do?_search=false' \
                    '&dataSet.rows=100&dataSet.page=1&dataSet.sidx=&dataSet.sord=asc'
        referer = 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery.do'

        # 第一次请求页面并提取更新日期
        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get(entry, timeout=TIMEOUT)
        r1 = request_content()
        soup = bs4.BeautifulSoup(r1.text, "html.parser")
        publish_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"日期：")))

        # 第二次请求并传输cookie, 获取返回的json字符串
        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get(index_url, cookies=r1.cookies, timeout=TIMEOUT)
        r2 = request_content()
        data_string = json.loads(r2.text)
        rate_data = []

        # 轮询找到美元, 写入product_data后跳出
        for data_row in data_string["rows"]:
            if data_row["cell"][1] in ['USD', 'GBP', 'EUR', 'AUD', 'JPY']:
                rate_data.append(['C10309',
                             'IBCN',
                             data_row["cell"][1],
                             data_row["cell"][4],
                             data_row["cell"][6],
                             data_row["cell"][5],
                             data_row["cell"][7],
                             data_row["cell"][3],
                             format_datetime(publish_datetime)])

        # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10309'")
        # logger_local.info('IBCN ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""REPLACE INTO t_listing_rate
                       (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash,
                       publisher_mid_rate, publish_time, update_time)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        for r in rate_data:
            cursor.execute(add_product, r)

        logger_local.info('IBCN rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def get_SPDB_rate():
    try:
        index_url = 'http://ebank.spdb.com.cn/net/QueryExchangeRate.do'

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get(index_url, timeout=TIMEOUT)

        response = request_content()
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        publish_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"更新时间")))

        rate_data = []

        rate_list_tr = soup.find("table", class_="table_comm").find_all("tr")

        for rates in rate_list_tr:
            r = rates.find_all("td", class_="td20ce03")
            if len(r) == 5 and r[0].string.strip() == u'美元\xa0USD':
                rate_data.append(['C10310',
                                  'SPDB',
                                  'USD',
                                  r[2].string.strip(),
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[4].string.strip(),
                                  r[1].string.strip(),
                                  format_datetime(publish_datetime)])
            elif len(r) == 5 and r[0].string.strip() == u'英镑\xa0GBP':
                rate_data.append(['C10310',
                                  'SPDB',
                                  'GBP',
                                  r[2].string.strip(),
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[4].string.strip(),
                                  r[1].string.strip(),
                                  format_datetime(publish_datetime)])
            elif len(r) == 5 and r[0].string.strip() == u'欧元\xa0EUR':
                rate_data.append(['C10310',
                                  'SPDB',
                                  'EUR',
                                  r[2].string.strip(),
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[4].string.strip(),
                                  r[1].string.strip(),
                                  format_datetime(publish_datetime)])
            elif len(r) == 5 and r[0].string.strip() == u'澳大利亚元\xa0AUD':
                rate_data.append(['C10310',
                                  'SPDB',
                                  'AUD',
                                  r[2].string.strip(),
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[4].string.strip(),
                                  r[1].string.strip(),
                                  format_datetime(publish_datetime)])
            elif len(r) == 5 and r[0].string.strip() == u'日元\xa0JPY':
                rate_data.append(['C10310',
                                  'SPDB',
                                  'JPY',
                                  round(float(r[2].string.strip().replace(",", ""))/1000, 4),
                                  round(float(r[3].string.strip().replace(",", ""))/1000, 4),
                                  round(float(r[4].string.strip().replace(",", ""))/1000, 4),
                                  round(float(r[4].string.strip().replace(",", ""))/1000, 4),
                                  round(float(r[1].string.strip().replace(",", ""))/1000, 4),
                                  format_datetime(publish_datetime)])

        # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10310'")
        # logger_local.info('SPDB ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""REPLACE INTO t_listing_rate
                        (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash,
                        publisher_mid_rate, publish_time, update_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        for r in rate_data:
            cursor.execute(add_product, r)

        logger_local.info('SPDB rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def get_DESZ_rate():
    try:
        index_url = 'https://bank.pingan.com.cn/ibp/portal/exchange/qryExchangeList.do'
        rate_data = []

        for currency in ['USD', 'GBP', 'EUR', 'AUD', 'JPY']:
            @retry(stop_max_attempt_number=10, wait_fixed=2000)
            def request_content():
                return requests.post(index_url,
                                     data={"realFlag": "1", "currencyCode": currency, "pageIndex": "1"},
                                     timeout=TIMEOUT)

            response = request_content()
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            publish_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"时间：")))

            rates = soup.find_all("td", class_="tac")

            rate_data.append(['C10307',
                              'DESZ',
                              currency,
                              rates[2].string.strip(),
                              rates[3].string.strip(),
                              rates[4].string.strip(),
                              rates[4].string.strip(),
                              rates[5].string.strip(),
                              rates[1].string.strip(),
                              format_datetime(publish_datetime)])

        # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10307'")
        # logger_local.info('DESZ ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""REPLACE INTO t_listing_rate
                        (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash, mid_rate,
                        publisher_mid_rate, publish_time, update_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        for r in rate_data:
            cursor.execute(add_product, r)

        logger_local.info('DESZ rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def get_BKSH_rate():
    try:
        index_url = 'http://www.bankofshanghai.com/WebServlet?go=bank_sellfund_pg_Banking&code=whpj'

        # response = requests.post(index_url, data={"realFlag": "1", "currencyCode": "USD", "pageIndex": "1"})
        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get(index_url, timeout=TIMEOUT)

        response = request_content()
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        rate_data = []
        rate_list_tr = soup.find("table", class_="table01").tbody.find_all("tr")

        for rates in rate_list_tr:
            r = rates.find_all("td")
            if r[1].string.strip() in ['USD', 'GBP', 'EUR', 'AUD']:
                rate_data.append(['C10912',
                                  'BKSH',
                                  r[1].string.strip(),
                                  r[4].string.strip(),
                                  r[6].string.strip(),
                                  r[5].string.strip(),
                                  r[5].string.strip(),
                                  r[3].string.strip(),
                                  format_datetime(r[7].string.strip())])
            elif r[1].string.strip() == 'JPY':
                rate_data.append(['C10912',
                                  'BKSH',
                                  r[1].string.strip(),
                                  round(float(r[4].string.strip())/1000, 4),
                                  round(float(r[6].string.strip())/1000, 4),
                                  round(float(r[5].string.strip())/1000, 4),
                                  round(float(r[5].string.strip())/1000, 4),
                                  round(float(r[3].string.strip())/1000, 4),
                                  format_datetime(r[7].string.strip())])

        # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10912'")
        # logger_local.info('BKSH ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""REPLACE INTO t_listing_rate
                        (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash,
                        publisher_mid_rate, publish_time, update_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        for r in rate_data:
            cursor.execute(add_product, r)

        logger_local.info('BKSH rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def get_BOBJ_rate():
    try:
        index_url = 'http://www.bankofbeijing.com.cn/personal/whpj.aspx'

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get(index_url, timeout=TIMEOUT)

        response = request_content()
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        publish_datetime = ''
        strings = soup.find("form", id="form1")
        for string in strings.stripped_strings:
            publish_datetime = unicode(string)
            break

        rate_data = []
        rate_list_tr = soup.find("table", id="GridView1").find_all("tr")

        for rates in rate_list_tr:
            r = rates.find_all("td")
            if r[0].string.strip() in ['USD/CNY', 'GBP/CNY', 'EUR/CNY', 'AUD/CNY', 'JPY/CNY']:
                rate_data.append(['C10802',
                                  'BOBJ',
                                  r[0].string.strip()[:3],
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  r[5].string.strip(),
                                  r[7].string.strip(),
                                  r[6].string.strip(),
                                  format_datetime(publish_datetime)])

        if publish_datetime == LOCALDATE:
            # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10802'")
            # logger_local.info('BOBJ ' + unicode(cursor.rowcount) + ' rows deleted')

            add_product = ("""REPLACE INTO t_listing_rate
                            (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash,
                            mid_rate, publisher_mid_rate, publish_time, update_time)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
            for r in rate_data:
                cursor.execute(add_product, r)

            logger_local.info('BOBJ rate imported.')
        else:
            logger_local.info('BOBJ rate not updated.')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))

def get_HXBJ_rate():
    try:
        index_url = 'https://sbank.hxb.com.cn/gateway/forexquote.jsp'

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get(index_url, timeout=TIMEOUT)

        response = request_content()
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        rate_data = []
        rate_list_tr = soup.find_all("tr", class_="table_list_body_odd")

        for rates in rate_list_tr:
            r = rates.find_all("td")
            if r[0].string.strip() in ['USDCNY', 'GBPCNY', 'EURCNY', 'AUDCNY', 'JPYCNY']:
                rate_data.append(['C10304',
                                  'HXBJ',
                                  r[0].string.strip()[:3],
                                  r[2].string.strip(),
                                  r[3].string.strip(),
                                  r[4].string.strip(),
                                  r[4].string.strip(),
                                  r[5].string.strip(),
                                  format_datetime(r[6].string.strip())])

        # cursor.execute("DELETE FROM t_listing_rate WHERE publisher_code='C10304'")
        # logger_local.info('HXBJ ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""REPLACE INTO t_listing_rate
                        (publisher_code, publisher_name, currency, bid_remit, bid_cash, ask_remit, ask_cash,
                        publisher_mid_rate, publish_time, update_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        for r in rate_data:
            cursor.execute(add_product, r)

        logger_local.info('HXBJ rate imported')

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))

# def show_stats(options):
#     pool = Pool(8)
#     page_urls = get_CW_product()
#     results = pool.map(get_data, page_urls)


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

        get_CMHO_rate()
        get_ICBC_rate()
        get_BCHO_rate()
        get_ABCI_rate()
        get_CCBH_rate()
        get_CTIB_rate()
        get_BCOH_rate()
        get_EBBC_rate()
        get_IBCN_rate()
        get_SPDB_rate()
        get_DESZ_rate()
        get_BKSH_rate()
        # get_BOBJ_rate()
        get_HXBJ_rate()

#        generate_json()


        cnx.commit()
        cursor.close()
        cnx.close()
        logger_local.info('All rates retrieved\n\n')
