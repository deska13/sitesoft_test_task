from urllib.parse import urlparse


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
