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
    __tablename__ = 'stock_daily_line'
    id = Column(Integer, primary_key=True)
    ts_code = Column(String(length=225))


class ExchangeCalendar(ModelBase):
    __tablename__ = 'exchange_calendar'
    id = Column(Integer, primary_key=True)
    exchange = Column(String(length=225))
    date = Column(DateTime)
    is_open = Column(Boolean)
