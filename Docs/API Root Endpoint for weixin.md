#API Root Endpoint for weixin

```
http://139.196.16.157:5000/ucms/api/v1.0/weixin
```

<h1>目录</h1>

* [1.实时牌价](#1)
* [2.在售理财产品信息](#2)
* [3.精选理财产品](#3)

<br>

<h1 id="1">实时牌价</h1>

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

<br>

<h1 id="2">在售理财产品信息</h1>
```
GET /wmp/{currency}?preservable={Y|N|ALL}
```
Arguments  | required | Description
-----------|:--------:|---------------
currency   | Y        | 货币: USD,GBP,EUR,AUD
preservable|          |Y: 保本, N: 非保本, 其它: 全部
**Request Example**

```
$ curl -i http://139.196.16.157:5000/ucms/api/v1.0/weixin/wmp/USD?preservable=N
```
**Response Example**

```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1994
Server: Werkzeug/0.11.5 Python/2.7.11
Date: Mon, 04 Apr 2016 08:34:39 GMT

{
"currency": "USD",
"currencyname": "美元",
"preservable": "N",
"timestamp": "2016-03-29 16:00:00",
"total_rec": 13,
"tenor_group":[
	{
		"tenor": 3,
		"industry_1m_avg_yield": "1.0000%",
		"list": [
			{
				"issuer_name": "工商银行",
				"prod_name": "“安享回报”套利98天美元理财产品",	
				"expected_highest_yield": "0.6000%",
				"history_yield":"0.6000%",
				"return_type":"浮动收益",
				"risk_type":"较低风险",
				"sale_period": "2016/1/1~2016/2/1",
				"interest_period": "无固定期限",
				"starting_amount": "-"
			},
			{
				"issuer_name": "建设银行",
				"prod_name": "汇得盈非保本外币理财产品2015年第34期",	
				"expected_highest_yield": "1.0000%",
				"history_yield":"1.0000%",
				"return_type":"浮动收益",
				"risk_type":"较低风险",
				"sale_period": "2016/1/1~2016/2/1",
				"interest_period": "2016/1/6~2016/3/29",
				"starting_amount": "-"
			}]
	},
	{
		"tenor": 6,
		"industry_1m_avg_yield": "1.5300%",
		"list": [
			{
				"issuer_name": "招商银行",
				"prod_name": "美元鼎鼎成金0159号",	
				"expected_highest_yield": "1.8500%",
				"history_yield":"1.8500%",
				"return_type":"浮动收益",
				"risk_type":"较低风险",
				"sale_period": "2016/1/1~2016/2/1",
				"interest_period": "2016/1/7~2016/7/7",
				"starting_amount": "-"
			}]	
	}]
}
```
<br>

<h1 id="3">精选理财产品信息</h1>
```
GET /selectedwmp/{currency}
```
Arguments  | required | Description
-----------|:--------:|---------------
currency   | Y        | 货币: USD, GBP, EUR, AUD
**Request Example**

```
$ curl -i http://139.196.16.157:5000/ucms/api/v1.0/weixin/selectedwmp/USD
```
**Response Example**

```
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1994
Server: Werkzeug/0.11.5 Python/2.7.11
Date: Mon, 04 Apr 2016 08:34:39 GMT

{
"currency": "USD",
"currencyname": "美元",
"max_return": "3.1%",
"timestamp": "2016-03-29 16:00:00",
"total_rec": 8,
"tenor_group":[
	{
		"preservable": "N",
		"list": [
			{
				"issuer_name": "招商银行",
				"prod_name": "鼎鼎成金0196号美元728天",	
				"return_type":"浮动收益",
				"sale_period": "2015-12-30 ~ 2016-01-06",
				"expected_highest_yield": "3.1000%",
				"industry_1m_avg_yield": "3.1000%",				
				"deposit_period":12,
				"usd_rate":"1.0000%",
				"starting_amount": "8,000.00"
			},
			{
				"issuer_name": "招商银行",
				"prod_name": "鼎鼎成金960086号美元371天",	
				"return_type":"浮动收益",
				"sale_period": "2015-12-30 ~ 2016-01-06",
				"expected_highest_yield": "2.6000%",
				"industry_1m_avg_yield": "2.1286%",				
				"deposit_period":12,
				"usd_rate":"0.8000%",
				"starting_amount": "8,000.00"
			},		
			{
				"issuer_name": "兴业银行",
				"prod_name": "2016年第1期天天万汇通B款美元181天",	
				"return_type":"浮动收益",
				"sale_period": "2015-12-29 ~ 2016-01-04",
				"expected_highest_yield": "1.8500%",
				"industry_1m_avg_yield": "1.5300%",				
				"deposit_period":6,
				"usd_rate":"0.5000%",
				"starting_amount": "8,000.00"
			},	
			{
				"issuer_name": "招商银行",
				"prod_name": "美元鼎鼎成金0159号美元182天",	
				"return_type":"浮动收益",
				"sale_period": "2015-12-30 ~ 2016-01-06",
				"expected_highest_yield": "1.8500%",
				"industry_1m_avg_yield": "1.5300%",				
				"deposit_period":6,
				"usd_rate":"0.5000%",
				"starting_amount": "8,000.00"
			},	
			{
				"issuer_name": "民生银行",
				"prod_name": "非凡资产管理季汇赢B型第002期美元91天",	
				"return_type":"浮动收益",
				"sale_period": "2015-12-29 ~ 2016-01-06",
				"expected_highest_yield": "1.4000%",
				"industry_1m_avg_yield": "1.0000%",				
				"deposit_period":3,
				"usd_rate":"0.3000%",
				"starting_amount": "9,000.00"
			}]
	},
	{
		"preservable": "Y",
		"list": [
			{
				"issuer_name": "北京银行",
				"prod_name": "美元12个月美元365天",	
				"return_type":"保收益",
				"sale_period": "2015-12-25 ~ 2016-01-04",
				"expected_highest_yield": "1.8000%",
				"industry_1m_avg_yield": "1.4167%",				
				"deposit_period":12,
				"usd_rate":"1.0000%",
				"starting_amount": "8,000.00"
			},
			{
				"issuer_name": "上海银行",
				"prod_name": "“慧财”货币及债券系列(金鑫)理财产品(150M652期)美元180天",	
				"return_type":"保收益",
				"sale_period": "2015-12-28 ~ 2016-01-03",
				"expected_highest_yield": "1.3350%",
				"industry_1m_avg_yield": "1.0713%",				
				"deposit_period":6,
				"usd_rate":"0.8000%",
				"starting_amount": "8,000.00"
			},		
			{
				"issuer_name": "平安银行",
				"prod_name": "平安财富-(保本滚动)现金管理类2013年13期美元理财产品美元91天",	
				"return_type":"浮动收益",
				"sale_period": "2016-01-01 ~ 2016-01-07",
				"expected_highest_yield": "0.7500%",
				"industry_1m_avg_yield": "0.7500%",				
				"deposit_period":3,
				"usd_rate":"0.3000%",
				"starting_amount": "8,000.00"
			}]				
	}]
}
```
