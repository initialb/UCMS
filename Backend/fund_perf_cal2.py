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
            isin_code, months, perf_year, perf_month
        FROM
            t_fund_performance
        WHERE
            perf_type = 'mthly_performance'
                AND isin_code <> ''
        ORDER BY isin_code ,months
    """

    cursor.execute(query)
    for (isin_code, months, perf_year, perf_month) in cursor:
        isin_list.append([isin_code, months, perf_year, perf_month])

    logging.info(unicode(len(isin_list)) + ' zyq_score data imported')

    for index, isin in enumerate(isin_list):

        query = u"""
            SELECT
                performance
            FROM
                t_fund_performance
            WHERE
                perf_type = 'zyq_score'
                    AND isin_code = '%s'
                    AND months = %s
        """ % (isin[0], isin[1])
        cursor.execute(query)
        for (performance,) in cursor:
            performance = performance
        if cursor.rowcount == 1:
            isin.append(performance)
        else:
            isin.append('')

        for prev in (60, 36, 12, 6, 3, 1):
            perf_result = 1.0
            sub_query = u"""
                SELECT
                    performance
                FROM
                    t_fund_performance
                WHERE
                    isin_code = '%s'
                        AND perf_type = 'mthly_performance'
                        and months between %s-%s and %s-1
                        and performance <> ''
            """ % (isin[0], isin[1], prev, isin[1])
            cursor.execute(sub_query)
            for (performance,) in cursor:
                perf_result = perf_result*(1+float(performance)/100)
            if cursor.rowcount != prev:
                isin.append('')
            else:
                isin.append(round((perf_result-1)*100,2))

        for next in (1, 3, 6, 12, 36, 60):
            perf_result = 1.0
            sub_query = u"""
                SELECT
                    performance
                FROM
                    t_fund_performance
                WHERE
                    isin_code = '%s'
                        AND perf_type = 'mthly_performance'
                        and months between %s and %s-1+%s
                        and performance <> ''
            """ % (isin[0], isin[1], isin[1], next)
            cursor.execute(sub_query)
            for (performance,) in cursor:
                perf_result = perf_result*(1+float(performance)/100)
            if cursor.rowcount != next:
                isin.append('')
            else:
                isin.append(round((perf_result-1)*100,2))

        logging.info("(%s/%s)\r" % (index+1, unicode(len(isin_list))))
        print isin

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "PERFORMANCE"
    ws_title = [
        "isin_code",
        "months",
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
        if isin[4] == '' and isin[5] == '' and isin[6] == '' and isin[7] == '' and isin[8] == '' and isin[9] == ''\
                 and isin[10] == '' and isin[11] == '' and isin[12] == '' and isin[13] == '' and isin[14] == ''\
                 and isin[15] == '' and isin[16] == '':
            pass
        else:
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
