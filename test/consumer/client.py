import unittest

from src.consumer.client import ConsumerClient


class TestConsumerDB(unittest.TestCase):
    """Function tests of consumer client"""
    def test_read_cmd(self):
        """Test reading command from redis stream"""
        client = ConsumerClient('localhost', 6379, 0, 1)
        cmd = client.read_cmd()
        print('read cmd id: %s, op: %s, kw: %s, eng: %s' % (cmd.redis_id, cmd.operation, cmd.keyword, cmd.engines))
        client.ack_cmd(cmd.redis_id)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
