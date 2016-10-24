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


def download_indicator(region):
    try:
        # use requests.session to handle cookies etc.
        s = requests.session()

        # get EVENTVALIDATION and VIEWSTATE for asp validation check
        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return s.get('http://analytics.tradingeconomics.com/',
                         timeout=TIMEOUT)
        r1 = request_content()
        soup = bs4.BeautifulSoup(butils.bs_preprocess(r1.text), "html.parser")
        __EVENTVALIDATION = soup.find("input", id="__EVENTVALIDATION")
        __VIEWSTATE = soup.find("input", id="__VIEWSTATE")
        print "EVENTVALIDATION:", __EVENTVALIDATION["value"]
        print "VIEWSTATE:", __VIEWSTATE["value"]

        # login
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
        request_content()

        # load default page(United States) and get EVENTVALIDATION/VIEWSTATE
        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return s.get('http://analytics.tradingeconomics.com/export/export-data-national.aspx',
                         timeout=TIMEOUT)
        response = request_content()
        soup = bs4.BeautifulSoup(butils.bs_preprocess(response.text), "html.parser")
        __EVENTVALIDATION = soup.find("input", id="__EVENTVALIDATION")
        __VIEWSTATE = soup.find("input", id="__VIEWSTATE")

        # jump to region page
        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return s.post('http://analytics.tradingeconomics.com/export/export-data-national.aspx',
                          timeout=TIMEOUT,
                          data={"__EVENTTARGET": "ctl00$ContentPlaceHolder1$ExportDataUC1$DropDownList1",
                                "__VIEWSTATE": __VIEWSTATE["value"],
                                "__EVENTVALIDATION": __EVENTVALIDATION["value"],
                                "ctl00$ContentPlaceHolder1$ExportDataUC1$DropDownList1": region,
                                "ctl00$ContentPlaceHolder1$ExportDataUC1$DropDownList2": "All Indicators"})
        response = request_content()
        soup = bs4.BeautifulSoup(butils.bs_preprocess(response.text), "html.parser")

        csv_table = soup.find("table", class_="table table-condensed table-striped table-hover")
        csv_list = csv_table.find_all("tr")
        del csv_list[0]

        print len(csv_list)
        for c in csv_list:
            url = c.find("span", class_="label label-info").a["href"]
            print url

        for c in csv_list:
            url = c.find("span", class_="label label-info").a["href"]
            r = s.get("http://analytics.tradingeconomics.com/export/"+url)
            # get default filename from url
            try:
                filename = re.findall("filename=(.+)", r.headers['Content-Disposition'])
                fn = "indicator_output/%s/%s" % (region, filename[0])
                # if path not exists, create it
                if not os.path.exists(os.path.dirname(fn)):
                    try:
                        os.makedirs(os.path.dirname(fn))
                    except OSError as exc:
                        # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise

                print "downloading "+filename[0]
                with open(fn, "wb") as code:
                    code.write(r.content)

            except KeyError:
                print "Failed parsing filename: "+url

    except:
        logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))


def download_US_indicator():
    try:
        region = 'United States'
        # use requests.session to handle cookies etc.
        s = requests.session()

        # get EVENTVALIDATION and VIEWSTATE for asp validation check
        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return s.get('http://analytics.tradingeconomics.com/',
                         timeout=TIMEOUT)
        r1 = request_content()
        soup = bs4.BeautifulSoup(butils.bs_preprocess(r1.text), "html.parser")
        __EVENTVALIDATION = soup.find("input", id="__EVENTVALIDATION")
        __VIEWSTATE = soup.find("input", id="__VIEWSTATE")
        print "EVENTVALIDATION:", __EVENTVALIDATION["value"]
        print "VIEWSTATE:", __VIEWSTATE["value"]

        # login
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
        request_content()

        # load default page(United States) and get EVENTVALIDATION/VIEWSTATE
        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return s.get('http://analytics.tradingeconomics.com/export/export-data-national.aspx',
                         timeout=TIMEOUT)
        response = request_content()
        soup = bs4.BeautifulSoup(butils.bs_preprocess(response.text), "html.parser")
        __EVENTVALIDATION = soup.find("input", id="__EVENTVALIDATION")
        __VIEWSTATE = soup.find("input", id="__VIEWSTATE")

        csv_table = soup.find("table", class_="table table-condensed table-striped table-hover")
        csv_list = csv_table.find_all("tr")
        del csv_list[0]

        print len(csv_list)
        for c in csv_list:
            url = c.find("span", class_="label label-info").a["href"]
            print url

        for c in csv_list:
            url = c.find("span", class_="label label-info").a["href"]
            r = s.get("http://analytics.tradingeconomics.com/export/"+url)
            # get default filename from url
            try:
                filename = re.findall("filename=(.+)", r.headers['Content-Disposition'])
                fn = "indicator_output/%s/%s" % (region, filename[0])
                # if path not exists, create it
                if not os.path.exists(os.path.dirname(fn)):
                    try:
                        os.makedirs(os.path.dirname(fn))
                    except OSError as exc:
                        # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise

                print "downloading "+filename[0]
                with open(fn, "wb") as code:
                    code.write(r.content)

            except KeyError:
                print "Failed parsing filename: "+url

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

        # G20
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
        download_US_indicator()
        # download_indicator('European Union')
        # download_indicator("Euro Area")

        # other
        # download_indicator('Spain')
        # download_indicator('New Zealand')
        # download_indicator('Thailand')
        # download_indicator('Vietnam')
        # download_indicator('Singapore')
        # download_indicator('Malaysia')

        # others other
        # download_indicator('Chile')

        cnx.commit()
        cursor.close()
        cnx.close()
        logger_local.info('All indicators retrieved\n\n')
