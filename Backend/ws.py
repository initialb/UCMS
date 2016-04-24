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

    rate_list = {"total_rec": "", "list": []}
    total_rec = ""

    # query = u"""
    #     SELECT count(*) FROM t_issuer, t_listing_rate
    #     WHERE t_issuer.issuer_code=t_listing_rate.publisher_code and t_listing_rate.currency='%s'
    #     """ % currency
    #
    # cursor.execute(query)
    # for (total_rec,) in cursor:
    #     rate_list["total_rec"] = total_rec
    #
    # if total_rec == 0:
    #     logger_local.info('Not found')
    #     abort(404)

    # 定义基准价
    query = u"""
        SELECT
            AVG(bid_remit), AVG(bid_cash), AVG(ask_remit), AVG(ask_cash)
        FROM
            t_listing_rate
        WHERE
            currency = '%s'
                AND DATE(publish_time) = CURDATE()
                AND publisher_code IN ('C10102' , 'C10103', 'C10104', 'C10105', 'C10301', 'C10308')
        """ % currency
    cursor.execute(query)
    for (bm_bid_remit, bm_bid_cash, bm_ask_remit, bm_ask_cash) in cursor:
        bm_bid_remit = bm_bid_remit
        bm_bid_cash = bm_bid_cash
        bm_ask_remit = bm_ask_remit
        bm_ask_cash = bm_ask_cash

    logger_local.info('Bench rates: %s, %s, %s, %s' % (bm_bid_remit, bm_bid_cash, bm_ask_remit, bm_ask_cash))

    query = u"""
        SELECT
            t_issuer.cn_short_name,
            t_listing_rate.bid_remit,
            t_listing_rate.bid_cash,
            t_listing_rate.ask_remit,
            t_listing_rate.ask_cash,
            t_listing_rate.publish_time
        FROM
            t_issuer,
            t_listing_rate
        WHERE
            t_issuer.issuer_code = t_listing_rate.publisher_code
                AND currency = '%s'
                AND DATE(publish_time) = CURDATE()
        """ % currency
    cursor.execute(query)
    rate_list["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    rate_list["currency"] = currency
    rate_list["currencyname"] = decode(currency, "USD", u"美元", "GBP", u"英镑", "AUD", u"澳元", "EUR", u"欧元", 'JPY', u'日元', "")
    for (cn_short_name, bid_remit, bid_cash, ask_remit, ask_cash, publish_time) in cursor:
        # logger_local.debug('bm_bid_remit*1.008: %s' % (bm_bid_remit*1.008,))
        # logger_local.debug('bm_bid_cash*1.008: %s' % (bm_bid_cash*1.008,))
        # logger_local.debug('bm_ask_remit*0.992: %s' % (bm_ask_remit*0.992,))
        # logger_local.debug('bm_ask_cash*0.992: %s' % (bm_ask_cash*0.992,))
        # logger_local.debug('bid_remit, bid_cash, ask_remit, ask_cash: %s, %s, %s, %s' % (bid_remit, bid_cash, ask_remit, ask_cash))
        if float(bid_remit) > bm_bid_remit*1.0008 or float(bid_cash) > bm_bid_cash*1.0008 \
                or float(ask_remit) < bm_ask_remit*0.9992 or float(ask_cash) < bm_ask_cash*0.9992:
            rate_list["list"].append({})
            rate_list["list"][-1]["bank"] = "**"+cn_short_name
            if currency == 'JPY':
                rate_list["list"][-1]["remitbid"] = '%.4f' % float(bid_remit)
                rate_list["list"][-1]["cashbid"] = '%.4f' % float(bid_cash)
                rate_list["list"][-1]["remitask"] = '%.4f' % float(ask_remit)
                rate_list["list"][-1]["cashask"] = '%.4f' % float(ask_cash)
            else:
                rate_list["list"][-1]["remitbid"] = '%.2f' % float(bid_remit)
                rate_list["list"][-1]["cashbid"] = '%.2f' % float(bid_cash)
                rate_list["list"][-1]["remitask"] = '%.2f' % float(ask_remit)
                rate_list["list"][-1]["cashask"] = '%.2f' % float(ask_cash)
            rate_list["list"][-1]["publish_time"] = publish_time
        else:
            rate_list["list"].append({})
            rate_list["list"][-1]["bank"] = cn_short_name
            if currency == 'JPY':
                rate_list["list"][-1]["remitbid"] = '%.4f' % float(bid_remit)
                rate_list["list"][-1]["cashbid"] = '%.4f' % float(bid_cash)
                rate_list["list"][-1]["remitask"] = '%.4f' % float(ask_remit)
                rate_list["list"][-1]["cashask"] = '%.4f' % float(ask_cash)
            else:
                rate_list["list"][-1]["remitbid"] = '%.2f' % float(bid_remit)
                rate_list["list"][-1]["cashbid"] = '%.2f' % float(bid_cash)
                rate_list["list"][-1]["remitask"] = '%.2f' % float(ask_remit)
                rate_list["list"][-1]["cashask"] = '%.2f' % float(ask_cash)
            rate_list["list"][-1]["publish_time"] = publish_time

    pprint(rate_list)

    bid_remit_list = []
    bid_cash_list = []
    ask_remit_list = []
    ask_cash_list = []

    for r in rate_list["list"]:
        bid_remit_list.append(r["remitbid"])
        bid_cash_list.append(r["cashbid"])
        ask_remit_list.append(r["remitask"])
        ask_cash_list.append(r["cashask"])

    max_bid_remit = max(bid_remit_list)
    max_bid_cash = max(bid_cash_list)
    min_ask_remit = max(ask_remit_list)
    min_ask_cash = max(ask_cash_list)

    for r in rate_list["list"]:
        if currency == 'JPY':
            if r["remitbid"] == '%.4f' % float(max_bid_remit):
                r["remitbid"] = "*"+r["remitbid"]
            if r["cashbid"] == '%.4f' % float(max_bid_cash):
                r["cashbid"] = "*"+r["cashbid"]
            if r["remitask"] == '%.4f' % float(min_ask_remit):
                r["remitask"] = "*"+r["remitask"]
            if r["cashask"] == '%.4f' % float(min_ask_cash):
                r["cashask"] = "*"+r["cashask"]
        else:
            if r["remitbid"] == '%.2f' % float(max_bid_remit):
                r["remitbid"] = "*"+r["remitbid"]
            if r["cashbid"] == '%.2f' % float(max_bid_cash):
                r["cashbid"] = "*"+r["cashbid"]
            if r["remitask"] == '%.2f' % float(min_ask_remit):
                r["remitask"] = "*"+r["remitask"]
            if r["cashask"] == '%.2f' % float(min_ask_cash):
                r["cashask"] = "*"+r["cashask"]

    rate_list["total_rec"] = len(rate_list["list"])

    cnx.commit()
    cursor.close()
    cnx.close()

    logger_local.info('Rates requested for %s \n\n' % currency)

    pprint(rate_list)

    # return jsonify(rate_list)
    return json.dumps(rate_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/wmp/<string:currency>', methods=['GET'])
def get_wmp(currency):
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

    total_rec = None
    prod_list = {"currency": currency,
                 "currencyname": decode(currency, "USD", u"美元", "GBP", u"英镑", "AUD", u"澳元", "EUR", u"欧元", ""),
                 "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 "preservable": "ALL",
                 "total_rec": "",
                 "tenor_group": []
                }

    preservable = request.args.get('preservable', '')

    if preservable == 'N' or preservable == 'Y':
        if preservable == 'N':
            preservable_str = u'非保本'
        else:
            preservable_str = u'保本'

        tenor_list = []
        prod_list["preservable"] = preservable

        # 统计记录数
        query = u"""
            SELECT
                count(*)
            FROM
                t_product
            WHERE
                status = '在售'
                    AND preservable = '%s'
                    AND redeemable = '封闭'
                    AND currency = '%s'
            """ % (preservable_str, currency)
        cursor.execute(query)
        for (csr_total_rec,) in cursor:
            total_rec = csr_total_rec

        if total_rec == 0:
            logger_local.info('Not found')
            abort(404)
        else:
            prod_list["total_rec"] = total_rec

        # 获取期限列表
        query = u"""
            SELECT
                ROUND(tenor / 30) AS tenor
            FROM
                t_product
            WHERE
                status = '在售'
                    AND preservable = '%s'
                    AND redeemable = '封闭'
                    AND currency = '%s'
            GROUP BY ROUND(tenor / 30)
            ORDER BY tenor DESC
            """ % (preservable_str, currency)
        cursor.execute(query)
        for (tenor_desc) in cursor:
            tenor_list.append(tenor_desc)

        # 按期限
        for tn in tenor_list:
            prod_list["tenor_group"].append({"tenor": int(tn[0]), "list": []})
            industry_1m_avg_yield = None

            # 计算月平均
            query = u"""
                SELECT
                    AVG(bank_avg) AS avg
                FROM
                    (SELECT
                        issuer_name, AVG(expected_highest_yield) AS bank_avg
                    FROM
                        zyq.t_product
                    WHERE
                        (DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(open_start_date)
                            OR (open_start_date = '每天' AND status = '在售'))
                        AND currency = '%s'
                        AND ROUND(tenor / 30) = '%s'
                        AND preservable = '%s'
                        AND redeemable = '封闭'
                    GROUP BY issuer_name) t
                """ % (currency, tn[0], preservable_str)
            cursor.execute(query)
            for (cursor_avg,) in cursor:
                industry_1m_avg_yield = '%.4f%%' % (float(cursor_avg)*100,)
                # prod_list["tenor_group"][-1]["industry_1m_avg_yield"] = '%.4f%%' % (float(cursor_avg)*100,)

            prod_list["tenor_group"][-1]["industry_1m_avg_yield"] = industry_1m_avg_yield

            # 获取明细列表
            query = u"""
                SELECT
                    prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date,
                    expected_highest_yield, last_yield, preservable, pledgeable, risk_desc, starting_amount
                FROM
                    t_product
                WHERE
                    status = '在售'
                        AND preservable = '%s'
                        AND redeemable = '封闭'
                        AND currency = '%s'
                        AND ROUND(tenor / 30) = '%s'
                """ % (preservable_str, currency, tn[0])
            cursor.execute(query)
            for (prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date, expected_highest_yield,
                 last_yield, preservable, pledgeable, risk_desc, starting_amount) in cursor:
                prod_list["tenor_group"][-1]["list"].append({
                    "prod_name": prod_name,
                    "issuer_name": issuer_name,
                    "sale_period": '%s~%s' % (open_start_date, open_end_date) if open_start_date.isdigit() else u"每天",
                    "interest_period": '%s~%s' % (start_date, end_date) if start_date.isdigit() else u"无固定期限",
                    "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield)*100,),
                    "history_yield": '-' if not last_yield else '%.4f%%' % (float(last_yield)*100,),
                    "return_type": pledgeable,
                    "risk_type": risk_desc,
                    "starting_amount": '%.2f' % float(starting_amount)})

    else:
        tenor_list = []
        prod_list["preservable"] = "ALL"

        # 统计记录数
        query = u"""
            SELECT
                count(*)
            FROM
                t_product
            WHERE
                status = '在售'
                    AND redeemable = '封闭'
                    AND currency = '%s'
            """ % currency
        cursor.execute(query)
        for (csr_total_rec,) in cursor:
            total_rec = csr_total_rec

        if total_rec == 0:
            logger_local.info('Not found')
            abort(404)
        else:
            prod_list["total_rec"] = total_rec

        # 获取期限列表
        query = u"""
            SELECT
                ROUND(tenor / 30) AS tenor
            FROM
                t_product
            WHERE
                status = '在售'
                    AND redeemable = '封闭'
                    AND currency = '%s'
            GROUP BY ROUND(tenor / 30)
            ORDER BY tenor DESC
            """ % (currency,)
        cursor.execute(query)
        for (tenor_desc) in cursor:
            tenor_list.append(tenor_desc)

        # 按期限
        for tn in tenor_list:
            prod_list["tenor_group"].append({"tenor": int(tn[0]), "list": []})
            industry_1m_avg_yield = None

            # 计算月平均
            query = u"""
                SELECT
                    AVG(bank_avg) AS avg
                FROM
                    (SELECT
                        issuer_name, AVG(expected_highest_yield) AS bank_avg
                    FROM
                        zyq.t_product
                    WHERE
                        (DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(open_start_date)
                            OR (open_start_date = '每天' AND status = '在售'))
                        AND currency = '%s'
                        AND ROUND(tenor / 30) = '%s'
                        AND redeemable = '封闭'
                    GROUP BY issuer_name) t
                """ % (currency, tn[0])
            cursor.execute(query)
            for (cursor_avg,) in cursor:
                industry_1m_avg_yield = '%.4f%%' % (float(cursor_avg)*100,)
                # prod_list["tenor_group"][-1]["industry_1m_avg_yield"] = '%.4f%%' % (float(cursor_avg)*100,)

            prod_list["tenor_group"][-1]["industry_1m_avg_yield"] = industry_1m_avg_yield

            # 获取明细列表
            query = u"""
                SELECT
                    prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date,
                    expected_highest_yield, last_yield, preservable, pledgeable, risk_desc, starting_amount
                FROM
                    t_product
                WHERE
                    status = '在售'
                        AND redeemable = '封闭'
                        AND currency = '%s'
                        AND ROUND(tenor / 30) = '%s'
                """ % (currency, tn[0])
            cursor.execute(query)
            for (prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date, expected_highest_yield,
                 last_yield, preservable, pledgeable, risk_desc, starting_amount) in cursor:
                prod_list["tenor_group"][-1]["list"].append({
                    "prod_name": prod_name,
                    "issuer_name": issuer_name,
                    "sale_period": '%s~%s' % (open_start_date, open_end_date) if open_start_date.isdigit() else u"每天",
                    "interest_period": '%s~%s' % (start_date, end_date) if start_date.isdigit() else u"无固定期限",
                    "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield)*100,),
                    "history_yield": '-' if not last_yield else '%.4f%%' % (float(last_yield)*100,),
                    "return_type": pledgeable,
                    "risk_type": risk_desc,
                    "starting_amount": '%.2f' % float(starting_amount)})

    pprint(prod_list)

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('Selected WM Products requested for %s \n\n' % currency)

    # return jsonify(rate_list)
    return json.dumps(prod_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/selectedwmp/<string:currency>', methods=['GET'])
def get_selectedwmp(currency):
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

    total_rec = None
    max_yield = 0
    prod_list = {"currency": currency,
                 "currencyname": decode(currency, "USD", u"美元", "GBP", u"英镑", "AUD", u"澳元", "EUR", u"欧元", ""),
                 "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 "total_rec": "",
                 "tenor_group": [{"preservable": "N", "list": []}, {"preservable": "Y", "list": []}]
                }

    # 非保本
    np_list = []
    query = u"""
        SELECT
            MAX(expected_highest_yield), ROUND(tenor / 30) as TENOR
        FROM
            t_product
        WHERE
            status = '在售'
                AND preservable = '非保本'
                AND redeemable = '封闭'
                AND currency = '%s'
        GROUP BY ROUND(tenor / 30)
        ORDER BY TENOR desc
        """ % (currency,)
    cursor.execute(query)
    for (expected_highest_yield, tenor_desc) in cursor:
        np_list.append([tenor_desc, expected_highest_yield])

    # 按期限
    for np in np_list:
        # 计算月平均
        industry_1m_avg_yield = None
        query0 = u"""
            SELECT
                AVG(bank_avg) AS avg
            FROM
                (SELECT
                    issuer_name, AVG(expected_highest_yield) AS bank_avg
                FROM
                    zyq.t_product
                WHERE
                    (DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(open_start_date)
                        OR (open_start_date = '每天' AND status = '在售'))
                    AND currency = '%s'
                    AND ROUND(tenor / 30) = '%s'
                    AND preservable = '非保本'
                    AND redeemable = '封闭'
                GROUP BY issuer_name) t
            """ % (currency, np[0])
        cursor.execute(query0)

        for (cursor_avg,) in cursor:
            industry_1m_avg_yield = cursor_avg

        # prod_list["tenor_group"][0]["list"].append({"tenor": int(ty[0]), "list": []})
        query = u"""
            SELECT
                prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date,
                expected_highest_yield, last_yield, preservable, pledgeable, risk_desc, starting_amount
            FROM
                t_product
            WHERE
                status = '在售'
                    AND preservable = '非保本'
                    AND redeemable = '封闭'
                    AND currency = '%s'
                    AND expected_highest_yield = '%s'
                    AND ROUND(tenor / 30) = '%s'
            """ % (currency, np[1], np[0])
        cursor.execute(query)

        for (prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date, expected_highest_yield,
             last_yield, preservable, pledgeable, risk_desc, starting_amount) in cursor:
            prod_list["tenor_group"][0]["list"].append({
                "prod_name": prod_name,
                "issuer_name": issuer_name,
                "sale_period": '%s~%s' % (open_start_date, open_end_date) if open_start_date.isdigit() else u"每天",
                "deposit_period": int(np[0]),
                "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield)*100,),
                "industry_1m_avg_yield": '%.4f%%' % (float(industry_1m_avg_yield)*100,),
                "return_type": pledgeable,
                "usd_rate": "",
                "starting_amount": '%.2f' % float(starting_amount)})

            if expected_highest_yield > max_yield:
                max_yield = expected_highest_yield

    # 保本
    ty_list = []
    query = u"""
        SELECT
            MAX(expected_highest_yield), ROUND(tenor / 30) as TENOR
        FROM
            t_product
        WHERE
            status = '在售'
                AND preservable = '非保本'
                AND redeemable = '封闭'
                AND currency = '%s'
        GROUP BY ROUND(tenor / 30)
        ORDER BY TENOR desc
        """ % (currency,)
    cursor.execute(query)
    for (expected_highest_yield, tenor_desc) in cursor:
        ty_list.append([tenor_desc, expected_highest_yield])

    # 按期限
    for ty in ty_list:
        # 计算月平均
        industry_1m_avg_yield = None
        query0 = u"""
            SELECT
                AVG(bank_avg) AS avg
            FROM
                (SELECT
                    issuer_name, AVG(expected_highest_yield) AS bank_avg
                FROM
                    zyq.t_product
                WHERE
                    (DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(open_start_date)
                        OR (open_start_date = '每天' AND status = '在售'))
                    AND currency = '%s'
                    AND ROUND(tenor / 30) = '%s'
                    AND preservable = '非保本'
                    AND redeemable = '封闭'
                GROUP BY issuer_name) t
            """ % (currency, ty[0])
        cursor.execute(query0)

        for (cursor_avg,) in cursor:
            industry_1m_avg_yield = cursor_avg

        # prod_list["tenor_group"][0]["list"].append({"tenor": int(ty[0]), "list": []})
        query = u"""
            SELECT
                prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date,
                expected_highest_yield, last_yield, preservable, pledgeable, risk_desc, starting_amount
            FROM
                t_product
            WHERE
                status = '在售'
                    AND preservable = '非保本'
                    AND redeemable = '封闭'
                    AND currency = '%s'
                    AND expected_highest_yield = '%s'
                    AND ROUND(tenor / 30) = '%s'
            """ % (currency, ty[1], ty[0])
        cursor.execute(query)

        for (prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date, expected_highest_yield,
             last_yield, preservable, pledgeable, risk_desc, starting_amount) in cursor:
            prod_list["tenor_group"][1]["list"].append({
                "prod_name": prod_name,
                "issuer_name": issuer_name,
                "sale_period": '%s~%s' % (open_start_date, open_end_date) if open_start_date.isdigit() else u"每天",
                "deposit_period": int(ty[0]),
                "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield)*100,),
                "industry_1m_avg_yield": '%.4f%%' % (float(industry_1m_avg_yield)*100,),
                "return_type": pledgeable,
                "usd_rate": "",
                "starting_amount": '%.2f' % float(starting_amount)})

            if expected_highest_yield > max_yield:
                max_yield = expected_highest_yield

    prod_list["max_return"] = '%.2f%%' % (float(max_yield)*100,)

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('Selected WM Products requested for %s \n\n' % currency)

    # return jsonify(rate_list)
    return json.dumps(prod_list, ensure_ascii=False)


if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0")
