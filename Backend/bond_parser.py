# -*- coding: utf-8 -*-
import sys, getopt
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
import StringIO
import time
import openpyxl
import mysql.connector
from mysql.connector import errorcode
from multiprocessing import Pool
from decimal import Decimal
from butils.butils import decode
from butils.butils import fix_json
from butils.pprint import pprint
from datetime import datetime
from HTMLParser import HTMLParser


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import random
from retrying import retry

LOCALTIME = time.strftime('%Y%m%d', time.localtime(time.time()))
VERSION = 0.5

# FundSuperMart
# 请求格式：http post
# 返回格式：html

def get_FSM_bond_product():
    try:
        index_url = 'https://secure.fundsupermart.com.hk/hk/main/bond/bond-info/selectorResult.svdo?lang=zh'
        logging.info("Retrieving " + index_url + " ...")

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.get(index_url, timeout=60)
        #     return requests.post(index_url, data={"bondCategory": "",
        #                                           "currency": "AUD",
        #                                           "currency": "CHF",
        #                                           "currency": "CNY",
        #                                           "currency": "EUR",
        #                                           "currency": "GBP",
        #                                           "currency": "HKD",
        #                                           "currency": "JPY",
        #                                           "currency": "SGD",
        #                                           "currency": "USD",
        #                                           "netYieldMaturityRangeFrom": "0",
        #                                           "netYieldMaturityRangeTo": "17",
        #                                           "yrsMaturityRangeFrom": "0",
        #                                           "yrsMaturityRangeTo": "17",
        #                                           "annualCouponRateRangeFrom": "0",
        #                                           "annualCouponRateRangeTo": "17",
        #                                           "issuer": "",
        #                                           "investmentObjective": "",
        #                                           "couponFrequency": "",
        #                                           "modifiedDurationRangeFrom": "0",
        #                                           "modifiedDurationRangeTo": "17",
        #                                           "minInvestmentAmountRangeFrom": "0",
        #                                           "minInvestmentAmountRangeTo": "21",
        #                                           "creditRatingRangeFrom": "0",
        #                                           "creditRatingRangeTo": "9",
        #                                           "numberOfCriteria": "1"})

        response = request_content()

        soup = bs4.BeautifulSoup(response.text.replace('</br>', ''), "html.parser")
        bond_list = soup.find("table", id="bondInfoTable").find("tbody").find_all("tr")

        bond_data = []

        for idx, bond in enumerate(bond_list):
            tds = bond.find_all("td")
            bond_data.append([tds[0].input["value"],
                              tds[1].span.text.strip(),
                              tds[1].a.span.text.strip(),
                              tds[2].span.text.strip(),
                              tds[3].span.text.strip(),
                              tds[4].span.text.strip(),
                              re.sub(r".*/", "", tds[5].img["src"].strip()).replace(".gif",""),
                              tds[6].span.text.strip(),
                              tds[7].span.text.strip(),
                              tds[8].span.text.strip(),
                              tds[9].span.text.strip(),
                              tds[10].span.text.strip(),
                              tds[11].span.text.strip(),
                              tds[12].span.text.strip(),
                              tds[13].span.text.strip(),
                              tds[14].span.text.strip(),
                              tds[15].font.text.strip()])

        logging.debug(bond_data)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "BONDLIST"
        ws_title = ["prod_code",
                    "issuer_name",
                    "prod_name",
                    "bond_type",
                    "currency",
                    "credit_rating",
                    "investment_obj",
                    "years_to_maturity",
                    "annual_coupon",
                    "annual_coupon_frequency",
                    "bid",
                    "ask",
                    "net_bid_yield",
                    "net_offer_yield",
                    "modified_duration",
                    "min_purchase_quantity",
                    "special_feature"]
        ws.append(ws_title)
        for bond in bond_data:
            ws.append(bond)
        wb.save(output_file)

        # delete all duplicated records:
        cursor = cnx.cursor()
        cursor.execute("""DELETE FROM t_bond_product WHERE data_source='FSM' and date(update_time)=curdate()""")
        logging.info(unicode(cursor.rowcount) + ' FSM bonds deleted')

        add_product = ("""INSERT INTO t_bond_product(prod_code, issuer_name, prod_name, bond_type, currency,
                          credit_rating, investment_obj, years_to_maturity, annual_coupon, annual_coupon_frequency,
                          bid, ask, net_bid_yield, net_offer_yield, modified_duration, min_purchase_quantity,
                          special_feature, data_source, update_time)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'FSM', now())""")

        for bond in bond_data:
            cursor.execute(add_product, bond)

        logging.info(unicode(len(bond_data)) + ' FSM bonds imported')
        cursor.close()

    except:
        raise


def usage():
    print "-o [output_file] -v -h"


def version():
    print VERSION

if __name__ == '__main__':
    DB_NAME = 'zyq'

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvo:", ["help", "version", "output="])

        output_destination = ''

        for op, value in opts:
            if op == '-o':
                output_destination = value
            elif op == '-h' or op == '--help':
                usage()
                exit(0)
            elif op == '-v' or op == '--version':
                version()
                exit(0)

        if not output_destination:
            output_file = "output/bond_FSM_" + LOCALTIME + ".xlsx"
        else:
            output_file = output_destination + "bond_FSM_" + LOCALTIME + ".xlsx"

        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database=DB_NAME)
        cnx = mysql.connector.connect(user='zyq', password='zyq', database=DB_NAME)
        logging.info('MYSQL connected.')

        get_FSM_bond_product()

        cnx.commit()
        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            raise
