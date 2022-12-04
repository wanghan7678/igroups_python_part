import sys

import numpy as np
from sklearn.linear_model import LinearRegression

TRENDLINE_INTERV = 10

RESISTENCE_LINE_DAYS = 60
SUPPORT_LINE_DAYS = 60

CANDLE_BULLISH_WHITE = 10010
CANDLE_BEARISH_BLACK = 10020
CANDLE_DOJI = 10030
CANDLE_LONG_LEGGED_DOJI = 10040
CANDLE_GRAVESTONE_DOJI = 10050
CANDLE_SPINNING_TOP = 10060
CANDLE_SHOOTING_STAR = 10070
CANDLE_HANGING_MAN = 10080
CANDLE_PIERCING = 10090
CANDLE_DARK_CLOUD_COVER = 10100
CANDLE_HARAMI_CROSS = 10110
CANDLE_HARAMI = 10120
CANDLE_TWO_BLACK_CROWS = 10130
CANDLE_BEARISH_ENFULFING = 10140
CANDLE_BULLISH_ENGULFING = 10150
CANDLE_MORNING_STAR = 10160
CANDLE_EVENING_STAR = 10170
CANDLE_THREE_WHITE_SOLDIERS = 10180
CANDLE_THREE_BLACK_CROWS = 10190

CANDLE_GAP_UP = 10200
CANDLE_GAP_DOWN = 10210

CHART_5D_UPTREND = 20010
CHART_5D_DOWNTREND = 20020
CHART_5D_HORIZONTAL = 20030
CHART_5D_REG = 20040

CHART_10D_UPTREND = 20050
CHART_10D_DOWNTREND = 20060
CHART_10D_HORIZONTAL = 20070
CHART_10D_REG = 20080

CHART_20D_UPTREND = 20090
CHART_20D_DOWNTREND = 20100
CHART_20D_HORIZONTAL = 20110
CHART_20D_REG = 20120

CHART_60D_UPTREND = 20130
CHART_60D_DOWNTREND = 20140
CHART_60D_HORIZONTAL = 20150
CHART_60D_REG = 20160

CHART_60_RESISTANCE_UP = 21100
CHART_60_SUPPORT_DOWN = 21110

CHART_RECTANGLE = 22100
CHART_RISING_CHANEL = 22110
CHART_DOWNWARD_CHANEL = 22120
CHART_TRIANGLE = 22130
CHART_TRIANGLE_ASCENDING = 22140
CHART_TRIANGLE_DESCENDING = 22150
CHART_TRIANGLE_SYMMETRICAL = 22160
CHART_TRIANGLE_ENLARGE = 22170

DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_HORIZON = 3


