import asyncio
import sys

from habr import HabrPageParser
from loguru import logger


@logger.catch
async def parse() -> None:
    """
    Makes a request to the main page of Habr and parses it.
    Gets all urls from the page, parses them and logs the results.
    Then it waits for 10 minutes and repeats the process.
    """
    habr_parser = HabrPageParser()
    urls = await habr_parser.get_title_urls("https://habr.com")
    parsers = []
    for url in urls:
        parsers.append(habr_parser.get_content_by_url(url))
    answers = await asyncio.gather(*parsers)
    for answer in answers:
        logger.info(answer)
    await asyncio.sleep(10 * 60)


def main() -> None:
    """
    Starts the main loop of the application.
    Removes the default handler and adds a handler that logs to sys.stdout with
    level TRACE.
    Calls parse() in a loop, waiting for 10 minutes between calls.
    """
    logger.remove(0)
    logger.add(sys.stdout, level="TRACE")
    while True:
        asyncio.run(parse())


if __name__ == "__main__":
    main()
