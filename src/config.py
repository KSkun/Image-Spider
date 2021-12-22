import json

from typing import Dict


class SpiderConfig:
    """Spider config data class"""

    redis_addr: str
    redis_port: int
    redis_db: int
    consumer_id: int

    gg_engine_id: str
    gg_api_key: str

    proxies: Dict[str, str]


C: SpiderConfig = SpiderConfig()


def load_config(file_path: str):
    file = open(file_path, 'r')
    json_str = file.read()
    file.close()

    json_obj = json.loads(json_str)

    var_list = SpiderConfig.__annotations__
    for v in var_list:
        if v in json_obj:
            setattr(C, v, json_obj[v])
        else:
            raise ValueError('missing field %s in config file %s' % (v, file_path))
