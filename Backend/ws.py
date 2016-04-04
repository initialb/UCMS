# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, request

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
# import lib.butils.finutils
from lib.butils import decode
from lib.butils import fix_json
from lib.butils import ppprint
from lib.butils.pprint import pprint

TIMEOUT = 10
LOCALDATE = time.strftime('%Y%m%d', time.localtime(time.time()))
TIMESTAMP = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
LOGNAME = 'log/rates_ws_' + LOCALDATE + '.log'

# # initialize root logger to write verbose log file
# logging.basicConfig(level=logging.DEBUG,
#                     filename="log/price_parser_" + LOCALDATE + ".verbose.log",
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# initialize a local logger
logger_local = logging.getLogger("ucms.birdie.ws.rates")
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


app = Flask(__name__)


@app.route('/ucms/api/v1.0/weixin/listingrate/<string:currency>', methods=['GET'])
def get_listing_rate(currency):
    cursor = cnx.cursor()

    rate_list = {"total_rec": "", "list": []}
    total_rec = ""

    query = "SELECT count(*) FROM t_issuer, t_listing_rate\
             WHERE t_issuer.issuer_code=t_listing_rate.publisher_code and t_listing_rate.currency='%s'" % currency

    cursor.execute(query)
    for (total_rec,) in cursor:
        rate_list["total_rec"] = total_rec

    if total_rec == 0:
        logger_local.info('Not found')
        abort(404)

    query = "SELECT\
             t_issuer.cn_short_name,\
             t_listing_rate.bid_remit, t_listing_rate.bid_cash, t_listing_rate.ask_remit, t_listing_rate.ask_cash,\
             t_listing_rate.publish_time\
             FROM t_issuer, t_listing_rate\
             WHERE t_issuer.issuer_code=t_listing_rate.publisher_code and t_listing_rate.currency='%s'" % currency
    cursor.execute(query)
    rate_list["timestamp"] = TIMESTAMP
    rate_list["currency"] = currency
    rate_list["currencyname"] = decode(currency, "USD", u"美元", "GBP", u"英镑", "AUD", u"澳元", "EUR", u"欧元", "")
    for (cn_short_name, bid_remit, bid_cash, ask_remit, ask_cash, publish_time) in cursor:
        rate_list["list"].append({})
        rate_list["list"][-1]["publisher"] = cn_short_name
        rate_list["list"][-1]["bid_remit"] = bid_remit
        rate_list["list"][-1]["bid_cash"] = bid_cash
        rate_list["list"][-1]["ask_remit"] = ask_remit
        rate_list["list"][-1]["ask_cash"] = ask_cash
        rate_list["list"][-1]["publish_time"] = publish_time

    query = "SELECT max(bid_remit), max(bid_cash), min(ask_remit), min(ask_cash)\
             FROM t_listing_rate\
             WHERE currency='%s'" % currency
    cursor.execute(query)
    for (max_bid_remit, max_bid_cash, min_ask_remit, min_ask_cash) in cursor:
        for r in rate_list["list"]:
            if r["bid_remit"] == max_bid_remit:
                r["bid_remit"] = "*"+r["bid_remit"]
            if r["bid_cash"] == max_bid_cash:
                r["bid_cash"] = "*"+r["bid_cash"]
            if r["ask_remit"] == min_ask_remit:
                r["ask_remit"] = "*"+r["ask_remit"]
            if r["ask_cash"] == min_ask_cash:
                r["ask_cash"] = "*"+r["ask_cash"]

    cnx.commit()
    cursor.close()
    logger_local.info('Rates requested for %s \n\n' % currency)

    pprint(rate_list)

    # return jsonify(rate_list)
    return json.dumps(rate_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/selectedwmp/<string:currency>', methods=['GET'])
def get_selected_wmp(currency):
    cursor = cnx.cursor()

    total_rec = None
    prod_list = {"currency": currency,
                 "timestamp": TIMESTAMP,
                 "preservable": "ALL",
                 "tenor_group": []
                }

    query = u"SELECT count(*)\
             FROM t_product\
             WHERE status='在售' and currency='%s'" % currency
    cursor.execute(query)
    for (ttl_rec,) in cursor:
        total_rec = ttl_rec

    if total_rec == 0:
        logger_local.info('Not found')
        abort(404)

    preservable = request.args.get('preservable', '')

    if preservable == "N":
        # 非保本
        ty_list =[]
        prod_list["preservable"] = "N"
        query = u"SELECT max(expected_highest_yield),round(tenor/30)\
                  FROM t_product\
                  WHERE status='在售' and preservable='非保本' and currency='%s' group by round(tenor/30)" % currency
        cursor.execute(query)
        for (expected_highest_yield, tenor_desc) in cursor:
            ty_list.append([tenor_desc, expected_highest_yield])

        # 按期限
        for ty in ty_list:
            prod_list["tenor_group"].append({"tenor": int(ty[0]), "list": []})
            query = u"SELECT prod_name, issuer_name, open_start_date, open_end_date, expected_highest_yield, preservable, starting_amount\
                      FROM t_product\
                      WHERE status='在售' and preservable='非保本' and currency='%s' and expected_highest_yield='%s' and round(tenor/30)='%s'" % (currency, ty[1], ty[0])
            cursor.execute(query)
            for (prod_name, issuer_name, open_start_date, open_end_date, expected_highest_yield, preservable, starting_amount) in cursor:
                prod_list["tenor_group"][-1]["list"].append({"prod_name": prod_name,
                                                             "issuer_name": issuer_name,
                                                             "open_start_date": open_start_date,
                                                             "open_end_date": open_end_date,
                                                             "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield)*100,),
                                                             "starting_amount": '%.2f' % float(starting_amount)})
            #计算月平均
            query = u"SELECT avg(bank_avg) as avg FROM\
                        (SELECT issuer_name,avg(expected_highest_yield) as bank_avg FROM zyq.t_product\
                        WHERE (date_sub(curdate(), INTERVAL 30 DAY)<=date(open_start_date) or (open_start_date='每天' and status='在售'))\
                        AND currency='%s' AND round(tenor/30)='%s' AND preservable='非保本'\
                        GROUP BY issuer_name) t" % (currency, ty[0])
            cursor.execute(query)
            for (cursor_avg,) in cursor:
                prod_list["tenor_group"][-1]["industry_1m_avg_yield"] = '%.4f%%' % (float(cursor_avg)*100,)

    elif preservable == "Y":
        # 保本
        ty_list =[]
        prod_list["preservable"] = "Y"
        query = u"SELECT max(expected_highest_yield),round(tenor/30)\
                  FROM t_product\
                  WHERE status='在售' and preservable='保本' and currency='%s' group by round(tenor/30)" % currency
        cursor.execute(query)
        for (expected_highest_yield, tenor_desc) in cursor:
            ty_list.append([tenor_desc, expected_highest_yield])

        for ty in ty_list:
            prod_list["tenor_group"].append({"tenor": int(ty[0]), "list" :[]})
            query = u"SELECT prod_name, issuer_name, open_start_date, open_end_date, expected_highest_yield, preservable, starting_amount\
                      FROM t_product\
                      WHERE status='在售' and preservable='保本' and currency='%s' and expected_highest_yield='%s' and round(tenor/30)='%s'" % (currency, ty[1], ty[0])
            cursor.execute(query)
            for (prod_name, issuer_name, open_start_date, open_end_date, expected_highest_yield, preservable, starting_amount) in cursor:
                prod_list["tenor_group"][-1]["list"].append({"prod_name": prod_name,
                                                             "issuer_name": issuer_name,
                                                             "open_start_date": open_start_date,
                                                             "open_end_date": open_end_date,
                                                             "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield)*100,),
                                                             "starting_amount": '%.2f' % float(starting_amount)})
            #计算月平均
            query = u"SELECT avg(bank_avg) as avg FROM\
                        (SELECT issuer_name,avg(expected_highest_yield) as bank_avg FROM zyq.t_product\
                        WHERE (date_sub(curdate(), INTERVAL 30 DAY)<=date(open_start_date) or (open_start_date='每天' and status='在售'))\
                        AND currency='%s' AND round(tenor/30)='%s' AND preservable='保本'\
                        GROUP BY issuer_name) t" % (currency, ty[0])
            cursor.execute(query)
            for (cursor_avg,) in cursor:
                prod_list["tenor_group"][-1]["industry_1m_avg_yield"] = '%.4f%%' % (float(cursor_avg)*100,)


    else:
         # 全部
        ty_list =[]
        query = u"SELECT max(expected_highest_yield),round(tenor/30)\
                  FROM t_product\
                  WHERE status='在售' and currency='%s' group by round(tenor/30)" % currency
        cursor.execute(query)
        for (expected_highest_yield, tenor_desc) in cursor:
            ty_list.append([tenor_desc, expected_highest_yield])

        for ty in ty_list:
            prod_list["tenor_group"].append({"tenor": int(ty[0]), "list" :[]})
            query = u"SELECT prod_name, issuer_name, open_start_date, open_end_date, expected_highest_yield, preservable, starting_amount\
                      FROM t_product\
                      WHERE status='在售' and currency='%s' and expected_highest_yield='%s' and round(tenor/30)='%s'" % (currency, ty[1], ty[0])
            cursor.execute(query)
            for (prod_name, issuer_name, open_start_date, open_end_date, expected_highest_yield, preservable, starting_amount) in cursor:
                prod_list["tenor_group"][-1]["list"].append({"prod_name": prod_name,
                                                             "issuer_name": issuer_name,
                                                             "open_start_date": open_start_date,
                                                             "open_end_date": open_end_date,
                                                             "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield)*100,),
                                                             "starting_amount": '%.2f' % float(starting_amount)})
            #计算月平均
            query = u"SELECT avg(bank_avg) as avg FROM\
                        (SELECT issuer_name,avg(expected_highest_yield) as bank_avg FROM zyq.t_product\
                        WHERE (date_sub(curdate(), INTERVAL 30 DAY)<=date(open_start_date) or (open_start_date='每天' and status='在售'))\
                        AND currency='%s' AND round(tenor/30)='%s'\
                        GROUP BY issuer_name) t" % (currency, ty[0])
            cursor.execute(query)
            for (cursor_avg,) in cursor:
                prod_list["tenor_group"][-1]["industry_1m_avg_yield"] = '%.4f%%' % (float(cursor_avg)*100,)


    pprint(prod_list)

    cnx.commit()
    cursor.close()
    logger_local.info('Selected WM Products requested for %s \n\n' % currency)

    # return jsonify(rate_list)
    return json.dumps(prod_list, ensure_ascii=False)



if __name__ == '__main__':
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

    app.run(debug=True, host="0.0.0.0")
