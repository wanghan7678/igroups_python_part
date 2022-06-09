import tushare as tu

import model_stock as stock
import Config as cfg
import Util


def get_tushare_api():
    token = cfg.CONSTANT.Tushare_Token
    tu.set_token(token)
    pro = tu.pro_api()
    return pro


def read_stockbasic():
    pro = get_tushare_api()
    data = pro.stock_basic(exchange='', list_status='L',
                           fields='ts_code, name, area, industry, enname, '
                                  'market, exchange, list_status, list_date, '
                                  'is_hs')
    if data.empty:
        print("stock basic list is empty.  tushare.")
    stocks = []
    for i in range(0, len(data)):
        item = stock.StockBasic()
        item.ts_code = data.iat[i, 0]
        item.name = data.iat[i, 1]
        item.area = data.iat[i, 2]
        item.industry = data.iat[i, 3]
        item.en_name = data.iat[i, 4]
        item.market = data.iat[i, 5]
        item.exchange = data.iat[i, 6]
        item.list_status = data.iat[i, 7]
        item.list_date = Util.date_cn2us(data.iat[i, 8])
        item.is_hs = data.iat[i, 9]
        item.hash = Util.get_hash([item.name, item.ts_code])
        stocks.append(item)
    return stocks


def read_stock_day_line(code, start, end):
    pro = get_tushare_api()
    print("read: " + str(code) + " from " + start + " to " + end)
    data = pro.daily(ts_code=code, start_date=start, end_date=end)
    if data.empty:
        print("stock daily line is empty.  tushare.")
    lines = []
    for i in range(0, len(data)):
        item = stock.StockDailyLine()
        item.ts_code = data.iat[i, 0]
        item.trade_date = Util.date_cn2us(data.iat[i, 1])
        item.open = Util.to_float(data.iat[i, 2])
        item.high = Util.to_float(data.iat[i, 3])
        item.low = Util.to_float(data.iat[i, 4])
        item.close = Util.to_float(data.iat[i, 5])
        item.pre_close = Util.to_float(data.iat[i, 6])
        item.change = Util.to_float(data.iat[i, 7])
        item.pct_chg = Util.to_float(data.iat[i, 8])
        item.vol = Util.to_float(data.iat[i, 9])
        item.amount = Util.to_float(data.iat[i, 10])
        lines.append(item)
    return lines


def read_stock_day_line_one(input_date):
    pro = get_tushare_api()
    data = pro.daily(date=input_date)
    if data.empty:
        print("stock daily line is empty.  date = " + input_date)
    lines = []
    for i in range(0, len(data)):
        item = stock.StockDailyLine()
        item.ts_code = data.iat[i, 0]
        item.trade_date = Util.date_cn2us(data.iat[i, 1])
        item.open = Util.to_float(data.iat[i, 2])
        item.high = Util.to_float(data.iat[i, 3])
        item.low = Util.to_float(data.iat[i, 4])
        item.close = Util.to_float(data.iat[i, 5])
        item.pre_close = Util.to_float(data.iat[i, 6])
        item.change = Util.to_float(data.iat[i, 7])
        item.pct_chg = Util.to_float(data.iat[i, 8])
        item.vol = Util.to_float(data.iat[i, 9])
        item.amount = Util.to_float(data.iat[i, 10])
        lines.append(item)
    return lines

def read_exchange_calendar():
    pro = get_tushare_api()
    data = pro.trade_cal(exchange='', start_date='20180101', end_date='20221231')
    if data.empty:
        print("stock basic list is empty.  tushare.")
    dates = []
    for i in range(0, len(data)):
        item = stock.ExchangeCalendar()
        item.exchange = data.iat[i, 0]
        item.date = Util.date_cn2us(data.iat[i, 1])
        item.is_open = Util.int_to_bool(data.iat[i, 2])
        dates.append(item)
    return dates