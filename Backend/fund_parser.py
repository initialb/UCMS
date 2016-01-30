# -*- coding: utf-8 -*-

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
from butils.butils import ppprint
from datetime import datetime
from HTMLParser import HTMLParser
from butils.pprint import pprint

import sys, getopt
reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import random
from retrying import retry

LOCALTIME = time.strftime('%Y%m%d', time.localtime(time.time()))
VERSION = 0.5

# FundSuperMart
# 请求格式：http post
# 返回格式：html

def get_FSM_fund_product():
    try:
        index_url = 'http://www.fundsupermart.com.hk/hk/main/fundinfo/generateTable.svdo?lang=zh'
        logging.info("Retrieving " + index_url + " ...")

        @retry(stop_max_attempt_number=10, wait_fixed=2000)
        def request_content():
            return requests.post(index_url, timeout=60, data={"baseCur": "fundCurrency"})

        response = request_content()

        buf = StringIO.StringIO(response.text)
        f = StringIO.StringIO()

        is_first_tr = True
        line = True

        # 处理返回结果中<tr>未闭合的问题, 否则soup分析出错.
        while line:
            line = buf.readline()
            if " --------------Start displaying fund list-------------------  " in line:
                while True:
                    line = buf.readline()
                    if "<tr" in line:
                        # 第一行前不增加</br>
                        if is_first_tr is True:
                            is_first_tr = False
                        else:
                            f.write(" "*17*4 + "</tr>\n")
                    # 读取到table最后一个tr
                    if "</table>" in line:
                        break
                    # 跳过空行
                    if line.strip() == "":
                        continue
                    f.write(line)
                break

        buf.close()

        # 回到文件头, 读取至soup分析
        f.seek(0)
        fund_list_html = f.read()
        f.close()

        soup = bs4.BeautifulSoup(fund_list_html, "html.parser")
        fund_list = soup.find_all("tr")

        fund_data = []

        for idx, fund in enumerate(fund_list):
            tds = fund.find_all("td")
            if len(tds) == 22:
                fund_data.append([tds[0].input["value"],
                                  tds[1].a.font.text.strip(),
                                  tds[2].font.text.strip(),
                                  tds[3].font.text.strip(),
                                  tds[4].font.text.strip(),
                                  tds[5].font.text.strip(),
                                  tds[6].font.text.strip(),
                                  tds[7].font.text.strip(),
                                  tds[8].font.text.strip(),
                                  tds[9].font.text.strip(),
                                  tds[10].font.text.strip(),
                                  tds[11].font.text.strip(),
                                  tds[12].font.text.strip(),
                                  tds[13].font.text.strip(),
                                  tds[14].font.text.strip(),
                                  tds[15].font.text.strip(),
                                  tds[16].font.text.strip(),
                                  tds[17].font.text.strip(),
                                  tds[18].font.text.strip(),
                                  tds[19].font.text.strip(),
                                  tds[20].font.text.strip(),
                                  tds[21].font.text.strip()])
        logging.debug(fund_data)

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "FUNDLIST"
        ws_title = ["prod_code",
                    "prod_name",
                    "risk_rating",
                    "currency",
                    "latest_nav_price",
                    "3year_risk_return_ratio",
                    "sharpe_ratio",
                    "valuation_date",
                    "cp_1m",
                    "cp_3m",
                    "cp_6m",
                    "cp_ytd",
                    "cp_1y",
                    "cp_3y",
                    "cp_5y",
                    "cp_since_launch",
                    "launch_date",
                    "cyp_1",
                    "cyp_2",
                    "cyp_3",
                    "cyp_4",
                    "cyp_5"]
        ws.append(ws_title)
        for fund in fund_data:
            ws.append(fund)
        wb.save(output_file)

        # delete all duplicated records:
        cursor = cnx.cursor()
        cursor.execute("""DELETE FROM t_fund_product WHERE data_source='FSM' and date(update_time)=curdate()""")
        logging.info(unicode(cursor.rowcount) + ' FSM funds deleted')

        add_product = ("""INSERT INTO t_fund_product(prod_code, prod_name, risk_rating, currency, latest_nav_price,
                          3year_risk_return_ratio, sharpe_ratio, valuation_date, cp_1m, cp_3m, cp_6m, cp_ytd,
                          cp_1y, cp_3y, cp_5y, cp_since_launch, launch_date, cyp_1, cyp_2, cyp_3, cyp_4, cyp_5,
                          data_source, update_time)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'FSM', now())""")

        for fund in fund_data:
            cursor.execute(add_product, fund)

        logging.info(unicode(len(fund_data)) + ' FSM funds imported')
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
            output_file = "output/fund_FSM_" + LOCALTIME + ".xlsx"
        else:
            output_file = output_destination + "fund_FSM_" + LOCALTIME + ".xlsx"


        cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database=DB_NAME)
        # cnx = mysql.connector.connect(user='zyq', password='zyq', database=DB_NAME)
        logging.info('MYSQL connected.')

        get_FSM_fund_product()

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
