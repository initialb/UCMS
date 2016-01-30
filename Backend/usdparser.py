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
from butils.pprint import pprint
from datetime import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pprint as ppr
pp = ppr.PrettyPrinter(indent=4)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import random
from retrying import retry

TIMEOUT = 10

def get_CMHO_product():
    # 招商银行
    # 请求格式：http get
    # 返回格式：json

    legal_group = 'CMHO'
    root_url = 'http://www.cmbchina.com'
    index_url = 'http://www.cmbchina.com/CFWEB/svrajax/product.ashx?op=search&type=m&pageindex=1&salestatus=&baoben=' \
                '&currency=32&term=&keyword=&series=01&risk=&city=&date=&pagesize=20&orderby=ord1'
    # currency = 32 means USD

    total_page = json.loads(fix_json(requests.get(index_url).text.encode('utf-8')))["totalPage"]
    # logging.info('total page = '+unicode(total_page))

    j = []
    count = 0

    # delete all duplicated records:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='OW' and issuer_code='C10308'
     and date(update_time)=curdate()""")
    logging.info(unicode(cursor.rowcount) + ' ' + unicode(legal_group) + ' rows deleted')

    for page_index in xrange(1, total_page + 1):
        _index_url = root_url + '/CFWEB/svrajax/product.ashx?op=search&type=m&pageindex=' + unicode(page_index) + \
                     '&salestatus=&baoben=&currency=32&term=&keyword=&series=01&risk=&city=&date=&pagesize=200'
        response = requests.get(_index_url)
        j.append(fix_json(response.text.encode('utf-8')))
        data_string = json.loads(j[page_index - 1])

        # pp.pprint(data_string)

        product_data = []

        for i in range(len(data_string["list"])):
            # 预期收益格式化
            # ield = re.sub(r'[^\d.]+', '', data_string["list"][i]["NetValue"])
            # if ield == '':
            #     ield = 0
            if data_string["list"][i]["IsCanBuy"] == 'true':
                product_data.append([u'C10308',
                                     data_string["list"][i]["AreaCode"],
                                     filter(unicode.isdigit, data_string["list"][i]["BeginDate"]),
                                     u'USD',
                                     filter(unicode.isdigit, data_string["list"][i]["EndDate"]),
                                     filter(unicode.isdigit, data_string["list"][i]["ExpireDate"]),
                                     filter(unicode.isdigit, data_string["list"][i]["FinDate"]),
                                     data_string["list"][i]["IncresingMoney"],
                                     data_string["list"][i]["InitMoney"],
                                     data_string["list"][i]["IsCanBuy"],
                                     # data_string["list"][i]["IsNewFlag"],
                                     re.sub(r'[^\d.]+', '', data_string["list"][i]["NetValue"]),
                                     data_string["list"][i]["PrdCode"],
                                     data_string["list"][i]["PrdName"],
                                     data_string["list"][i]["Risk"],
                                     data_string["list"][i]["SaleChannel"],
                                     data_string["list"][i]["SaleChannelName"],
                                     data_string["list"][i]["Status"],
                                     data_string["list"][i]["Style"],
                                     data_string["list"][i]["Term"],
                                     data_string["list"][i]["TypeCode"],
                                     u'OW'])
                logging.debug(product_data[-1])

#
#                 query = ("SELECT first_name, last_name, hire_date FROM employees "
# #              "WHERE hire_date BETWEEN %s AND %s")
# #
# # hire_start = datetime.date(1999, 1, 1)
# # hire_end = datetime.date(1999, 12, 31)
# #
# # cursor.execute(query, (hire_start, hire_end))
# #
# # for (first_name, last_name, hire_date) in cursor:
# #   print("{}, {} was hired on {:%d %b %Y}".format(
# #     last_name, first_name, hire_date))



                add_product = ("""INSERT INTO t_product
                                  (issuer_code, sales_region, start_date, currency, end_date, value_date, tenor,
                                   increasing_amount, starting_amount, buyable, expected_highest_yield, prod_code,
                                   prod_name, risk, sales_channel, sales_channel_desc, status, coupon_type_desc,
                                   tenor_desc, coupon_type, data_source, update_time) VALUES (""" + "%s, "*21 +
                               """now())""")
                cursor.execute(add_product, product_data[-1])
                count += 1

    cnx.commit()
    cursor.close()
    logging.info(unicode(count) + ' CMHO products imported')


def get_ICBC_product():
    # 工商银行
    # 请求格式：http get
    # 返回格式：json

    root_url = 'http://www.icbc.com.cn'
    index_url = 'http://www.icbc.com.cn/ICBCDynamicSite2/money/services/MoenyListService.ashx?ctl1=4&ctl2=6&keyword='

    data_string = json.loads(requests.get(index_url).text.encode('utf-8'))
    logging.debug('data_string = ' + unicode(data_string))

    # pp.pprint(data_string)

    count = 0
    product_data = []

    # delete all duplicated records:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='OW' and issuer_code='C10102'
                   and date(update_time)=curdate()""")
    logging.info(unicode(cursor.rowcount) + ' ICBC rows deleted')

    for i in range(len(data_string)):
        product_data.append([data_string[i]["buyPaamt"],
                             decode(data_string[i]["buyflag"], '1', 'Y', 'N'),
                             # data_string[i]["categoryL1"],
                             # data_string[i]["categoryL2"],
                             data_string[i]["intendYield"],
                             # data_string[i]["introJs"],
                             # data_string[i]["isUnitValue"],
                             data_string[i]["matudate"],
                             data_string[i]["offerPeriod"][:8],
                             data_string[i]["offerPeriod"][-8:],
                             data_string[i]["prodID"],
                             filter(unicode.isalpha, data_string[i]["prodID"]),
                             filter(unicode.isdigit, data_string[i]["prodID"]),
                             # data_string[i]["prodintro"],
                             data_string[i]["productName"],
                             data_string[i]["productTerm"],
                             data_string[i]["saleZone"],
                             data_string[i]["sellStatus"],
                             u'C10102',
                             u'OW'])
                             # data_string[i]["totalValue"],
                             # data_string[i]["value"],
                             # data_string[i]["valueLink"],
                             # data_string[i]["workdate"]])
        logging.debug(product_data[i])
        add_product = ("INSERT INTO t_product "
                       "(starting_amount, buyable, expected_highest_yield, maturity_date, start_date, end_date,"
                       "prod_code, currency, tenor, prod_name, tenor_desc, sales_region_desc, status,"
                       "issuer_code, data_source, update_time) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())")
        cursor.execute(add_product, product_data[i])
        count += 1

    cnx.commit()
    cursor.close()
    logging.info(unicode(count) + ' ICBC products imported')