class TechSignalResolver:
    THRESHOLD = 0.02

    def __init__(self, data):
        self.close = data[0]
        self.open = data[1]
        self.high = data[2]
        self.low = data[3]
        self.pre_close = data[4]
        self.pre_open = data[5]
        self.pre_high = data[6]
        self.pre_low = data[7]
        self.pre2_close = data[8]
        self.pre2_open = data[9]
        self.pre2_high = data[10]
        self.pre2_low = data[11]

    def if_bullish_white(self):
        ratio = (self.high - self.low) / self.low
        return self.high == self.close and self.open == self.low and ratio >= self.THRESHOLD

    def if_bearish_black(self):
        ratio = (self.open - self.close) / self.open
        return self.open == self.high and self.close == self.low and ratio >= self.THRESHOLD

    def if_doji(self):
        return self.open == self.close

    def if_long_legged_doji(self):
        ratio1 = (self.close - self.low) / self.low
        ratio2 = (self.high - self.open) / self.open
        return self.open == self.close and (ratio1 >= self.THRESHOLD or ratio2 >= self.THRESHOLD)

    def if_gravestone_doji(self):
        ratio = (self.high - self.close) / self.close
        return self.open == self.close and self.close == self.low and ratio >= self.THRESHOLD

    def if_dragonfly_doji(self):
        ratio = (self.close - self.low) / self.close
        return self.open == self.close and self.open == self.high and ratio >= self.THRESHOLD

    def if_spinning_top(self):
        if self.close > self.open:
            arm = self.high - self.close
            leg = self.open - self.low
            body = self.close - self.open
        else:
            arm = self.high - self.open
            leg = self.close - self.low
            body = self.open - self.close
        return arm == leg and (arm / body) > 1

    def if_shooting_star(self):
        if self.close > self.open:
            arm = self.high - self.close
            leg = self.open - self.low
            body = self.close - self.open
        else:
            arm = self.high - self.open
            leg = self.close - self.low
            body = self.open - self.close
        if leg == 0 and body > 0:
            return (arm / body) > self.THRESHOLD
        if leg == 0 and body == 0:
            return arm > 0
        if leg > 0 and body == 0:
            return arm / leg > self.THRESHOLD
        return (arm / body) > self.THRESHOLD and (body / leg) > self.THRESHOLD

    def if_hanging_man(self):
        if self.close > self.open:
            arm = self.high - self.close
            leg = self.open - self.low
            body = self.close - self.open
        else:
            arm = self.high - self.open
            leg = self.close - self.low
            body = self.open - self.close
        if arm == 0 and body > 0:
            return (leg / body) > 2
        if arm > 0 and body == 0:
            return leg / arm > self.THRESHOLD
        if arm == 0 and body == 0:
            return leg > 0
        return (leg / body) > 2 and (body / arm) > 2

    def _if_big_yin(self, close_price, open_price, high_price, low_price):
        ratio = (open_price - close_price) / close_price
        body = open_price - close_price
        arm = high_price - open_price
        leg = close_price - low_price
        if arm == 0 or leg == 0:
            return ratio > self.THRESHOLD
        return body > 0 and (arm == 0 or body / arm > self.THRESHOLD) and (
                leg == 0 or body / leg > self.THRESHOLD) and ratio > self.THRESHOLD

    def _if_big_yang(self, close_price, open_price, high_price, low_price):
        ratio = (close_price - open_price) / open_price
        body = close_price - open_price
        arm = high_price - close_price
        leg = open_price - low_price
        if arm == 0 or leg == 0:
            return ratio > self.THRESHOLD
        return body > 0 and (arm == 0 or body / arm > self.THRESHOLD) and (
                leg == 0 or body / leg > self.THRESHOLD) and ratio > self.THRESHOLD

    def if_piercing_line(self):
        pre_mid = (self.pre_open + self.pre_close) / 2
        return self._if_big_yin(self.pre_close, self.pre_open, self.pre_high, self.pre_low) and self._if_big_yang(
            self.close, self.open, self.high, self.low) and self.close > pre_mid

    def if_dark_cloud_cover(self):
        pre_mid = (self.pre_close - self.pre_open) / 2
        return self._if_big_yang(self.pre_close, self.pre_open, self.pre_high, self.pre_low) and self._if_big_yin(
            self.close, self.open, self.high, self.low) and self.close < pre_mid

    def if_harami_cross(self):
        if self._if_big_yang(self.pre_close, self.pre_open, self.pre_high, self.pre_low):
            return self.if_doji() and self.high < self.pre_close and self.low > self.pre_open
        elif self._if_big_yin(self.pre_close, self.pre_open, self.pre_high, self.pre_low):
            return self.if_doji() and self.high < self.pre_open and self.low > self.pre_close
        else:
            return False

    def if_harami(self):
        body = self.open - self.close
        pre_body = self.pre_open - self.pre_close
        if pre_body == 0:
            return False
        ratio = abs(body) / abs(pre_body)
        if body > 0 and pre_body > 0:
            return self.pre_open > self.open and self.close > self.pre_close and ratio > self.THRESHOLD
        elif body > 0:
            return self.pre_open > self.close and self.open > self.pre_close and ratio > self.THRESHOLD
        elif pre_body > 0:
            return self.pre_close > self.open and self.close > self.pre_open and ratio > self.THRESHOLD
        else:
            return self.pre_close > self.close and self.open > self.pre_open and ratio > self.THRESHOLD

    def if_tow_black_crows(self):
        body = self.open - self.close
        pre_body = self.pre_open - self.pre_close
        return body > 0 and pre_body > 0 and self.open > self.pre_open and self.pre_close > self.close

    def if_bearish_engulfing(self):
        if self._if_big_yin(self.close, self.open, self.high, self.low):
            if self.pre_open > self.pre_close:
                return self.open > self.pre_open and self.pre_close > self.close
            else:
                return self.pre_close > self.open and self.close > self.pre_open
        return False

    def if_bullish_engulfing(self):
        if self._if_big_yang(self.close, self.open, self.high, self.low):
            if self.pre_open > self.pre_close:
                return self.close > self.pre_open and self.pre_close > self.open
            else:
                return self.close > self.pre_close and self.pre_open > self.open

    def if_morning_star(self):
        if self._if_big_yang(self.close, self.open, self.high, self.low) and self._if_big_yin(self.pre2_close,
                                                                                              self.pre2_open,
                                                                                              self.pre2_high,
                                                                                              self.pre2_low):
            return self.pre2_close > self.pre_close and self.pre2_close > self.pre_open and self.close > (
                    self.pre2_close + self.pre2_open) / 2
        return False

    def if_evening_star(self):
        if self._if_big_yang(self.pre2_close, self.pre2_open, self.pre_high, self.pre_low) and self._if_big_yin(
                self.close, self.open, self.high, self.low):
            return self.pre_open > self.pre2_close and self.pre_close > self.pre2_close and self.close < (
                    self.pre2_open + self.pre2_close) / 2

    def if_three_white_soldiers(self):
        if self._if_big_yang(self.close, self.open, self.high, self.low) and self._if_big_yang(self.pre_close,
                                                                                               self.pre_open,
                                                                                               self.pre_high,
                                                                                               self.pre_low) and self._if_big_yang(
            self.pre2_close, self.pre2_open, self.pre2_high, self.pre2_low):
            body1 = self.close - self.open
            body2 = self.pre_close - self.pre_open
            body3 = self.pre2_close - self.pre2_open
            return body3 > body2 > body1 and self.close > self.pre_close > self.open > self.pre_open and self.pre_close > self.pre2_close > self.pre_open > self.pre2_open
        return False

    def if_three_black_crows(self):
        if self._if_big_yin(self.close, self.open, self.high, self.open) and self._if_big_yin(self.pre_close,
                                                                                              self.pre_open,
                                                                                              self.pre_high,
                                                                                              self.pre_open) and self._if_big_yin(
            self.pre2_close, self.pre2_open, self.pre2_high, self.pre2_open):
            body1 = self.open - self.close
            body2 = self.pre_open - self.pre_close
            body3 = self.pre2_open - self.pre2_close
            return body1 > body2 > body3 and self.pre2_open > self.pre_open > self.pre2_close > self.pre_close and self.pre_open > self.open > self.pre_close > self.close
        return False

    def if_gap_up(self):
        return self.low > self.pre_high

    def if_gap_down(self):
        return self.high < self.pre_low

    def cal_signals(self):
        signals = []
        if self.if_bullish_white():
            signals.append(CANDLE_BULLISH_WHITE)
        if self.if_bearish_black():
            signals.append(CANDLE_BEARISH_BLACK)
        if self.if_doji():
            signals.append(CANDLE_DOJI)
        if self.if_long_legged_doji():
            signals.append(CANDLE_LONG_LEGGED_DOJI)
        if self.if_gravestone_doji():
            signals.append(CANDLE_GRAVESTONE_DOJI)
        if self.if_shooting_star():
            signals.append(CANDLE_SHOOTING_STAR)
        if self.if_hanging_man():
            signals.append(CANDLE_HANGING_MAN)
        if self.if_piercing_line():
            signals.append(CANDLE_PIERCING)
        if self.if_dark_cloud_cover():
            signals.append(CANDLE_DARK_CLOUD_COVER)
        if self.if_harami_cross():
            signals.append(CANDLE_HARAMI_CROSS)
        if self.if_harami():
            signals.append(CANDLE_HARAMI)
        if self.if_tow_black_crows():
            signals.append(CANDLE_TWO_BLACK_CROWS)
        if self.if_bearish_engulfing():
            signals.append(CANDLE_BEARISH_ENFULFING)
        if self.if_bullish_engulfing():
            signals.append(CANDLE_BULLISH_ENGULFING)
        if self.if_morning_star():
            signals.append(CANDLE_MORNING_STAR)
        if self.if_evening_star():
            signals.append(CANDLE_EVENING_STAR)
        if self.if_three_white_soldiers():
            signals.append(CANDLE_THREE_WHITE_SOLDIERS)
        if self.if_three_black_crows():
            signals.append(CANDLE_THREE_BLACK_CROWS)
        if self.if_gap_up():
            signals.append(CANDLE_GAP_UP)
        if self.if_gap_down():
            signals.append(CANDLE_GAP_DOWN)
        return signals


