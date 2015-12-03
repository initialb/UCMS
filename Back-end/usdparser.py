import argparse
import re
from multiprocessing import Pool
import requests
import bs4
import json

def get_CMB_product():
    root_url = 'http://www.cmbchina.com'
    page_index = 1
    index_url = root_url + '/CFWEB/svrajax/product.ashx?op=search&type=m&pageindex=' + unicode(page_index) + '&salestatus=&baoben=&currency=32&term=&keyword=&series=01&risk=&city=&date=&pagesize=20&orderby=ord1&t=0.10380132240243256'
    j = []

    response = requests.get(index_url)
    j.append(fix_json(response.text.encode('utf-8')))

    data_string = json.loads(j[0])
    total_page = data_string["totalPage"]
    page_index+=1
    for page_index in xrange(2,total_page+1):
        print page_index
        index_url = root_url + '/CFWEB/svrajax/product.ashx?op=search&type=m&pageindex=' + unicode(page_index) + '&salestatus=&baoben=&currency=32&term=&keyword=&series=01&risk=&city=&date=&pagesize=20&orderby=ord1&t=0.10380132240243256'
        response = requests.get(index_url)
        j.append(fix_json(response.text.encode('utf-8')))

def get_ICBC_product():
    root_url='http://www.icbc.com.cn'
    index_url = root_url ＋ '/ICBCDynamicSite2/money/services/MoenyListService.ashx'
    response = requests.get(index_url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    print soup
    # for tag in soup.find_all(True):
    #     print(tag.name)
    print soup.find_all("div","tabs_4")





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
    # get_CMB_product()
    get_ICBC_product()
