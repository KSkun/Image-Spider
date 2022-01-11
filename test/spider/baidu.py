import os
import random
import unittest

from src.spider.baidu import BaiduSpider


class TestBaiduSpider(unittest.TestCase):
    """Function tests of Baidu spider"""
    def test_spider(self):
        """Test crawling results"""
        spider = BaiduSpider('甘雨')
        results = []
        for i in range(0, 5):
            results += spider.next_page()
        print('fetched %d result(s)' % (len(results)))
        for i in range(0, 5):
            idx = random.randint(0, len(results) - 1)
            print('index %d: %s' % (idx, results[idx]))
        self.assertTrue(True)

    def test_spider_with_proxy(self):
        """Test crawling results with proxy"""
        spider = BaiduSpider('甘雨', proxy_addr=os.getenv('HTTP_PROXY'))
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
