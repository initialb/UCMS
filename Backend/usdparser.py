# -*- coding: utf-8 -*-

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

logging.basicConfig(level = logging.INFO)

def get_CMHO_product():
    root_url = 'http://www.cmbchina.com'
    index_url = root_url + '/CFWEB/svrajax/product.ashx?op=search&type=m&pageindex=1&salestatus=&baoben=&currency=32&term=&keyword=&series=01&risk=&city=&date=&pagesize=20&orderby=ord1'
    # currency = 32 means USD

    total_page = json.loads(fix_json(requests.get(index_url).text.encode('utf-8')))["totalPage"]
    logging.info('total page = '+unicode(total_page))

    j = []
    count = 0

    for page_index in xrange(1,total_page+1):
        _index_url = root_url + '/CFWEB/svrajax/product.ashx?op=search&type=m&pageindex=' + unicode(page_index) + '&salestatus=&baoben=&currency=32&term=&keyword=&series=01&risk=&city=&date=&pagesize=20&orderby=ord1'
        response = requests.get(_index_url)
        j.append(fix_json(response.text.encode('utf-8')))
        data_string = json.loads(j[page_index-1])

        product_data = []
        cursor = cnx.cursor()

        for i in range(len(data_string["list"])):
            ield = re.sub(r'[^\d.]+', '', data_string["list"][i]["NetValue"])
            if ield == '':
                ield = 0
            product_data.append([data_string["list"][i]["PrdCode"], data_string["list"][i]["PrdName"], u'CMHO', data_string["list"][i]["Currency"], ield])
            logging.debug(product_data[i])
            add_product = ("INSERT INTO PRODUCT "
                    "(PROD_ID, PROD_CODE, PROD_NAME, LEGAL_GROUP, CURRENCY, YIELD, UPDATE_DATE) "
                    "VALUES (NULL, %s, %s, %s, %s, %s, now())")
            cursor.execute(add_product, product_data[i])
            count += 1

        cnx.commit()
        cursor.close()
    logging.info(unicode(count) + ' CMBC products imported')

def get_ICBC_product():
    root_url='http://www.icbc.com.cn'
    index_url = root_url + '/ICBCDynamicSite2/money/services/MoenyListService.ashx?ctl1=4&ctl2=6&keyword='

    data_string = json.loads(requests.get(index_url).text.encode('utf-8'))
    logging.debug('data_string = '+unicode(data_string))

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

def get_CCBH_product():
    root_url='http://finance.ccb.com'
    index_url = root_url + '/Channel/3080'

    response = requests.post(index_url, data = {"querytype":"query", "investmentCurrency":"14"})
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    pl_data_table = soup.find("table", id = "pl_data_list")

    for child in pl_data_table.children:
        if isinstance(child, bs4.element.Tag):
            if child.has_attr("onmouseover"):
                if child["onmouseover"] == "this.className='table_select_bg AcqProductItem'":
                    cells = child.find_all("td")
                    print cells[0]["title"].encode("utf-8")
                    print cells[1].string.encode("utf-8").strip()
                    print cells[2].string.encode("utf-8").strip()
                    print cells[3].string.encode("utf-8").strip()
                    print cells[4].string.encode("utf-8").strip()
                    print cells[5].string.encode("utf-8").strip()
                    print cells[6].string.encode("utf-8").strip()
                    # print cells[7].string.encode("utf-8").strip()
                    print cells[8].string.encode("utf-8").strip()
                    print cells[9].string.encode("utf-8").strip()
                    print cells[10].string.encode("utf-8").strip()
                    print cells[11].string.encode("utf-8").strip()
                    print cells[12].string.encode("utf-8").strip()
                    print cells[13]["id"].encode("utf-8")



# <tr onmouseover="this.className='table_select_bg AcqProductItem'" onmouseout="this.className=''" class="">
#     <!--td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="ZH030220151203214"><a href="/Info/88087583" class="blue4" target="_blank">ZH030220151203214</a></td-->
#     <td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="汇得盈非保本外币理财产品2015年第32期">&nbsp;<a href="/Info/88087583" class="blue4 AcqProductName AcqProductClick" target="_blank" onclick="LinkClickFunction(this)">汇得盈非保本外币理财产品2015年第32期</a></td>
#     <td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="">
    
#     已售完</td>
#     <td align="center" class="AcqProductType" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="">美元产品</td>
#     <td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="">美元</td>
#     <td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="">短期（半年以内）</td>
#     <td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="">全国&nbsp;</td>
    
#     <td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="">11.27 07:00 - 11.30 17:00</td>
    
#     <td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis">&nbsp;</td>
#     <td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="0.90万">0.90万&nbsp;</td>
#     <td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="">非保本</td>
#     <td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="">封闭</td>
#     <td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="0.80%">0.80%&nbsp;</td>
#     <!-- td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" >&nbsp;</td-->
#     <td align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title="">低风险</td>
#     <td id="ZH030220151203214" width="20%" align="center" style="line-height:16px; overflow:hidden; text-overflow:ellipsis" title=""><a class="w_btn_39px AcqProductClick" acqproductbtnname="认购" acqproductbtnid="productID1" id="LK_0_ZH030220151203214" title="认购" target="_blank" onclick="LinkClickFunction(this)">认购</a><a class="w_btn_39px" id="LK_1_ZH030220151203214" title="申购" target="_blank" onclick="LinkClickFunction(this)">申购</a><a class="w_btn_39px AcqProductClick" acqproductbtnname="赎回" acqproductbtnid="productID2" id="LK_2_ZH030220151203214" title="赎回" target="_blank" onclick="LinkClickFunction(this)">赎回</a><a class="w_btn_70px" id="LK_3_ZH030220151203214" title="自动理财" target="_blank" onclick="LinkClickFunction(this)">自动理财</a></td>
#     <td style="display:none" class="AcqProductID">ZH030220151203214</td>
#   </tr>

def get_BCHO_product():
    root_url = 'http://www.bankcomm.com/BankCommSite/zonghang/cn/lcpd/queryFundInfoList.do?currency=2&tradeType=-1&safeFlg=-1&ratio=-1&term=-4&asc=-undefined'

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

        get_CCBH_product()
        
        cnx.close
