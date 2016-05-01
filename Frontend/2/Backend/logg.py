# -*- coding: utf-8 -*-

import time
import datetime
import subprocess


filepath = "autoinclog"
delaysec = 5
nowrectime='9999999999'

seccnt = {}
timepos = 0

def time2yyyymmddhhmiss():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def yyyymmddhhmiss2time(yyyymmddhhmiss):
    return time.mktime(time.strptime(yyyymmddhhmiss,'%Y%m%d%H%M%S'))

f = subprocess.Popen(['tail','-F',filepath], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
while True:
    line = f.stdout.readline()
    rectime = filter(str.isdigit, line[0:19])
    if nowrectime<rectime:
        print nowrectime,seccnt[nowrectime]

    while (time.time() - yyyymmddhhmiss2time(rectime) < delaysec):
        time.sleep(1)

    if rectime in seccnt.keys():
        seccnt[rectime] +=1
    else:
        seccnt[rectime] = 1

    nowrectime = rectime
