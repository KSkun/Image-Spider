import json

from typing import Dict


class SpiderConfig:
    """
    Spider config data class
    See https://github.com/KSkun/Image-Spider/blob/master/README.md
    """

    mongo_addr: str
    mongo_port: int
    mongo_db: str

    image_tmp_dir: str
    image_url: str

    redis_addr: str
    redis_port: int
    redis_db: int
    consumer_id: int

    gg_engine_id: str
    gg_api_key: str

    proxies: Dict[str, str]


C: SpiderConfig = SpiderConfig()


def load_config(file_path: str):
    """Load config fields to object C from file"""
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
