# Image Spider by KSkun
# for Software Course Project
# 2021/12
import logging
import os

from config import load_config, C
from consumer.client import ConsumerClient

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('image-spider')
    logger.info('starting Image Spider by KSkun')

    config_file = os.getenv('CONFIG_FILE', default='default.json')
    load_config(config_file)
    logger.info('config file %s loaded' % config_file)

    client = ConsumerClient(C.redis_addr, C.redis_port, C.redis_db, C.consumer_id)
    while True:
        cmd = client.read_cmd()
        logger.info(
            'recv cmd id: %s, op: %s, kw: %s, engs: %s' % (cmd.redis_id, cmd.operation, cmd.keyword, cmd.engines))
        cmd.execute()
        client.ack_cmd(cmd.redis_id)
        logger.info('done cmd id: %s' % cmd.redis_id)
