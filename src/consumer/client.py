from typing import Dict

import walrus

from src.consumer.command import SpiderCmd, from_json

_stream_name: str = 'spider_cmd'
_group_name: str = 'spider'
_consumer_name_pattern: str = 'con_%d'

_block_time: int = 1000  # 1 second


class ConsumerClient:
    """Spider redis client class"""

    # constants
    __addr: str
    __port: int
    __db: int

    __client: walrus.Database
    __stream: walrus.containers.ConsumerGroupStream
    __group: walrus.ConsumerGroup
    __consumer_id: int

    def __init__(self, addr: str, port: int, db: int, consumer_id: int):
        self.__addr = addr
        self.__port = port
        self.__db = db

        self.__consumer_id = consumer_id
        self.__client = walrus.Database(host=self.__addr, port=self.__port, db=self.__db)
        self.__group = self.__client.consumer_group(_group_name, [_stream_name],
                                                    consumer=_consumer_name_pattern % self.__consumer_id)
        self.__stream = getattr(self.__group, _stream_name)

    def read_cmd(self) -> SpiderCmd:
        result = []
        while len(result) == 0:
            orig_result = self.__group.read(count=1, block=_block_time)
            if len(orig_result) == 0:
                continue
            result = orig_result[0][1][0]
        redis_id: str = result[0].decode()
        obj: Dict[bytes, bytes] = result[1]
        return from_json(redis_id, obj[b'cmd'].decode())

    def ack_cmd(self, redis_id: str):
        self.__stream.ack(redis_id)
