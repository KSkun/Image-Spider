# Image Spider by KSkun
# for Software Course Project
# 2021/12

import logging
import os
from time import sleep

from config import load_config, C
from consumer.client import ConsumerClient
from db.main import init_db
from db.task import mark_task_done

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('image-spider')
    logger.info('starting Image Spider by KSkun')

    # load config file
    config_file = 'config/' + os.getenv('CONFIG_FILE', default='default.json')
    load_config(config_file)
    logger.info('config file %s loaded' % config_file)

    # init database objects
    init_db()

    client = ConsumerClient(C.redis_addr, C.redis_port, C.redis_db, C.consumer_id)
    while True:
        # fetch command
        cmd = None
        try:
            cmd = client.read_cmd()
        except Exception as e:
            logger.error('exception while fetching cmd')
            logger.error(e)
            sleep(1)
            continue

        if cmd is None:
            continue
        logger.info(
            'recv cmd id: %s, task_id: %s, op: %s, kw: %s, engs: %s' %
            (cmd.redis_id, cmd.task_id, cmd.operation, cmd.keyword, cmd.engines)
        )

        # skip init command
        if cmd.operation == 'init':
            logger.info('skip init cmd')
            continue

        # execution
        try:
            cmd.execute()
        except Exception as e:
            logger.error('exception while execute cmd')
            logger.error(e)

        # acknowledge
        try:
            client.ack_cmd(cmd.redis_id)
            mark_task_done(cmd.task_id)
        except Exception as e:
            logger.error('exception while io with database')
            logger.error(e)

        logger.info('done cmd id: %s' % cmd.redis_id)
