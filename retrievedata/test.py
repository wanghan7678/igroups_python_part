import sys

import numpy as np

import Config as cfg
import tushare as tu
import operation_daily_data as op
import logging
import analyser_tech as tch
import service_toshare as stu
import os

# logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

# load exchange calendar
# op.load_exchange_calendar('20200101', '20221231')

# load all stock basic information
# op.load_all_stock_basic()

# check the updates every day:
# op.update_stock_basic()

# read the day line data:
# op.load_stock_day_lines_oneday('20220624')

# calculate the signals:
# op.load_chart_signals_oneday('20220708')

# op.load_chart_signals_oneday('2022-09-16')

pro = stu.get_tushare_api()

# df = pro.index_classify(level='L2', src='SW2021')
df = pro.index_member(index_code='801230.SI', is_new='Y')

print(df)