from typing import Callable

import aiohttp

from .config import settings
from .exceptions import ParseError


class RaiderIoClient:
    def __init__(
        self,
        url: str,
        timeout: int,
        headers: dict,
        parse_function: Callable,
    ):
        self.url = url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.headers = headers
        self.parse = parse_function

    async def get_top_scores(self, *, class_: str = "rogue", limit: int = 10) -> str:
        url = self.url.format(class_=class_)
        headers = self.headers
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url, headers=headers) as response:
                content = await response.read()

                try:
                    parsed_content = self.parse(content.decode("utf-8"))
                except Exception as exc:
                    raise ParseError from exc

            return parsed_content


raiderio_client = RaiderIoClient(
    url=settings.RAIDER_IO_URL,
    timeout=10,
    headers={},
    parse_function=lambda x: x,
)
