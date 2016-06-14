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
import mysql.connector
from mysql.connector import errorcode
from multiprocessing import Pool
from decimal import Decimal
from butils import decode
from butils import fix_json
from butils import ppprint
from butils.pprint import pprint
from butils.finutils import *
from datetime import datetime
from retrying import retry

import pprint as ppr
pp = ppr.PrettyPrinter(indent=4)


TIMEOUT = 10
LOCALTIME = time.strftime('%Y%m%d', time.localtime(time.time()))
LOGNAME = 'log/wmp_parser_' + LOCALTIME + '.log'

# initialize root logger to write verbose log file (inculding logs from all called packages like requests etc.)
logging.basicConfig(level=logging.DEBUG,
                    filename="log/wmp_parser_" + LOCALTIME + ".verbose.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# initialize a local logger
logger_local = logging.getLogger("ucms.birdie.parser.wmp")
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


def get_CMHO_product():
    """
    招商银行 C10308
    请求格式：http get
    返回格式：json
    :return:
    """
    legal_group = 'CMHO'
    issuer_code = 'C10308'
    product_data = []
    root_url = 'http://www.cmbchina.com'

    # 保本
    index_url = 'http://www.cmbchina.com/CFWEB/svrajax/product.ashx?op=search&type=m&pageindex=1&salestatus=&baoben=Y' \
                '&currency=32&term=&keyword=&series=01&risk=&city=&date=&pagesize=20&orderby=ord1'
    # currency = 32 means USD

    logger_local.info(unicode(legal_group) + ' - Begin parsing...')

    total_page = json.loads(fix_json(requests.get(index_url).text.encode('utf-8')))["totalPage"]
    logger_local.debug('total page : '+unicode(total_page))

    for page_index in xrange(1, total_page + 1):
        _index_url = root_url + '/CFWEB/svrajax/product.ashx?op=search&type=m&pageindex=' + unicode(page_index) + \
                     '&salestatus=&baoben=Y&currency=32&term=&keyword=&series=01&risk=&city=&date=&pagesize=200'

        @retry(stop_max_attempt_number=10, wait_fixed=500)
        def request_content():
            return requests.get(_index_url)
        response = request_content()
        data_string = json.loads(fix_json(response.text.encode('utf-8')))

        for pd in data_string["list"]:
            if pd["IsCanBuy"] == 'true':
                product_data.append([issuer_code,
                                     pd["AreaCode"],
                                     filter(unicode.isdigit, pd["BeginDate"]),
                                     u'USD',
                                     filter(unicode.isdigit, pd["EndDate"]),
                                     filter(unicode.isdigit, pd["ExpireDate"]),
                                     filter(unicode.isdigit, pd["FinDate"]),
                                     pd["IncresingMoney"],
                                     pd["InitMoney"],
                                     u"Y",  # pd["IsCanBuy"]
                                     u"Y",  # preservable
                                     # pd["IsNewFlag"],
                                     re.sub(r'[^\d.]+', '', pd["NetValue"]),
                                     pd["PrdCode"],
                                     pd["PrdName"],
                                     pd["Risk"],
                                     pd["SaleChannel"],
                                     pd["SaleChannelName"],
                                     pd["Status"],
                                     pd["Style"],
                                     pd["Term"],
                                     pd["TypeCode"]])
                logger_local.debug(unicode(legal_group) + ' - ' + repr_zh(product_data[-1]))
                # logger_local.debug(unicode(legal_group) + ' - ' + json.dumps(product_data[-1],
                #                                                              ensure_ascii=False,
                #                                                              indent=2))

    index_url = 'http://www.cmbchina.com/CFWEB/svrajax/product.ashx?op=search&type=m&pageindex=1&salestatus=&baoben=N' \
                '&currency=32&term=&keyword=&series=01&risk=&city=&date=&pagesize=20&orderby=ord1'
    # currency = 32 means USD
    # currency = 29 means AUD

    total_page = json.loads(fix_json(requests.get(index_url).text.encode('utf-8')))["totalPage"]
    logger_local.debug('total page : '+unicode(total_page))

    for page_index in xrange(1, total_page + 1):
        _index_url = root_url + '/CFWEB/svrajax/product.ashx?op=search&type=m&pageindex=' + unicode(page_index) + \
                     '&salestatus=&baoben=N&currency=32&term=&keyword=&series=01&risk=&city=&date=&pagesize=200'
        response = requests.get(_index_url)
        data_string = json.loads(fix_json(response.text.encode('utf-8')))

        for pd in data_string["list"]:
            if pd["IsCanBuy"] == 'true':
                product_data.append([issuer_code,
                                     pd["AreaCode"],
                                     filter(unicode.isdigit, pd["BeginDate"]),
                                     u'USD',
                                     filter(unicode.isdigit, pd["EndDate"]),
                                     filter(unicode.isdigit, pd["ExpireDate"]),
                                     filter(unicode.isdigit, pd["FinDate"]),
                                     pd["IncresingMoney"],
                                     pd["InitMoney"],
                                     u"Y",  # pd["IsCanBuy"]
                                     u"N",  # preservable
                                     # pd["IsNewFlag"],
                                     re.sub(r'[^\d.]+', '', pd["NetValue"]),
                                     pd["PrdCode"],
                                     pd["PrdName"],
                                     pd["Risk"],
                                     pd["SaleChannel"],
                                     pd["SaleChannelName"],
                                     pd["Status"],
                                     pd["Style"],
                                     pd["Term"],
                                     pd["TypeCode"]])
                logger_local.debug(unicode(legal_group) + ' - ' + repr_zh(product_data[-1]))

    # DB manipulation:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='OW' and issuer_code=%s
                      and date(update_time)=curdate()""", (issuer_code,))
    logger_local.info(unicode(legal_group) + ' - ' + unicode(cursor.rowcount) + ' rows deleted')

    add_product = ("""INSERT INTO t_product
                      (issuer_code, sales_region, start_date, currency, end_date, value_date, tenor,
                       increasing_amount, starting_amount, buyable, preservable, expected_highest_yield, prod_code,
                       prod_name, risk_desc, sales_channel, sales_channel_desc, status, coupon_type_desc,
                       tenor_desc, coupon_type, data_source, update_time)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                              'OW', now())""")

    for p in product_data:
        cursor.execute(add_product, p)

    cnx.commit()
    cursor.close()
    logger_local.info(unicode(legal_group) + ' - ' + unicode(len(product_data)) + ' products imported')


def get_CMHO2_product():

    index_url = 'https://pbsz.ebank.cmbchina.com/CmbBank_Invest/UI/InvestPC/Financing/CFHomeV3.aspx'
    index_url = 'https://mall.bank.ecitic.com/fmall/pd/fin-pic-index.htm'


    response = requests.post(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    print soup



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


def get_ABCI_product():
    """
    农业银行 C10103
    请求格式：http get
    返回格式：json
    :return:
    """
    legal_group = 'ABCI'
    issuer_code = 'C10103'
    # page_index = 1
    # page_max = 150
    root_url = 'http://ewealth.abchina.com'
    manual_url = 'http://ewealth.abchina.com/fs/filter/'
    index_url = 'http://ewealth.abchina.com/app/data/api/DataService/BoeProductV2?i=1&s=100&o=0&w=%25E5%258F%25AF%2' \
                '5E5%2594%25AE%257C%257C%257C%25E7%25BE%258E%25E5%2585%2583%257C%257C%257C%257C1%257C%257C0%257C%257C0'
    product_data = []
    logger_local.info(unicode(legal_group) + ' - Begin parsing...')

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    data_string = json.loads(soup.text)

# <ProductNo>BF161002</ProductNo>
# <ProdName>“金钥匙·本利丰”2016年第1002期美元理财产品</ProdName>
# <ProdClass>封闭</ProdClass>
# <ProdLimit>363天</ProdLimit>
# <ProdProfit>1.3%</ProdProfit>
# <ProdYildType>保证收益</ProdYildType>
# <PrdYildTypeOrder>0</PrdYildTypeOrder>
# <ProdArea>全国发行</ProdArea>
# <szComDat>2016.01.12</szComDat>
# <ProdSaleDate>16.01.12-16.01.18</ProdSaleDate>
# <IsCanBuy>0</IsCanBuy>
# <PurStarAmo>9000.00</PurStarAmo>
# <RowNumber>1</RowNumber>

    for p in data_string["Data"]["Table"]:
        product_data.append([issuer_code,
                             issuer_list[issuer_code],
                             u'USD',
                             p["ProductNo"],
                             p["ProdName"],
                             p["ProdClass"],
                             re.sub(r'[^\d]+', '', p["ProdLimit"]),
                             decode(re.sub(r'[^\d.]+', '', p["ProdProfit"]),
                                    u'', u'0',
                                    re.sub(r'[^\d.]+', '', p["ProdProfit"])),
                             decode(p["ProdYildType"], u'保证收益', u'Y', u'N'),
                             p["ProdArea"],
                             re.sub(r'[^\d]+', '', p["szComDat"]),
                             '20' + re.sub(r'[^\d]+', '', p["ProdSaleDate"].split("-")[0]),
                             '20' + re.sub(r'[^\d]+', '', p["ProdSaleDate"].split("-")[1])])
        logger_local.debug(unicode(legal_group) + ' - ' + repr_zh(product_data[-1]))

    # DB manipulation:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='OW' and issuer_code=%s
                      and date(update_time)=curdate()""", (issuer_code,))
    logger_local.info(unicode(legal_group) + ' - ' + unicode(cursor.rowcount) + ' rows deleted')

    add_product = ("""INSERT INTO t_product
                (issuer_code, issuer_name, currency, prod_code, prod_name, redeemable, tenor, expected_highest_yield,
                 preservable, sales_region_desc, start_date, open_start_date, open_end_date, buyable, data_source,
                 update_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Y', 'OW', now())""")

    for p in product_data:
        cursor.execute(add_product, p)

    cnx.commit()
    cursor.close()
    logger_local.info(unicode(legal_group) + ' - ' + unicode(len(product_data)) + ' products imported')


