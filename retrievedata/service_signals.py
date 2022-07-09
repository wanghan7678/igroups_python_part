import Util
import analyser_tech as tech
import service_dao as dao
import model_stock as model
import numpy as np

PREDICT_5D_REGRESSION = 10010


def calculate_ta_signals(ts_code, trade_date, data):
    tech_data = data[:12]
    signals = []
    print("cal signals: $code, $trade_date, $data: ", ts_code, trade_date, tech_data)
    if len(tech_data) < 12:
        return signals
    tech_res = tech.TechSignalResolver(tech_data)
    codes = tech_res.cal_signals()
    for code in codes:
        sig = model.StockSignals()
        sig.ts_code = ts_code
        sig.trade_date = Util.date_cn2us(trade_date)
        sig.type_code = code
        sig.status = "new"
        signals.append(sig)
    return signals


def calculate_chart_5d_regression(back_days, data):
    if len(data) < back_days:
        print("less than $back_days, only $size: ", back_days, len(data))
        return None
    return tech.ChartPatternsResolver(data).trend_line()


def calculate_chart_signals(ts_code, trade_date, chart_reg):
    signals = []
    if chart_reg is None:
        return signals
    chart_res = tech.ChartPatternsResolver(None)
    trends = chart_res.get_trend(chart_reg)
    if trends is not None:
        sig = model.StockSignals()
        sig.ts_code = ts_code
        sig.trade_date = trade_date
        sig.type_code = trends
        sig.status = "new"
        signals.append(sig)
    return signals
