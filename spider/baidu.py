import json
from abc import ABC
from typing import List, Dict
from urllib.parse import parse_qs, urlparse

import parse
import requests

from spider.spider import Spider


class BaiduSpider(Spider, ABC):
    """Baidu Image Search Engine spider"""

    # constants
    __api_url: str = 'https://image.baidu.com/search/acjson'
    __page_limit: int = 100

    __decoding_map_digit_letter: Dict[str, str] = {
        'w': 'a', 'k': 'b', 'v': 'c', '1': 'd', 'j': 'e', 'u': 'f', '2': 'g', 'i': 'h', 't': 'i', '3': 'j', 'h': 'k',
        's': 'l', '4': 'm', 'g': 'n', '5': 'o', 'r': 'p', 'q': 'q', '6': 'r', 'f': 's', 'p': 't', '7': 'u', 'e': 'v',
        'o': 'w', '8': '1', 'd': '2', 'n': '3', '9': '4', 'c': '5', 'm': '6', '0': '7', 'b': '8', 'l': '9', 'a': '0'
    }
    __decoding_map_symbol: Dict[str, str] = {'_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}

    # variables
    __fetched_count: int = 0

    def __init__(self, keyword):
        super().__init__(keyword)

    def __decode_url(self, url_encoded: str):
        url = ''
        for src, dst in self.__decoding_map_symbol.items():
            url_encoded = url_encoded.replace(src, dst)
        for c in url_encoded:
            if c in self.__decoding_map_digit_letter:
                url += self.__decoding_map_digit_letter[c]
            else:
                url += c
        return url

    def request(self) -> List[str]:
        # send request
        params = {
            'tn': 'resultjson_com',
            'ipn': 'rj',
            'word': self.keyword,
            'pn': self.__fetched_count,
            'rn': self.__page_limit
        }
        headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Host': 'image.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
            'X-Requested-With': 'XMLHttpRequest'
        }
        r = requests.get(self.__api_url, params=params, headers=headers)
        r.raise_for_status()

        # parse body
        json_obj = json.loads(r.content)
        results = []
        for result_obj in json_obj['data']:
            if 'objURL' not in result_obj:
                continue
            url_encoded = result_obj['objURL']
            url_str = self.__decode_url(url_encoded).replace('https://gimg2.baidu.com/image_search/',
                                                             'https://gimg2.baidu.com/image_search/?')
            url_params = parse_qs(urlparse(url_str).query)
            real_url: str
            if 'src' not in url_params:
                real_url = url_str
            else:
                real_url = url_params['src'][0]
            results.append(real_url)

        self.__fetched_count += self.__page_limit
        return results