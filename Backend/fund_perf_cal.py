# -*- coding: utf-8 -*-

import openpyxl
import logging
import re
import datetime
import mysql.connector
from mysql.connector import errorcode

import sys
reload(sys)
sys.setdefaultencoding('utf8')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

import random
from retrying import retry

from openpyxl import load_workbook


def cal():

    isin_list = []
    query = u"""
        SELECT
            isin_code, perf_year, perf_month, performance
        FROM
            t_fund_performance
        WHERE
            perf_type = 'zyq_score'
                AND isin_code <> ''
                AND performance <> ''
        ORDER BY isin_code , perf_year , perf_month
    """

    cursor.execute(query)
    for (isin_code, perf_year, perf_month, performance) in cursor:
        isin_list.append([isin_code, perf_year, perf_month, performance])

    logging.info(unicode(len(isin_list)) + ' zyq_score data imported')

    for index, isin in enumerate(isin_list):
        # -5Y
        sub_query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                isin_code = '%s'
                    AND perf_type = 'mthly_performance'
                    and perf_year = %s-5 and perf_month = %s
                    and performance <> ''
        """ % (isin[0], isin[1], isin[2])
        cursor.execute(sub_query)
        for (performance,) in cursor:
            isin.append(performance)
        if cursor.rowcount == -1:
            isin.append('')

        # -3Y
        sub_query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                isin_code = '%s'
                    AND perf_type = 'mthly_performance'
                    and perf_year = %s-3 and perf_month = %s
                    and performance <> ''
        """ % (isin[0], isin[1], isin[2])
        cursor.execute(sub_query)
        for (performance,) in cursor:
            isin.append(performance)
        if cursor.rowcount == -1:
            isin.append('')

        # -1Y
        sub_query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                isin_code = '%s'
                    AND perf_type = 'mthly_performance'
                    and perf_year = %s-1 and perf_month = %s
                    and performance <> ''
        """ % (isin[0], isin[1], isin[2])
        cursor.execute(sub_query)
        for (performance,) in cursor:
            isin.append(performance)
        if cursor.rowcount == -1:
            isin.append('')

        # -6M
        if int(isin[2]) <= 6:
            year = int(isin[1])-1
            month = int(isin[2])+6
        else:
            year = int(isin[1])
            month = int(isin[2])-6
        sub_query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                isin_code = '%s'
                    AND perf_type = 'mthly_performance'
                    and perf_year = %s and perf_month = %s
                    and performance <> ''
        """ % (isin[0], year, month)
        cursor.execute(sub_query)
        for (performance,) in cursor:
            isin.append(performance)
        if cursor.rowcount == -1:
            isin.append('')

        # -3M
        if int(isin[2]) <= 3:
            year = int(isin[1])-1
            month = int(isin[2])+9
        else:
            year = int(isin[1])
            month = int(isin[2])-3
        sub_query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                isin_code = '%s'
                    AND perf_type = 'mthly_performance'
                    and perf_year = %s and perf_month = %s
                    and performance <> ''
        """ % (isin[0], year, month)
        cursor.execute(sub_query)
        for (performance,) in cursor:
            isin.append(performance)
        if cursor.rowcount == -1:
            isin.append('')

        # -1M
        if int(isin[2]) == 1:
            year = int(isin[1])-1
            month = 12
        else:
            year = int(isin[1])
            month = int(isin[2])-1
        sub_query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                isin_code = '%s'
                    AND perf_type = 'mthly_performance'
                    and perf_year = %s and perf_month = %s
                    and performance <> ''
        """ % (isin[0], year, month)
        cursor.execute(sub_query)
        for (performance,) in cursor:
            isin.append(performance)
        if cursor.rowcount == -1:
            isin.append('')

        # 1M
        sub_query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                isin_code = '%s'
                    AND perf_type = 'mthly_performance'
                    and perf_year = %s and perf_month = %s
                    and performance <> ''
        """ % (isin[0], isin[1], isin[2])
        cursor.execute(sub_query)
        for (performance,) in cursor:
            isin.append(performance)
        if cursor.rowcount == -1:
            isin.append('')

        # 3M
        if int(isin[2]) >= 10:
            year = int(isin[1])+1
            month = int(isin[2])-9
        else:
            year = int(isin[1])
            month = int(isin[2])+3
        sub_query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                isin_code = '%s'
                    AND perf_type = 'mthly_performance'
                    and perf_year = %s and perf_month = %s
                    and performance <> ''
        """ % (isin[0], year, month)
        cursor.execute(sub_query)
        for (performance,) in cursor:
            isin.append(performance)
        if cursor.rowcount == -1:
            isin.append('')

        # 6M
        if int(isin[2]) >= 7:
            year = int(isin[1])+1
            month = int(isin[2])-6
        else:
            year = int(isin[1])
            month = int(isin[2])+6
        sub_query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                isin_code = '%s'
                    AND perf_type = 'mthly_performance'
                    and perf_year = %s and perf_month = %s
                    and performance <> ''
        """ % (isin[0], year, month)
        cursor.execute(sub_query)
        for (performance,) in cursor:
            isin.append(performance)
        if cursor.rowcount == -1:
            isin.append('')

        # 1Y
        sub_query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                isin_code = '%s'
                    AND perf_type = 'mthly_performance'
                    and perf_year = %s+1 and perf_month = %s
                    and performance <> ''
        """ % (isin[0], isin[1], isin[2])
        cursor.execute(sub_query)
        for (performance,) in cursor:
            isin.append(performance)
        if cursor.rowcount == -1:
            isin.append('')

        # 3Y
        sub_query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                isin_code = '%s'
                    AND perf_type = 'mthly_performance'
                    and perf_year = %s+3 and perf_month = %s
                    and performance <> ''
        """ % (isin[0], isin[1], isin[2])
        cursor.execute(sub_query)
        for (performance,) in cursor:
            isin.append(performance)
        if cursor.rowcount == -1:
            isin.append('')

        # 5Y
        sub_query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                isin_code = '%s'
                    AND perf_type = 'mthly_performance'
                    and perf_year = %s+5 and perf_month = %s
                    and performance <> ''
        """ % (isin[0], isin[1], isin[2])
        cursor.execute(sub_query)
        for (performance,) in cursor:
            isin.append(performance)
        if cursor.rowcount == -1:
            isin.append('')

        logging.info("(%s/%s)" % (index, unicode(len(isin_list))))
        # print isin

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "PERFORMANCE"
    ws_title = [
        "isin_code",
        "year",
        "month",
        "ZYQ 5Y Score",
        "Perf -5y",
        "Perf -3y",
        "Perf -1y",
        "Perf -6m",
        "Perf -3m",
        "Perf -1m",
        "Perf 1m",
        "Perf 3m",
        "Perf 6m",
        "Perf 1y",
        "Perf 3y",
        "Perf 5y"]

    ws.append(ws_title)
    for isin in isin_list:
        ws.append(isin)
    wb.save("output/performance.xlsx")

    cursor.close()

