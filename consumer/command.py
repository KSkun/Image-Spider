import json
from typing import List, Dict

# constants
_supported_ops: Dict[str, str] = {'crawl': 'execute_crawl'}


class SpiderCmd:
    """Spider consumer data class"""

    # constants
    redis_id: str
    operation: str
    keyword: str
    engines: List[str]

    def __init__(self, redis_id: str, operation: str, keyword: str, engines: List[str]):
        self.redis_id = redis_id
        self.operation = operation
        self.keyword = keyword
        self.engines = engines

    def execute_crawl(self):
        pass  # TODO

    def execute(self):
        # consumer validation
        if self.operation not in _supported_ops:
            raise NotImplementedError('unknown spider operation')
        if len(self.keyword) == 0:
            raise ValueError('empty keyword in consumer')
        if len(self.engines) == 0:
            raise ValueError('empty engines in consumer')

        # call registered execution method
        func_name = _supported_ops[self.operation]
        getattr(self, func_name)()  # call registered execution method


# simple ORM for consumer

def from_dict(dict_obj: Dict[str, object]) -> SpiderCmd:
    """Make SpiderCmd object from a dict"""
    obj = SpiderCmd('', '', '', [])
    var_list = vars(obj)
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
