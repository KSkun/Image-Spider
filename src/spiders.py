from typing import Dict, Type

from spider.baidu import BaiduSpider
from spider.google import GoogleSpider

# search engine name to spider class
spider_classes: Dict[str, Type] = {
    'baidu': BaiduSpider,
    'google': GoogleSpider
}
