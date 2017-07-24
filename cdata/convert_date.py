# -*- coding: utf-8 -*-
import os
import sys
import json
import logging
import codecs
import hashlib
import datetime
import logging
import time
import argparse
import re
import libfile
from misc import main_subtask

reload(sys)
sys.setdefaultencoding('utf-8')
VERSION = 'v20170721'



def check_excel(date):
    __s_date = datetime.date(1899, 12, 31).toordinal()-1
    if date.isdigit():
        date = int(date)
        d = datetime.date.fromordinal(__s_date + date)
        return d.strftime("%Y-%m-%d")
    return date

def date_confirm(norm_date):
    if len(norm_date.split("-")) !=3:
        date_list = norm_date.split("-")
        norm_date_v2 = "-".join(date_list[:3])
    else:
        norm_date_v2 = norm_date
    try:
        clean_date = datetime.datetime.strptime(norm_date_v2, "%Y-%m-%d").strftime('%Y-%m-%d')
        return clean_date
    except  Exception as err :
        logging.warn(u"It's a illgeal date type ")
        logging.warn(norm_date)
        logging.warn(err)
        return None

def validate_date(str_date):
    str_date = check_excel(str_date)
    str_date = str_date.strip()
    str_date = str_date.replace(u' ', '')
    if len(str_date) ==0 :
        return None
    str_date = codecs.decode(str_date,'utf-8')
    zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
    norm_date = re.sub(ur"[\.-]","-",str_date)
    norm_date = re.sub(u",","-",norm_date)
    norm_date = re.sub(u"/","-",norm_date)
    norm_date = re.sub(u"--","-",norm_date)
    match = zh_pattern.search(norm_date)
    zh_pattern2 = re.compile(u'^[\u4e00-\u9fa5]+')
    if zh_pattern2.search(norm_date):
        norm_date = re.sub(ur"[\u4e00-\u9fa5]",'-', norm_date)[1:-1]
    elif match :
        norm_date = re.sub(ur"[\u4e00-\u9fa5]",'-', norm_date)[0:-1]
    norm_date = norm_date.strip()
    return date_confirm(norm_date)

def test_date():

    str_date = u'2016-3-4'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'2016,3-4'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'2016/3/4'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'2016-3.4'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'2016-03-4'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'2016-3-04'
    assert '2016-03-04' == validate_date(str_date)
    #
    str_date = u'2016年3月4日'
    assert '2016-03-04' == validate_date(str_date)
    #
    str_date = u'2016年03月04日'
    assert '2016-03-04' == validate_date(str_date)
    #
    str_date = u'2016年3月04日'
    assert '2016-03-04' == validate_date(str_date)
    #
    str_date = u'2016年3月4日--7日'
    assert '2016-03-04' == validate_date(str_date)
    #
    str_date = u'2016年3月4-7日'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'2016年3月4至7日'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'2016年3月04,07日'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'2016年3月04---07日'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'2016年3月04到07'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'2016年3月4到07'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'2016-03-4至2016-03-05'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'从2016年3月4日起'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'从2016年3月4日到23日'
    assert '2016-03-04' == validate_date(str_date)

    str_date = u'自2016年3月4日起至23日'
    assert '2016-03-04' == validate_date(str_date)



if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s][%(asctime)s][%(module)s][%(funcName)s][%(lineno)s] %(message)s', level=logging.DEBUG)  # noqa
    main_subtask(__name__)

    '''
    python cdata/convert_date.py test_date
    '''
