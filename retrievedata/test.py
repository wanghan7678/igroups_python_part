import sys

import operation_daily_data as op
import logging

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

op.update_stock_basic()