def decode(*arguments):
    """Compares first item to subsequent item one by one.

    If first item is equal to a key, returns the corresponding value (next item).
    If no match is found, returns None, or, if default is omitted, returns None.

    example usage:
    return_value = decode('b', 'a', 1, 'b', 2, 3)
    var = 'list'
    return_type = decode(var, 'tuple', (), 'dict', {}, 'list', [], 'string', '')
    """
    if len(arguments) < 3:
        raise TypeError, 'decode() takes at least 3 arguments (%d given)' % (len(arguments))
    de_dict = list(arguments[1:])
    if arguments[0] in de_dict:
        index = de_dict.index(arguments[0]);
        if index % 2 == 0 and len(de_dict) > index+1:
            return de_dict[index+1]
        return de_dict[-1]
    elif len(de_dict) % 2 != 0:
        return de_dict[-1]


if __name__ == '__main__':
    DB_NAME = 'zyq'

    try:
        # setup console parameters

        cnx = mysql.connector.connect(host='localhost', user='zyq', password='zyq', database=DB_NAME)
        # cnx = mysql.connector.connect(host='localhost', user='zyq', password='zyq', database=DB_NAME)
        logging.info('MYSQL connected.')
        cursor = cnx.cursor()

        cal()

        cnx.commit()
        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            raise
