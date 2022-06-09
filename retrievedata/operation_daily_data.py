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
