import sys

import operation_daily_data as op
import logging

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


op.load_stock_day_lines('20220101', '20220608')
