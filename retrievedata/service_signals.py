import Util
import retrievedata.analyser_tech as tech
import retrievedata.model_stock as model


def calculate_ta_signals(ts_code, trade_date, data):
    tech_data = data[:12]
    signals = []
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


def calculate_trends_signals(ts_code, trade_date, data):
    signals = []
    tech_res = tech.ChartPatternsResolver(data)
    support_line = tech_res.support_line()
    resistance_line = tech_res.resistance_line()
    if support_line is None or len(support_line) < 4 :
        return signals
    if resistance_line is None or len(resistance_line) < 4:
        return signals
    if data[-1] < support_line[3]:
        signals.append(set_signal(ts_code, trade_date, tech.CHART_60_SUPPORT_DOWN))
    if data[-1] > resistance_line[3]:
        signals.append(set_signal(ts_code, trade_date, tech.CHART_60_RESISTANCE_UP))
    if - 0.05 < support_line[0] < 0.05 and - 0.05 < resistance_line[0] < 0.05:
        signals.append(set_signal(ts_code, trade_date, tech.CHART_RECTANGLE))
    if support_line[0] > 0.3 and abs((support_line[0] - resistance_line[0])/support_line[0]) < 0.05:
        signals.append(set_signal(ts_code, trade_date, tech.CHART_RISING_CHANEL))
    if support_line[0] < - 0.3 and abs((support_line[0] - resistance_line[0]) / support_line[0]) < 0.05:
        signals.append(set_signal(ts_code, trade_date, tech.CHART_DOWNWARD_CHANEL))
    if - 0.05 < resistance_line[0] < 0.05 and support_line[0] > 0.3 and abs(resistance_line[3] - support_line[3])/support_line[3] < 0.1:
        signals.append(set_signal(ts_code, trade_date, tech.CHART_TRIANGLE_ASCENDING))
    if - 0.05 < support_line[0] < 0.05 and resistance_line[0] < - 0.3 and abs(resistance_line[3] - support_line[3])/support_line[3] < 0.1:
        signals.append(set_signal(ts_code, trade_date, tech.CHART_TRIANGLE_DESCENDING))
    if support_line[0] > 0.3 and resistance_line[0] < - 0.3 and (support_line[0] - abs(resistance_line[0])/support_line[0] < 0.05) and abs(resistance_line[3] - support_line[3])/support_line[3] < 0.1:
        signals.append(set_signal(ts_code, trade_date, tech.CHART_TRIANGLE_SYMMETRICAL))
    start_part = abs((support_line[0] - resistance_line[0]) / support_line[0])
    end_part = abs((support_line[-1] - resistance_line[-1]) / support_line[-1])
    if start_part < 0.05 and end_part / start_part > 5:
        signals.append(set_signal(ts_code, trade_date, tech.CHART_TRIANGLE_ENLARGE))
    return signals


def set_signal(ts_code, trade_date, sig_code):
    sig = model.StockSignals()
    sig.ts_code = ts_code
    sig.trade_date = trade_date
    sig.type_code = sig_code
    sig.status = "new"
    return sig


def calculate_chart_reg_signals(ts_code, trade_date, back_days, data):
    signals = []
    chart_res = tech.ChartPatternsResolver(data)
    direction = chart_res.get_trend_direction()
    code = None
    if back_days == 5:
        if direction == tech.DIRECTION_UP:
            code = tech.CHART_5D_UPTREND
        if direction == tech.DIRECTION_DOWN:
            code = tech.CHART_5D_DOWNTREND
        if direction == tech.DIRECTION_HORIZON:
            code = tech.CHART_5D_HORIZONTAL
    if back_days == 10:
        if direction == tech.DIRECTION_UP:
            code = tech.CHART_10D_UPTREND
        if direction == tech.DIRECTION_DOWN:
            code = tech.CHART_10D_DOWNTREND
        if direction == tech.DIRECTION_HORIZON:
            code = tech.CHART_10D_HORIZONTAL
    if back_days == 20:
        if direction == tech.DIRECTION_UP:
            code = tech.CHART_20D_UPTREND
        if direction == tech.DIRECTION_DOWN:
            code = tech.CHART_20D_DOWNTREND
        if direction == tech.DIRECTION_HORIZON:
            code = tech.CHART_20D_HORIZONTAL
    if back_days == 60:
        if direction == tech.DIRECTION_UP:
            code = tech.CHART_60D_UPTREND
        if direction == tech.DIRECTION_DOWN:
            code = tech.CHART_60D_DOWNTREND
        if direction == tech.DIRECTION_HORIZON:
            code = tech.CHART_60D_HORIZONTAL
    if code is not None:
        sig = model.StockSignals()
        sig.ts_code = ts_code
        sig.trade_date = trade_date
        sig.type_code = code
        sig.status = "new"
        signals.append(sig)
    return signals
