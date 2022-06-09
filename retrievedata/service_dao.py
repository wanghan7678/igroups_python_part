import sys
import traceback

import sqlalchemy
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
    except Exception as err:
        logging.debug("Database operation exception: " + str(err))
        session.rollback()
        raise
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
        instance = session.query(stock.StockBasic).filter(stock.StockBasic.ts_code == item.ts_code)\
            .filter(stock.StockBasic.hash != item.hash).first()
        if instance:
            if instance.hash != item.hash:
                session.query(stock.StockBasic).filter(stock.StockBasic.ts_code == item.ts_code) \
                    .update({'name': item.name, 'area': item.area, 'industry': item.industry,
                             'en_name': item.en_name, 'market': item.market, 'exchange': item.exchange,
                             'list_status': item.list_status, 'is_hs': item.is_hs, 'hash': item.hash})
        else:
            add_one_item(item)


def get_stock_basic_all():
    with session_scope() as session:
        result = session.query(stock.StockBasic).all()
        return result
