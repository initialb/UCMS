# -*- coding: utf-8 -*-

import math
import codecs
import argparse
import logging
import re
import requests
import bs4
import json
import time
import datetime
import StringIO
import openpyxl
import mysql.connector
from mysql.connector import errorcode
from multiprocessing import Pool
from decimal import Decimal
from butils import decode
from butils import fix_json
from butils import ppprint
from HTMLParser import HTMLParser
from butils.pprint import pprint

import sys
reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import random
from retrying import retry

from openpyxl import load_workbook

def import_xlsx():

    result = []

    wb = load_workbook('./xlsx/20160403.xlsx')
    ws = wb['国内银行总汇']

    # for row_index, row in enumerate(ws.rows):
    #     for col_index, cell in enumerate(row):
    #         print row_index, col_index, cell.value

    for row in ws.rows:
        if isinstance(row[8].value, datetime.datetime):
            open_start_date = row[8].value.strftime("%Y%m%d")
        else:
            open_start_date = row[8].value
        if isinstance(row[9].value, datetime.datetime):
            open_end_date = row[9].value.strftime("%Y%m%d")
        else:
            open_end_date = row[9].value
        if isinstance(row[12].value, datetime.datetime):
            start_date = row[12].value.strftime("%Y%m%d")
        else:
            start_date = row[12].value
        if isinstance(row[13].value, datetime.datetime):
            end_date = row[13].value.strftime("%Y%m%d")
        else:
            end_date = row[13].value
        result.append([row[1].value,
                       row[2].value,
                       row[3].value,
                       decode(row[4].value,
                              "美元", "USD",
                              "港币", "HKD",
                              "澳元", "AUD",
                              "英镑", "GBP",
                              "欧元", "EUR",
                              row[4].value),
                       re.sub(r'[^\d]+', '', row[5].value),
                       row[6].value,
                       row[7].value,
                       open_start_date,
                       open_end_date,
                       row[10].value,
                       row[11].value,
                       start_date,
                       end_date,
                       row[14].value,
                       row[15].value,
                       row[16].value,
                       row[17].value,
                       row[18].value,
                       row[19].value])

    # delete all duplicated records:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='MN' and date(update_time)=curdate()""")
    logging.info(unicode(cursor.rowcount) + ' manually collected products deleted')

    add_product = ("""INSERT INTO t_product(issuer_name, prod_name, prod_code, currency, tenor, tenor_desc,
                      expected_highest_yield, open_start_date, open_end_date, remark, starting_amount,
                      start_date, end_date, redeemable, pledgeable, preservable, risk_desc, last_yield, status,
                      data_source, update_time)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                              'MN', now())""")

    for pd in result[1:]:
        cursor.execute(add_product, pd)

    logging.info(unicode(len(result[1:])) + ' products imported')
    cursor.close()


if __name__ == '__main__':
    DB_NAME = 'zyq'

    try:
        cnx = mysql.connector.connect(host='localhost', user='zyq', password='zyq', database=DB_NAME)
        # cnx = mysql.connector.connect(host='localhost', user='zyq', password='zyq', database=DB_NAME)
        logging.info('MYSQL connected.')

        import_xlsx()

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
