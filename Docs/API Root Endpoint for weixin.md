#API Root Endpoint for weixin

```
http://139.196.16.157:5000/ucms/api/v1.0/weixin
```
<br /> 
# 获取最新牌价
```
GET /listingrate/{currency}
```
Arguments  | required | Description
-----------|:--------:|---------------
currency   | Y        | 货币: USD,GBP,EUR,AUD
**Request Example**

```
$ curl -i http://139.196.16.157:5000/ucms/api/v1.0/weixin/listingrate/USD
```
**Response Example**

```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 2199
Server: Werkzeug/0.11.5 Python/2.7.11
Date: Mon, 04 Apr 2016 08:22:51 GMT

{'currency': u'USD',
 'currencyname': u'美元',
 'list': [{'ask_cash': u'652.30',
           'ask_remit': u'652.30',
           'bid_cash': u'644.49',
           'bid_remit': u'649.70',
           'publish_time': u'2016-03-05 21:01:00',
           'publisher': u'农业银行'},
          {'ask_cash': u'652.52',
           'ask_remit': u'652.52',
           'bid_cash': u'644.71',
           'bid_remit': u'649.92',
           'publish_time': u'2016-03-05 10:30:00',
           'publisher': u'中国银行'}
],
 'timestamp': '2016-04-04 16:24:51',
 'total_rec': 2}
```
<br />
# 获取每日精选产品

```
GET /selectedwmp/{currency}?preservable={Y|N|ALL}

```

Arguments  | required | Description
-----------|:--------:|---------------
currency   | Y        | 货币: USD,GBP,EUR,AUD
preservable|          |Y: 保本, N: 非保本, 其它: 全部
**Request Example**

```
$ curl -i http://139.196.16.157:5000/ucms/api/v1.0/weixin/selectedwmp/USD?preservable=N
```
**Response Example**

```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1994
Server: Werkzeug/0.11.5 Python/2.7.11
Date: Mon, 04 Apr 2016 08:34:39 GMT

{'currency': u'USD',
 'preservable': 'N',
 'tenor_group': [{'industry_1m_avg_yield': '0.7000%',
                  'list': [{'expected_highest_yield': '0.7500%',
                            'issuer_name': u'招商银行',
                            'open_end_date': u'每天',
                            'open_start_date': u'每天',
                            'prod_name': u'美元日益月鑫30天',
                            'starting_amount': '8000.00'}],
                  'tenor': 1},
                 {'industry_1m_avg_yield': '0.6000%',
                  'list': [{'expected_highest_yield': '0.6000%',
                            'issuer_name': u'工商银行',
                            'open_end_date': u'每天',
                            'open_start_date': u'每天',
                            'prod_name': u'“安享回报”套利98天美元理财产品',
                            'starting_amount': '8000.00'}],
                  'tenor': 3},
                 {'industry_1m_avg_yield': '1.4738%',
                  'list': [{'expected_highest_yield': '2.3000%',
                            'issuer_name': u'兴业银行',
                            'open_end_date': u'20160405',
                            'open_start_date': u'20160328',
                            'prod_name': u'“万汇通－跨境通QDII”开放式非保本浮动收益美元理财产品第1款',
                            'starting_amount': '8000.00'}],
                  'tenor': 6},
                 {'industry_1m_avg_yield': '1.9667%',
                  'list': [{'expected_highest_yield': '1.9000%',
                            'issuer_name': u'工商银行',
                            'open_end_date': u'每天',
                            'open_start_date': u'每天',
                            'prod_name': u'“安享回报”套利273天美元理财产品',
                            'starting_amount': '8000.00'}],
                  'tenor': 9},
                 {'industry_1m_avg_yield': '2.0168%',
                  'list': [{'expected_highest_yield': '2.6000%',
                            'issuer_name': u'兴业银行',
                            'open_end_date': u'20160405',
                            'open_start_date': u'20160330',
                            'prod_name': u'2016年第13期天天万汇通C款（20万美元以上）',
                            'starting_amount': '200000.00'}],
                  'tenor': 12},
                 {'industry_1m_avg_yield': '2.9000%',
                  'list': [{'expected_highest_yield': '2.9000%',
                            'issuer_name': u'招商银行',
                            'open_end_date': u'20160413',
                            'open_start_date': u'20160401',
                            'prod_name': u'美元鼎鼎成金0289号',
                            'starting_amount': '8000.00'},
                           {'expected_highest_yield': '2.9000%',
                            'issuer_name': u'招商银行',
                            'open_end_date': u'20160407',
                            'open_start_date': u'20160328',
                            'prod_name': u'美元鼎鼎成金0288号',
                            'starting_amount': '8000.00'}],
                  'tenor': 24}],
 'timestamp': '2016-04-04 16:24:51'}
```