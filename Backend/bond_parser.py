# -*- coding: utf-8 -*-

import math
import codecs
import argparse
import logging
import re
import requests
import bs4
import json
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

import sys
reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import random
from retrying import retry


# FundSuperMart
# 请求格式：http post
# 返回格式：html

def get_FSM_bond_product():
    try:
        # index_url = 'https://secure.fundsupermart.com.hk/hk/main/bond/bond-info/selectorResult.svdo'
        #
        # @retry(stop_max_attempt_number=10, wait_fixed=2000)
        # def request_content():
        #     return requests.get(index_url)
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
        #
        # response = request_content()
        # soup = bs4.BeautifulSoup(response.text.replace('</br>', ''), "html.parser")
        # bond_list = soup.find("table", id="bondInfoTable").find("tbody").find_all("tr")
        #
        # f = codecs.open("FSM_bond.html", encoding='utf-8', mode="w")
        # f.write(unicode(rate_list))
        # f.close

        f = codecs.open("FSM_bond.html", encoding='utf-8', mode="r")
        bond_list_body = f.read()
        f.close

        soup = bs4.BeautifulSoup(bond_list_body, "html.parser")
        bond_list = soup.find_all("tr")

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
                              tds[15].font.text.strip(),
                              idx])

            pprint(bond_data[-1])



            # current_tag = bond.td
            # print current_tag.input["value"]
            # current_tag
            # print bond.td.next_sibling.next_sibling.span.text
            # print bond.td.next_sibling.next_sibling.a.span.text
            # print
