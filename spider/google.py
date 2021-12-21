from typing import List, Union

import requests

from spider.spider import Spider


class GoogleSpider(Spider):
    """Google Image Search Engine spider"""

    # constants
    __api_url: str = 'https://customsearch.googleapis.com/customsearch/v1'
    __page_limit: int = 10
    __engine_id: str
    __api_key: str

    # variables
    __fetched_count: int = 0

    def __init__(self, keyword: str, engine_id: str, api_key: str, proxy_addr: Union[str, None] = None):
        super().__init__(keyword, proxy_addr)
        self.search_engine_name = 'google'

        self.__engine_id = engine_id
        self.__api_key = api_key

    def request(self) -> List[str]:
        # send request
        params = {
            'cx': self.__engine_id,
            'key': self.__api_key,
            'q': self.keyword,
            'num': self.__page_limit,
            'start': self.__fetched_count + 1
        }
        proxies = {}
        if self.proxy_addr is not None:
            proxies['https'] = self.proxy_addr
        r = requests.get(self.__api_url, params=params, proxies=proxies)
        r.raise_for_status()

        # parse body
        json_obj = r.json()
        results = []
        for result_obj in json_obj['items']:
            if 'pagemap' not in result_obj or 'cse_image' not in result_obj['pagemap']:
                continue
            images = result_obj['pagemap']['cse_image']
            for image in images:
                if 'src' not in image:
                    continue
                url = image['src']
                if 'http' not in url:
                    continue
                results.append(url)

        self.__fetched_count += self.__page_limit
        return results
