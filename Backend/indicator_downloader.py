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


def log_in():
    try:
        s = requests.session()

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return s.get('http://analytics.tradingeconomics.com/',
                         timeout=TIMEOUT)
        r1 = request_content()
        soup = bs4.BeautifulSoup(butils.bs_preprocess(r1.text), "html.parser")
        __EVENTVALIDATION = soup.find("input", id="__EVENTVALIDATION")
        __VIEWSTATE = soup.find("input", id="__VIEWSTATE")
        print __EVENTVALIDATION["value"]
        print __VIEWSTATE["value"]

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return s.post('http://analytics.tradingeconomics.com/',
                                 timeout=TIMEOUT,
                                 data={"__VIEWSTATE": __VIEWSTATE["value"],
                                       "__EVENTVALIDATION": __EVENTVALIDATION["value"],
                                       "ctl00$ContentPlaceHolder1$LoginView1$LoginUC1$Login1$UserName": "chenjiahua@hotmail.com",
                                       "ctl00$ContentPlaceHolder1$LoginView1$LoginUC1$Login1$Password": "123456",
                                       "ctl00$ContentPlaceHolder1$LoginView1$LoginUC1$Login1$RememberMe": "on",
                                       "ctl00$ContentPlaceHolder1$LoginView1$LoginUC1$Login1$LoginButton": "Log In"})
        r2 = request_content()

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return s.get('http://analytics.tradingeconomics.com/export/export-data-national.aspx',
                         timeout=TIMEOUT)

        response = request_content()
        soup = bs4.BeautifulSoup(butils.bs_preprocess(response.text), "html.parser")
        print response.text

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def get_indicator_link_by_country():
    try:
        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get('http://www.tradingeconomics.com/countries', timeout=TIMEOUT)

        response = request_content()

        soup = bs4.BeautifulSoup(butils.bs_preprocess(response.text), "html.parser")

        __indicator_url = []
        __indicator_links = soup.find_all("a", class_="country")

        for i in __indicator_links:
            __indicator_url.append([i.get_text(), u"http://www.tradingeconomics.com"+i["href"]])

        return __indicator_url

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def download_trading_indicator(region):
    try:
        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.post("http://analytics.tradingeconomics.com/export/export-data-national.aspx",
                                 timeout=TIMEOUT,
                                 data={"ctl00$ContentPlaceHolder1$ExportDataUC1$DropDownList1": region,
                                       "ctl00$ContentPlaceHolder1$ExportDataUC1$DropDownList2": "All Indicators"})

        response = request_content()

        # filename = "indicator_download/%s.html" % (region,)
        # if not os.path.exists(os.path.dirname(filename)):
        #     try:
        #         os.makedirs(os.path.dirname(filename))
        #     except OSError as exc:  # Guard against race condition
        #         if exc.errno != errno.EEXIST:
        #             raise
        # file = open(filename, "w")
        # file.write(response.content)
        # file.close()

        # response.raise_for_status()  # ensure we notice bad responses
        # file = open("indicator_output/%s/%s.html" % (LOCALDATE, region), "w")
        # file.write(response.content)
        # file.close()

        soup = bs4.BeautifulSoup(butils.bs_preprocess(response.text), "html.parser")
        print soup

        # publish_date = filter(unicode.isdigit, soup.find(text=re.compile(u"当前日期")))

        # indicator_div = soup.find_all("div", class_="table-responsive panel panel-default")
        # indicator_list = indicator_div[-1].find("table", class_="table table-condensed table-hover")
        #
        # add_product = ("""INSERT INTO wm_data
        #                   (region, category, indicator, reference, value, previous_value, unit, frequency, update_time)
        #                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())
        #                   ON DUPLICATE KEY UPDATE value=%s, previous_value=%s, update_time=now()
        #                """)
        #
        # current_category = None
        # for child in indicator_list.children:
        #     if child.name == "thead":
        #         current_category = child.tr.th.span.text.strip()
        #     else:
        #         indicator_table = child.find_all("td")

                # indicator_category = current_category
                # indicator_name = indicator_table[0].a.get_text()
                # indicator_value_and_unit = indicator_table[1].get_text()
                # indicator_reference = indicator_table[2].span.get_text()
                # indicator_previous_value = indicator_table[3].get_text()
                # indicator_range = indicator_table[4].get_text()
                # indicator_frequency = indicator_table[5].get_text()
                #
                # rs = re.search(r"^[\d.-]+", indicator_value_and_unit)
                # indicator_value = rs.group(0)
                # indicator_unit = re.sub(r"^[\d.-]+", "", indicator_value_and_unit)
                # print indicator_value_and_unit, indicator_value, indicator_unit

                # cursor.execute(add_product, (region,
                #                              indicator_category,
                #                              indicator_name,
                #                              indicator_reference,
                #                              indicator_value,
                #                              indicator_previous_value,
                #                              indicator_unit,
                #                              indicator_frequency,
                #                              indicator_value,
                #                              indicator_previous_value))

        # pprint(indicators)

        # DB manipulation:
        # add_product = ("""INSERT INTO wm_data
        #                   (region, category, indicator, reference, value, previous_value, unit, frequency,
        #                   update_time)
        #                   VALUES (%s, %s, %s, %s, %s, %s, %s, now())
        #                   ON DUPLICATE KEY UPDATE value=%s, previous_value=%s, update_time=now()
        #                """)
        #
        # for i in indicators:
        #     cursor.execute(add_product, (region, i[0], i[1], i[3], i[2], i[4], i[5], i[2], i[4]))

        logger_local.info('All %s indicators retrieved' % region)

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


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

        log_in()

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
        logger_local.info('All indicators retrieved\n\n')
