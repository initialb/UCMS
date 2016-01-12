# -*- coding: utf-8 -*-

import math
import codecs
import argparse
import logging
import sys
import pprint
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
from butils import decode
from butils import fix_json
from butils import ppprint
from datetime import datetime
from xml.dom.minidom import parse
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

reload(sys)
sys.setdefaultencoding('utf8')

pp = pprint.PrettyPrinter(indent=4)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_CMHO_rate():
    index_url = 'http://fx.cmbchina.com/hq/'

    while True:
        try:
            response = requests.get(index_url, timeout=5)
        except requests.exceptions.ConnectionError, e:
            print e
            continue
        except requests.exceptions.Timeout, e:
            print e
            continue
        break

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    publish_date = filter(unicode.isdigit, soup.find(text=re.compile(u"当前日期")))

    rate_data = []

    rate_list_tr = soup.find("table", class_="data").find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if r[0].string.strip() == "美元":
            rate_data = ['C10308',
                         'USD',
                         r[6].string.strip(),
                         r[7].string.strip(),
                         r[4].string.strip(),
                         r[5].string.strip(),
                         r[3].string.strip(),
                         format_datetime(publish_date + r[8].string.strip())]
            break

    add_product = ("""INSERT INTO t_listing_rate
                    (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publisher_mid_rate,
                    publish_time, update_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('CMHO rate imported')


def get_ICBC_rate():

    index_url = 'http://www.icbc.com.cn/ICBCDynamicSite/Optimize/Quotation/QuotationListIframe.aspx?variety=2' \
                '&beginDate=' + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '&endDate=' \
                + time.strftime('%Y-%m-%d',time.localtime(time.time())) + '&currency=USD&ppublishDate='

    while True:
        try:
            response = requests.get(index_url, timeout=5)
        except requests.exceptions.ConnectionError, e:
            print e
            continue
        except requests.exceptions.Timeout, e:
            print e
            continue
        break
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    rate_data = []

    rate_list_tr = soup.find("table", class_="tableDataTable").find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if len(r) == 6 and r[0].string.strip() == "美元(USD)":
            rate_data = ['C10102',
                         'USD',
                         r[2].string.strip(),
                         r[3].string.strip(),
                         r[4].string.strip(),
                         r[4].string.strip(),
                         format_datetime(r[1].string.strip() + r[5].string.strip())]
            break

    add_product = ("""INSERT INTO t_listing_rate
                    (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publish_time, update_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('ICBC rate imported')


def get_BCHO_rate():
    index_url = 'http://srh.bankofchina.com/search/whpj/search.jsp'

    while True:
        try:
            response = requests.post(index_url, data={"pjname": "1316"}, timeout=5)
        except requests.exceptions.ConnectionError, e:
            print e
            continue
        except requests.exceptions.Timeout, e:
            print e
            continue
        break

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    rate_data = []

    rate_list_tr = soup.find("div", class_="BOC_main publish").find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if len(r) == 8 and r[0].string.strip() == "美元":
            rate_data = ['C10104',
                         'USD',
                         r[1].string.strip(),
                         r[2].string.strip(),
                         r[3].string.strip(),
                         r[4].string.strip(),
                         r[5].string.strip(),
                         r[6].string.strip(),
                         format_datetime(r[7].string.strip())]
            break

    add_product = ("""INSERT INTO t_listing_rate
                      (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, mid_rate,
                      publisher_mid_rate, publish_time, update_time)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('BCHO rate imported')


def get_ABCI_rate():
    index_url = 'http://app.abchina.com/rateinfo/RateSearch.aspx?id=1'

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    publish_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"更新日期")))

    rate_data = []

    rate_list_tr = soup.find("table", class_="DataList").find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if len(r) == 4 and r[0].string.strip() == "美元(USD)":
            rate_data = ['C10103',
                         'USD',
                         r[1].string.strip(),
                         r[3].string.strip(),
                         r[2].string.strip(),
                         r[2].string.strip(),
                         format_datetime(publish_datetime)]
            break

    add_product = ("""INSERT INTO t_listing_rate
                   (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publish_time, update_time)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('ABCI rates imported')


def get_CCBH_rate():
    index_url = 'http://forex.ccb.com/cn/home/news/jshckpj.xml'

    response = requests.post(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    publish_datetime = unicode(soup.timestamp.string)

    rate_data = []

    rt_data_array = soup.find_all("referencepricesettlement")

    for rt_data in rt_data_array:
        if rt_data.cm_curr_cod.string == '14':
            rate_data = ['C10105',
                         'USD',
                         Decimal(Decimal(rt_data.fxr_xch_buyin.string)*100).quantize(Decimal('.00')),
                         Decimal(Decimal(rt_data.fxr_cur_buyin.string)*100).quantize(Decimal('.00')),
                         Decimal(Decimal(rt_data.fxr_xch_sellout.string)*100).quantize(Decimal('.00')),
                         Decimal(Decimal(rt_data.fxr_cur_sellout.string)*100).quantize(Decimal('.00')),
                         Decimal(Decimal(rt_data.mid_rate.string)*100).quantize(Decimal('.00')),
                         format_datetime(publish_datetime)]
            break

    add_product = ("""INSERT INTO t_listing_rate
                      (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publisher_mid_rate,
                      publish_time, update_time)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('CCBH rate imported')


def get_CTIB_rate():
    index_url = 'http://www.ecitic.com/xml/ftp.txt'
    response = requests.get(index_url)

    rate_data = []

    rt_data_list = response.text.split()
    for rt_data in rt_data_list:
        if rt_data[15:17] == '14':
            rate_data = ['C10302',
                         'USD',
                         rt_data[33:36] + '.' + rt_data[36:38],
                         rt_data[21:24] + '.' + rt_data[24:26],
                         rt_data[45:48] + '.' + rt_data[48:50],
                         rt_data[69:72] + '.' + rt_data[72:74],
                         rt_data[57:60] + '.' + rt_data[60:62],
                         format_datetime(rt_data[1:9] + rt_data[9:15])]
            break

    add_product = ("""INSERT INTO t_listing_rate
                    (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publisher_mid_rate,
                    publish_time, update_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('CTIB rate imported')


def get_BCOH_rate():
    index_url = 'http://www.bankcomm.com/BankCommSite/simple/cn/whpj/queryExchangeResult.do?type=simple'

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    publish_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"更新时间")))

    rate_data = []

    rate_list_tr = soup.find("table", class_="exchangeTab").find_all("tr", class_="data")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if  r[0].string.strip() == "美元(USD/CNY)":
            rate_data = ['C10301',
                         'USD',
                         r[2].string.strip(),
                         r[4].string.strip(),
                         r[3].string.strip(),
                         r[5].string.strip(),
                         format_datetime(publish_datetime)]
            break

    add_product = ("""INSERT INTO t_listing_rate
                   (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publish_time, update_time)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('BCOH rate imported')


def get_EBBC_rate():
    index_url = 'http://www.cebbank.com/eportal/ui?pageId=477257'

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    publish_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"更新时间")))

    rate_data = []

    rate_list_tr = soup.find("table", class_="lczj_box").find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if r[0].string.strip() == "美元(USD)":
            rate_data = ['C10303',
                         'USD',
                         r[3].string.strip(),
                         r[1].string.strip(),
                         r[4].string.strip(),
                         r[2].string.strip(),
                         r[5].string.strip(),
                         format_datetime(publish_datetime)]
            break

    add_product = ("""INSERT INTO t_listing_rate
                   (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publisher_mid_rate,
                   publish_time, update_time)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('EBBC rate imported')


def get_IBCN_rate():
    entry = 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery.do'
    index_url = 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery!list.do?_search=false' \
                '&dataSet.rows=100&dataSet.page=1&dataSet.sidx=&dataSet.sord=asc'
    referer = 'https://personalbank.cib.com.cn/pers/main/pubinfo/ifxQuotationQuery.do'

    # 第一次请求页面并提取更新日期
    r1 = requests.get(entry)
    soup = bs4.BeautifulSoup(r1.text, "html.parser")
    publish_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"日期：")))

    # 第二次请求并传输cookie, 获取返回的json字符串
    r2 = requests.get(index_url, cookies=r1.cookies)
    data_string = json.loads(r2.text)
    rate_data = []

    # 轮询找到美元, 写入product_data后跳出
    for data_row in data_string["rows"]:
        if data_row["cell"][1] == 'USD':
            rate_data = [u'C10309',
                         u'USD',
                         data_row["cell"][4],
                         data_row["cell"][6],
                         data_row["cell"][5],
                         data_row["cell"][7],
                         data_row["cell"][3],
                         format_datetime(publish_datetime)]
            break

    add_product = ("""INSERT INTO t_listing_rate
                   (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publisher_mid_rate,
                   publish_time, update_time)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('IBCN rate imported')


def get_SPDB_rate():
    index_url = 'http://ebank.spdb.com.cn/net/QueryExchangeRate.do'

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    publish_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"更新时间")))

    rate_data = []

    rate_list_tr = soup.find("table", class_="table_comm").find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td", class_="td20ce03")
        if len(r) == 5 and r[0].string.strip() == u'美元\xa0USD':
            rate_data = ['C10310',
                         'USD',
                         r[2].string.strip(),
                         r[3].string.strip(),
                         r[4].string.strip(),
                         r[4].string.strip(),
                         r[1].string.strip(),
                         format_datetime(publish_datetime)]
            break

    add_product = ("""INSERT INTO t_listing_rate
                    (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publisher_mid_rate,
                    publish_time, update_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('SPDB rate imported')


def get_DESZ_rate():
    index_url = 'https://bank.pingan.com.cn/ibp/portal/exchange/qryExchangeList.do'

    response = requests.post(index_url, data={"realFlag": "1", "currencyCode": "USD", "pageIndex": "1"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    publish_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"时间：")))

    rates = soup.find_all("td", class_="tac")

    rate_data = ['C10310',
                 'USD',
                 rates[2].string.strip(),
                 rates[3].string.strip(),
                 rates[4].string.strip(),
                 rates[4].string.strip(),
                 rates[5].string.strip(),
                 rates[1].string.strip(),
                 format_datetime(publish_datetime)]

    add_product = ("""INSERT INTO t_listing_rate
                    (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, mid_rate, publisher_mid_rate,
                    publish_time, update_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('DESZ rate imported')


def get_BKSH_rate():
    index_url = 'http://www.bankofshanghai.com//WebServlet?go=bank_sellfund_pg_Banking&code=whpj'

    # response = requests.post(index_url, data={"realFlag": "1", "currencyCode": "USD", "pageIndex": "1"})
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    rate_data = []
    rate_list_tr = soup.find("table", class_="table01").tbody.find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if r[1].string.strip() == u'USD':
            rate_data = ['C10912',
                         'USD',
                         r[4].string.strip(),
                         r[6].string.strip(),
                         r[5].string.strip(),
                         r[5].string.strip(),
                         r[3].string.strip(),
                         format_datetime(r[7].string.strip())]
            break

    add_product = ("""INSERT INTO t_listing_rate
                    (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publisher_mid_rate,
                    publish_time, update_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('BKSH rate imported')


def get_BOBJ_rate():
    index_url = 'http://www.bankofbeijing.com.cn/personal/whpj.aspx'

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    strings = soup.find("form", id="form1")
    for string in strings.stripped_strings:
        publish_datetime = unicode(string)
        break

    rate_data = []
    rate_list_tr = soup.find("table", id="GridView1").find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if r[0].string.strip() == u'USD/CNY':
            rate_data = ['C10802',
                         'USD',
                         r[3].string.strip(),
                         r[4].string.strip(),
                         r[5].string.strip(),
                         r[5].string.strip(),
                         r[7].string.strip(),
                         r[6].string.strip(),
                         format_datetime(publish_datetime)]
            break

    add_product = ("""INSERT INTO t_listing_rate
                    (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, mid_rate, publisher_mid_rate,
                    publish_time, update_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
    cursor.execute(add_product, rate_data)

    logging.info('BOBJ rate imported')


# def show_stats(options):
#     pool = Pool(8)
#     page_urls = get_CW_product()
#     results = pool.map(get_data, page_urls)


class MyThread(threading.Thread):
    """docstring for MyThread"""

    def __init__(self, thread_id, name, counter) :
        super(MyThread, self).__init__()  #调用父类的构造函数
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        print "Exiting " + self.name


def print_time(thread_name, delay, counter) :
    while counter :
        time.sleep(delay)
        print "%s %s" % (thread_name, time.ctime(time.time()))
        counter -= 1


def parse_rate(legal_group):
    call_func = eval("get_"+legal_group+"_rate")
    call_func()


def format_datetime(raw_datetime):
    pure_datetime = filter(unicode.isdigit, raw_datetime)

    if len(pure_datetime) == 8:
        return pure_datetime[:4] + '-' + pure_datetime[4:6] + '-' + pure_datetime[6:] + ' 00:00:00'
    elif len(pure_datetime) == 12:
        return pure_datetime[:4] + '-' + pure_datetime[4:6] + '-' + pure_datetime[6:8] + ' ' + \
           pure_datetime[8:10] + ':' + pure_datetime[10:] + ':00'
    elif len(pure_datetime) == 14:
        return pure_datetime[:4] + '-' + pure_datetime[4:6] + '-' + pure_datetime[6:8] + ' ' + \
           pure_datetime[8:10] + ':' + pure_datetime[10:12] + ':' + pure_datetime[12:]
    else:
        return '0000-00-00 00:00:00'


# def main():
    # #创建新的线程
    # thread1 = MyThread(1, "Thread-1", 1)
    # thread2 = MyThread(2, "Thread-2", 2)
    #
    # #开启线程
    # thread1.start()
    # thread2.start()
    #
    #
    # thread1.join()
    # thread2.join()
    # print "Exiting Main Thread"


if __name__ == '__main__':
    try:
        cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        # cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        logging.info('MYSQL connected.')

        cursor = cnx.cursor()
        cursor.execute("""DELETE FROM t_listing_rate WHERE date(update_time)=curdate()""")
        logging.info(unicode(cursor.rowcount) + ' rows deleted')

        pool = ThreadPool(8) # Sets the pool size to 4

        legal_groups = ['CMHO',  # 招商银行
                        'ICBC',  # 工商银行
                        'BCHO',  # 中国银行
                        'ABCI',  # 农业银行
                        'CCBH',  # 建设银行
                        'CTIB',  # 中信银行
                        'BCOH',  # 交通银行
                        'EBBC',  # 光大银行
                        'IBCN',  # 兴业银行
                        'SPDB',  # 浦发银行
                        'DESZ',  # 平安银行
                        'BKSH',  # 上海银行
                        'BOBJ']  # 北京银行

        # results = pool.map(parse_rate, legal_groups)

        # close the pool and wait for the work to finish
        pool.close()
        pool.join()

        get_CMHO_rate()
        get_ICBC_rate()
        get_BCHO_rate()
        get_ABCI_rate()
        get_CCBH_rate()
        get_CTIB_rate()
        get_BCOH_rate()
        get_EBBC_rate()
        get_IBCN_rate()
        get_SPDB_rate()
        get_DESZ_rate()
        get_BKSH_rate()
        get_BOBJ_rate()

        cnx.commit()
        cursor.close()
        cnx.close
        logging.info('All rates retrieved')
