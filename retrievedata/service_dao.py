import sys
import traceback

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.sql import func

import model_stock as stock
import Config as Cfg
import logging

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def get_session():
    engine = sqlalchemy.create_engine(Cfg.CONSTANT.Database_Url, poolclass=sqlalchemy.pool.NullPool, echo=False)
    dbsession = sessionmaker(bind=engine)
    session = dbsession()
    return session


@contextmanager
def session_scope():
    session = get_session()
    try:
        yield session
        session.commit()
    except IntegrityError as integrity_err:
        logging.debug("Data base integrity exception: " + str(integrity_err))
        print("Data base integrity exception: " + str(integrity_err))
    finally:
        session.close()


def add_item_list(item_list):
    if item_list is None:
        logging.debug("input list is None")
        return
    with session_scope() as session:
        for item in item_list:
            session.add(item)


def add_one_item(item):
    if item is None:
        logging.debug("input item is None")
        return
    with session_scope() as session:
        session.add(item)


def add_stock_basic(items):
    logging.debug("Insert Stock Basic Items...")
    add_item_list(items)
    logging.debug("Finished the insert")


def update_stock_basic(item):
    logging.debug("update item...")
    with session_scope() as session:
        instance = session.query(stock.StockBasic).filter(stock.StockBasic.ts_code == item.ts_code).first()
        if instance:
            if instance.hash != item.hash:
                session.query(stock.StockBasic).filter(stock.StockBasic.ts_code == item.ts_code) \
                    .update({'name': item.name, 'area': item.area, 'industry': item.industry,
                             'en_name': item.en_name, 'market': item.market, 'exchange': item.exchange,
                             'list_status': item.list_status, 'is_hs': item.is_hs, 'hash': item.hash})
        else:
            add_one_item(item)


def update_stock_day_line(item):
    logging.debug("update day line...")
    with session_scope() as session:
        instance = session.query(stock.StockDailyLine).filter(stock.StockDailyLine.ts_code == item.ts_code).first()
        if instance:
            if instance.close != item.close:
                session.query(stock.StockDailyLine).filter(stock.StockDailyLine.ts_code == item.ts_code) \
                    .update({'trade_date': item.trade_date, 'open': item.open, 'high': item.high,
                             'low': item.low, 'close': item.close, 'pre_close': item.pre_close,
                             'change': item.change, 'pct_chg': item.pct_chg, 'vol': item.vol,
                             'amount': item.amount})
        else:
            add_one_item(item)


def get_stock_basic_all():
    logging.debug("get all recorded stocks")
    with session_scope() as session:
        result = session.query(stock.StockBasic).all()
        return result


def get_stock_tscode_all():
    logging.debug("get all recorded tscode")
    with session_scope() as session:
        result = session.query(stock.StockBasic.ts_code).all()
        return result


def get_day_lines_close(ts_code, trade_date, back_days):
    logging.debug("get last $days from $today: ", back_days, trade_date)
    with session_scope() as session:
        result = session.query(stock.StockDailyLine.close).filter(stock.StockDailyLine.ts_code == ts_code).filter(
            stock.StockDailyLine.trade_date <= trade_date).order_by(stock.StockDailyLine.trade_date.desc()).limit(
            back_days).all()
        return result


def get_day_lines_4prices(ts_code, trade_date, back_days):
    logging.debug("get last $days from $today: ", back_days, trade_date)
    with session_scope() as session:
        result = session.query(stock.StockDailyLine.close, stock.StockDailyLine.open, stock.StockDailyLine.high, stock.StockDailyLine.low).filter(stock.StockDailyLine.ts_code == ts_code).filter(
            stock.StockDailyLine.trade_date <= trade_date).order_by(stock.StockDailyLine.trade_date.desc()).limit(
            back_days).all()
        return result


def get_stock_day_lines_one_day(trade_date):
    logging.debug("get all day line data for $today: ", trade_date)
    with session_scope() as session:
        result = session.query(stock.StockDailyLine).filter(
            stock.StockDailyLine.trade_date == trade_date).all()
        return result


def get_tscode_day_lines_one_day(trade_date):
    logging.debug("get all day line data for $today: ", trade_date)
    with session_scope() as session:
        result = session.query(stock.StockDailyLine.ts_code).filter(
            stock.StockDailyLine.trade_date == trade_date).all()
        return result
