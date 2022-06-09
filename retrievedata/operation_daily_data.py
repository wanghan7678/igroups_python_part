import service_dao as dao
import service_toshare as tu


def update_stock_basic():
    stocks_from_tushare = tu.read_stockbasic()
    for one_stock in stocks_from_tushare:
        dao.update_stock_basic(one_stock)


def load_all_stock_basic():
    stocks_from_tushare = tu.read_stockbasic()
    dao.add_stock_basic(stocks_from_tushare)


def load_exchange_calendar():
    days = tu.read_exchange_calendar()
    dao.add_item_list(days)


def load_stock_day_lines(start_date, end_date):
    stocks = dao.get_stock_tscode_all()
    for stock in stocks:
        lines = tu.read_stock_day_line(stock.ts_code, start_date, end_date)
        dao.add_item_list(lines)


def load_stock_day_lines_oneday(date):
    lines = tu.read_stock_day_line_one(date)
    dao.add_item_list(lines)