def _linear_regression(part):
    x = np.arange(len(part)).reshape(len(part), 1)
    model = LinearRegression()
    reg = model.fit(x, part)
    score = reg.score(x, part)
    pred = reg.predict([[len(part) + 1]])
    return [score, model.coef_[0], pred[0]]


class ChartPatternsResolver:
    R_THRESHOLD = 0.7

    def __init__(self, data):
        self.close = data

    def trend_line(self):
        return _linear_regression(self.close)

    # resistance line: the line created by the highest and the 2nd highest.
    #   2nd highest must be at least 10 days far away.
    def resistance_line(self):
        if len(self.close) < 60:
            print('close is less than 60')
            return None
        c = self.close[0:-1]
        a = np.array(c)
        c2 = []
        y1 = np.max(a)
        x1 = np.argmax(a)
        if x1 + (TRENDLINE_INTERV + 1) < len(c) and x1 - TRENDLINE_INTERV > 0:
            c2 = c[0:(x1 - TRENDLINE_INTERV)] + ([0] * (2 * TRENDLINE_INTERV + 1)) + c[x1 + TRENDLINE_INTERV + 1:]
        elif x1 - TRENDLINE_INTERV > 0:
            n = len(c) - (x1 - TRENDLINE_INTERV)
            c2 = c[0:(x1 - TRENDLINE_INTERV)] + [0] * n
        elif x1 + (TRENDLINE_INTERV + 1) < len(c):
            c2 = [0] * (x1 + TRENDLINE_INTERV + 1) + c[x1 + (TRENDLINE_INTERV + 1):]
        a2 = np.array(c2)
        y2 = np.max(a2)
        x2 = np.argmax(a2)
        # y2 = np.sort(a)[-2]
        # x2 = np.argsort(a)[-2]
        if x1 == x2:
            return y1
        coef = (y1 - y2) / (x1 - x2)
        b = y1 - coef * x1
        # return [coef, b, x(n+1), y(n+1)]
        return [coef, b, len(c), len(c) * coef + b]

    # support line: the line created by the lowest and the 2nd lowest.
    def support_line(self):
        print(self.close)
        if self.close is not None and len(self.close) < 60:
            return None
        c = self.close[0:-1]
        a = np.array(c)
        c2 = []
        y1 = np.min(a)
        x1 = np.argmin(a)
        if x1 + (TRENDLINE_INTERV + 1) < len(c) and x1 - TRENDLINE_INTERV > 0:
            c2 = c[0:(x1 - TRENDLINE_INTERV)] + ([sys.maxsize] * (2 * TRENDLINE_INTERV + 1)) + c[
                                                                                               x1 + TRENDLINE_INTERV + 1:]
        elif x1 - TRENDLINE_INTERV > 0:
            n = len(c) - (x1 - TRENDLINE_INTERV)
            c2 = c[0:(x1 - TRENDLINE_INTERV)] + [sys.maxsize] * n
        elif x1 + (TRENDLINE_INTERV + 1) < len(c):
            c2 = [sys.maxsize] * (x1 + TRENDLINE_INTERV + 1) + c[x1 + (TRENDLINE_INTERV + 1):]
        a2 = np.array(c2)
        y2 = np.min(a2)
        x2 = np.argmin(a2)
        if x1 == x2:
            return y1
        coef = (y1 - y2) / (x1 - x2)
        b = y1 - coef * x1
        # return [coef, b, x(n+1), y(n+1)]
        return [coef, b, len(c), len(c) * coef + b]

    def get_trend_direction(self):
        result = self.trend_line()
        if result[0] > self.R_THRESHOLD:
            if result[1] > 0.3:
                return DIRECTION_UP
            elif result[1] < - 0.3:
                return DIRECTION_DOWN
            else:
                return DIRECTION_HORIZON
        return -1
