from abc import abstractmethod, ABC
from typing import List, Union


class Spider(ABC):
    """Spider abstract class"""

    # constants
    keyword: str  # keyword of this spider instance
    search_engine_name: str  # name of the crawled search engine
    proxy_addr: Union[str, None]  # proxy settings

    # variables
    __result_buffer: List[str] = []  # temporarily store fetched results

    def __init__(self, keyword: str, proxy_addr: Union[str, None] = None):
        self.keyword = keyword
        self.proxy_addr = proxy_addr

    @abstractmethod
    def request(self) -> List[str]:
        """
        Request for search results
        :return: list of image URLs
        """
        pass

    def refresh_buffer(self) -> None:
        """
        Refresh the result buffer with results from a new request
        """
        assert (len(self.__result_buffer) == 0), 'refresh when buffer is not empty'
        self.__result_buffer = self.request()
        assert (len(self.__result_buffer) > 0), 'buffer is still empty after refresh'

    def next_page(self) -> List[str]:
        """
        Fetch results in one page
        :return: list of image URLs
        """
        if len(self.__result_buffer) == 0:
            self.refresh_buffer()
        results = self.__result_buffer.copy()
        self.__result_buffer.clear()
        return results

    def next_result(self) -> str:
        """
        Fetch one result
        :return: an image URL
        """
        if len(self.__result_buffer) == 0:
            self.refresh_buffer()
        result = self.__result_buffer.pop(0)
        return result
