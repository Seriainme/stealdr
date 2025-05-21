# encoding:utf-8
import os
import threading
import logging
import tomli
import inspect
import pymongo
from loguru import logger
from pathlib import Path


class MongoHandler(logging.Handler):
    # 单例模式，确保每次实例化都调用一个对象。
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(MongoHandler, "_instance"):
            with MongoHandler._instance_lock:
                MongoHandler._instance = object.__new__(cls)
                return MongoHandler._instance

        return MongoHandler._instance

    def __init__(self, client, db=None, collection=None):
        super().__init__()
        self.client = client
        self.db = db
        self.collection = collection

    def emit(self, record):
        log_record = {
            "level": record.levelname,
            "timestamp": record.created,
            "message": self.format(record),
            "file": record.filename,
            "line": record.lineno,
        }
        if not self.db:
            self.db = record.extra.get("db")
        if not self.collection:
            self.collection = record.extra.get("collection")
        self.client[self.db][self.collection].insert_one(log_record)


class MongoLog(MongoHandler):
    def __init__(self):
        # toml_config_dict
        td = tomli.loads(Path('pyproject.toml').read_text())
        m_user = td["MONGODB_USER"]
        m_pwd = td["MONGODB_PASSWORD"]
        m_host = td["MONGODB_HOST"]
        m_port = td["MONGODB_PORT"]
        m_db = td["MONGODB_DATABASE"]

        # 根据文件的名称确认集合的名称，如b.py继承这个class ，那么集合名为log_b
        collection = 'log_' + os.path.basename(inspect.stack()[1].filename).split(".")[0]
        client = pymongo.MongoClient(f'mongodb://{m_user}:{m_pwd}@{m_host}:{m_port}/{m_db}')
        super().__init__(client, m_db, collection)
        logger.add(self)
        self.log = logger

    def __call__(self, *args, **kwargs):
        return self.log
