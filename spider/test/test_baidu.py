import random
import unittest

from spider.baidu import BaiduSpider


class TestBaiduSpider(unittest.TestCase):
    def test_spider(self):
        spider = BaiduSpider('甘雨')
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
