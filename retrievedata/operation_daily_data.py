import service_dao as dao
import service_toshare as tu
import service_signals as sig
import service_predict as predict

back_days = 5

def update_stock_basic():
    stocks_from_tushare = tu.read_stockbasic()
    for one_stock in stocks_from_tushare:
        dao.update_stock_basic(one_stock)


def load_all_stock_basic():
    stocks_from_tushare = tu.read_stockbasic()
    dao.add_stock_basic(stocks_from_tushare)


def load_exchange_calendar(start_d, end_d):
    days = tu.read_exchange_calendar(start_d, end_d)
    dao.add_item_list(days)


def load_stock_day_lines(start_date, end_date):
    stocks = dao.get_stock_tscode_all()
    for stock in stocks:
        lines = tu.read_stock_day_line(stock.ts_code, start_date, end_date)
        dao.add_item_list(lines)


def load_stock_day_lines_oneday(date):
    lines = tu.read_stock_day_line_one(date)
    dao.add_item_list(lines)


def load_ta_signals_oneday(date):
    ts_codes = dao.get_tscode_day_lines_one_day(date)
    for code in ts_codes:
        tsc = code[0]
        print(tsc)
        rs = dao.get_day_lines_4prices(tsc, date, 3)
        data = []
        for row in rs:
            data.append(row[0])
            data.append(row[1])
            data.append(row[2])
            data.append(row[3])
        sigs = sig.calculate_ta_signals(tsc, date, data)
        dao.add_item_list(sigs)


def load_chart_signals_oneday(date):
    ts_codes = dao.get_tscode_day_lines_one_day(date)
    for code in ts_codes:
        tsc = code[0]
        rs = dao.get_day_lines_close(tsc, date, back_days)
        data = []
        for row in rs:
            data.append(row[0])
        regs = sig.calculate_chart_5d_regression(back_days, data)
        sigs = sig.calculate_chart_signals(tsc, date, regs)
        preds = predict.calculate_5d_regression(tsc, date, regs)
        print("load sigs and predicts: $ts_code, $date, $line: ", tsc, date, regs)
        dao.add_item_list(sigs)
        dao.add_item_list(preds)


