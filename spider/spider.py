from abc import abstractmethod
from typing import List


class Spider:
    """Spider abstract class"""

    # constants
    keyword: str  # keyword of this spider instance

    # variables
    __result_buffer: List[str] = []  # temporarily store fetched results

    def __init__(self, keyword: str):
        self.keyword = keyword

    @abstractmethod
    def request(self) -> List[str]:
        """
        request for search results
        :return: list of image URLs
        """
        pass

    def refresh_buffer(self) -> None:
        """
        refresh the result buffer with results from a new request
        """
        assert (len(self.__result_buffer) == 0), 'refresh when buffer is not empty'
        self.__result_buffer = self.request()
        assert (len(self.__result_buffer) > 0), 'buffer is still empty after refresh'

    def next_page(self) -> List[str]:
        """
        fetch results in one page
        :return: list of image URLs
        """
        if len(self.__result_buffer) == 0:
            self.refresh_buffer()
        results = self.__result_buffer.copy()
        self.__result_buffer.clear()
        return results

    def next_result(self) -> str:
        """
        fetch one result
        :return: an image URL
        """
        if len(self.__result_buffer) == 0:
            self.__refresh_buffer()
        result = self.__result_buffer.pop(0)
        return result
