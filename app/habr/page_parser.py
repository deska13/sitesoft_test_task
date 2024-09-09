from urllib.parse import urljoin, urlparse

import aiohttp
from bs4 import BeautifulSoup
from dto import HabrPostContent
from loguru import logger


class HabrPageParser:
    """Class for parsing Habr page."""

    @staticmethod
    def get_base_domain(url: str) -> str:
        """
        Gets base domain from given url.

        Examples:
            >>> get_base_domain('https://habr.com/ru/post/442222/')
            'https://habr.com'

        :param url: url to parse
        :return: base domain
        """
        return f"{urlparse(url).scheme}://{urlparse(url).hostname}"

    @logger.catch
    async def get_title_urls(self, url: str) -> list[str]:
        """
        Gets all urls from given page.

        :param url: url to parse
        :return: list of urls
        """
        logger.debug(f"Getting urls from {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                assert response.status == 200
                page = BeautifulSoup(await response.text(), "html.parser")
                base_domain = self.get_base_domain(url)
                return [
                    urljoin(base_domain, link.get("href"))
                    for link in page.find_all("a", class_="tm-title__link")
                ]

    @logger.catch
    async def get_content_by_url(self, url: str) -> HabrPostContent:
        """
        Gets content by given url.

        :param url: url to parse
        :return: parsed content
        """
        logger.debug(f"Getting content by url: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                assert response.status == 200
                page = BeautifulSoup(await response.text(), "html.parser")
                logger.info(response.request_info)
                base_domain = self.get_base_domain(url)
                return HabrPostContent(
                    url=urljoin(base_domain, url),
                    created_at=page.find("span", class_="tm-article-datetime-published")
                    .find("time")
                    .get("datetime"),
                    title=page.find("h1", class_="tm-title tm-title_h1").text,
                    author=page.find("a", class_="tm-user-info__userpic").get("title"),
                    author_url=urljoin(
                        base_domain,
                        page.find("a", class_="tm-user-info__userpic", href=True).get(
                            "href"
                        ),
                    ),
                )
