import pika
from pika.adapters.blocking_connection import BlockingChannel

from .settings import RabbitSettings


def create_channel_rabbit() -> BlockingChannel:
    setting = RabbitSettings()
    credentials = pika.PlainCredentials(
        username=setting.user,
        password=setting.password,
    )
    connection_parameters = pika.ConnectionParameters(
        host=setting.host,
        port=setting.port,
        credentials=credentials,
    )
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    return channel
