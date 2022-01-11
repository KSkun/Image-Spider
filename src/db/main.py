import logging

from pymongo import MongoClient
from redis.client import Redis

from config import C

_mongo_client = None
_mongo_db = None

_redis_client = None


def mongo_db():
    global _mongo_db
    return _mongo_db


def redis_client():
    global _redis_client
    return _redis_client


def init_db():
    """Init database objects"""
    global _mongo_client, _mongo_db, _redis_client

    _mongo_client = MongoClient(C.mongo_addr, C.mongo_port)
    try:
        _mongo_client.server_info()
    except Exception as e:
        logging.getLogger('image-classifier-backend').error('mongo error, ' + str(e))
        exit(1)
    _mongo_db = _mongo_client[C.mongo_db]

    _redis_client = Redis(C.redis_addr, C.redis_port, C.redis_db)
    try:
        _redis_client.ping()
    except Exception as e:
        logging.getLogger('image-classifier-backend').error('redis error, ' + str(e))
        exit(1)
