from __future__ import unicode_literals, absolute_import

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base


ModelBase = declarative_base()


class StockBasic(ModelBase):
    __tablename__ = 'stock_basic'
    id = Column(Integer, primary_key=True)
    ts_code = Column(String(length=225))
    name = Column(String(length=225))
    area = Column(String(length=225))
    industry = Column(String(length=225))
    en_name = Column(String(length=225))
    market = Column(String(length=225))
    exchange = Column(String(length=225))
    list_status = Column(String(length=225))
    list_date = Column(DateTime)
    is_hs = Column(String(length=225))
    hash = Column(String(length=255))
    __table_args__ = {"mysql_charset": "utf8mb4"}


class StockDailyLine(ModelBase):
    __tablename__ = 'stock_day_line'
    id = Column(Integer, primary_key=True)
    ts_code = Column(String(length=225))
    trade_date = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    pre_close = Column(Float)
    change = Column(Float)
    pct_chg = Column(Float)
    vol = Column(Float)
    amount = Column(Float)


class StockSignals(ModelBase):
    __tablename__ = 'signals'
    id = Column(Integer, primary_key=True)
    ts_code = Column(String(length=225))
    trade_date = Column(DateTime)
    type_code = Column(Integer)
    status = Column(String(length=45))


class SignalType(ModelBase):
    __tablename__ = 'signal_type'
    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    name = Column(String(length=45))
    english_name = Column(String(length=45))
    direction = Column(Integer)
    priority = Column(Integer)
    description = Column(String(length=200))
    type = Column(String(length=45))


class Prediction(ModelBase):
    __tablename__ = 'prediction'
    id = Column(Integer, primary_key=True)
    ts_code = Column(String(length=45))
    predict_date = Column(DateTime)
    signal_code = Column(Integer)
    value_name = Column(String(length=45))
    predict_days = Column(Integer)
    algorithm_code = Column(Integer)
    predict_value = Column(Float)
    predict_score = Column(Float)
    score_method = Column(String(length=45))
    label_value = Column(Float)



class ExchangeCalendar(ModelBase):
    __tablename__ = 'exchange_calendar'
    id = Column(Integer, primary_key=True)
    exchange = Column(String(length=45))
    date = Column(DateTime)
    is_open = Column(Boolean)