# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, request

import logging
import json
import time
import mysql.connector
from mysql.connector import errorcode
from lib.butils import decode
from lib.butils import fix_json
from lib.butils import ppprint
from lib.butils.pprint import pprint

TIMEOUT = 10
LOCALDATE = time.strftime('%Y%m%d', time.localtime(time.time()))
TIMESTAMP = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
LOGNAME = 'log/ws_' + LOCALDATE + '.log'

# # initialize root logger to write verbose log file
# logging.basicConfig(level=logging.DEBUG,
#                     filename="log/ws_" + LOCALDATE + ".verbose.log",
#                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# initialize a local logger
logger_local = logging.getLogger("ucms.birdie.ws")
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

app = Flask(__name__)


@app.route('/ucms/api/v1.0/weixin/listingrate/<string:currency>', methods=['GET'])
def get_listing_rate(currency):
    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')

    cursor = cnx.cursor()

    rate_list = {"total_rec": "", "list": []}
    total_rec = ""

    # query = u"""
    #     SELECT count(*) FROM t_issuer, t_listing_rate
    #     WHERE t_issuer.issuer_code=t_listing_rate.publisher_code and t_listing_rate.currency='%s'
    #     """ % currency
    #
    # cursor.execute(query)
    # for (total_rec,) in cursor:
    #     rate_list["total_rec"] = total_rec
    #
    # if total_rec == 0:
    #     logger_local.info('Not found')
    #     abort(404)

    # 定义基准价
    query = u"""
        SELECT
            AVG(bid_remit), AVG(bid_cash), AVG(ask_remit), AVG(ask_cash)
        FROM
            t_listing_rate
        WHERE
            currency = '%s'
                AND DATE(publish_time) = CURDATE()
                AND publisher_code IN ('C10102' , 'C10103', 'C10104', 'C10105', 'C10301', 'C10308')
        """ % currency
    cursor.execute(query)
    for (bm_bid_remit, bm_bid_cash, bm_ask_remit, bm_ask_cash) in cursor:
        bm_bid_remit = bm_bid_remit
        bm_bid_cash = bm_bid_cash
        bm_ask_remit = bm_ask_remit
        bm_ask_cash = bm_ask_cash

    logger_local.info('Bench rates: %s, %s, %s, %s' % (bm_bid_remit, bm_bid_cash, bm_ask_remit, bm_ask_cash))

    query = u"""
        SELECT
            t_issuer.cn_short_name,
            t_listing_rate.bid_remit,
            t_listing_rate.bid_cash,
            t_listing_rate.ask_remit,
            t_listing_rate.ask_cash,
            t_listing_rate.publish_time
        FROM
            t_issuer,
            t_listing_rate
        WHERE
            t_issuer.issuer_code = t_listing_rate.publisher_code
                AND currency = '%s'
                AND DATE(publish_time) = CURDATE()
        """ % currency
    cursor.execute(query)
    rate_list["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    rate_list["currency"] = currency
    rate_list["currencyname"] = decode(currency, "USD", u"美元", "GBP", u"英镑", "AUD", u"澳元", "EUR", u"欧元",
                                       'JPY', u'日元', 'HKD', u"港币", 'CAD', u"加元", "")
    # logger_local.info('bm_bid_remit*1.0008: %s' % (bm_bid_remit*1.0008,))
    # logger_local.info('bm_bid_cash*1.0008: %s' % (bm_bid_cash*1.0008,))
    # logger_local.info('bm_ask_remit*0.9992: %s' % (bm_ask_remit*0.9992,))
    # logger_local.info('bm_ask_cash*0.9992: %s' % (bm_ask_cash*0.9992,))
    for (cn_short_name, bid_remit, bid_cash, ask_remit, ask_cash, publish_time) in cursor:
        if float(bid_remit) > bm_bid_remit * 1.008 or float(bid_cash) > bm_bid_cash * 1.008 \
                or float(ask_remit) < bm_ask_remit * 0.992 or float(ask_cash) < bm_ask_cash * 0.992:
            rate_list["list"].append({})
            rate_list["list"][-1]["bank"] = cn_short_name
            if currency == 'JPY':
                rate_list["list"][-1]["remitbid"] = '%.4f' % float(bid_remit)
                rate_list["list"][-1]["cashbid"] = '%.4f' % float(bid_cash)
                rate_list["list"][-1]["remitask"] = '%.4f' % float(ask_remit)
                rate_list["list"][-1]["cashask"] = '%.4f' % float(ask_cash)
            else:
                rate_list["list"][-1]["remitbid"] = '%.2f' % float(bid_remit)
                rate_list["list"][-1]["cashbid"] = '%.2f' % float(bid_cash)
                rate_list["list"][-1]["remitask"] = '%.2f' % float(ask_remit)
                rate_list["list"][-1]["cashask"] = '%.2f' % float(ask_cash)
            rate_list["list"][-1]["publish_time"] = publish_time
        else:
            rate_list["list"].append({})
            rate_list["list"][-1]["bank"] = cn_short_name
            if currency == 'JPY':
                rate_list["list"][-1]["remitbid"] = '%.4f' % float(bid_remit)
                rate_list["list"][-1]["cashbid"] = '%.4f' % float(bid_cash)
                rate_list["list"][-1]["remitask"] = '%.4f' % float(ask_remit)
                rate_list["list"][-1]["cashask"] = '%.4f' % float(ask_cash)
            else:
                rate_list["list"][-1]["remitbid"] = '%.2f' % float(bid_remit)
                rate_list["list"][-1]["cashbid"] = '%.2f' % float(bid_cash)
                rate_list["list"][-1]["remitask"] = '%.2f' % float(ask_remit)
                rate_list["list"][-1]["cashask"] = '%.2f' % float(ask_cash)
            rate_list["list"][-1]["publish_time"] = publish_time

    bid_remit_list = []
    bid_cash_list = []
    ask_remit_list = []
    ask_cash_list = []

    for r in rate_list["list"]:
        bid_remit_list.append(r["remitbid"])
        bid_cash_list.append(r["cashbid"])
        ask_remit_list.append(r["remitask"])
        ask_cash_list.append(r["cashask"])

    max_bid_remit = max(bid_remit_list)
    max_bid_cash = max(bid_cash_list)
    min_ask_remit = min(ask_remit_list)
    min_ask_cash = min(ask_cash_list)

    for r in rate_list["list"]:
        if currency == 'JPY':
            if r["remitbid"] == '%.4f' % float(max_bid_remit):
                r["remitbid"] = "*" + r["remitbid"]
            if r["cashbid"] == '%.4f' % float(max_bid_cash):
                r["cashbid"] = "*" + r["cashbid"]
            if r["remitask"] == '%.4f' % float(min_ask_remit):
                r["remitask"] = "*" + r["remitask"]
            if r["cashask"] == '%.4f' % float(min_ask_cash):
                r["cashask"] = "*" + r["cashask"]
        else:
            if r["remitbid"] == '%.2f' % float(max_bid_remit):
                r["remitbid"] = "*" + r["remitbid"]
            if r["cashbid"] == '%.2f' % float(max_bid_cash):
                r["cashbid"] = "*" + r["cashbid"]
            if r["remitask"] == '%.2f' % float(min_ask_remit):
                r["remitask"] = "*" + r["remitask"]
            if r["cashask"] == '%.2f' % float(min_ask_cash):
                r["cashask"] = "*" + r["cashask"]

    rate_list["total_rec"] = len(rate_list["list"])

    cnx.commit()
    cursor.close()
    cnx.close()

    logger_local.info('Rates requested for %s \n\n' % currency)

    # return jsonify(rate_list)
    return json.dumps(rate_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/selectedwmp/<string:currency>', methods=['GET'])
def get_selectedwmp(currency):
    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')
    cursor = cnx.cursor()

    total_rec = None
    max_yield = 0
    prod_list = {"currency": currency,
                 "currencyname": decode(currency, "USD", u"美元", "GBP", u"英镑", "AUD", u"澳元", "EUR", u"欧元", ""),
                 "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 "total_rec": "",
                 "tenor_group": [{"preservable": "N", "list": []}, {"preservable": "Y", "list": []}]
                 }

    # 非保本
    np_list = []
    query = u"""
        SELECT
            MAX(expected_highest_yield), ROUND(tenor / (365/12)) as TENOR
        FROM
            t_product
        WHERE
            (open_end_date >= CURDATE()
                OR (open_end_date = '每天' AND status = '在售'))
                AND preservable = '非保本'
                AND redeemable = '封闭'
                AND remark = '普通'
                AND currency = '%s'
        GROUP BY ROUND(tenor / (365/12))
        HAVING TENOR >= 3
        ORDER BY TENOR desc
        """ % (currency,)
    cursor.execute(query)
    for (expected_highest_yield, tenor_desc) in cursor:
        np_list.append([tenor_desc, expected_highest_yield])

    # 按期限
    for np in np_list:
        # 计算月平均
        industry_1m_avg_yield = None
        query0 = u"""
            SELECT
                AVG(bank_avg) AS avg
            FROM
                (SELECT
                    issuer_name, AVG(expected_highest_yield) AS bank_avg
                FROM
                    zyq.t_product
                WHERE
                    (DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(open_start_date)
                        OR (open_start_date = '每天' AND status = '在售'))
                    AND currency = '%s'
                    AND ROUND(tenor / (365/12)) = '%s'
                    AND preservable = '非保本'
                    AND redeemable = '封闭'
                    AND remark = '普通'
                GROUP BY issuer_name) t
            """ % (currency, np[0])
        cursor.execute(query0)

        for (cursor_avg,) in cursor:
            industry_1m_avg_yield = cursor_avg

        # prod_list["tenor_group"][0]["list"].append({"tenor": int(ty[0]), "list": []})
        query = u"""
            SELECT
                prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date,
                expected_highest_yield, last_yield, preservable, pledgeable, risk_desc, starting_amount
            FROM
                t_product
            WHERE
                (open_end_date >= CURDATE()
                    OR (open_end_date = '每天' AND status = '在售'))
                    AND preservable = '非保本'
                    AND redeemable = '封闭'
                    AND remark = '普通'
                    AND currency = '%s'
                    AND expected_highest_yield = '%s'
                    AND ROUND(tenor / (365/12)) = '%s'
            """ % (currency, np[1], np[0])
        cursor.execute(query)

        for (prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date, expected_highest_yield,
             last_yield, preservable, pledgeable, risk_desc, starting_amount) in cursor:
            prod_list["tenor_group"][0]["list"].append({
                "prod_name": prod_name,
                "issuer_name": issuer_name,
                "sale_period": '%s~%s' % (
                    dsf(open_start_date), dsf(open_end_date)) if open_start_date.isdigit() else u"每天",
                "deposit_period": int(np[0]),
                "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield) * 100,),
                "industry_1m_avg_yield": '%.4f%%' % (float(industry_1m_avg_yield) * 100,),
                "return_type": pledgeable,
                "usd_rate": get_USD_depo(np[0]),
                "starting_amount": '%.2f' % float(starting_amount)})

            if expected_highest_yield > max_yield:
                max_yield = expected_highest_yield

    # 保本
    ty_list = []
    query = u"""
        SELECT
            MAX(expected_highest_yield), ROUND(tenor / (365/12)) as TENOR
        FROM
            t_product
        WHERE
            (open_end_date >= CURDATE()
                OR (open_end_date = '每天' AND status = '在售'))
                AND preservable = '保本'
                AND redeemable = '封闭'
                AND remark = '普通'
                AND currency = '%s'
        GROUP BY ROUND(tenor / (365/12))
        HAVING TENOR >= 3
        ORDER BY TENOR desc
        """ % (currency,)
    cursor.execute(query)
    for (expected_highest_yield, tenor_desc) in cursor:
        ty_list.append([tenor_desc, expected_highest_yield])

    # 按期限
    for ty in ty_list:
        # 计算月平均
        industry_1m_avg_yield = None
        query0 = u"""
            SELECT
                AVG(bank_avg) AS avg
            FROM
                (SELECT
                    issuer_name, AVG(expected_highest_yield) AS bank_avg
                FROM
                    zyq.t_product
                WHERE
                    (DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(open_start_date)
                        OR (open_start_date = '每天' AND status = '在售'))
                    AND currency = '%s'
                    AND ROUND(tenor / (365/12)) = '%s'
                    AND preservable = '保本'
                    AND redeemable = '封闭'
                    AND remark = '普通'
                GROUP BY issuer_name) t
            """ % (currency, ty[0])
        cursor.execute(query0)

        for (cursor_avg,) in cursor:
            industry_1m_avg_yield = cursor_avg

        # prod_list["tenor_group"][0]["list"].append({"tenor": int(ty[0]), "list": []})
        query = u"""
            SELECT
                prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date,
                expected_highest_yield, last_yield, preservable, pledgeable, risk_desc, starting_amount
            FROM
                t_product
            WHERE
                (open_end_date >= CURDATE()
                    OR (open_end_date = '每天' AND status = '在售'))
                    AND preservable = '保本'
                    AND redeemable = '封闭'
                    AND remark = '普通'
                    AND currency = '%s'
                    AND expected_highest_yield = '%s'
                    AND ROUND(tenor / (365/12)) = '%s'
            """ % (currency, ty[1], ty[0])
        cursor.execute(query)

        for (prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date, expected_highest_yield,
             last_yield, preservable, pledgeable, risk_desc, starting_amount) in cursor:
            prod_list["tenor_group"][1]["list"].append({
                "prod_name": prod_name,
                "issuer_name": issuer_name,
                "sale_period": '%s~%s' % (
                    dsf(open_start_date), dsf(open_end_date)) if open_start_date.isdigit() else u"每天",
                "deposit_period": int(ty[0]),
                "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield) * 100,),
                "industry_1m_avg_yield": '%.4f%%' % (float(industry_1m_avg_yield) * 100,),
                "return_type": pledgeable,
                "usd_rate": get_USD_depo(np[0]),
                "starting_amount": '%.2f' % float(starting_amount)})

            if expected_highest_yield > max_yield:
                max_yield = expected_highest_yield

    prod_list["max_return"] = '%.2f%%' % (float(max_yield) * 100,)

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('Selected WM Products requested for %s \n\n' % currency)

    # return jsonify(rate_list)
    return json.dumps(prod_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/wmp/<string:currency>', methods=['GET'])
def get_wmp(currency):
    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')
    cursor = cnx.cursor()

    if currency == 'NONUSD':
        ccy_list = []
        total_rec = 0
        prod_list = {"timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                     "total_rec": "",
                     "tenor_group": []
                     }

        # 获取货币对
        query = u"""
            SELECT
                distinct currency
            FROM
                t_product
            WHERE
                (open_end_date >= CURDATE()
                    OR (open_end_date = '每天' AND status = '在售'))
                    AND redeemable = '封闭'
                    AND remark = '普通'
                    AND currency <> 'USD'
            """
        cursor.execute(query)
        for (currency,) in cursor:
            ccy_list.append(currency)

        for ccy in ccy_list:
            prod_list["tenor_group"].append({
                "currency": ccy,
                "currencyname": decode(ccy, "GBP", u"英镑", "AUD", u"澳元", "EUR", u"欧元", "HKD", u"港币", ccy),
                "list": []})

            # 获取明细列表
            query = u"""
                SELECT
                    prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date,
                    ROUND(tenor / (365/12)) as tenor_desc, expected_highest_yield, last_yield, preservable, pledgeable,
                    risk_desc, starting_amount
                FROM
                    t_product
                WHERE
                    (open_end_date >= CURDATE()
                        OR (open_end_date = '每天' AND status = '在售'))
                        AND redeemable = '封闭'
                        AND remark = '普通'
                        AND currency = '%s'
                ORDER BY tenor_desc DESC
                """ % ccy
            cursor.execute(query)
            for (prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date, tenor_desc,
                 expected_highest_yield, last_yield, preservable, pledgeable, risk_desc, starting_amount) in cursor:
                prod_list["tenor_group"][-1]["list"].append({
                    "prod_name": prod_name,
                    "issuer_name": issuer_name,
                    "tenor": int(tenor_desc),
                    "sale_period": '%s~%s' % (
                        dsf(open_start_date), dsf(open_end_date)) if open_start_date.isdigit() else u"每天",
                    "interest_period": '%s~%s' % (dsf(start_date), dsf(end_date)) if start_date.isdigit() else u"无固定期限",
                    "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield) * 100,),
                    "history_yield": '%.4f%%' % (float(last_yield) * 100,) if isnum(last_yield) else '-',
                    "preservable": 'Y' if preservable == u"保本" else 'N',
                    "return_type": pledgeable,
                    "risk_type": risk_desc + u"风险",
                    "starting_amount": '%.2f' % float(starting_amount)})

            total_rec += len(prod_list["tenor_group"][-1]["list"])

        prod_list["total_rec"] = total_rec

    else:
        total_rec = None
        prod_list = {"currency": currency,
                     "currencyname": decode(currency, "USD", u"美元", "GBP", u"英镑", "AUD", u"澳元", "EUR", u"欧元", ""),
                     "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                     "preservable": "ALL",
                     "total_rec": "",
                     "tenor_group": []
                     }

        preservable = request.args.get('preservable', '')

        if preservable == 'N' or preservable == 'Y':
            if preservable == 'N':
                preservable_str = u'非保本'
            else:
                preservable_str = u'保本'

            tenor_list = []
            prod_list["preservable"] = preservable

            # 统计记录数
            query = u"""
                SELECT
                    count(*)
                FROM
                    t_product
                WHERE
                    (open_end_date >= CURDATE()
                        OR (open_end_date = '每天' AND status = '在售'))
                        AND preservable = '%s'
                        AND redeemable = '封闭'
                        AND remark = '普通'
                        AND currency = '%s'
                """ % (preservable_str, currency)
            cursor.execute(query)
            for (csr_total_rec,) in cursor:
                total_rec = csr_total_rec

            if total_rec == 0:
                logger_local.info('Not found')
                abort(404)
            else:
                prod_list["total_rec"] = total_rec

            # 获取期限列表
            query = u"""
                SELECT
                    ROUND(tenor / (365/12)) AS tenor
                FROM
                    t_product
                WHERE
                    (open_end_date >= CURDATE()
                        OR (open_end_date = '每天' AND status = '在售'))
                        AND preservable = '%s'
                        AND redeemable = '封闭'
                        AND remark = '普通'
                        AND currency = '%s'
                GROUP BY ROUND(tenor / (365/12))
                ORDER BY tenor DESC
                """ % (preservable_str, currency)
            cursor.execute(query)
            for (tenor_desc) in cursor:
                tenor_list.append(tenor_desc)

            # 按期限
            for tn in tenor_list:
                prod_list["tenor_group"].append({"tenor": int(tn[0]), "list": []})
                industry_1m_avg_yield = None

                # 计算月平均
                query = u"""
                    SELECT
                        AVG(bank_avg) AS avg
                    FROM
                        (SELECT
                            issuer_name, AVG(expected_highest_yield) AS bank_avg
                        FROM
                            zyq.t_product
                        WHERE
                            (DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(open_start_date)
                                OR (open_start_date = '每天' AND status = '在售'))
                            AND currency = '%s'
                            AND ROUND(tenor / (365/12)) = '%s'
                            AND preservable = '%s'
                            AND redeemable = '封闭'
                            AND remark = '普通'
                        GROUP BY issuer_name) t
                    """ % (currency, tn[0], preservable_str)
                cursor.execute(query)
                for (cursor_avg,) in cursor:
                    industry_1m_avg_yield = '%.4f%%' % (float(cursor_avg) * 100,)
                    # prod_list["tenor_group"][-1]["industry_1m_avg_yield"] = '%.4f%%' % (float(cursor_avg)*100,)

                prod_list["tenor_group"][-1]["industry_1m_avg_yield"] = industry_1m_avg_yield

                # 获取明细列表
                query = u"""
                    SELECT
                        prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date,
                        expected_highest_yield, last_yield, preservable, pledgeable, risk_desc, starting_amount
                    FROM
                        t_product
                    WHERE
                        (open_end_date >= CURDATE()
                            OR (open_end_date = '每天' AND status = '在售'))
                            AND preservable = '%s'
                            AND redeemable = '封闭'
                            AND remark = '普通'
                            AND currency = '%s'
                            AND ROUND(tenor / (365/12)) = '%s'
                    """ % (preservable_str, currency, tn[0])
                cursor.execute(query)
                for (
                        prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date,
                        expected_highest_yield,
                        last_yield, preservable, pledgeable, risk_desc, starting_amount) in cursor:
                    prod_list["tenor_group"][-1]["list"].append({
                        "prod_name": prod_name,
                        "issuer_name": issuer_name,
                        "sale_period": '%s~%s' % (
                            dsf(open_start_date), dsf(open_end_date)) if open_start_date.isdigit() else u"每天",
                        "interest_period": '%s~%s' % (
                            dsf(start_date), dsf(end_date)) if start_date.isdigit() else u"无固定期限",
                        "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield) * 100,),
                        "history_yield": '%.4f%%' % (float(last_yield) * 100,) if isnum(last_yield) else '-',
                        "return_type": pledgeable,
                        "risk_type": risk_desc + u"风险",
                        "starting_amount": '%.2f' % float(starting_amount)})

        else:
            tenor_list = []
            prod_list["preservable"] = "ALL"

            # 统计记录数
            query = u"""
                SELECT
                    count(*)
                FROM
                    t_product
                WHERE
                    (open_end_date >= CURDATE()
                        OR (open_end_date = '每天' AND status = '在售'))
                        AND redeemable = '封闭'
                        AND remark = '普通'
                        AND currency = '%s'
                """ % currency
            cursor.execute(query)
            for (csr_total_rec,) in cursor:
                total_rec = csr_total_rec

            if total_rec == 0:
                logger_local.info('Not found')
                abort(404)
            else:
                prod_list["total_rec"] = total_rec

            # 获取期限列表
            query = u"""
                SELECT
                    ROUND(tenor / (365/12)) AS tenor
                FROM
                    t_product
                WHERE
                    (open_end_date >= CURDATE()
                        OR (open_end_date = '每天' AND status = '在售'))
                        AND redeemable = '封闭'
                        AND remark = '普通'
                        AND currency = '%s'
                GROUP BY ROUND(tenor / (365/12))
                ORDER BY tenor DESC
                """ % (currency,)
            cursor.execute(query)
            for (tenor_desc) in cursor:
                tenor_list.append(tenor_desc)

            # 按期限
            for tn in tenor_list:
                prod_list["tenor_group"].append({"tenor": int(tn[0]), "list": []})
                industry_1m_avg_yield = None

                # 计算月平均
                query = u"""
                    SELECT
                        AVG(bank_avg) AS avg
                    FROM
                        (SELECT
                            issuer_name, AVG(expected_highest_yield) AS bank_avg
                        FROM
                            zyq.t_product
                        WHERE
                            (DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(open_start_date)
                                OR (open_start_date = '每天' AND status = '在售'))
                            AND currency = '%s'
                            AND ROUND(tenor / (365/12)) = '%s'
                            AND redeemable = '封闭'
                            AND remark = '普通'
                        GROUP BY issuer_name) t
                    """ % (currency, tn[0])
                cursor.execute(query)
                for (cursor_avg,) in cursor:
                    industry_1m_avg_yield = '%.4f%%' % (float(cursor_avg) * 100,)
                    # prod_list["tenor_group"][-1]["industry_1m_avg_yield"] = '%.4f%%' % (float(cursor_avg)*100,)

                prod_list["tenor_group"][-1]["industry_1m_avg_yield"] = industry_1m_avg_yield

                # 获取明细列表
                query = u"""
                    SELECT
                        prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date,
                        expected_highest_yield, last_yield, preservable, pledgeable, risk_desc, starting_amount
                    FROM
                        t_product
                    WHERE
                        (open_end_date >= CURDATE()
                            OR (open_end_date = '每天' AND status = '在售'))
                            AND redeemable = '封闭'
                            AND remark = '普通'
                            AND currency = '%s'
                            AND ROUND(tenor / (365/12)) = '%s'
                    """ % (currency, tn[0])
                cursor.execute(query)
                for (
                        prod_name, issuer_name, start_date, end_date, open_start_date, open_end_date,
                        expected_highest_yield,
                        last_yield, preservable, pledgeable, risk_desc, starting_amount) in cursor:
                    prod_list["tenor_group"][-1]["list"].append({
                        "prod_name": prod_name,
                        "issuer_name": issuer_name,
                        "sale_period": '%s~%s' % (
                            dsf(open_start_date), dsf(open_end_date)) if open_start_date.isdigit() else u"每天",
                        "interest_period": '%s~%s' % (
                            dsf(start_date), dsf(end_date)) if start_date.isdigit() else u"无固定期限",
                        "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield) * 100,),
                        "history_yield": '%.4f%%' % (float(last_yield) * 100,) if isnum(last_yield) else '-',
                        "return_type": pledgeable,
                        "risk_type": risk_desc + u"风险",
                        "starting_amount": '%.2f' % float(starting_amount)})

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('Selected WM Products requested for %s \n\n' % currency)

    # return jsonify(rate_list)
    return json.dumps(prod_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/wmpcomp', methods=['GET'])
def wmp_comp():
    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')
    cursor = cnx.cursor()

    ccy_list = []
    total_rec = 0
    prod_list = {"timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 "total_rec": "",
                 "tenor_group": [{"currency": "USD",
                                  "currencyname": u"美元",
                                  "preservable": "N",
                                  "list": []},
                                 {"currency": "USD",
                                  "currencyname": u"美元",
                                  "preservable": "Y",
                                  "list": []}]
                 }

    tenor_list = ["1", "2", "3", "6", "9", "12", "24"]

    # 非保本
    for tn in tenor_list:
        query = u"""
            SELECT
                issuer_name, ROUND(tenor / (365/12)) as tenor_desc, expected_highest_yield
            FROM
                t_product
            WHERE
                (DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(open_start_date)
                    OR (open_start_date = '每天' AND status = '在售'))
                    AND redeemable = '封闭'
                    AND preservable = '非保本'
                    AND remark = '普通'
                    AND currency = 'USD'
                    AND tenor_desc = %s
            ORDER BY expected_highest_yield desc
            LIMIT 1
        """ % tn
        cursor.execute(query)
        for (issuer_name, tenor_desc, expected_highest_yield) in cursor:
            prod_list["tenor_group"][0]["list"].append({
                "tenor": tn,
                "issuer_name": issuer_name,
                "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield) * 100,)
            })

        if cursor.rowcount == -1:
            prod_list["tenor_group"][0]["list"].append({
                "tenor": tn,
                "issuer_name": "-",
                "expected_highest_yield": "-"
            })

        # 计算月平均
        query = u"""
            SELECT
                AVG(bank_avg) AS avg
            FROM
                (SELECT
                    issuer_name, AVG(expected_highest_yield) AS bank_avg
                FROM
                    zyq.t_product
                WHERE
                    (DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(open_start_date)
                        OR (open_start_date = '每天' AND status = '在售'))
                    AND currency = 'USD'
                    AND ROUND(tenor / (365/12)) = %s
                    AND redeemable = '封闭'
                    AND preservable = '非保本'
                    AND remark = '普通'
                GROUP BY issuer_name) t
            """ % tn
        cursor.execute(query)
        for (avg,) in cursor:
            if avg is None:
                prod_list["tenor_group"][0]["list"][-1]["average_yield"] = "-"
            else:
                prod_list["tenor_group"][0]["list"][-1]["average_yield"] = '%.4f%%' % (float(avg) * 100,)

    # 保本
    for tn in tenor_list:
        query = u"""
            SELECT
                issuer_name, ROUND(tenor / (365/12)) as tenor_desc, expected_highest_yield
            FROM
                t_product
            WHERE
                (DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(open_start_date)
                    OR (open_start_date = '每天' AND status = '在售'))
                    AND redeemable = '封闭'
                    AND preservable = '保本'
                    AND remark = '普通'
                    AND currency = 'USD'
                    AND tenor_desc = %s
            ORDER BY expected_highest_yield desc
            LIMIT 1
        """ % tn
        cursor.execute(query)
        for (issuer_name, tenor_desc, expected_highest_yield) in cursor:
            prod_list["tenor_group"][1]["list"].append({
                "tenor": tn,
                "issuer_name": issuer_name,
                "expected_highest_yield": '%.4f%%' % (float(expected_highest_yield) * 100,)
            })

        if cursor.rowcount == -1:
            prod_list["tenor_group"][1]["list"].append({
                "tenor": tn,
                "issuer_name": "-",
                "expected_highest_yield": "-"
            })

        # 计算月平均
        query = u"""
            SELECT
                AVG(bank_avg) AS avg
            FROM
                (SELECT
                    issuer_name, AVG(expected_highest_yield) AS bank_avg
                FROM
                    zyq.t_product
                WHERE
                    (DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= DATE(open_start_date)
                        OR (open_start_date = '每天' AND status = '在售'))
                        AND currency = 'USD'
                        AND ROUND(tenor / (365/12)) = %s
                        AND redeemable = '封闭'
                        AND preservable = '保本'
                        AND remark = '普通'
                GROUP BY issuer_name) t
            """ % tn
        cursor.execute(query)
        for (avg,) in cursor:
            if avg is None:
                prod_list["tenor_group"][1]["list"][-1]["average_yield"] = "-"
            else:
                prod_list["tenor_group"][1]["list"][-1]["average_yield"] = '%.4f%%' % (float(avg) * 100,)

    total_rec += (len(prod_list["tenor_group"][0]["list"]) + len(prod_list["tenor_group"][1]["list"]))
    prod_list["total_rec"] = total_rec

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('wmp comp tenor %s \n\n' % tn)

    # return jsonify(rate_list)
    return json.dumps(prod_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/gstockfund', methods=['GET'])
def get_fund_stock_general():
    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')
    cursor = cnx.cursor()

    group_type_list = []
    total_rec = 0
    prod_list = {"fundtype": 1,
                 "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 "releasedate": "2016.08",
                 "total_rec": "",
                 "sec_group": []
                 }

    # 获取group
    query = u"""
            SELECT
                DISTINCT group_type
            FROM
                zyq.t_selected_fund_product
            WHERE
                category = 'B11';
        """
    cursor.execute(query)
    for (group_type,) in cursor:
        group_type_list.append(group_type)

    for gt in group_type_list:
        if gt == "Developed Market":
            gt_ch = u"投资发达市场股票型基金"
        elif gt == "Emerging Market":
            gt_ch = u"投资新兴市场股票型基金"
        elif gt == "Global":
            gt_ch = u"投资全球股票型基金"
        elif gt == "Sector Funds":
            gt_ch = u"投资行业股票型基金"
        elif gt == "Smaller Companies":
            gt_ch = u"投资中小公司股票型基金"
        else:
            gt_ch = gt

        prod_list["sec_group"].append({"group_type": gt_ch,
                                       "group_list": []})
        query = u"""
                SELECT
                    ranking,
                    prod_name,
                    ISIN_code,
                    cp_1m,
                    cp_1y,
                    cp_3y,
                    cp_5y
                FROM
                    zyq.t_selected_fund_product
                WHERE
                    category = 'B11' and group_type = '%s'
                ORDER BY ranking;
            """ % gt
        cursor.execute(query)

        for (ranking, prod_name, ISIN_code, cp_1m, cp_1y, cp_3y, cp_5y) in cursor:
            prod_list["sec_group"][-1]["group_list"].append({"rank": ranking,
                                                             "fund_name": prod_name,
                                                             "ISIN": ISIN_code,
                                                             "return1m": cp_1m + "%",
                                                             "return1y": cp_1y + "%",
                                                             "return3y": cp_3y + "%",
                                                             "return5y": cp_5y + "%"})

        total_rec += cursor.rowcount

    prod_list["total_rec"] = total_rec

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('Stock Fund general performance requested\n\n')

    return json.dumps(prod_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/bstockfund', methods=['GET'])
def get_fund_stock_best():
    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')
    cursor = cnx.cursor()

    tenor_list = []
    total_rec = 0
    prod_list = {"fundtype": 1,
                 "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 "releasedate": "2016.08",
                 "total_rec": "",
                 "tenor_group": []
                 }

    # 获取group
    query = u"""
            SELECT
                DISTINCT tenor
            FROM
                zyq.t_selected_fund_product
            WHERE
                category = 'B12';
        """
    cursor.execute(query)
    for (tenor,) in cursor:
        tenor_list.append(tenor)

    for tn in tenor_list:
        prod_list["tenor_group"].append({"tenor": tn,
                                         "list": []})
        query = u"""
                SELECT
                    prod_name,
                    ISIN_code,
                    annual_dividend,
                    group_type
                FROM
                    zyq.t_selected_fund_product
                WHERE
                    category = 'B12' and tenor = '%s';
            """ % tn
        cursor.execute(query)

        for (prod_name, ISIN_code, annual_dividend, group_type) in cursor:
            if group_type == "Developed Market":
                gt_ch = u"投资发达市场"
            elif group_type == "Emerging Market":
                gt_ch = u"投资新兴市场"
            elif group_type == "Global":
                gt_ch = u"投资全球"
            elif group_type == "Sector Funds":
                gt_ch = u"投资行业股票"
            elif group_type == "Smaller Companies":
                gt_ch = u"投资中小型公司"
            else:
                gt_ch = group_type

            prod_list["tenor_group"][-1]["list"].append({"fund_name": prod_name,
                                                         "isin": ISIN_code,
                                                         "return": annual_dividend + "%",
                                                         "group_type": gt_ch})

        total_rec += cursor.rowcount

    prod_list["total_rec"] = total_rec

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('Stock Fund best performance requested\n\n')

    return json.dumps(prod_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/gbondfund', methods=['GET'])
def get_fund_bond_general():
    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')
    cursor = cnx.cursor()

    group_type_list = []
    total_rec = 0
    prod_list = {"fundtype": 2,
                 "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 "releasedate": "2016.08",
                 "total_rec": "",
                 "sec_group": []
                 }

    # 获取group
    query = u"""
            SELECT
                DISTINCT group_type
            FROM
                zyq.t_selected_fund_product
            WHERE
                category = 'B21';
        """
    cursor.execute(query)
    for (group_type,) in cursor:
        group_type_list.append(group_type)

    for gt in group_type_list:
        if gt == "Composite":
            gt_ch = u"综合债券型基金"
        elif gt == "Government":
            gt_ch = u"投资政府债型基金"
        elif gt == "Corporate":
            gt_ch = u"投资公司债型基金"
        elif gt == "High-Yield":
            gt_ch = u"投资高收益债型基金"
        elif gt == "Inflation-Linked":
            gt_ch = u"投资通胀挂钩债券型基金"
        else:
            gt_ch = gt

        prod_list["sec_group"].append({"group_type": gt_ch,
                                       "group_list": []})
        query = u"""
                SELECT
                    ranking,
                    prod_name,
                    ISIN_code,
                    cp_1m,
                    cp_1y,
                    cp_3y,
                    cp_5y
                FROM
                    zyq.t_selected_fund_product
                WHERE
                    category = 'B21' and group_type = '%s'
                ORDER BY ranking;
            """ % gt
        cursor.execute(query)

        for (ranking, prod_name, ISIN_code, cp_1m, cp_1y, cp_3y, cp_5y) in cursor:
            prod_list["sec_group"][-1]["group_list"].append({"rank": ranking,
                                                             "fund_name": prod_name,
                                                             "ISIN": ISIN_code,
                                                             "return1m": cp_1m + "%",
                                                             "return1y": cp_1y + "%",
                                                             "return3y": cp_3y + "%",
                                                             "return5y": cp_5y + "%"})

        total_rec += cursor.rowcount

    prod_list["total_rec"] = total_rec

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('Bond Fund general performance requested\n\n')

    return json.dumps(prod_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/bbondfund', methods=['GET'])
def get_fund_bond_best():
    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')
    cursor = cnx.cursor()

    tenor_list = []
    total_rec = 0
    prod_list = {"fundtype": 2,
                 "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 "releasedate": "2016.08",
                 "total_rec": "",
                 "tenor_group": []
                 }

    # 获取group
    query = u"""
            SELECT
                DISTINCT tenor
            FROM
                zyq.t_selected_fund_product
            WHERE
                category = 'B22';
        """
    cursor.execute(query)
    for (tenor,) in cursor:
        tenor_list.append(tenor)

    for tn in tenor_list:
        prod_list["tenor_group"].append({"tenor": tn,
                                         "list": []})
        query = u"""
                SELECT
                    prod_name,
                    ISIN_code,
                    annual_dividend,
                    group_type
                FROM
                    zyq.t_selected_fund_product
                WHERE
                    category = 'B22' and tenor = '%s';
            """ % tn
        cursor.execute(query)

        for (prod_name, ISIN_code, annual_dividend, group_type) in cursor:
            if group_type == "Composite":
                gt_ch = u"综合债券投资型"
            elif group_type == "Government":
                gt_ch = u"投资政府债"
            elif group_type == "Corporate":
                gt_ch = u"投资公司债"
            elif group_type == "High-Yield":
                gt_ch = u"投资高收益债型"
            elif group_type == "Inflation-Linked":
                gt_ch = u"投资通胀挂钩型"
            else:
                gt_ch = group_type

            prod_list["tenor_group"][-1]["list"].append({"fund_name": prod_name,
                                                         "isin": ISIN_code,
                                                         "return": annual_dividend + "%",
                                                         "group_type": gt_ch})

        total_rec += cursor.rowcount

    prod_list["total_rec"] = total_rec

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('Stock Fund best performance requested\n\n')

    return json.dumps(prod_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/gbalancedfund', methods=['GET'])
def get_fund_balance_general():
    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')
    cursor = cnx.cursor()

    group_type_list = []
    total_rec = 0
    prod_list = {"fundtype": 3,
                 "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 "releasedate": "2016.08",
                 "total_rec": "",
                 "sec_group": []
                 }

    # 获取group
    # query = u"""
    #         SELECT
    #             DISTINCT group_type
    #         FROM
    #             zyq.t_selected_fund_product
    #         WHERE
    #             category = 'B31';
    #     """
    # cursor.execute(query)
    # for (group_type,) in cursor:
    #     group_type_list.append(group_type)

    # for gt in group_type_list:
    #     if gt == "Global":
    #         gt_ch = u"投资全球"
    #     elif gt == "Far East & Pac":
    #         gt_ch = u"投资远东太平洋"
    #     elif gt == "Regional(ex Asia Pacific)":
    #         gt_ch = u"投资非亚太地区"
    #     else:
    #         gt_ch = gt
    #
    #     prod_list["sec_group"].append({"group_type": gt_ch,
    #                                    "group_list": []})
    #     query = u"""
    #             SELECT
    #                 ranking,
    #                 prod_name,
    #                 ISIN_code,
    #                 cp_1m,
    #                 cp_1y,
    #                 cp_3y,
    #                 cp_5y
    #             FROM
    #                 zyq.t_selected_fund_product
    #             WHERE
    #                 category = 'B31' and group_type = '%s'
    #             ORDER BY ranking;
    #         """ % gt

    prod_list["sec_group"].append({"group_type": "--",
                                   "group_list": []})
    query = u"""
            SELECT
                ranking,
                prod_name,
                ISIN_code,
                cp_1m,
                cp_1y,
                cp_3y,
                cp_5y
            FROM
                zyq.t_selected_fund_product
            WHERE
                category = 'B31'
            ORDER BY ranking;
        """

    cursor.execute(query)

    for (ranking, prod_name, ISIN_code, cp_1m, cp_1y, cp_3y, cp_5y) in cursor:
        prod_list["sec_group"][-1]["group_list"].append({"rank": ranking,
                                                         "fund_name": prod_name,
                                                         "ISIN": ISIN_code,
                                                         "return1m": cp_1m + "%",
                                                         "return1y": cp_1y + "%",
                                                         "return3y": cp_3y + "%",
                                                         "return5y": cp_5y + "%"})

    total_rec += cursor.rowcount

    prod_list["total_rec"] = total_rec

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('Bond Fund general performance requested\n\n')

    return json.dumps(prod_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/bbalancedfund', methods=['GET'])
def get_fund_balance_best():
    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')
    cursor = cnx.cursor()

    tenor_list = []
    total_rec = 0
    prod_list = {"fundtype": 3,
                 "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 "releasedate": "2016.08",
                 "total_rec": "",
                 "tenor_group": []
                 }

    # 获取group
    query = u"""
            SELECT
                DISTINCT tenor
            FROM
                zyq.t_selected_fund_product
            WHERE
                category = 'B32';
        """
    cursor.execute(query)
    for (tenor,) in cursor:
        tenor_list.append(tenor)

    for tn in tenor_list:
        prod_list["tenor_group"].append({"tenor": tn,
                                         "list": []})
        query = u"""
                SELECT
                    prod_name,
                    ISIN_code,
                    annual_dividend,
                    group_type
                FROM
                    zyq.t_selected_fund_product
                WHERE
                    category = 'B32' and tenor = '%s';
            """ % tn
        cursor.execute(query)

        for (prod_name, ISIN_code, annual_dividend, group_type) in cursor:
            if group_type == "Global":
                gt_ch = u"投资全球"
            elif group_type == "Far East & Pac":
                gt_ch = u"投资远东太平洋"
            elif group_type == "Regional (ex Asia Pacific)":
                gt_ch = u"投资非亚太地区"
            else:
                gt_ch = group_type
            prod_list["tenor_group"][-1]["list"].append({"fund_name": prod_name,
                                                         "isin": ISIN_code,
                                                         "return": annual_dividend + "%",
                                                         "group_type": gt_ch})

        total_rec += cursor.rowcount

    prod_list["total_rec"] = total_rec

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('Stock Fund best performance requested\n\n')

    return json.dumps(prod_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/selectedbond', methods=['GET'])
def get_selected_bond():
    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='root', password='passwd', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')
    cursor = cnx.cursor()

    prod_list = {"currency": "USD",
                 "currencyname": u"美元",
                 "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 "total_rec": 9,
                 "tenor_group": []
                 }

    query = u"""
            SELECT
                ranking,
                issuer_name,
                expected_yield,
                bond_type,
                coupon,
                credit_rating,
                rating_firm,
                risk_rating,
                maturity_date,
                bid_price,
                coupon_code
            FROM
                zyq.t_selected_bond
            WHERE
                title = '持有半年预期收益最高海外债券';
        """
    cursor.execute(query)
    prod_list["tenor_group"].append({"tenor": 0.5, "list": []})
    for (ranking, issuer_name, expected_yield, bond_type, coupon, credit_rating, rating_firm, risk_rating,
         maturity_date, bid_price, coupon_code) in cursor:
        prod_list["tenor_group"][-1]["list"].append({"rank": ranking,
                                                     "issuer_name": issuer_name,
                                                     "period": u"半年",
                                                     "rate": coupon + "%",
                                                     "expected_highest_yield": expected_yield + "%",
                                                     "creadit_rank": risk_rating,
                                                     "grading": credit_rating,
                                                     "grading_owner": rating_firm,
                                                     "deadline": maturity_date,
                                                     "buy_price": bid_price,
                                                     "sale_price": "",
                                                     "bond_code": coupon_code})

    query = u"""
            SELECT
                ranking,
                issuer_name,
                expected_yield,
                bond_type,
                coupon,
                credit_rating,
                rating_firm,
                risk_rating,
                maturity_date,
                bid_price,
                coupon_code
            FROM
                zyq.t_selected_bond
            WHERE
                title = '持有一年预期收益最高海外债券';
        """
    cursor.execute(query)
    prod_list["tenor_group"].append({"tenor": 1, "list": []})
    for (ranking, issuer_name, expected_yield, bond_type, coupon, credit_rating, rating_firm, risk_rating,
         maturity_date, bid_price, coupon_code) in cursor:
        prod_list["tenor_group"][-1]["list"].append({"rank": ranking,
                                                     "issuer_name": issuer_name,
                                                     "period": u"一年",
                                                     "rate": coupon + "%",
                                                     "expected_highest_yield": expected_yield + "%",
                                                     "creadit_rank": risk_rating,
                                                     "grading": credit_rating,
                                                     "grading_owner": rating_firm,
                                                     "deadline": maturity_date,
                                                     "buy_price": bid_price,
                                                     "sale_price": "",
                                                     "bond_code": coupon_code})

    query = u"""
            SELECT
                ranking,
                issuer_name,
                expected_yield,
                bond_type,
                coupon,
                credit_rating,
                rating_firm,
                risk_rating,
                maturity_date,
                bid_price,
                coupon_code
            FROM
                zyq.t_selected_bond
            WHERE
                title = '持有两年预期收益最高海外债券';
        """
    cursor.execute(query)
    prod_list["tenor_group"].append({"tenor": 2, "list": []})
    for (ranking, issuer_name, expected_yield, bond_type, coupon, credit_rating, rating_firm, risk_rating,
         maturity_date, bid_price, coupon_code) in cursor:
        prod_list["tenor_group"][-1]["list"].append({"rank": ranking,
                                                     "issuer_name": issuer_name,
                                                     "period": u"两年",
                                                     "rate": coupon + "%",
                                                     "expected_highest_yield": expected_yield + "%",
                                                     "creadit_rank": risk_rating,
                                                     "grading": credit_rating,
                                                     "grading_owner": rating_firm,
                                                     "deadline": maturity_date,
                                                     "buy_price": bid_price,
                                                     "sale_price": "",
                                                     "bond_code": coupon_code})

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('Selected Bond requested\n\n')

    # return jsonify(rate_list)
    return json.dumps(prod_list, ensure_ascii=False)


@app.route('/ucms/api/v1.0/weixin/bond', methods=['GET'])
def get_bond():
    try:
        # cnx = mysql.connector.connect(host='139.196.16.157', user='zyq', password='zyq', database='zyq')
        cnx = mysql.connector.connect(user='zyq', password='zyq', database='zyq')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger_local.error("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger_local.error("Database does not exist")
        else:
            logger_local.error(err)
    else:
        logger_local.info('MYSQL connected.')
    cursor = cnx.cursor()

    prod_list = {"timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                 "total_rec": 9,
                 "sec_group": []
                 }

    query = u"""
            SELECT
                ranking,
                issuer_name,
                tenor,
                coupon,
                expected_6m_yield,
                expected_1y_yield,
                expected_2y_yield,
                currency,
                bond_type,
                credit_rating,
                rating_firm,
                risk_rating,
                maturity_date,
                bid_price,
                coupon_code
            FROM
                zyq.t_rating_bond
            WHERE
                risk_rating = 2;
        """
    cursor.execute(query)
    prod_list["sec_group"].append({"level": 2, "list": []})
    for (ranking, issuer_name, tenor, coupon, expected_6m_yield, expected_1y_yield, expected_2y_yield, currency,
         bond_type, credit_rating, rating_firm, risk_rating, maturity_date, bid_price, coupon_code) in cursor:
        prod_list["sec_group"][-1]["list"].append({"rank": ranking,
                                                   "issuer_name": issuer_name,
                                                   "currency": currency,
                                                   "period": tenor,
                                                   "rate": coupon + "%",
                                                   "yield12": expected_6m_yield + "%",
                                                   "yield24": expected_1y_yield + "%",
                                                   "yield36": expected_2y_yield + "%",
                                                   "deadline": maturity_date,
                                                   "buy_price": bid_price,
                                                   "sale_price": "",
                                                   "grading": credit_rating,
                                                   "grading_owner": rating_firm,
                                                   "bond_code": coupon_code})

    query = u"""
            SELECT
                ranking,
                issuer_name,
                tenor,
                coupon,
                expected_6m_yield,
                expected_1y_yield,
                expected_2y_yield,
                currency,
                bond_type,
                credit_rating,
                rating_firm,
                risk_rating,
                maturity_date,
                bid_price,
                coupon_code
            FROM
                zyq.t_rating_bond
            WHERE
                risk_rating = 3;
        """
    cursor.execute(query)
    prod_list["sec_group"].append({"level": 3, "list": []})
    for (ranking, issuer_name, tenor, coupon, expected_6m_yield, expected_1y_yield, expected_2y_yield, currency,
         bond_type, credit_rating, rating_firm, risk_rating, maturity_date, bid_price, coupon_code) in cursor:
        prod_list["sec_group"][-1]["list"].append({"rank": ranking,
                                                   "issuer_name": issuer_name,
                                                   "currency": currency,
                                                   "period": tenor,
                                                   "rate": coupon + "%",
                                                   "yield12": expected_6m_yield + "%",
                                                   "yield24": expected_1y_yield + "%",
                                                   "yield36": expected_2y_yield + "%",
                                                   "deadline": maturity_date,
                                                   "buy_price": bid_price,
                                                   "sale_price": "",
                                                   "grading": credit_rating,
                                                   "grading_owner": rating_firm,
                                                   "bond_code": coupon_code})

    query = u"""
            SELECT
                ranking,
                issuer_name,
                tenor,
                coupon,
                expected_6m_yield,
                expected_1y_yield,
                expected_2y_yield,
                currency,
                bond_type,
                credit_rating,
                rating_firm,
                risk_rating,
                maturity_date,
                bid_price,
                coupon_code
            FROM
                zyq.t_rating_bond
            WHERE
                risk_rating = 4;
        """
    cursor.execute(query)
    prod_list["sec_group"].append({"level": 4, "list": []})
    for (ranking, issuer_name, tenor, coupon, expected_6m_yield, expected_1y_yield, expected_2y_yield, currency,
         bond_type, credit_rating, rating_firm, risk_rating, maturity_date, bid_price, coupon_code) in cursor:
        prod_list["sec_group"][-1]["list"].append({"rank": ranking,
                                                   "issuer_name": issuer_name,
                                                   "currency": currency,
                                                   "period": tenor,
                                                   "rate": coupon + "%",
                                                   "yield12": expected_6m_yield + "%",
                                                   "yield24": expected_1y_yield + "%",
                                                   "yield36": expected_2y_yield + "%",
                                                   "deadline": maturity_date,
                                                   "buy_price": bid_price,
                                                   "sale_price": "",
                                                   "grading": credit_rating,
                                                   "grading_owner": rating_firm,
                                                   "bond_code": coupon_code})

    cnx.commit()
    cursor.close()
    cnx.close()
    logger_local.info('Selected Bond requested\n\n')

    # return jsonify(rate_list)
    return json.dumps(prod_list, ensure_ascii=False)


def get_USD_depo(tenor):
    return decode(tenor,
                  1, u"0.2000%",
                  3, u"0.3000%",
                  6, u"0.5000%",
                  9, u"0.5000%",
                  12, u"0.7500%",
                  18, u"0.7500%",
                  24, u"0.7500%",
                  "--")


def get_fund_type(e_name):
    return decode(e_name,
                  "Developed Market", u"发达市场",
                  "Emerging Market", u"新兴市场",
                  "Global", u"",
                  "Sector Funds", u"",
                  "Smaller Companies", u"",
                  "Smaller Companies", u"",
                  "Smaller Companies", u"",
                  "Smaller Companies", u"",
                  "Smaller Companies", u"",
                  "Smaller Companies", u"",
                  "Smaller Companies", u"",
                  "Smaller Companies", u"",
                  "Smaller Companies", u"",
                  "Smaller Companies", u"",

                  "--")


def dsf(date):
    try:
        if len(date) == 8:
            return date[:4] + "." + date[4:6] + "." + date[6:8]
        else:
            return date
    except:
        return date


def isnum(value):
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
