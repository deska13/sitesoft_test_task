import os
from urllib.parse import urljoin
from uuid import UUID

import aiohttp
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from django.core.asgi import get_asgi_application
from loguru import logger

from parser_app.dto import HabrParseContentDTO
from parser_app.models import HabrPostContent, HabrSourceURLs

from .utils import get_base_domain

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")

application = get_asgi_application()


async def get_title_urls(
    url: str,
    url_habr_parser_id: UUID,
) -> list[HabrParseContentDTO]:
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
            base_domain = get_base_domain(url)
            return [
                HabrParseContentDTO(
                    url=urljoin(base_domain, link.get("href")),
                    url_habr_parser_id=url_habr_parser_id,
                )
                for link in page.find_all("a", class_="tm-title__link")
            ]


async def get_content_by_url(habr_parsed_content: HabrParseContentDTO) -> None:
    """
    Gets content by given url.

    :param url: url to parse
    :return: parsed content
    """
    logger.debug(f"Getting content by url: {habr_parsed_content}")
    async with aiohttp.ClientSession() as session:
        async with session.get(habr_parsed_content.url) as response:
            assert response.status == 200
            page = BeautifulSoup(await response.text(), "html.parser")
            logger.info(response.request_info)
            base_domain = get_base_domain(habr_parsed_content.url)
            habr_parse = await sync_to_async(
                HabrSourceURLs.objects.get, thread_sensitive=True
            )(pk=str(habr_parsed_content.url_habr_parser_id))
            post_content = HabrPostContent(
                url=urljoin(base_domain, habr_parsed_content.url),
                post_at=page.find("span", class_="tm-article-datetime-published")
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
                url_habr_parser_id=habr_parse,
            )
            if post_content is not None:
                try:
                    await post_content.asave()
                except Exception as e:
                    logger.error("Content exist.")
