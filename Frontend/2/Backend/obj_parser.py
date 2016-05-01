# -*- coding: utf-8 -*-

import sys
import math
import time
import random
import codecs
import argparse
import traceback
import logging
import re
import requests
import bs4
import json
import butils
import mysql.connector
from mysql.connector import errorcode
from multiprocessing import Pool
from decimal import Decimal
from butils.pprint import pprint
from datetime import datetime
from retrying import retry
from money_parser import *

import pprint as ppr
pp = ppr.PrettyPrinter(indent=4)


def get_ICBC_product():
    """
    工商银行 C10102
    请求格式：http get
    返回格式：json
    :return:
    """
    legal_group = 'ICBC'
    issuer_code = 'C10102'
    root_url = 'http://www.icbc.com.cn'
    index_url = 'http://www.icbc.com.cn/ICBCDynamicSite2/money/services/MoenyListService.ashx?ctl1=4&ctl2=6&keyword='
    product_data = []
    logger_local.info(unicode(legal_group) + ' - Begin parsing...')

    data_string = json.loads(requests.get(index_url).text.encode('utf-8'))
    # logger_local.debug('data_string = ' + unicode(data_string))

    for pd in data_string:
        product_data.append([issuer_code,
                             pd["buyPaamt"],
                             decode(pd["buyflag"], '1', 'Y', 'N'),
                             # pd["categoryL1"],
                             # pd["categoryL2"],
                             re.sub(r'[^\d.]+', '', pd["intendYield"]),
                             # pd["introJs"],
                             # pd["isUnitValue"],
                             pd["matudate"],
                             pd["offerPeriod"][:8],
                             pd["offerPeriod"][-8:],
                             pd["prodID"],
                             filter(unicode.isalpha, pd["prodID"]),
                             filter(unicode.isdigit, pd["prodID"]),
                             # pd["prodintro"],
                             pd["productName"],
                             pd["productTerm"],
                             pd["saleZone"],
                             pd["sellStatus"]])
                             # pd["totalValue"],
                             # pd["value"],
                             # pd["valueLink"],
                             # pd["workdate"]])

        logger_local.debug(unicode(legal_group) + ' - ' + repr_zh(product_data[-1]))

    # DB manipulation:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='OW' and issuer_code=%s
                      and date(update_time)=curdate()""", (issuer_code,))
    logger_local.info(unicode(legal_group) + ' - ' + unicode(cursor.rowcount) + ' rows deleted')

    add_product = ("""INSERT INTO t_product
                      (issuer_code, starting_amount, buyable, expected_highest_yield, maturity_date, start_date,
                       end_date, prod_code, currency, tenor, prod_name, tenor_desc, sales_region_desc, status,
                       data_source, update_time)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'OW', now())""")

    for p in product_data:
        cursor.execute(add_product, p)

    cnx.commit()
    cursor.close()
    logger_local.info(unicode(legal_group) + ' - ' + unicode(len(product_data)) + ' products imported')


def generate_report():
    """
    generate report to t_daily_rcmd
    :return:
    """
    prod_list = []
    max_avg = []
    cursor = cnx.cursor()

    query = ("""SELECT issuer_code, prod_code, prod_name, expected_highest_yield, round(tenor/30) as tnr FROM t_product
                WHERE data_source = 'OW' AND buyable = 'Y' AND currency = 'USD'
                AND expected_highest_yield <> '' AND tenor <> ''
                AND DATE(update_time) = (SELECT MAX(DATE(update_time)) FROM t_product) ORDER BY tnr""")
    cursor.execute(query)
    for (issuer_code, prod_code, prod_name, expected_highest_yield, tnr) in cursor:
        prod_list.append([issuer_code, prod_code, prod_name, round(float(expected_highest_yield),2), u"%g" % tnr])


    # 30天内最大最小值
    query = ("""SELECT MAX(expected_highest_yield) AS max,
                AVG(expected_highest_yield) AS avg,
                round(tenor/30) as tnr FROM t_product
                WHERE DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= STR_TO_DATE(start_date, '%Y%m%d')
                AND data_source = 'MN' AND currency = 'USD'
                GROUP BY tnr""")
    cursor.execute(query)
    for (max, avg, tnr) in cursor:
        max_avg.append([max, avg, u"%g" % tnr])

    # 无效率实现, 后续用lambda或pandas重写
    prod_list_rt = [prod_list[0][:]]
    for p in prod_list:
        if p[4] == prod_list_rt[-1][4]:
            if p[3] >= prod_list_rt[-1][3]:
                prod_list_rt.pop()
                prod_list_rt.append(p)
        else:
            prod_list_rt.append(p)

    for idx, p in enumerate(prod_list_rt):
        for pp in max_avg:
            if pp[2] == p[4]:
                prod_list_rt[idx].append(round(float(pp[0])*100,2))
                prod_list_rt[idx].append(round(float(pp[1])*100,2))

    cursor.execute("""DELETE FROM t_product_screening""")

    add_product = ("""INSERT INTO t_product_screening
                      (issuer_code, prod_code, prod_name, expected_highest_yield, tenor_type, max_yield, avg_yield)
                      VALUES (%s, %s, %s, %s, %s, %s, %s)""")

    for p in prod_list_rt:
        cursor.execute(add_product, p)
        logger_local.debug('Product Screening - ' + repr_zh(p))


    cnx.commit()
    cursor.close()
    logger_local.info(unicode(len(prod_list_rt)) + ' products filtered')


if __name__ == '__main__':
    DB_NAME = 'zyq'
    mylog = PLogging(__name__)

    mylog.logger.info('')
    mylog.logger.info('')
    mylog.logger.info('============================================================')
    mylog.logger.info('')
    mylog.logger.info('WMP Parser starting...')
    mylog.logger.info('')
    mylog.logger.info('============================================================')

    cnx = PConnectDB("localhost", "zyq", "zyq", "zyq")


    # get_CMHO_product()
    # get_ICBC_product()
    # get_ABCI_product()
    # get_CCBH_product()
    # get_CTIB_product()
    # get_BCOH_product()
    # get_EBBC_product()
    # get_DESZ_product()
    # get_IBCN_product()
    # get_SPDB_product()
    # get_BKSH_product()
    # get_BOBJ_product()
    # get_CW_product()

    # generate_report()