def get_CCBH_product():
    # 建设银行
    # 请求格式：http post
    # 返回格式：html

    root_url = 'http://finance.ccb.com'
    index_url = 'http://finance.ccb.com/Channel/3080'

    response = requests.post(index_url, data={"querytype": "query", "investmentCurrency": "14"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    pl_data_table = soup.find("table", id="pl_data_list")

    product_data = []

    for child in pl_data_table.children:
        if isinstance(child, bs4.element.Tag):
            if child.has_attr("onmouseover"):
                if child["onmouseover"] == "this.className='table_select_bg AcqProductItem'":
                    cells = child.find_all("td")
                    product_data.append([u'C10105',
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

    pprint(product_data)

    # delete all duplicated records:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='OW' and issuer_code='C10105'
                      and date(update_time)=curdate()""")
    logging.info(unicode(cursor.rowcount) + ' CCBH products deleted')

    for p in product_data:
        add_product = ("""INSERT INTO t_product
                          (issuer_code, prod_code, prod_name,currency, tenor_desc, expected_highest_yield, risk_desc,
                           status, remark, data_source, update_time)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'OW', now())""")
        cursor.execute(add_product, p)

    cnx.commit()
    cursor.close()
    logging.info(unicode(len(product_data)) + ' CCBH products imported')


def get_ABCI_product():
    # 农业银行
    # 请求格式：http get
    # 返回格式：json

    # page_index = 1
    # page_max = 150
    root_url = 'http://ewealth.abchina.com'
    # index_url = 'http://ewealth.abchina.com/app/data/api/DataService/BoeProductV2?i=1&s=15&o=0
    # &w=%257C%257C%257C%25E7%25BE%258E%25E5%2585%2583%257C%257C%257C%257C1%257C%257C0%257C%257C0'
    index_url = 'http://ewealth.abchina.com/app/data/api/DataService/BoeProductV2?i=1&s=100&o=0' \
                '&w=%257C%257C%257C%25E7%25BE%258E%25E5%2585%2583%257C%257C%257C%257C1%257C%257C0%257C%257C0'

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    data_string = json.loads(soup.text)

    # delete all duplicated records:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='OW' and issuer_code='C10103'
                      and date(update_time)=curdate()""")
    logging.info(unicode(cursor.rowcount) + ' ABCI products deleted')

    product_data = []

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
        product_data.append([u'C10103',
                             u'USD',
                             p["ProductNo"],
                             p["ProdName"],
                             p["ProdClass"],
                             p["ProdLimit"],
                             decode(re.sub(r'[^\d.]+', '', p["ProdProfit"]),
                                    u'', u'0',
                                    re.sub(r'[^\d.]+', '', p["ProdProfit"])),
                             decode(p["ProdYildType"], u'保证收益', u'Y', u'N'),
                             p["ProdArea"],
                             p["szComDat"],
                             p["ProdSaleDate"].split("-")[0],
                             p["ProdSaleDate"].split("-")[1]])

        add_product = ("""INSERT INTO t_product
                    (issuer_code, currency, prod_code, prod_name, redeemable, tenor, expected_highest_yield,
                     preservable, sales_region_desc, start_date, open_start_date, open_end_date, data_source,
                     update_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'OW', now())""")
        cursor.execute(add_product, product_data[-1])

    cnx.commit()
    cursor.close()
    logging.info(unicode(len(product_data)) + ' ABCI products imported')


def get_BCOH_product():
    # 交通银行
    # 请求格式：http get
    # 返回格式：html

    root_url = 'http://www.bankcomm.com'
    index_url = 'http://www.bankcomm.com/BankCommSite/zonghang/cn/lcpd/queryFundInfoList.do?currency=2' \
                '&tradeType=-1&safeFlg=-1&ratio=-1&term=-4&asc=-undefined'

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    dl_data_list = soup.find("div", class_="con_main").find_all("dl")

    product_data = []

    for dl in dl_data_list:
        span_list = dl.dt.find_all("span")
        product_data.append([dl["id"].strip(),
                             span_list[0].text.strip(),
                             span_list[1].text.strip(),
                             span_list[2].text.strip(),
                             span_list[3].text.strip().replace(" ",""),
                             span_list[4].text.strip(),
                             dl.dd.h3.text.strip()])

    pprint(product_data)

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


    # delete all duplicated records:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE issuer_code='C10301' and data_source='OW'
                      and date(update_time)=curdate()""")
    logging.info(unicode(cursor.rowcount) + ' BCOH products deleted')

    for p in product_data:
        add_product = ("""INSERT INTO t_product
                    (issuer_code, prod_code, prod_name, tenor, maturity_date, starting_amount, risk_desc,
                     expected_highest_yield, data_source, update_time)
                    VALUES ('C10301', %s, %s, %s, %s, %s, %s, %s, 'OW', now())""")
        cursor.execute(add_product, p)

    cnx.commit()
    cursor.close()
    logging.info(unicode(len(product_data)) + ' BCOH products imported')


def get_DESZ_product():
    # 平安银行
    # request：http get
    # response：html

    product_data = []

    index_url = 'http://chaoshi.pingan.com/bankListIframe.shtml'
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # parse
    total_count_tag = soup.find("meta", attrs={"name": "WT.oss_r"})
    total_count = int(total_count_tag["content"])
    total_page = -(-total_count // 10)

    # debug
    logging.info("total_count: " + str(total_count))
    logging.info("total_page: " + str(total_page))

    # 遍历
    for page in range(total_page):
        index_url = 'http://chaoshi.pingan.com/bankListIframe.shtml?npage=' + unicode(page + 1)
        try:
            response = requests.get(index_url)
        except requests.exceptions.Timeout as e:
            # Maybe set up for a retry, or continue in a retry loop
            print e
            sys.exit(1)
        except requests.exceptions.TooManyRedirects as e:
            # Tell the user their URL was bad and try a different one
            print e
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            print e
            sys.exit(1)

        soup = bs4.BeautifulSoup(response.text, "html.parser")

        pl_data_list = soup.find("div", class_="search_list_box")
        for child in pl_data_list.children:
            if isinstance(child, bs4.element.Tag):
                if "人民币" not in child.h1.a.string:
                    print unicode(page + 1) + ':' + child.h1.a.string + ':',
                    # 打开详情页面
                    rs = re.search(r"http\S*html", child.h1.a["onclick"])
                    detail_url = rs.group()
                    p_soup = bs4.BeautifulSoup(requests.get(detail_url).text, "html.parser")
                    pl_table = p_soup.find("table", class_="detail_tab3")
                    pl_tds = pl_table.tbody.find_all("td")

                    product_data.append({"ProdCode": re.sub(r'.shtml', '', detail_url.split("/")[-1]),
                                         "ProdName": child.h1.a.string.strip(),
                                         "StartDate": re.sub(r'[^\d]+', '', pl_tds[1].stripped_strings.next()),
                                         "EndDate": re.sub(r'[^\d]+', '', pl_tds[3].string),
                                         "ValueDate": re.sub(r'[^\d]+', '', pl_tds[5].string),
                                         "MaturityDate": re.sub(r'[^\d]+', '', pl_tds[7].string),
                                         "Tenor": re.sub(ur'[^\d\u5929]+', '', pl_tds[9].string),
                                         "Currency": pl_tds[11].string.strip(),
                                         "Yield": re.sub(r'[^\d.]+', '', pl_tds[17].string),
                                         "CouponType": "Fixed" if ("固定" in pl_tds[19].string) else "Floating",
                                         "Preservable": "Y" if ("保本" in pl_tds[19].string) else "N",
                                         "Remark": detail_url
                                         })
                    ppprint(product_data[-1])

    # 入库
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM PRODUCT WHERE LEGAL_GROUP='DESZ' and date(UPDATE_DATE)=curdate()""")
    logging.info(unicode(cursor.rowcount) + ' DESZ products deleted')

    for i in range(len(product_data)):
        product_detail = [u'DESZ',
                          product_data[i]["ProdCode"],
                          product_data[i]["ProdName"],
                          datetime.strptime(product_data[i]["StartDate"], '%Y%m%d'),
                          datetime.strptime(product_data[i]["EndDate"], '%Y%m%d'),
                          datetime.strptime(product_data[i]["ValueDate"], '%Y%m%d'),
                          datetime.strptime(product_data[i]["MaturityDate"], '%Y%m%d'),
                          product_data[i]["Tenor"],
                          product_data[i]["Currency"],
                          product_data[i]["CouponType"],
                          product_data[i]["Preservable"],
                          product_data[i]["Yield"],
                          product_data[i]["Remark"]]
        add_product = ("""INSERT INTO PRODUCT
                    (PROD_ID, LEGAL_GROUP, PROD_CODE, PROD_NAME, ISSUE_DATE, END_DATE, VALUE_DATE, MATURITY_DATE,
                    TENOR, CURRENCY, COUPONTYPE, PRESERVABLE, YIELD, REMARK, UPDATE_DATE)
                    VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        cursor.execute(add_product, product_detail)

    cnx.commit()
    cursor.close()
    logging.info(unicode(len(product_data)) + ' DESZ products imported')


def get_CTIB_product():
    # 中信银行
    # 请求格式：http post
    # 返回格式：html

    root_url = 'http://finance.ccb.com'
    index_url = 'https://mall.bank.ecitic.com/fmall/pd/fin-pic-index.htm'

    response = requests.post(index_url, data={"curr_type": "014", "orderasc": "desc", "branch_id": "701100",
                                              "skeywordsfin": "代码/名称"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    print soup

    pl_data_list = soup.find_all("div", class_="fund_listw2")

    product_data = []
    f = codecs.open("CTIB_result.html", encoding='utf-8', mode="w")

    for prod in pl_data_list:
        f.write(unicode(prod))
        for child in prod.descendants:
            if isinstance(child, bs4.element.Tag):
                if child.name == 'input':
                    if child.has_attr("field") and child["field"] == 'prod_no':
                        print child["finname"].encode("utf-8")

    f.close()


# 光大银行
# 请求格式：http post
# 返回格式：html

def get_EBBC_product():
    index_url = 'http://www.cebbank.com/eportal/ui?pageId=478550&currentPage=1&moduleId=12218'
    response = requests.post(index_url, data={"filter_EQ_TZBZMC": "美元"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    total_count_tag = soup.find("i", attrs={"class": "listshu"})
    total_count = int(total_count_tag.string)
    total_page = -(-total_count // 20)

    # debug
    logging.info("total_count: " + str(total_count))
    logging.info("total_page: " + str(total_page))

    product_data = []

    # 遍历
    for page in range(total_page):
        index_url = 'http://www.cebbank.com/eportal/ui?pageId=478550&currentPage=' + unicode(
            page + 1) + '&moduleId=12218'
        try:
            response = requests.post(index_url, data={"filter_EQ_TZBZMC": "美元"})
        except requests.exceptions.Timeout as e:
            # Maybe set up for a retry, or continue in a retry loop
            print e
            sys.exit(1)
        except requests.exceptions.TooManyRedirects as e:
            # Tell the user their URL was bad and try a different one
            print e
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            print e
            sys.exit(1)

        soup = bs4.BeautifulSoup(response.text, "html.parser")

        pl_data_list = soup.find("table", class_="zslccp").find_all("tr")
        for pl in pl_data_list[1:]:
            pd = pl.find_all("td")

            product_data.append({"ProdCode": pd[0].string.strip(),
                                 "ProdName": pd[1].a.string.strip(),
                                 "StartDate": re.sub(r'[^\d]+', '', pd[2].string),
                                 "EndDate": re.sub(r'[^\d]+', '', pd[3].string),
                                 "Preservable": "Y" if ("保本" in pd[4].string) else "N",
                                 "Currency": pd[5].string.strip(),
                                 "Yield": re.sub(r'[^\d.]+', '', pd[8].string),
                                 "Risk": pd[9].string.strip(),
                                 "Remark": 'http://www.cebbank.com/' + pd[1].a["href"]
                                 })
            ppprint(product_data[-1])

    # 数据库操作
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM PRODUCT WHERE LEGAL_GROUP='EBBC' and date(UPDATE_DATE)=curdate()""")
    logging.info(unicode(cursor.rowcount) + ' EBBC products deleted')

    for i in range(len(product_data)):
        product_detail = [u'EBBC',
                          product_data[i]["ProdCode"],
                          product_data[i]["ProdName"],
                          datetime.strptime(product_data[i]["StartDate"], '%Y%m%d'),
                          datetime.strptime(product_data[i]["EndDate"], '%Y%m%d'),
                          # datetime.strptime(product_data[i]["ValueDate"], '%Y%m%d'),
                          # datetime.strptime(product_data[i]["MaturityDate"], '%Y%m%d'),
                          # product_data[i]["Tenor"],
                          product_data[i]["Currency"],
                          # product_data[i]["CouponType"],
                          product_data[i]["Preservable"],
                          product_data[i]["Yield"],
                          product_data[i]["Risk"],
                          product_data[i]["Remark"]]
        add_product = ("""INSERT INTO PRODUCT
                    (PROD_ID, LEGAL_GROUP, PROD_CODE, PROD_NAME, ISSUE_DATE, END_DATE, CURRENCY,
                    PRESERVABLE, YIELD, RISK, REMARK, UPDATE_DATE)
                    VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        cursor.execute(add_product, product_detail)

    cnx.commit()
    cursor.close()
    logging.info(unicode(len(product_data)) + ' EBBC products imported')


# 兴业银行
# 请求格式：http post
# 返回格式：html

def get_IBCN_product():
    index_url = 'http://www.cib.com.cn/cn/Financing_Release/sale/mb22.html'

    response = requests.get(index_url, timeout=TIMEOUT)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    print soup

    pl_data_list = soup.find_all("div", class_="fund_listw2")

    product_data = []
    f = codecs.open("CTIB_result.html", encoding='utf-8', mode="w")

    for prod in pl_data_list:
        f.write(unicode(prod))
        for child in prod.descendants:
            if isinstance(child, bs4.element.Tag):
                if child.name == 'input':
                    if child.has_attr("field") and child["field"] == 'prod_no':
                        print child["finname"].encode("utf-8")

    f.close()


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


# 中国理财网
# 请求格式：http post
# 返回格式：html

def get_CW_product():
    index_url = 'http://www.chinawealth.com.cn/lccpAllProJzyServlet.go'
    response = requests.post(index_url, data={"cpzt": "02,04", "pagenum": "1", "drawPageToolEnd": "5"})

    total_count = json.loads(response.text.encode('utf-8'))["Count"]
    total_page = -(-total_count // 500)

    # debug
    logging.info("total_count: " + str(total_count))
    logging.info("total_page: " + str(total_page))

    j = []
    count = 0

    # delete all duplicated records:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM t_product WHERE data_source='ChinaWealth' and date(update_time)=curdate()""")
    logging.info(unicode(cursor.rowcount) + ' ChinaWealth ' + 'rows deleted')

    for page_index in xrange(1, total_page + 1):

        @retry(stop_max_attempt_number=10, wait_fixed=500)
        def request_content():
            return requests.post(index_url,
                                data={"cpzt": "02,04", "pagenum": page_index, "drawPageToolEnd": "5"},
                                timeout=5)
        response = request_content()

        # while True:
        #     try:
        #         response = requests.post(index_url,
        #                                  data={"cpzt": "02,04", "pagenum": page_index, "drawPageToolEnd": "5"},
        #                                  timeout=10)
        #     except requests.exceptions.ConnectionError, e:
        #         print e
        #         continue
        #     except requests.exceptions.Timeout, e:
        #         print e
        #         continue
        #     break

        data_string = json.loads(response.text.encode('utf-8'))
        product_data = []

        for i in range(len(data_string["List"])):
            if 'CNY' not in data_string["List"][i]["mjbz"]:
                product_data.append([data_string["List"][i]["cpid"],  # 产品id
                                     data_string["List"][i]["cpdjbm"],  # 产品登记编码
                                     data_string["List"][i]["cpdm"],  # 产品代码
                                     data_string["List"][i]["cpms"],  # 产品描述
                                     data_string["List"][i]["fxjgdm"],  # 发行机构代码
                                     data_string["List"][i]["fxjgms"],  # 发行机构描述
                                     data_string["List"][i]["mjbz"],  # 募集币种
                                     data_string["List"][i]["cpqx"],  # 产品期限
                                     data_string["List"][i]["qxms"],  # 期限描述
                                     data_string["List"][i]["mjqsrq"],  # 募集起始日期
                                     data_string["List"][i]["mjjsrq"],  # 募集结束日期
                                     data_string["List"][i]["kfzqqsr"],  # 开放周期起始日
                                     data_string["List"][i]["kfzqjsr"],  # 开放周期结束日
                                     data_string["List"][i]["cpqsrq"],  # 产品起始日期
                                     data_string["List"][i]["cpyjzzrq"],  # 产品预计终止日期
                                     data_string["List"][i]["cplx"],  # 产品类型
                                     data_string["List"][i]["cplxms"],  # 产品类型描述(如: 封闭式非净值型)
                                     data_string["List"][i]["cpsylx"],  # 产品收益类型
                                     data_string["List"][i]["cpsylxms"],  # 产品收益类型描述(如: 保本浮动收益)
                                     data_string["List"][i]["cpfxdj"],  # 产品风险等级
                                     data_string["List"][i]["fxdjms"],  # 风险等级描述
                                     data_string["List"][i]["cpjz"],  # 产品净值
                                     data_string["List"][i]["bqjz"],  # bq净值
                                     data_string["List"][i]["csjz"],  # cs净值
                                     data_string["List"][i]["xsqy"],  # 销售区域
                                     data_string["List"][i]["cpxsqy"],  # 产品销售区域
                                     data_string["List"][i]["orderby"],  # order
                                     data_string["List"][i]["yjkhzgnsyl"],  # 预计客户最高年收益率
                                     data_string["List"][i]["yjkhzdnsyl"],  # 预计客户最低年收益率
                                     data_string["List"][i]["dqsjsyl"],  # 到期实际收益率
                                     data_string["List"][i]["cpztms"],  # 产品状态描述
                                     data_string["List"][i]["qdxsje"]])  # 起点销售金额

                add_product = ("""INSERT INTO t_product
                                  (prod_id, prod_reg_code, prod_code, prod_name, issuer_code, issuer_name, currency,
                                  tenor, tenor_desc, start_date, end_date, open_start_date, open_end_date,
                                  value_date, maturity_date, prod_type, prod_type_desc, coupon_type, coupon_type_desc,
                                  risk, risk_desc, net_value, bq_net_value, cs_net_value, sales_region, sales_region_desc,
                                  order_by, expected_highest_yield, expected_lowest_yield, actual_yield, status,
                                  starting_amount, data_source, update_time)
                                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                          'ChinaWealth', now())""")
                cursor.execute(add_product, product_data[-1])
                count += 1

        logging.info(unicode(count) + ' ChinaWealth products imported')

    cnx.commit()
    cursor.close()
    logging.info(unicode(count) + ' ChinaWealth products imported')

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


def show_stats(options):
    pool = Pool(8)
    page_urls = get_CW_product()
    results = pool.map(get_data, page_urls)


if __name__ == '__main__':
    DB_NAME = 'zyq'

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
        logging.info('MYSQL connected.')

    # get_CW_product()
    get_CMHO_product()
    # get_ICBC_product()
    # get_CCBH_product()
    # get_ABCI_product()
    # get_BCOH_product()
    # get_DESZ_product()
    # get_CTIB_product()
    # get_EBBC_product()
    # get_IBCN_product()
    # get_SPDB_product()
    # get_BKSH_product()
    # get_BOBJ_product()

    cnx.close()
