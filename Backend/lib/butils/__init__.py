# -*- coding: utf-8 -*-

import logging
import re
import pprint


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


def ppprint(obj):
    print re.sub(r"\\u([a-f0-9]{4})", lambda mg: unichr(int(mg.group(1), 16)), obj.__repr__())


def bs_preprocess(html):
    """remove distracting whitespaces and newline characters"""
    pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
    html = re.sub(pat, '', html)  # remove leading and trailing whitespaces
    html = re.sub('\n', ' ', html)  # convert newlines to spaces
    # this preserves newline delimiters
    html = re.sub('[\s]+<', '<', html)  # remove whitespaces before opening tags
    html = re.sub('>[\s]+', '>', html)  # remove whitespaces after closing tags
    return html


def get_sibling(element):
    """remove blank lines of a beautifulsoup instance"""
    sibling = element.next_sibling
    if sibling == "\n":
        return get_sibling(sibling)
    else:
        return sibling


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

