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

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    current_date = filter(unicode.isdigit, soup.find(text=re.compile(u"当前日期")))

    rate_list = []
    count = 0

    rate_list_tr = soup.find("table", class_="data").find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if r[0].string.strip() == "美元":
            rate_list.append(['C10308', 'USD', r[6].string.strip(), r[7].string.strip(), r[4].string.strip(),
                              r[5].string.strip(), r[3].string.strip(), current_date + ' ' + r[8].string.strip()])

    for rate in rate_list:
        add_product = ("""INSERT INTO t_listing_rate
                        (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publisher_mid_rate,
                        publish_time, update_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
        cursor.execute(add_product, rate)
        count += 1

    logging.info(unicode(count) + ' CMHO rates imported')


def get_ICBC_rate():
    index_url = 'http://www.icbc.com.cn/ICBCDynamicSite/Optimize/Quotation/QuotationListIframe.aspx?variety=2' \
                '&beginDate=2015-12-09&endDate=2016-01-08&currency=USD&ppublishDate='

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # print soup

    rate_list = []
    count = 0

    rate_list_table = soup.find("table", class_="tableDataTable")
    rate_list_tr = rate_list_table.find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if len(r) == 6 and r[0].string.strip() == "美元(USD)":
            rate_list.append(['C10102', 'USD', r[2].string.strip(), r[3].string.strip(), r[4].string.strip(),
                              r[4].string.strip(), r[1].string.strip() + ' ' + r[5].string.strip()])
            break

    for rate in rate_list:
        add_product = ("""INSERT INTO t_listing_rate
                        (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publish_time, update_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, now())""")
        cursor.execute(add_product, rate)
        count += 1

    logging.info(unicode(count) + ' ICBC rates imported')


def get_BCHO_rate():
    index_url = 'http://srh.bankofchina.com/search/whpj/search.jsp'

    response = requests.post(index_url, data={"pjname": "1316"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    rate_list = []
    count = 0

    rate_list_div = soup.find("div", class_="BOC_main publish")
    rate_list_tr = rate_list_div.find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if len(r) == 8 and r[0].string.strip() == "美元":
            rate_list.append(['C10104', 'USD', r[1].string.strip(), r[2].string.strip(), r[3].string.strip(),
                              r[4].string.strip(), r[5].string.strip(), r[6].string.strip(), r[7].string.strip()])
            break

    for rate in rate_list:
        add_product = ("""INSERT INTO t_listing_rate
                          (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, mid_rate,
                          publisher_mid_rate, publish_time, update_time)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        cursor.execute(add_product, rate)
        count += 1

    logging.info(unicode(count) + ' BCHO rates imported')


def get_ABCI_rate():
    index_url = 'http://app.abchina.com/rateinfo/RateSearch.aspx?id=1'

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    current_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"更新日期")))

    rate_list = []
    count = 0

    rate_list_tr = soup.find("table", class_="DataList").find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if  len(r) == 4 and r[0].string.strip() == "美元(USD)":
            rate_list.append(['C10103', 'USD', r[1].string.strip(), r[3].string.strip(), r[2].string.strip(),
                              r[2].string.strip(), current_datetime])

    for rate in rate_list:
        add_product = ("""INSERT INTO t_listing_rate
                       (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publish_time, update_time)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, now())""")
        cursor.execute(add_product, rate)
        count += 1

    logging.info(unicode(count) + ' ABCI rates imported')


