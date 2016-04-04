# -*- coding: utf-8 -*-
import sys

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


def generate_AUD_rates_json():
    rate_list = {"total_rec": "", "list": []}
    query = """select count(*) from v_listing_rate_aud"""
    cursor.execute(query)
    for (total_rec,) in cursor:
        rate_list["total_rec"] = total_rec

    query = """select cn_short_name, bid_remit, bid_cash, ask_remit, ask_cash, publish_time
               from v_listing_rate_aud"""
    cursor.execute(query)
    rate_list["currency"] = "AUD"
    for (cn_short_name, bid_remit, bid_cash, ask_remit, ask_cash, publish_time) in cursor:
        rate_list["list"].append({})
        rate_list["list"][-1]["publisher"] = cn_short_name
        rate_list["list"][-1]["bid_remit"] = bid_remit
        rate_list["list"][-1]["bid_cash"] = bid_cash
        rate_list["list"][-1]["ask_remit"] = ask_remit
        rate_list["list"][-1]["ask_cash"] = ask_cash
        rate_list["list"][-1]["publish_time"] = publish_time

    pprint(rate_list)

    with codecs.open("output/rate_list_AUD.json", "w", encoding="utf-8") as outfile:
        json.dump(rate_list, outfile, ensure_ascii=False)


def generate_USD_rates_json():
    rate_list = {"total_rec": "", "list": []}
    query = """select count(*) from v_listing_rate_usd"""
    cursor.execute(query)
    for (total_rec,) in cursor:
        rate_list["total_rec"] = total_rec

    query = """select cn_short_name, bid_remit, bid_cash, ask_remit, ask_cash, publish_time
               from v_listing_rate_usd"""
    cursor.execute(query)
    rate_list["currency"] = "USD"
    for (cn_short_name, bid_remit, bid_cash, ask_remit, ask_cash, publish_time) in cursor:
        rate_list["list"].append({})
        rate_list["list"][-1]["publisher"] = cn_short_name
        rate_list["list"][-1]["bid_remit"] = bid_remit
        rate_list["list"][-1]["bid_cash"] = bid_cash
        rate_list["list"][-1]["ask_remit"] = ask_remit
        rate_list["list"][-1]["ask_cash"] = ask_cash
        rate_list["list"][-1]["publish_time"] = publish_time

    pprint(rate_list)

    with codecs.open("output/rate_list_USD.json", "w", encoding="utf-8") as outfile:
        json.dump(rate_list, outfile, ensure_ascii=False)


def generate_EUR_rates_json():
    rate_list = {"total_rec": "", "list": []}
    query = """select count(*) from v_listing_rate_eur"""
    cursor.execute(query)
    for (total_rec,) in cursor:
        rate_list["total_rec"] = total_rec

    query = """select cn_short_name, bid_remit, bid_cash, ask_remit, ask_cash, publish_time
               from v_listing_rate_eur"""
    cursor.execute(query)
    rate_list["currency"] = "EUR"
    for (cn_short_name, bid_remit, bid_cash, ask_remit, ask_cash, publish_time) in cursor:
        rate_list["list"].append({})
        rate_list["list"][-1]["publisher"] = cn_short_name
        rate_list["list"][-1]["bid_remit"] = bid_remit
        rate_list["list"][-1]["bid_cash"] = bid_cash
        rate_list["list"][-1]["ask_remit"] = ask_remit
        rate_list["list"][-1]["ask_cash"] = ask_cash
        rate_list["list"][-1]["publish_time"] = publish_time

    pprint(rate_list)

    with codecs.open("output/rate_list_EUR.json", "w", encoding="utf-8") as outfile:
        json.dump(rate_list, outfile, ensure_ascii=False)


def generate_GBP_rates_json():
    rate_list = {"total_rec": "", "list": []}
    query = """select count(*) from v_listing_rate_gbp"""
    cursor.execute(query)
    for (total_rec,) in cursor:
        rate_list["total_rec"] = total_rec

    query = """select cn_short_name, bid_remit, bid_cash, ask_remit, ask_cash, publish_time
               from v_listing_rate_gbp"""
    cursor.execute(query)
    rate_list["currency"] = "GBP"
    for (cn_short_name, bid_remit, bid_cash, ask_remit, ask_cash, publish_time) in cursor:
        rate_list["list"].append({})
        rate_list["list"][-1]["publisher"] = cn_short_name
        rate_list["list"][-1]["bid_remit"] = bid_remit
        rate_list["list"][-1]["bid_cash"] = bid_cash
        rate_list["list"][-1]["ask_remit"] = ask_remit
        rate_list["list"][-1]["ask_cash"] = ask_cash
        rate_list["list"][-1]["publish_time"] = publish_time

    pprint(rate_list)

    with codecs.open("output/rate_list_GBP.json", "w", encoding="utf-8") as outfile:
        json.dump(rate_list, outfile, ensure_ascii=False)


def generate_wmp_json():
    """
    名称 - 期限 - 非保本/保本
    发售时间 start end
    预期收益
    当月平均
    美元12月定存
    起购金额
    """
    prod_list = {"total_rec": "", "list": []}
    query = """select count(*) from t_product where data_source='MN' and status='在售'
               and date(update_time)=(select max(date(update_time)) from zyq.t_product where data_source='MN')
               order by tenor"""
    cursor.execute(query)
    for (total_rec,) in cursor:
        prod_list["total_rec"] = total_rec

    query = """SELECT issuer_name, prod_name, tenor_desc, open_start_date, open_end_date,
               expected_highest_yield, update_time
               FROM t_product WHERE data_source='MN' AND status='在售'
               AND date(update_time)=(SELECT max(date(update_time)) FROM t_product WHERE data_source='MN')
               ORDER BY tenor"""

    cursor.execute(query)
    for (issuer_name, prod_name, tenor_desc, open_start_date, open_end_date, update_time) in cursor:
        prod_list["list"].append({})
        prod_list["list"][-1]["issuer_name"] = issuer_name
        prod_list["list"][-1]["prod_name"] = prod_name
        prod_list["list"][-1]["tenor_desc"] = tenor_desc
        prod_list["list"][-1]["open_start_date"] = open_start_date
        prod_list["list"][-1]["open_end_date"] = open_end_date
        prod_list["list"][-1]["update_time"] = update_time

    with codecs.open("output/selected_wmp.json", "w", encoding="utf-8") as outfile:
        json.dump(prod_list, outfile, ensure_ascii=False)


if __name__ == '__main__':
    logger_local.info('====================================================================================')
    logger_local.info('generator started')
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

        generate_USD_rates_json()
        generate_AUD_rates_json()
        generate_EUR_rates_json()
        generate_GBP_rates_json()

        cnx.commit()
        cursor.close()
        cnx.close()
        logger_local.info('All rates retrieved\n\n')