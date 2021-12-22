import json
import logging
import random
from typing import List, Dict

# constants
from config import C
from spiders import spider_classes

_supported_ops: Dict[str, str] = {'crawl': 'execute_crawl'}
_logger = logging.getLogger('image-spider')


class SpiderCmd:
    """Spider consumer data class"""

    # constants
    redis_id: str
    operation: str
    keyword: str
    engines: List[str]
    limit: int

    def execute_crawl(self):
        for engine in self.engines:
            if engine not in spider_classes:
                raise NotImplementedError('unsupported search engine')
            klass = spider_classes[engine]
            proxy = ''
            if engine in C.proxies:
                proxy = C.proxies[engine]
            spider = klass(self.keyword, proxy_addr=proxy)
            results = []
            while len(results) < self.limit:
                try:
                    page = spider.next_page()
                    if len(page) == 0:
                        break
                    results += page
                except Exception as e:
                    _logger.error('error when fetching search results: %s' % e)
                    break
            results = results[0:min(len(results), self.limit)]
            print('fetched %d results from engine %s' % (len(results), engine))
            print(results[random.randint(0, len(results) - 1)])

    def execute(self):
        # consumer validation
        if self.operation not in _supported_ops:
            raise NotImplementedError('unknown spider operation')
        if len(self.keyword) == 0:
            raise ValueError('empty keyword in consumer')
        if len(self.engines) == 0:
            raise ValueError('empty engines in consumer')
        if self.limit <= 0:
            raise ValueError('limit less than or equals to 0')

        # call registered execution method
        func_name = _supported_ops[self.operation]
        getattr(self, func_name)()  # call registered execution method


# simple ORM for SpiderCmd

def from_dict(dict_obj: Dict[str, object]) -> SpiderCmd:
    """Make SpiderCmd object from a dict"""
    obj = SpiderCmd()
    var_list = SpiderCmd.__annotations__
    for v in var_list:
        if v in dict_obj:
            setattr(obj, v, dict_obj[v])
        else:
            raise ValueError('missing field %s for making SpiderCmd' % v)
    return obj


def from_json(redis_id: str, json_str: str) -> SpiderCmd:
    """Make SpiderCmd object from a JSON document"""
    json_obj = json.loads(json_str)
    json_obj['redis_id'] = redis_id
    return from_dict(json_obj)
