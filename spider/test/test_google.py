import os
import random
import unittest

from spider.google import GoogleSpider


class TestGoogleSpider(unittest.TestCase):
    def test_spider(self):
        spider = GoogleSpider('ganyu', engine_id=os.getenv('GG_ENGINE_ID'), api_key=os.getenv('GG_API_KEY'))
        results = []
        for i in range(0, 5):
            results += spider.next_page()
        print('fetched %d result(s)' % (len(results)))
        for i in range(0, 5):
            idx = random.randint(0, len(results) - 1)
            print('index %d: %s' % (idx, results[idx]))
        self.assertTrue(True)

    def test_spider_with_proxy(self):
        spider = GoogleSpider('ganyu', engine_id=os.getenv('GG_ENGINE_ID'), api_key=os.getenv('GG_API_KEY'),
                              proxy_addr=os.getenv('HTTP_PROXY'))
        results = []
        for i in range(0, 5):
            results += spider.next_page()
        print('fetched %d result(s)' % (len(results)))
        for i in range(0, 5):
            idx = random.randint(0, len(results) - 1)
            print('index %d: %s' % (idx, results[idx]))
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
