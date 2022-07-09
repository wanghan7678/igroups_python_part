import numpy as np
from sklearn.linear_model import LinearRegression

TECH_BULLISH_WHITE = 10010
TECH_BEARISH_BLACK = 10020
TECH_DOJI = 10030
TECH_LONG_LEGGED_DOJI = 10040
TECH_GRAVESTONE_DOJI = 10050
TECH_SPINNING_TOP = 10060
TECH_SHOOTING_STAR = 10070
TECH_HANGING_MAN = 10080
TECH_PIERCING = 10090
TECH_DARK_CLOUD_COVER = 10100
TECH_HARAMI_CROSS = 10110
TECH_HARAMI = 10120
TECH_TWO_BLACK_CROWS = 10130
TECH_BEARISH_ENFULFING = 10140
TECH_BULLISH_ENGULFING = 10150
TECH_MORNING_STAR = 10160
TECH_EVENING_STAR = 10170
TECH_THREE_WHITE_SOLDIERS = 10180
TECH_THREE_BLACK_CROWS = 10190

CHART_5D_UPTREND = 20010
CHART_5D_DOWNTREND = 20020
CHART_5D_HORIZONTAL = 20030
CHART_5D_REG = 20040

CHART_GAP = 20050


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
        self.pre2_low = data[7]

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

    def cal_signals(self):
        signals = []
        if self.if_bullish_white():
            signals.append(TECH_BULLISH_WHITE)
        if self.if_bearish_black():
            signals.append(TECH_BEARISH_BLACK)
        if self.if_doji():
            signals.append(TECH_DOJI)
        if self.if_long_legged_doji():
            signals.append(TECH_LONG_LEGGED_DOJI)
        if self.if_gravestone_doji():
            signals.append(TECH_GRAVESTONE_DOJI)
        if self.if_shooting_star():
            signals.append(TECH_SHOOTING_STAR)
        if self.if_hanging_man():
            signals.append(TECH_HANGING_MAN)
        if self.if_piercing_line():
            signals.append(TECH_PIERCING)
        if self.if_dark_cloud_cover():
            signals.append(TECH_DARK_CLOUD_COVER)
        if self.if_harami_cross():
            signals.append(TECH_HARAMI_CROSS)
        if self.if_harami():
            signals.append(TECH_HARAMI)
        if self.if_tow_black_crows():
            signals.append(TECH_TWO_BLACK_CROWS)
        if self.if_bearish_engulfing():
            signals.append(TECH_BEARISH_ENFULFING)
        if self.if_bullish_engulfing():
            signals.append(TECH_BULLISH_ENGULFING)
        if self.if_morning_star():
            signals.append(TECH_MORNING_STAR)
        if self.if_evening_star():
            signals.append(TECH_EVENING_STAR)
        if self.if_three_white_soldiers():
            signals.append(TECH_THREE_WHITE_SOLDIERS)
        if self.if_three_black_crows():
            signals.append(TECH_THREE_BLACK_CROWS)
        return signals


class ChartPatternsResolver:
    R_THRESHOLD = 0.7

    def __init__(self, data):
        self.close = data

    def trend_line(self):
        x = np.arange(len(self.close)).reshape(len(self.close), 1)
        model = LinearRegression()
        reg = model.fit(x, self.close)
        score = reg.score(x, self.close)
        pred = reg.predict([[len(self.close) + 1]])
        return [score, model.coef_[0], pred[0]]

    def get_trend(self):
        result = self.trend_line()
        if result[0] > self.R_THRESHOLD:
            if result[1] > 0.3:
                return CHART_5D_UPTREND
            elif result[1] < - 0.3:
                return CHART_5D_DOWNTREND
            else:
                return CHART_5D_HORIZONTAL
        return None

    def get_trend(self, result):
        if result is not None and len(result) > 2 and result[0] > self.R_THRESHOLD:
            if result[1] > 0.3:
                return CHART_5D_UPTREND
            elif result[1] < - 0.3:
                return CHART_5D_DOWNTREND
            else:
                return CHART_5D_HORIZONTAL
        return None
