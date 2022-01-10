import json
from typing import List, Dict, Union
from urllib.parse import parse_qs, urlparse

import requests

from spider.spider import Spider

# constants
_api_url: str = 'https://image.baidu.com/search/acjson'
_page_limit: int = 100

_decoding_map_digit_letter: Dict[str, str] = {
    'w': 'a', 'k': 'b', 'v': 'c', '1': 'd', 'j': 'e', 'u': 'f', '2': 'g', 'i': 'h', 't': 'i', '3': 'j', 'h': 'k',
    's': 'l', '4': 'm', 'g': 'n', '5': 'o', 'r': 'p', 'q': 'q', '6': 'r', 'f': 's', 'p': 't', '7': 'u', 'e': 'v',
    'o': 'w', '8': '1', 'd': '2', 'n': '3', '9': '4', 'c': '5', 'm': '6', '0': '7', 'b': '8', 'l': '9', 'a': '0'
}
_decoding_map_symbol: Dict[str, str] = {'_z2C$q': ':', '_z&e3B': '.', 'AzdH3F': '/'}


class BaiduSpider(Spider):
    """Baidu Image Search Engine spider"""

    # variables
    __fetched_count: int = 0

    def __init__(self, keyword: str, proxy_addr: Union[str, None] = None):
        super().__init__(keyword, proxy_addr)
        self.search_engine_name = 'baidu'

    @staticmethod
    def __decode_url(url_encoded: str):
        url = ''
        for src, dst in _decoding_map_symbol.items():
            url_encoded = url_encoded.replace(src, dst)
        for c in url_encoded:
            if c in _decoding_map_digit_letter:
                url += _decoding_map_digit_letter[c]
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
            'rn': _page_limit
        }
        headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Host': 'image.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
            'X-Requested-With': 'XMLHttpRequest'
        }
        proxies = {}
        if self.proxy_addr is not None:
            proxies['https'] = self.proxy_addr
        r = requests.get(_api_url, params=params, headers=headers, proxies=proxies)
        r.raise_for_status()

        # parse body
        json_obj = json.loads(r.content)
        results = []
        for result_obj in json_obj['data']:
            if 'objURL' not in result_obj:
                continue
            url_encoded = result_obj['objURL']
            url_str = self.__decode_url(url_encoded)
            url_str = url_str.replace('https://gimg2.baidu.com/image_search/',
                                      'https://gimg2.baidu.com/image_search/?')
            url_params = parse_qs(urlparse(url_str).query)
            real_url: str
            if 'src' not in url_params:
                real_url = url_str
            else:
                real_url = url_params['src'][0]
            results.append(real_url)

        self.__fetched_count += _page_limit
        return results
