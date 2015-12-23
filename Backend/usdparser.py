# -*- coding: utf-8 -*-

import codecs
import argparse
import logging
import re
from multiprocessing import Pool
import requests
import bs4
import json
import mysql.connector
from mysql.connector import errorcode
from decimal import Decimal

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

logging.basicConfig(level = logging.INFO)


def get_CMHO_product():
    # 招商银行
    # 请求格式：http get
    # 返回格式：json
    # 解析方法：json
    # 不需要登录，无公告
    legal_group = 'CMHO'
    root_url = 'http://www.cmbchina.com'
    index_url = 'http://www.cmbchina.com/CFWEB/svrajax/product.ashx?op=search&type=m&pageindex=1&salestatus=&baoben=&currency=32&term=&keyword=&series=01&risk=&city=&date=&pagesize=20&orderby=ord1'
    # currency = 32 means USD

    total_page = json.loads(fix_json(requests.get(index_url).text.encode('utf-8')))["totalPage"]
    # logging.info('total page = '+unicode(total_page))

    j = []
    count = 0

    # delete all duplicated records:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM PRODUCT WHERE date(UPDATE_DATE)=curdate()""")
    logging.info(unicode(cursor.rowcount) + '' + unicode(legal_group) + ' rows deleted')

    for page_index in xrange(1,total_page+1):
        _index_url = root_url + '/CFWEB/svrajax/product.ashx?op=search&type=m&pageindex=' + unicode(page_index) + '&salestatus=&baoben=&currency=32&term=&keyword=&series=01&risk=&city=&date=&pagesize=20&orderby=ord1'
        response = requests.get(_index_url)
        j.append(fix_json(response.text.encode('utf-8')))
        data_string = json.loads(j[page_index-1])

        product_data = []

        for i in range(len(data_string["list"])):
            ield = re.sub(r'[^\d.]+', '', data_string["list"][i]["NetValue"])
            if ield == '':
                ield = 0
            product_data.append([u'CMHO', data_string["list"][i]["PrdCode"], data_string["list"][i]["PrdName"], u'USD', data_string["list"][i]["FinDate"],
                                data_string["list"][i]["EndDate"], data_string["list"][i]["ExpireDate"], data_string["list"][i]["BeginDate"], ield,
                                data_string["list"][i]["Risk"], data_string["list"][i]["Status"],
                                data_string["list"][i]["Style"]])
            logging.debug(product_data[i])
            add_product = ("""INSERT INTO PRODUCT
                              (PROD_ID, LEGAL_GROUP, PROD_CODE, PROD_NAME, CURRENCY, TENOR, VALUE_DATE, MATURITY_DATE,
                               ISSUE_DATE, YIELD, RISK, STATUS, REMARK, UPDATE_DATE)
                              VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
            cursor.execute(add_product, product_data[i])
            count += 1

    cnx.commit()
    cursor.close()
    logging.info(unicode(count) + ' CMBC products imported')


def get_ICBC_product():
    # 工商银行
    # 请求格式：http get
    # 返回格式：json
    # 解析方法：json

    root_url='http://www.icbc.com.cn'
    index_url = 'http://www.icbc.com.cn/ICBCDynamicSite2/money/services/MoenyListService.ashx?ctl1=4&ctl2=6&keyword='

    data_string = json.loads(requests.get(index_url).text.encode('utf-8'))
    logging.debug('data_string = '+unicode(data_string))

    count = 0
    product_data = []

    # delete all duplicated records:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM PRODUCT WHERE date(UPDATE_DATE)=curdate()""")
    print cursor.rowcount 

    for i in range(len(data_string)):
        ield = re.sub(r'[^\d.]+', '', data_string[i]["intendYield"])
        if ield == '':
            ield = 0
        product_data.append([data_string[i]["prodID"], data_string[i]["productName"], u'ICBC', data_string[i]["prodID"][0:3], ield])
        logging.debug(product_data[i])
        add_product = ("INSERT INTO PRODUCT "
                "(PROD_ID, PROD_CODE, PROD_NAME, LEGAL_GROUP, CURRENCY, YIELD, UPDATE_DATE) "
                "VALUES (NULL, %s, %s, %s, %s, %s, now())")
        cursor.execute(add_product, product_data[i])
        count += 1

    cnx.commit()
    cursor.close()
    logging.info(unicode(count) + ' ICBC products imported')

