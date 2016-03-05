# -*- coding: utf-8 -*-

import butils


def tenor_decoder(tenor_desc):
    result = butils.decode(tenor_desc,
                           u'1个月', '30',
                           u'2个月', '60',
                           u'3个月', '90',
                           u'6个月', '180',
                           u'9个月', '270',
                           u'12个月', '360',
                           u'半年', '180',
                           u'1年', '360',
                           u'一年', '360',
                           u'2年', '720',
                           u'二年', '720',
                           u'3年', '1080',
                           u'三年', '1080',
                           u'5年', '1800',
                           u'五年', '1800',
                           '')
    return result


def currency_decoder(tenor_desc):
    result = butils.decode(tenor_desc,
                           u'美元', 'USD',
                           u'澳元', 'AUD',
                           u'欧元', 'EUR',
                           u'英镑', 'GBP',
                           '')
    return result