#         r = rates.find_all("td")
#         if len(r) == 8 and r[0].string.strip() == "美元":
#             rate_data = ['C10104',
#                          'USD',
#                          r[1].string.strip(),
#                          r[2].string.strip(),
#                          r[3].string.strip(),
#                          r[4].string.strip(),
#                          r[5].string.strip(),
#                          r[6].string.strip(),
#                          format_datetime(r[7].string.strip())]
#             break
#
#     add_product = ("""INSERT INTO t_listing_rate
#                       (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, mid_rate,
#                       publisher_mid_rate, publish_time, update_time)
#                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
#     cursor.execute(add_product, rate_data)
#
#     logger_local.info('BCHO rate imported')
#

    #
    # total_count = json.loads(response.text.encode('utf-8'))["Count"]
    # total_page = -(-total_count // 500)
    #
    # # debug
    # logging.info("total_count: " + str(total_count))
    # logging.info("total_page: " + str(total_page))
    #
    # j = []
    # count = 0
    #
    # # delete all duplicated records:
    # cursor = cnx.cursor()
    # cursor.execute("""DELETE FROM t_product WHERE data_source='ChinaWealth' and date(update_time)=curdate()""")
    # logging.info(unicode(cursor.rowcount) + ' ChinaWealth ' + 'rows deleted')
    #
    # for page_index in xrange(1, total_page + 1):
    #
    #     @retry(stop_max_attempt_number=10, wait_fixed=500)
    #     def request_content():
    #         return requests.post(index_url,
    #                             data={"cpzt": "02,04", "pagenum": page_index, "drawPageToolEnd": "5"},
    #                             timeout=5)
    #     response = request_content()
    #
    #     # while True:
    #     #     try:
    #     #         response = requests.post(index_url,
    #     #                                  data={"cpzt": "02,04", "pagenum": page_index, "drawPageToolEnd": "5"},
    #     #                                  timeout=10)
    #     #     except requests.exceptions.ConnectionError, e:
    #     #         print e
    #     #         continue
    #     #     except requests.exceptions.Timeout, e:
    #     #         print e
    #     #         continue
    #     #     break
    #
    #     data_string = json.loads(response.text.encode('utf-8'))
    #     product_data = []
    #
    #     for i in range(len(data_string["List"])):
    #         if 'CNY' not in data_string["List"][i]["mjbz"]:
    #             product_data.append([data_string["List"][i]["cpid"],  # 产品id
    #                                  data_string["List"][i]["cpdjbm"],  # 产品登记编码
    #                                  data_string["List"][i]["cpdm"],  # 产品代码
    #                                  data_string["List"][i]["cpms"],  # 产品描述
    #                                  data_string["List"][i]["fxjgdm"],  # 发行机构代码
    #                                  data_string["List"][i]["fxjgms"],  # 发行机构描述
    #                                  data_string["List"][i]["mjbz"],  # 募集币种
    #                                  data_string["List"][i]["cpqx"],  # 产品期限
    #                                  data_string["List"][i]["qxms"],  # 期限描述
    #                                  data_string["List"][i]["mjqsrq"],  # 募集起始日期
    #                                  data_string["List"][i]["mjjsrq"],  # 募集结束日期
    #                                  data_string["List"][i]["kfzqqsr"],  # 开放周期起始日
    #                                  data_string["List"][i]["kfzqjsr"],  # 开放周期结束日
    #                                  data_string["List"][i]["cpqsrq"],  # 产品起始日期
    #                                  data_string["List"][i]["cpyjzzrq"],  # 产品预计终止日期
    #                                  data_string["List"][i]["cplx"],  # 产品类型
    #                                  data_string["List"][i]["cplxms"],  # 产品类型描述(如: 封闭式非净值型)
    #                                  data_string["List"][i]["cpsylx"],  # 产品收益类型
    #                                  data_string["List"][i]["cpsylxms"],  # 产品收益类型描述(如: 保本浮动收益)
    #                                  data_string["List"][i]["cpfxdj"],  # 产品风险等级
    #                                  data_string["List"][i]["fxdjms"],  # 风险等级描述
    #                                  data_string["List"][i]["cpjz"],  # 产品净值
    #                                  data_string["List"][i]["bqjz"],  # bq净值
    #                                  data_string["List"][i]["csjz"],  # cs净值
    #                                  data_string["List"][i]["xsqy"],  # 销售区域
    #                                  data_string["List"][i]["cpxsqy"],  # 产品销售区域
    #                                  data_string["List"][i]["orderby"],  # order
    #                                  data_string["List"][i]["yjkhzgnsyl"],  # 预计客户最高年收益率
    #                                  data_string["List"][i]["yjkhzdnsyl"],  # 预计客户最低年收益率
    #                                  data_string["List"][i]["dqsjsyl"],  # 到期实际收益率
    #                                  data_string["List"][i]["cpztms"],  # 产品状态描述
    #                                  data_string["List"][i]["qdxsje"]])  # 起点销售金额
    #
    #             add_product = ("""INSERT INTO t_product
    #                               (prod_id, prod_reg_code, prod_code, prod_name, issuer_code, issuer_name, currency,
    #                               tenor, tenor_desc, start_date, end_date, open_start_date, open_end_date,
    #                               value_date, maturity_date, prod_type, prod_type_desc, coupon_type, coupon_type_desc,
    #                               risk, risk_desc, net_value, bq_net_value, cs_net_value, sales_region, sales_region_desc,
    #                               order_by, expected_highest_yield, expected_lowest_yield, actual_yield, status,
    #                               starting_amount, data_source, update_time)
    #                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    #                                       %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    #                                       'ChinaWealth', now())""")
    #             cursor.execute(add_product, product_data[-1])
    #             count += 1
    #
    #     logging.info(unicode(count) + ' ChinaWealth products imported')
    #
    # cnx.commit()
    # cursor.close()
    # logging.info(unicode(count) + ' ChinaWealth products imported')

    # sample = {
    #              "yjkhzdnsyl 预计最低收益率": "3.6",
    #              "cpyjzzrq 产品预计终止日期": "2016/03/02",
    #              "cpztms 状态": "在售",
    #              "cpqx 期限": "58",
    #              "fxjgdm 发行机构代码": "C11227",
    #              "mjjsrq 募集结束日期": "2016/01/03",
    #              "cpid 产品id": "947670",
    #              "bqjz 产品净值": "",
    #              "cpdm 产品代码": "",
    #              "cpsylxms 产品收益类型模式": "保本浮动收益",
    #              "cpfxdj 产品风险等级": "01",
    #              "qxms 期限类型": "1-3个月（含）",
    #              "mjqsrq 募集起始日期": "2015/12/27",
    #              "mjbz 募集币种": "人民币(CNY)",
    #              "cpms 产品描述": "“乐惠”2015年第181期",
    #              "cpqsrq 产品起始日期": "2016/01/04",
    #              "fxdjms 风险等级描述": "一级（低）",
    #              "kfzqqsr 开放周期起始日": "",
    #              "csjz": "",
    #              "cpdjbm 产品登记编码": "C1122715000169",
    #              "xsqy 销售区域": "",
    #              "yjkhzgnsyl 预计最高收益率": "3.8",
    #              "cplx 产品类型": "02",
    #              "cplxms 产品类型描述": "封闭式非净值型",
    #              "dqsjsyl 到期实际收益率": "",
    #              "cpxsqy 产品销售区域": "",
    #              "kfzqjsr 开放周期结束日": "",
    #              "fxjgms 发行机构描述": "杭州联合农村商业银行股份有限公司",
    #              "orderby": "",
    #              "cpjz 产品净值": "",
    #              "cpsylx 产品收益类型": "02",
    #              "qdxsje 起点销售金额": "50000"
    #          },
    except:
        raise



if __name__ == '__main__':
    DB_NAME = 'zyq'

    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database=DB_NAME)
        cnx = mysql.connector.connect(user='zyq', password='zyq', database=DB_NAME)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        logging.info('MYSQL connected.')

    get_FSM_bond_product()


    cnx.close