def get_CCBH_rate():
    index_url = 'http://forex.ccb.com/cn/home/news/jshckpj.xml'

    # xml_str = urllib.urlopen(index_url).read()
    # DOMTree = xml.dom.minidom.parseString(xml_str)
    # xdoc = DOMTree.getElementsByTagName("TIMESTAMP")
    # print xdoc[0].firstChild.nodeValue
    # collection = DOMTree.documentElement
    # if collection.hasAttribute("TIMESTAMP"):
    #     print "Time : %s" % collection.getAttribute("TIMESTAMP")
    #
    # # 在集合中获取所有电影
    # movies = collection.getElementsByTagName("movie")
    #
    # # 打印每部电影的详细信息
    # for movie in movies:
    #    print "*****Movie*****"
    #    if movie.hasAttribute("title"):
    #       print "Title: %s" % movie.getAttribute("title")
    #
    #    type = movie.getElementsByTagName('type')[0]
    #    print "Type: %s" % type.childNodes[0].data
    #    format = movie.getElementsByTagName('format')[0]
    #    print "Format: %s" % format.childNodes[0].data
    #    rating = movie.getElementsByTagName('rating')[0]
    #    print "Rating: %s" % rating.childNodes[0].data
    #    description = movie.getElementsByTagName('description')[0]
    #    print "Description: %s" % description.childNodes[0].data

    response = requests.post(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    current_datetime = unicode(soup.timestamp.string)

    rate_list = []
    count = 0
    rt_data_array = soup.find_all("referencepricesettlement")

    for rt_data in rt_data_array:
        if rt_data.cm_curr_cod.string == '14':
            rate_list.append(['C10105',
                              'USD',
                              Decimal(Decimal(rt_data.fxr_xch_buyin.string)*100).quantize(Decimal('.00')),
                              Decimal(Decimal(rt_data.fxr_cur_buyin.string)*100).quantize(Decimal('.00')),
                              Decimal(Decimal(rt_data.fxr_xch_sellout.string)*100).quantize(Decimal('.00')),
                              Decimal(Decimal(rt_data.fxr_cur_sellout.string)*100).quantize(Decimal('.00')),
                              Decimal(Decimal(rt_data.mid_rate.string)*100).quantize(Decimal('.00')),
                              current_datetime])

    for rate in rate_list:
        add_product = ("""INSERT INTO t_listing_rate
                          (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publisher_mid_rate,
                          publish_time, update_time)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
        cursor.execute(add_product, rate)
        count += 1

    logging.info(unicode(count) + ' CCBH rates imported')


def get_CTIB_rate():
    index_url = 'http://www.ecitic.com/xml/ftp.txt'
    response = requests.get(index_url)

    rate_list = []
    count = 0

    rt_data_list = response.text.split()
    for rt_data in rt_data_list:
        if rt_data[15:17] == '14':
            rate_list.append(['C10302',
                              'USD',
                              rt_data[33:36] + '.' + rt_data[36:38],
                              rt_data[21:24] + '.' + rt_data[24:26],
                              rt_data[45:48] + '.' + rt_data[48:50],
                              rt_data[69:72] + '.' + rt_data[72:74],
                              rt_data[57:60] + '.' + rt_data[60:62],
                              rt_data[1:9] + rt_data[9:15]])

    for rate in rate_list:
        add_product = ("""INSERT INTO t_listing_rate
                        (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publisher_mid_rate,
                        publish_time, update_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now())""")
        cursor.execute(add_product, rate)
        count += 1

    logging.info(unicode(count) + ' CTIB rates imported')


def get_BCOH_rate():
    index_url = 'http://www.bankcomm.com/BankCommSite/simple/cn/whpj/queryExchangeResult.do?type=simple'

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    current_datetime = filter(unicode.isdigit, soup.find(text=re.compile(u"更新时间")))

    rate_list = []
    count = 0

    rate_list_tr = soup.find("table", class_="exchangeTab").find_all("tr", class_="data")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if  r[0].string.strip() == "美元(USD/CNY)":
            rate_list.append(['C10301', 'USD', r[2].string.strip(), r[4].string.strip(), r[3].string.strip(),
                              r[5].string.strip(), current_datetime])

    for rate in rate_list:
        add_product = ("""INSERT INTO t_listing_rate
                       (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, update_time)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, now())""")
        cursor.execute(add_product, rate)
        count += 1

    logging.info(unicode(count) + ' BCOH rates imported')


def get_SPDB_rate():
    index_url = 'http://ebank.spdb.com.cn/net/QueryExchangeRate.do'

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    rate_list = []
    count = 0

    rate_list_table = soup.find("table", class_="tableDataTable")
    rate_list_tr = rate_list_table.find_all("tr")

    for rates in rate_list_tr:
        r = rates.find_all("td")
        if len(r) == 6 and r[0].string.strip() == "美元(USD)":
            rate_list.append(['C10102', 'USD', r[2].string.strip(), r[3].string.strip(), r[4].string.strip(),
                              r[4].string.strip(), r[1].string.strip() + ' ' + r[5].string.strip()])
            break

    for rate in rate_list:
        add_product = ("""INSERT INTO t_listing_rate
                        (publisher_code, currency, bid_remit, bid_cash, ask_remit, ask_cash, publish_time, update_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, now())""")
        cursor.execute(add_product, rate)
        count += 1

    logging.info(unicode(count) + ' SPDB rates imported')



def show_stats(options):
    pool = Pool(8)
    page_urls = get_CW_product()
    results = pool.map(get_data, page_urls)


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
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
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


        pool = ThreadPool(4) # Sets the pool size to 4

        legal_groups = ['CMHO', 'ICBC', 'BCHO', 'ABCI', 'CCBH', 'CTIB', 'BCOH']

        results = pool.map(parse_rate, legal_groups)

        # close the pool and wait for the work to finish
        pool.close()
        pool.join()

        # get_CMHO_rate()
        # get_ICBC_rate()
        # get_BCHO_rate()
        # get_ABCI_rate()
        # get_CCBH_rate()
        # get_CTIB_rate()
        # get_SPDB_rate()

        cnx.commit()
        cursor.close()
        cnx.close
