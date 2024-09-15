import uuid
from typing import Any

from django.db import models

from core import create_channel_rabbit
from parser_app.dto import HabrSourceUrlDTO


class HabrSourceURLs(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    url = models.URLField(unique=True)
    is_enable = models.BooleanField(default=True)
    shedule_ms = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.url)

    @property
    def queue_name(self) -> str:
        return f"habr_parser_url_{self.id}"

    @property
    def delay(self) -> int:
        return (
            self.shedule_ms.hour * 60 * 60
            + self.shedule_ms.minute * 60
            + self.shedule_ms.second
        )

    def repeat_parser(self) -> None:
        if self.is_enable:
            channel = create_channel_rabbit()
            channel.basic_publish(
                exchange="",
                routing_key="parser_habr_parse_urls",
                body=HabrSourceUrlDTO(id=self.id).model_dump_json(),
            )

    def save(self, *args: Any, **kwargs: Any) -> None:
        super().save(*args, **kwargs)
        self.repeat_parser()


class HabrPostContent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
    )
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    post_at = models.DateTimeField()
    author = models.CharField(max_length=255)
    author_url = models.URLField()
    url_habr_parser_id = models.ForeignKey(
        "HabrSourceURLs", on_delete=models.SET_NULL, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.title)