def get_CCBH_product():
    # 建设银行
    # 请求格式：http get
    # 返回格式：json
    # 解析方法：json

    root_url='http://finance.ccb.com'
    index_url = root_url + '/Channel/3080'

    response = requests.post(index_url, data = {"querytype":"query", "investmentCurrency":"14"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    pl_data_table = soup.find("table", id = "pl_data_list")

    product_data = []

    for child in pl_data_table.children:
        if isinstance(child, bs4.element.Tag):
            if child.has_attr("onmouseover"):
                if child["onmouseover"] == "this.className='table_select_bg AcqProductItem'":
                    cells = child.find_all("td")
                    product_data.append([u'CCBH',
                        cells[13]["id"],
                        cells[0]["title"],
                        u'USD',
                        cells[4].string.strip(),
                        decode(cells[11].string.strip(), u'', u'', re.sub(r'[^\d.]+', '', cells[11].string)),
                        decode(cells[12].string.strip(), u'低风险', u'L', u''),
                        cells[1].string.strip(),
                        u'', 
                        ]
                    )

   # delete all duplicated records:
    cursor = cnx.cursor()
    cursor.execute("""DELETE FROM PRODUCT WHERE date(UPDATE_DATE)=curdate()""")
    logging.info(unicode(cursor.rowcount) + ' CCHB products deleted')

    for p in product_data:
        for m in p:
            print m+',',
        print

        add_product = ("""INSERT INTO PRODUCT
                    (PROD_ID, LEGAL_GROUP, PROD_CODE, PROD_NAME, CURRENCY, TENOR, YIELD, RISK, STATUS, REMARK, UPDATE_DATE)
                    VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())""")
        cursor.execute(add_product, p)

    cnx.commit()
    cursor.close()
    logging.info(unicode(len(product_data)) + ' CCHB products imported')


def get_ABCI_product():
    # 农业银行
    # 请求格式：http get
    # 返回格式：json
    # 解析方法：json
    # 登录要求待确认

    page_index = 1
    page_max = 150
    root_url ='http://ewealth.abchina.com'
    index_url = root_url + '/app/data/api/DataService/BoeProductV2?i=1&s=15&o=0&w=%257C%257C%257C%25E7%25BE%258E%25E5%2585%2583%257C%257C%257C%257C1%257C%257C0%257C%257C0'

    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    data_string = json.loads(soup.text.encode('utf-8'))

    print data_string["Data"]["Table"][0]["ProductNo"].encode("utf-8")
    print data_string["Data"]["Table"][0]["ProdName"].encode("utf-8")
    print data_string["Data"]["Table"][0]["ProdClass"].encode("utf-8")
    print data_string["Data"]["Table"][0]["ProdLimit"].encode("utf-8")

def get_BCOH_product():
    # 交通银行
    # 请求格式：http get
    # 返回格式：html
    # 解析方法：soup find all
    # 可解析，登录待验证

    root_url = 'http://www.bankcomm.com'
    index_url = root_url + '/BankCommSite/zonghang/cn/lcpd/queryFundInfoList.do?currency=2&tradeType=-1&safeFlg=-1&ratio=-1&term=-4&asc=-undefined'
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    pl_data_list = soup.find_all("div", class_ = "con_main")

    product_data = []

    for child in pl_data_list.children:
        if isinstance(child, bs4.element.Tag):
            cells = child.dt.find_all("span")
            print cells
    #                 cells = child.find_all("td")
    #                 print cells[0]["title"].encode("utf-8")
    #                 print cells[1].string.encode("utf-8").strip()
    #                 print cells[2].string.encode("utf-8").strip()
    #                 print cells[3].string.encode("utf-8").strip()
    #                 print cells[4].string.encode("utf-8").strip()
    #                 print cells[5].string.encode("utf-8").strip()
    #                 print cells[6].string.encode("utf-8").strip()
    #                 # print cells[7].string.encode("utf-8").strip()
    #                 print cells[8].string.encode("utf-8").strip()
    #                 print cells[9].string.encode("utf-8").strip()
    #                 print cells[10].string.encode("utf-8").strip()
    #                 print cells[11].string.encode("utf-8").strip()
    #                 print cells[12].string.encode("utf-8").strip()
    #                 print cells[13]["id"].encode("utf-8")

def get_DESZ_product():
    # 平安银行
    # 请求格式：http get
    # 返回格式：html
    # 解析方法：soup find all
    # 可解析

    index_url = 'http://chaoshi.pingan.com/bankListIframe.shtml'
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    print soup

def get_CTIB_product():
    # 中信银行
    # 请求格式：http post
    # 返回格式：html
    # 解析方法：soup find all
    # 可解析，不需要登录

    root_url='http://finance.ccb.com'
    index_url = 'https://mall.bank.ecitic.com/fmall/pd/fin-pic-index.htm'

    response = requests.post(index_url, data = {"curr_type":"014", "orderasc":"desc", "branch_id":"701100", "skeywordsfin":"代码/名称"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    print soup

    pl_data_list = soup.find_all("div", class_ = "fund_listw2")

    product_data = []
    f = codecs.open("CTIB_result.html", encoding='utf-8', mode="w")

    for prod in pl_data_list:
        f.write(unicode(prod))
        for child in prod.descendants:
            if isinstance(child, bs4.element.Tag):
                if child.name == 'input':
                    if child.has_attr("field") and child["field"] == 'prod_no':
                        print child["finname"].encode("utf-8")

    f.close


# 光大银行
# 请求格式：http get
# 返回格式：html
# 解析方法：soup find all
# 可解析，不需要登录
def get_CEB_product():
    index_url = 'http://chaoshi.pingan.com/bankListIframe.shtml'
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    print soup


# 兴业银行
# 请求格式：http post
# 返回格式：html
# 解析方法：soup find all
# 可解析，不需要登录，需要分析公告
def get_CIB_product():
    root_url='http://finance.ccb.com'
    index_url = 'https://mall.bank.ecitic.com/fmall/pd/fin-pic-index.htm'

    response = requests.post(index_url, data = {"curr_type":"014", "orderasc":"desc", "branch_id":"701100", "skeywordsfin":"代码/名称"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    print soup

    pl_data_list = soup.find_all("div", class_ = "fund_listw2")


    product_data = []
    f = codecs.open("CTIB_result.html", encoding='utf-8', mode="w")

    for prod in pl_data_list:
        f.write(unicode(prod))
        for child in prod.descendants:
            if isinstance(child, bs4.element.Tag):
                if child.name == 'input':
                    if child.has_attr("field") and child["field"] == 'prod_no':
                        print child["finname"].encode("utf-8")

    f.close


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


def get_product_data(video_page_url):
    product_data = {}
    response = requests.get(root_url + video_page_url)
    soup = bs4.BeautifulSoup(response.text)
    video_data['title'] = soup.select('div#videobox h3')[0].get_text()
    video_data['speakers'] = [a.get_text() for a in soup.select('div#sidebar a[href^=/speaker]')]
    video_data['youtube_url'] = soup.select('div#sidebar a[href^=http://www.youtube.com]')[0].get_text()
    response = requests.get(video_data['youtube_url'])
    soup = bs4.BeautifulSoup(response.text)
    video_data['views'] = int(re.sub('[^0-9]', '',
                                     soup.select('.watch-view-count')[0].get_text().split()[0]))
    video_data['likes'] = int(re.sub('[^0-9]', '',
                                     soup.select('.likes-count')[0].get_text().split()[0]))
    video_data['dislikes'] = int(re.sub('[^0-9]', '',
                                        soup.select('.dislikes-count')[0].get_text().split()[0]))
    return video_data

def parse_args():
    parser = argparse.ArgumentParser(description='Show PyCon 2014 video statistics.')
    parser.add_argument('--sort', metavar='FIELD', choices=['views', 'likes', 'dislikes'],
                        default='views',
                        help='sort by the specified field. Options are views, likes and dislikes.')
    parser.add_argument('--max', metavar='MAX', type=int, help='show the top MAX entries only.')
    parser.add_argument('--csv', action='store_true', default=False,
                        help='output the data in CSV format.')
    parser.add_argument('--workers', type=int, default=8,
                        help='number of workers to use, 8 by default.')
    return parser.parse_args()



def show_video_stats(options):
    pool = Pool(options.workers)
    video_page_urls = get_video_page_urls()
    results = sorted(pool.map(get_video_data, video_page_urls), key=lambda video: video[options.sort],
                     reverse=True)
    max = options.max
    if max is None or max > len(results):
        max = len(results)
    if options.csv:
        print(u'"title","speakers", "views","likes","dislikes"')
    else:
        print(u'Views  +1  -1 Title (Speakers)')
    for i in range(max):
        if options.csv:
            print(u'"{0}","{1}",{2},{3},{4}'.format(
                results[i]['title'], ', '.join(results[i]['speakers']), results[i]['views'],
                results[i]['likes'], results[i]['dislikes']))
        else:
            print(u'{0:5d} {1:3d} {2:3d} {3} ({4})'.format(
                results[i]['views'], results[i]['likes'], results[i]['dislikes'], results[i]['title'],
                ', '.join(results[i]['speakers'])))

def fix_json(ugly_json):
    _fixed_json = ugly_json[1:-1]
    _fixed_json = re.sub(r"{\s*(\w)", r'{"\1', _fixed_json)
    _fixed_json = re.sub(r",\s*(\w)", r',"\1', _fixed_json)
    _fixed_json = re.sub(r"(\w):", r'\1":', _fixed_json)
    return _fixed_json


def decode(*arguments):
    """Compares first item to subsequent item one by one.

    If first item is equal to a key, returns the corresponding value (next item).
    If no match is found, returns None, or, if default is omitted, returns None.
    """
    if len(arguments) < 3:
        raise TypeError, 'decode() takes at least 3 arguments (%d given)' % (len(arguments))
    dict = list(arguments[1:])
    if arguments[0] in dict:
        index = dict.index(arguments[0]);
        if index % 2 == 0 and len(dict) > index+1:
            return dict[index+1]
        return dict[-1]
    elif len(dict) % 2 != 0:
        return dict[-1]

# example usage
# return_value = decode('b', 'a', 1, 'b', 2, 3)
# var = 'list'
# return_type = decode(var, 'tuple', (), 'dict', {}, 'list', [], 'string', '')


def insert_db(list):
    DB_NAME = 'UCMS'

    try:
        cnx = mysql.connector.connect(user='ucms',password='ucms',database=DB_NAME)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        logging.info('MYSQL connected.')



    count = 0
    product_data = []
    cursor = cnx.cursor()

    for i in range(len(data_string)):
        ield = re.sub(r'[^\d.]+', '', data_string[i]["intendYield"])
        if ield == '':
            ield = 0
        product_data.append([data_string[i]["prodID"], data_string[i]["productName"], u'ICBC', data_string[i]["prodID"][0:3], ield])
        logging.debug(product_data[i])
        add_product = ("INSERT INTO PRODUCT "
                "(PROD_ID, PROD_CODE, PROD_NAME, LEGAL_GROUP, CURRENCY, YIELD, UPDATE_DATE) "
                "VALUES (NULL, %s, %s, %s, %s, %s, now())")
        cursor.execute(add_product, product_data[i])
        count += 1

    cnx.commit()
    cursor.close()
    logging.info(unicode(count) + ' ICBC products imported')


    cnx.close



def pprint(obj):
    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())



if __name__ == '__main__':

    DB_NAME = 'UCMS'

    try:
        cnx = mysql.connector.connect(user='ucms',password='ucms',database=DB_NAME)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        logging.info('MYSQL connected.')

    get_CMHO_product()
    get_ICBC_product()
    get_CCBH_product()
        
    cnx.close