def get_CCBH_product():
    """
    建设银行 C10105
    请求格式：http post
    返回格式：html
    :return:
    """
    legal_group = 'CCBH'
    issuer_code = 'C10105'
    root_url = 'http://finance.ccb.com'
    index_url = 'http://finance.ccb.com/Channel/3080'
    product_data = []
    logger_local.info(unicode(legal_group) + ' - Begin parsing...')

    response = requests.post(index_url, data={"querytype": "query", "saleStatus": "2", "investmentCurrency": "14"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    pl_data_table = soup.find("table", id="pl_data_list")

    for child in pl_data_table.children:
        if isinstance(child, bs4.element.Tag):
            if child.has_attr("onmouseover"):
                if child["onmouseover"] == "this.className='table_select_bg AcqProductItem'":
                    cells = child.find_all("td")
                    product_data.append([issuer_code,
                                         cells[13]["id"],
                                         cells[0]["title"],
                                         u'USD',
                                         cells[4].string.strip(),
                                         decode(re.sub(r'[^\d.]+', '', cells[11].string),
                                                u'', u'0',
                                                re.sub(r'[^\d.]+', '', cells[11].string)),
                                         decode(cells[12].string.strip(), u'低风险', u'L', u''),
                                         cells[1].string.strip(),
                                         u'',
                                         ]
                                        )
                    logger_local.debug(unicode(legal_group) + ' - ' + repr_zh(product_data[-1]))

    # DB manipulation:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='OW' and issuer_code=%s
                      and date(update_time)=curdate()""", (issuer_code,))
    logger_local.info(unicode(legal_group) + ' - ' + unicode(cursor.rowcount) + ' rows deleted')

    add_product = ("""INSERT INTO t_product
                      (issuer_code, prod_code, prod_name,currency, tenor_desc, expected_highest_yield, risk_desc,
                       status, remark, buyable, data_source, update_time)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Y', 'OW', now())""")

    for p in product_data:
        cursor.execute(add_product, p)

    cnx.commit()
    cursor.close()
    logger_local.info(unicode(legal_group) + ' - ' + unicode(len(product_data)) + ' products imported')


def get_CTIB_product():
    """
    中信银行 C10302
    请求格式：http post
    返回格式：html
    :return:
    """
    legal_group = 'CTIB'
    issuer_code = 'C10302'
    root_url = 'http://finance.ccb.com'
    index_url = 'https://mall.bank.ecitic.com/fmall/pd/fin-pic-index.htm'
    prod_data = []
    product_data = []
    logger_local.info(unicode(legal_group) + ' - Begin parsing...')

    response = requests.post(index_url, data={"curr_type": "014", "orderasc": "desc"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    pl_data_list = soup.find_all("div", class_="fund_listw2")

    for pl in pl_data_list:
        prod_data.append([])
        prod_code = pl.ul.li.input["value"]
        prod_url = 'https://mall.bank.ecitic.com/fmall/finproduct/' + prod_code + '.html'
        prod_response = requests.get(prod_url)
        prod_response.encoding = 'utf-8'
        prod_soup = bs4.BeautifulSoup(prod_response.text, "html.parser")

        prod_detail_data_tr = prod_soup.find("table", class_="conduct_table").find_all("tr")

        for p_tr in prod_detail_data_tr:
            prod_data[-1].append([])
            prod_data_td = p_tr.find_all("td")
            for p_td in prod_data_td:
                prod_data[-1][-1].append(p_td.text)

    for p in prod_data:
        product_data.append([issuer_code,
                             p[0][1],  # prod_code
                             p[0][3],  # prod_name
                             u"USD",
                             p[1][3],  # risk_desc
                             re.sub(r"[^\d]+", "", p[3][1]),  # tenor
                             re.sub(r"[^\d]+", "", p[4][1]),  # value date
                             re.sub(r"[^\d]+", "", p[4][3]),  # maturity date
                             re.sub(r"[^\d.]+", "", p[5][1])  # yield
                            ])
        logger_local.debug(unicode(legal_group) + ' - ' + repr_zh(product_data[-1]))

         # [[u'产品代码', u'B160A0074', u'产品名称', u'汇赢1609期对私'],
         #  [u'币种', u'美元', u'风险等级', u'较低风险'],
         #  [u'产品状态', u'募集期', u'管理机构', u'中信银行'],
         #  [u'产品期限', u'367天', u'首次购买起点', u'0万元'],
         #  [u'起息日', u'2016-02-19', u'到期日', u'2017-02-20'],
         #  [u'符合条件的预期年化收益率',
         #   u'2.200%',
         #   u'净值日期',
         #   u'2016-02-14'],
         #  [u'下一开放日', u'2016-02-16', u'产品净值', u'1.0000'],
         #  [u'赎回单笔上限', u'0.00', u'赎回单笔下限', u'0.00'],
         #  [u'认购单笔上限', u'0.00', u'认购单笔下限', u'0.00'],
         #  [u'申购单笔上限', u'0.00', u'申购单笔下限', u'0.00'],
         #  [u'赎回基数', u'0.00', u'认购基数', u'0.00'],
         #  [u'申购基数', u'100.00', u'是否允许赎回', u'否'],
         #  [u'是否允许预约赎回', u'否', u'是否允许实时赎回', u'否'],
         #  [u'是否专属理财产品',
         #   u'  否 ',
         #   u'专属销售有效期至',
         #   u'- '],
         #  [u'产品面向客户群', u'', u'销售区域', u'全国  ']]

    # DB manipulation:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='OW' and issuer_code=%s
                      and date(update_time)=curdate()""", (issuer_code,))
    logger_local.info(unicode(legal_group) + ' - ' + unicode(cursor.rowcount) + ' rows deleted')

    add_product = ("""INSERT INTO t_product
                      (issuer_code, prod_code, prod_name, currency, risk_desc, tenor, value_date, maturity_date,
                      expected_highest_yield, buyable, data_source, update_time)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Y', 'OW', now())""")

    for p in product_data:
        cursor.execute(add_product, p)

    cnx.commit()
    cursor.close()
    logger_local.info(unicode(legal_group) + ' - ' + unicode(len(product_data)) + ' products imported')


def get_BCOH_product():
    """
    交通银行 C10301, 详细页面根据用户类型有不同收益率
    请求格式：http get
    返回格式：html
    :return:
    """
    legal_group = 'BCOH'
    issuer_code = 'C10301'
    root_url = 'http://www.bankcomm.com'
    index_url = 'http://www.bankcomm.com/BankCommSite/zonghang/cn/lcpd/queryFundInfoList.do?currency=2' \
                '&tradeType=-1&safeFlg=-1&ratio=-1&term=-4&asc=-undefined'
    product_data = []
    logger_local.info(unicode(legal_group) + ' - Begin parsing...')

    try:
        response = requests.get(index_url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        dl_data_list = soup.find("div", class_="con_main").find_all("dl")

        for dl in dl_data_list:
            span_list = dl.dt.find_all("span")
            product_data.append([issuer_code,
                                 dl["id"].strip(),
                                 span_list[0].text.strip(),
                                 re.sub(r"[^\d]+", "", span_list[1].text),
                                 re.sub(r"[^\d]+", "", span_list[2].text),
                                 re.sub(r"[^\d.]+", "", span_list[3].text),
                                 span_list[4].text.strip(),
                                 re.sub(r"[^\d.]+", "", dl.dd.h3.text)])
            logger_local.debug(unicode(legal_group) + ' - ' + repr_zh(product_data[-1]))

        # for pl in pl_data_list:
        #     for child in pl.children:
        #         if isinstance(child, bs4.element.Tag):
        #             cells = child.dt.find_all("span")
        #             for string in child.dd.h3.strings:
        #                 __yield = unicode(string)
        #                 break
        #             product_data.append({"ProdID": child["id"].strip(),
        #                                  "ProdName": cells[0].string.strip(),
        #                                  "Tenor": re.sub(ur'[^\d\u5929]+', '', cells[1].string),
        #                                  "ValueDate": re.sub(r'[^\d-]+', '', cells[2].string),
        #                                  "Risk": cells[4].string.strip()[7:],
        #                                  "Yield": __yield})

        # DB manipulation:
        cursor = cnx.cursor()
        cursor.execute("""DELETE FROM t_product WHERE data_source='OW' and issuer_code=%s
                          and date(update_time)=curdate()""", (issuer_code,))
        logger_local.info(unicode(legal_group) + ' - ' + unicode(cursor.rowcount) + ' rows deleted')

        add_product = ("""INSERT INTO t_product
                    (issuer_code, prod_code, prod_name, tenor, maturity_date, starting_amount, risk_desc,
                     expected_highest_yield, buyable, data_source, update_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Y', 'OW', now())""")

        for p in product_data:
            cursor.execute(add_product, p)

        cnx.commit()
        cursor.close()
        logger_local.info(unicode(legal_group) + ' - ' + unicode(len(product_data)) + ' products imported')

    except Exception, err:
        # logger_local.warning(unicode(sys.exc_info()[0]) + u':' + unicode(sys.exc_info()[1]))
        logger_local.exception(unicode(legal_group))
        # logger_local.exception(traceback.format_exc())


def get_EBBC_product():
    """
    光大银行 C10303
    request：http post
    data format：html
    :return:
    """
    legal_group = 'EBBC'
    issuer_code = 'C10303'
    index_url = 'http://www.cebbank.com/eportal/ui?pageId=478550&currentPage=1&moduleId=12218'
    # on sale, USD product
    product_data = []
    logger_local.info(unicode(legal_group) + ' - Begin parsing...')

    response = requests.post(index_url, data={"filter_combinedQuery_SFZS": "1", "filter_EQ_TZBZMC": "美元"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # count total page
    total_count_tag = soup.find("i", attrs={"class": "listshu"})
    total_count = int(total_count_tag.string)
    total_page = -(-total_count // 20)

    # debug
    logger_local.info("total_count: " + str(total_count))
    logger_local.info("total_page: " + str(total_page))

    # iterate
    for page in range(total_page):
        index_url = 'http://www.cebbank.com/eportal/ui?pageId=478550&currentPage=' + unicode(
            page + 1) + '&moduleId=12218'

        @retry(stop_max_attempt_number=10, wait_fixed=500)
        def request_content():
            return requests.post(index_url, data={"filter_combinedQuery_SFZS": "1", "filter_EQ_TZBZMC": u"美元"})

        response = request_content()
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        prod_data_list = soup.find("table", class_="zslccp").find_all("tr")
        for pl in prod_data_list[1:]:
            pd = pl.find_all("td")

            @retry(stop_max_attempt_number=10, wait_fixed=500)
            def request_content():
                return requests.get('http://www.cebbank.com/' + pd[1].a["href"], timeout=10)

            prod_response = request_content()
            prod_response.encoding = 'utf-8'
            soup = bs4.BeautifulSoup(prod_response.text, "html.parser")
            prod_detail_table = soup.find("table", class_="table-infor")

            # print prod_detail_table

            product_data.append([issuer_code,
                                 pd[0].string.strip(),  # prod code
                                 pd[1].a.string.strip(),  # prod name
                                 re.sub(r'[^\d]+', '', pd[2].string),  # open start date
                                 re.sub(r'[^\d]+', '', pd[3].string),  # open end date
                                 u"N" if (u"非保本" in pd[4].string) else u"Y",  # preservable
                                 u"USD",  # currency
                                 re.sub(r'[^\d.]+', '', pd[8].string),  # yield
                                 pd[9].string.strip(),  # risk
                                 re.sub(r'[^\d]+', '', prod_detail_table.find("td", id="cpsyqsr").string.strip()),
                                 # value date
                                 re.sub(r'[^\d]+', '', prod_detail_table.find("td", id="cpdqr").string.strip()),
                                 # maturity date
                                 tenor_decoder(prod_detail_table.find("td", id="cpqx").string.strip()),
                                 prod_detail_table.find("td", id="cpqx").string.strip(),  # tenor_desc
                                 re.sub(r'[^\d.]+', '', prod_detail_table.find("td", id="qgje").string.strip()),
                                 # starting amount
                                 re.sub(r'[^\d.]+', '', prod_detail_table.find("td", id="dzje").string.strip()),
                                 # increasing amount
                                 'http://www.cebbank.com/' + pd[1].a["href"]  # remark
                                 ])
            logger_local.debug(unicode(legal_group) + ' - ' + repr_zh(product_data[-1]))

    response = requests.post(index_url, data={"filter_combinedQuery_SFZS": "1", "filter_EQ_TZBZMC": "澳元"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # count total page
    total_count_tag = soup.find("i", attrs={"class": "listshu"})
    total_count = int(total_count_tag.string)
    total_page = -(-total_count // 20)

    # debug
    logger_local.info("total_count: " + str(total_count))
    logger_local.info("total_page: " + str(total_page))

    # iterate
    for page in range(total_page):
        index_url = 'http://www.cebbank.com/eportal/ui?pageId=478550&currentPage=' + unicode(
            page + 1) + '&moduleId=12218'

        @retry(stop_max_attempt_number=10, wait_fixed=500)
        def request_content():
            return requests.post(index_url, data={"filter_combinedQuery_SFZS": "1", "filter_EQ_TZBZMC": u"美元"})

        response = request_content()
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        prod_data_list = soup.find("table", class_="zslccp").find_all("tr")
        for pl in prod_data_list[1:]:
            pd = pl.find_all("td")

            @retry(stop_max_attempt_number=10, wait_fixed=500)
            def request_content():
                return requests.get('http://www.cebbank.com/' + pd[1].a["href"], timeout=10)

            prod_response = request_content()
            prod_response.encoding = 'utf-8'
            soup = bs4.BeautifulSoup(prod_response.text, "html.parser")
            prod_detail_table = soup.find("table", class_="table-infor")

            # print prod_detail_table

            product_data.append([issuer_code,
                                 pd[0].string.strip(),  # prod code
                                 pd[1].a.string.strip(),  # prod name
                                 re.sub(r'[^\d]+', '', pd[2].string),  # open start date
                                 re.sub(r'[^\d]+', '', pd[3].string),  # open end date
                                 u"N" if (u"非保本" in pd[4].string) else u"Y",  # preservable
                                 u"USD",  # currency
                                 re.sub(r'[^\d.]+', '', pd[8].string),  # yield
                                 pd[9].string.strip(),  # risk
                                 re.sub(r'[^\d]+', '', prod_detail_table.find("td", id="cpsyqsr").string.strip()),
                                 # value date
                                 re.sub(r'[^\d]+', '', prod_detail_table.find("td", id="cpdqr").string.strip()),
                                 # maturity date
                                 tenor_decoder(prod_detail_table.find("td", id="cpqx").string.strip()),  # tenor
                                 prod_detail_table.find("td", id="cpqx").string.strip(),  # tenor_desc
                                 re.sub(r'[^\d.]+', '', prod_detail_table.find("td", id="qgje").string.strip()),
                                 # starting amount
                                 re.sub(r'[^\d.]+', '', prod_detail_table.find("td", id="dzje").string.strip()),
                                 # increasing amount
                                 'http://www.cebbank.com/' + pd[1].a["href"]  # remark
                                 ])
            logger_local.debug(unicode(legal_group) + ' - ' + repr_zh(product_data[-1]))

    # DB manipulation:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='AT' and issuer_code=%s""", (issuer_code,))
    logger_local.info(unicode(legal_group) + ' - ' + unicode(cursor.rowcount) + ' rows deleted')

    add_product = ("""INSERT INTO t_product
                (issuer_code, prod_code, prod_name, open_start_date, open_end_date, preservable, currency,
                expected_highest_yield, risk_desc, value_date, maturity_date, tenor, tenor_desc, starting_amount,
                increasing_amount, remark, buyable, data_source, update_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Y', 'AT', now())""")

    for p in product_data:
        cursor.execute(add_product, p)

    cnx.commit()
    cursor.close()
    logger_local.info(unicode(legal_group) + ' - ' + unicode(len(product_data)) + ' products imported')


def get_DESZ_product():
    """
    平安银行 C10307
    request：http get
    response：html
    :return:
    """
    legal_group = 'DESZ'
    issuer_code = 'C10307'
    product_data = []
    index_url = 'http://chaoshi.pingan.com/bankListIframe.shtml'
    logger_local.info(unicode(legal_group) + ' - Begin parsing...')

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # parse
    total_count_tag = soup.find("meta", attrs={"name": "WT.oss_r"})
    total_count = int(total_count_tag["content"])
    total_page = -(-total_count // 10)

    # debug
    logger_local.debug("total_count: " + str(total_count))
    logger_local.debug("total_page: " + str(total_page))

    # 遍历
    for page in range(total_page):
        logger_local.debug("current page: " + str(page+1))

        @retry(stop_max_attempt_number=10, wait_fixed=500)
        def request_content():
            return requests.get('http://chaoshi.pingan.com/bankListIframe.shtml?npage=' + unicode(page + 1),
                                timeout=10)
        response = request_content()
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        prod_list_div = soup.find("div", class_="search_list_box")
        prod_detail_div = prod_list_div.find_all("div")

        for pd in prod_detail_div:
            # 判断是否有停售标志
            on_sale = pd.find("i", class_="ts")
            # 如果非停售(在售)
            if not on_sale:
                # 获取产品详细页面链接
                pd_a = pd.find("a", class_="detail_btn")
                rs = re.search(r"http\S*html", pd_a["onclick"])
                detail_url = rs.group()
                pd_code = re.sub(r"[(http:\/\/licai\.pingan\.com\/licaichanpin\/).shtml]+", "", detail_url)
                pd_name = pd.h1.a.text.strip()

                @retry(stop_max_attempt_number=10, wait_fixed=500)
                def pd_request_content():
                    return requests.get(detail_url, timeout=10)
                pd_response = pd_request_content()
                pd_soup = bs4.BeautifulSoup(pd_response.text, "html.parser")

                try:
                    pd_table = pd_soup.find("table", class_="detail_tab3")
                    pd_currency = pd_table.tbody.find_all("tr")[2].find_all("td")[3].text.strip()
                except AttributeError:
                    pd_currency = u"N/A"

                if pd_currency == u"美元" or pd_currency == u"澳元":
                    try:
                        product_data.append([issuer_code,
                                             pd_name,
                                             pd_code,
                                             currency_decoder(pd_currency),
                                             # open_start_date
                                             re.sub(r"[^\d]+", "",
                                                    pd_table.tbody.find_all("tr")[0].find_all("td")[1].text)[:8],
                                             # open_end_date
                                             re.sub(r"[^\d]+", "",
                                                    pd_table.tbody.find_all("tr")[0].find_all("td")[3].text),
                                             # value date
                                             re.sub(r"[^\d]+", "",
                                                    pd_table.tbody.find_all("tr")[1].find_all("td")[1].text),
                                             # maturity date
                                             re.sub(r"[^\d]+", "",
                                                    pd_table.tbody.find_all("tr")[1].find_all("td")[3].text),
                                             # tenor
                                             re.sub(r"[^\d]+", "",
                                                    pd_table.tbody.find_all("tr")[2].find_all("td")[1].text),
                                             # expected yield
                                             re.sub(r"[^\d.]+", "",
                                                    pd_table.tbody.find_all("tr")[4].find_all("td")[1].text),
                                             # remark
                                             detail_url])
                    except:
                        e = sys.exc_info()[0]
                        logger_local.error("Error: %s" % e)

                    logger_local.debug(unicode(legal_group) + ' - ' + repr_zh(product_data[-1]))

    # for child in pl_data_list.children:
    #     if isinstance(child, bs4.element.Tag):
    #         if "人民币" not in child.h1.a.string:
    #             print unicode(page + 1) + ':' + child.h1.a.string + ':',
    #             # 打开详情页面
    #             rs = re.search(r"http\S*html", child.h1.a["onclick"])
    #             detail_url = rs.group()
    #             p_soup = bs4.BeautifulSoup(requests.get(detail_url).text, "html.parser")
    #             pl_table = p_soup.find("table", class_="detail_tab3")
    #             pl_tds = pl_table.tbody.find_all("td")
    #
    #             product_data.append({"ProdCode": re.sub(r'.shtml', '', detail_url.split("/")[-1]),
    #                                  "ProdName": child.h1.a.string.strip(),
    #                                  "StartDate": re.sub(r'[^\d]+', '', pl_tds[1].stripped_strings.next()),
    #                                  "EndDate": re.sub(r'[^\d]+', '', pl_tds[3].string),
    #                                  "ValueDate": re.sub(r'[^\d]+', '', pl_tds[5].string),
    #                                  "MaturityDate": re.sub(r'[^\d]+', '', pl_tds[7].string),
    #                                  "Tenor": re.sub(ur'[^\d\u5929]+', '', pl_tds[9].string),
    #                                  "Currency": pl_tds[11].string.strip(),
    #                                  "Yield": re.sub(r'[^\d.]+', '', pl_tds[17].string),
    #                                  "CouponType": "Fixed" if ("固定" in pl_tds[19].string) else "Floating",
    #                                  "Preservable": "Y" if ("保本" in pl_tds[19].string) else "N",
    #                                  "Remark": detail_url
    #                                  })
    #             ppprint(product_data[-1])

    # DB manipulation:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='OW' and issuer_code=%s
                      and date(update_time)=curdate()""", (issuer_code,))
    logger_local.info(unicode(legal_group) + ' - ' + unicode(cursor.rowcount) + ' rows deleted')

    add_product = ("""INSERT INTO t_product
                (issuer_code, prod_name, prod_code, currency, open_start_date, open_end_date, value_date, maturity_date,
                tenor, expected_highest_yield, remark, buyable, data_source, update_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Y', 'OW', now())""")

    for p in product_data:
        cursor.execute(add_product, p)

    cnx.commit()
    cursor.close()
    logger_local.info(unicode(legal_group) + ' - ' + unicode(len(product_data)) + ' products imported')


def get_IBCN_product():
    """
    兴业银行
    请求格式：http post
    返回格式：html
    :return:
    """
    legal_group = 'IBCN'
    issuer_code = 'C10309'
    index_url = 'http://wealth.cib.com.cn/retail/onsale/index.html'
    product_data = []
    logger_local.info(unicode(legal_group) + ' - Begin parsing...')

    @retry(stop_max_attempt_number=10, wait_fixed=500)
    def request_content():
        return requests.post(index_url, timeout=TIMEOUT)

    response = request_content()
    response.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    prod_list_tr = soup.find("table", id="finTable").tbody.find_all("tr")

    for pd_tr in prod_list_tr:
        if pd_tr.find_all("td")[3].text.strip() == u'美元':
            detail_url = prod_list_tr[0].find("td").a["href"]
            break

    @retry(stop_max_attempt_number=10, wait_fixed=500)
    def request_content():
        return requests.post(index_url, timeout=TIMEOUT)

    pd_response = request_content()
    pd_response.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(pd_response.text, "html.parser")


# 浦发银行
# 需要登录
def get_SPDB_product():
    pass


# 上海银行
# 请求格式：http get
# 返回格式：html
# 解析方法：soup find all
# 需要分析公告
def get_SHDB_product():
    pass


# 北京银行
# 需要登录
def get_BKDB_product():
    pass


def get_CW_product():
    """
    中国理财网
    请求格式：http post
    返回格式：html
    :return:
    """
    product_data = []
    index_url = 'http://www.chinawealth.com.cn/lccpAllProJzyServlet.go'
    logger_local.info('ChinaWealth - Begin parsing...')

    response = requests.post(index_url, data={"cpzt": "02,04", "pagenum": "1", "drawPageToolEnd": "5"})

    total_count = json.loads(response.text.encode('utf-8'))["Count"]
    total_page = -(-total_count // 500)

    # debug
    logger_local.info("total_count: " + str(total_count))
    logger_local.info("total_page: " + str(total_page))

    for page_index in xrange(1, total_page + 1):

        @retry(stop_max_attempt_number=10, wait_fixed=500)
        def request_content():
            return requests.post(index_url,
                                 data={"cpzt": "02,04", "pagenum": page_index, "drawPageToolEnd": "5"},
                                 timeout=TIMEOUT)
        response = request_content()

        data_string = json.loads(response.text.encode('utf-8'))

        for pd in data_string["List"]:
            if 'CNY' not in pd["mjbz"]:
                product_data.append([pd["cpid"],  # 产品id
                                     pd["cpdjbm"],  # 产品登记编码
                                     pd["cpdm"],  # 产品代码
                                     pd["cpms"],  # 产品描述
                                     pd["fxjgdm"],  # 发行机构代码
                                     pd["fxjgms"],  # 发行机构描述
                                     pd["mjbz"],  # 募集币种
                                     pd["cpqx"],  # 产品期限
                                     pd["qxms"],  # 期限描述
                                     pd["mjqsrq"],  # 募集起始日期
                                     pd["mjjsrq"],  # 募集结束日期
                                     pd["kfzqqsr"],  # 开放周期起始日
                                     pd["kfzqjsr"],  # 开放周期结束日
                                     pd["cpqsrq"],  # 产品起始日期
                                     pd["cpyjzzrq"],  # 产品预计终止日期
                                     pd["cplx"],  # 产品类型
                                     pd["cplxms"],  # 产品类型描述(如: 封闭式非净值型)
                                     pd["cpsylx"],  # 产品收益类型
                                     pd["cpsylxms"],  # 产品收益类型描述(如: 保本浮动收益)
                                     pd["cpfxdj"],  # 产品风险等级
                                     pd["fxdjms"],  # 风险等级描述
                                     pd["cpjz"],  # 产品净值
                                     pd["bqjz"],  # bq净值
                                     pd["csjz"],  # cs净值
                                     pd["xsqy"],  # 销售区域
                                     pd["cpxsqy"],  # 产品销售区域
                                     pd["orderby"],  # order
                                     pd["yjkhzgnsyl"],  # 预计客户最高年收益率
                                     pd["yjkhzdnsyl"],  # 预计客户最低年收益率
                                     pd["dqsjsyl"],  # 到期实际收益率
                                     pd["cpztms"],  # 产品状态描述
                                     pd["qdxsje"]])  # 起点销售金额
                logger_local.debug('ChinaWealth - ' + repr_zh(product_data[-1]))


    # 数据库操作
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='CW' and date(update_time)=curdate()""")
    logger_local.info(unicode(cursor.rowcount) + ' ChinaWealth products deleted')

    add_product = ("""INSERT INTO t_product
                      (prod_id, prod_reg_code, prod_code, prod_name, issuer_code, issuer_name, currency, tenor,
                      tenor_desc, start_date, end_date, open_start_date, open_end_date, value_date, maturity_date,
                      prod_type, prod_type_desc, coupon_type, coupon_type_desc, risk, risk_desc, net_value,
                      bq_net_value, cs_net_value, sales_region, sales_region_desc, order_by, expected_highest_yield,
                      expected_lowest_yield, actual_yield, status, starting_amount, data_source, update_time)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                              %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                              'CW', now())""")

    for p in product_data:
        cursor.execute(add_product, p)

    cnx.commit()
    cursor.close()
    logger_local.info(unicode(len(product_data)) + ' ChinaWealth products imported')

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



# query = ("SELECT first_name, last_name, hire_date FROM employees "
#          "WHERE hire_date BETWEEN %s AND %s")
#
# hire_start = datetime.date(1999, 1, 1)
# hire_end = datetime.date(1999, 12, 31)
#
# cursor.execute(query, (hire_start, hire_end))
#
# for (first_name, last_name, hire_date) in cursor:
#     result.append[]



def repr_zh(obj):
    return re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())


if __name__ == '__main__':
    DB_NAME = 'zyq'
    logger_local.info('')
    logger_local.info('')
    logger_local.info('============================================================')
    logger_local.info('')
    logger_local.info('WMP Parser starting...')
    logger_local.info('')
    logger_local.info('============================================================')

    try:
        cnx = mysql.connector.connect(host='localhost', user='zyq', password='zyq', database=DB_NAME)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        logger_local.info('MYSQL connected.')

    issuer_list = {}
    cursor = cnx.cursor()

    query = """select issuer_code, en_short_name from t_issuer where en_short_name is not null"""
    cursor.execute(query)
    for (issuer_code, en_short_name) in cursor:
        issuer_list[issuer_code] = en_short_name
    cursor.close()
    logger_local.info(issuer_list)

    # get_CMHO_product()
    # get_CMHO2_product()

    # get_ICBC_product()
    # get_ABCI_product()
    # get_CCBH_product()
    # get_CTIB_product()
    # get_BCOH_product()
    get_EBBC_product()
    # get_DESZ_product()
    # get_IBCN_product()
    # get_SPDB_product()
    # get_BKSH_product()
    # get_BOBJ_product()
    # get_CW_product()

    # generate_report()

    cnx.close()
