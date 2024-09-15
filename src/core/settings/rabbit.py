from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitSettings(BaseSettings):
    host: str = "rabbit"
    port: int = 5672
    vhost: str
    user: str
    password: str

    @property
    def url(self) -> str:
        return (
            f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"
        )

    model_config = SettingsConfigDict(env_prefix="RABBIT_")
