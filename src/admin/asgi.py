"""
ASGI config for admin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from django.core.asgi import get_asgi_application
from faststream.rabbit import RabbitBroker
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from core import create_channel_rabbit
from core.settings import RabbitSettings
from parser_app.models import HabrSourceURLs
from parser_app.rpc import parser_worker_router

rabbit_setting = RabbitSettings()

broker = RabbitBroker(
    rabbit_setting.url,
)
broker.include_router(parser_worker_router)


async def start_broker() -> None:
    await broker.start()


async def close_broker() -> None:
    await broker.start()


def startup() -> None:
    channel = create_channel_rabbit()
    channel.queue_purge("parser_habr_parse_urls")
    urls = HabrSourceURLs.objects.all()
    for url in urls:
        url.repeat_parser()


app = Starlette(
    routes=(
        # /static is your STATIC_URL setting
        Mount("/static", StaticFiles(directory="static"), name="static"),
        Mount("/", get_asgi_application()),  # regular Django ASGI
    ),
    # lifespan=broker_lifespan,
    on_startup=[start_broker, startup],
    on_shutdown=[close_broker],
)
