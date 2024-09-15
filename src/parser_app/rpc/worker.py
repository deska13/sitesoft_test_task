import asyncio

from asgiref.sync import sync_to_async
from faststream.rabbit import RabbitRouter

from parser_app.dto import HabrParseContentDTO, HabrSourceUrlDTO
from parser_app.models import HabrSourceURLs
from parser_app.parser import get_content_by_url, get_title_urls

router = RabbitRouter("parser_habr_")


@router.subscriber("parse_urls")
@router.publisher("parse_content")
async def habr_parse_url(
    habr_parse_request: HabrSourceUrlDTO,
) -> list[HabrParseContentDTO]:
    habr_parse = await sync_to_async(HabrSourceURLs.objects.get, thread_sensitive=True)(
        pk=str(habr_parse_request.id)
    )
    await asyncio.sleep(habr_parse.delay)
    if habr_parse.is_enable:
        habr_parse.repeat_parser()
        result = await get_title_urls(habr_parse.url, habr_parse_request.id)
        return result
    return []


@router.subscriber("parse_content")
async def habr_parse_content(habr_parse_request: list[HabrParseContentDTO]) -> None:
    tasks = [get_content_by_url(task) for task in habr_parse_request]
    await asyncio.gather(*tasks)
