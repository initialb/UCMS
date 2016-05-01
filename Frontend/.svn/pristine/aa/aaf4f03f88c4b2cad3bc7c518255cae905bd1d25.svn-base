# -*- coding: utf-8 -*-
"""
 zhangbo2012
 http://www.cnblogs.com/zhangbo2012/
"""

import time
import datetime
import random

filepath = "autoinclog"

def time2yyyymmddhhmiss():
    return datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

with open(filepath,'w') as wf:
    for i in range(150):
        time.sleep(1)
        linecnt = int(random.random()*20)
        for i in range(linecnt):
            ol = "%s|%04d|%04d|%04d\n" % (time2yyyymmddhhmiss(),int(random.random()*9999),int(random.random()*9999),i)
            wf.write(ol)
            print ol,
        wf.flush()