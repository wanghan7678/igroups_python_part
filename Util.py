import datetime

import numpy as np

import Config as Cfg
import hashlib


def to_float(input_number):
    a = 0
    if input is None:
        return 0
    if input == '-':
        return -1;
    else:
        try:
            a = float(np.nan_to_num(input_number))
        except Exception as err:
            print("input is %s" % str(input_number))
            print("number to float exception: %s" % str(err))
            a = -1
        return a


def to_int(input_number):
    a = 0
    if input is None:
        return 0
    else:
        try:
            a = int(np.nan_to_num(input_number))
        except Exception as err:
            print("input is %s" % str(input_number))
            print("number to int exception: %s" % str(err))
        return a


def to_std(input_number):
    array = np.array(input_number)
    array -= array.mean(axis=0)
    array /= array.std(axis=0)
    array = np.nan_to_num(array)
    return array


def cmplx_to_float(input_number):
    n = 1
    if input_number is None:
        return 0
    input_string = str(input_number)
    input_string = input_string.strip()
    if input_string.endswith('M'):
        n = 1000000
    if input_string.endswith('B'):
        n = 1000000000
    input_string = input_string.replace('M', '')
    input_string = input_string.replace('B', '')
    input_string = input_string.replace('$', '')
    r = to_float(input_string)
    return r * n


def get_today_datestr():
    dt = datetime.datetime.now().strftime(Cfg.CONSTANT.DATE_FORMAT_US)
    return dt


def date_cn2us(datestr):
    dt = datetime.datetime.strptime(datestr, Cfg.CONSTANT.DATE_FORMAT_CN)
    d = dt.strftime(Cfg.CONSTANT.DATE_FORMAT_US)
    return d


def date_us2cn(datestr):
    dt = datetime.datetime.strptime(datestr, Cfg.CONSTANT.DATE_FORMAT_US)
    d = dt.strftime(Cfg.CONSTANT.DATE_FORMAT_CN)
    return d


def date_yf2us(datestr):
    dt = datetime.datetime.strptime(datestr, Cfg.CONSTANT.DATE_FORMAT_YF)
    d = dt.strftime(Cfg.CONSTANT.DATE_FORMAT_US)
    return d


def int_to_bool(input_number):
    if input_number == 1:
        return True
    else:
        return False


def get_hash(input_texts):
    md5 = hashlib.md5()
    for text in input_texts:
        md5.update(text.encode('Utf-8'))
    return md5.hexdigest()
