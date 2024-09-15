from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    db: str
    user: str
    password: str
    host: str
    port: int

    def get_django_settings(self) -> dict[str, str]:
        return {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": self.db,
            "USER": self.user,
            "PASSWORD": self.password,
            "HOST": self.host,
            "PORT": str(self.port),
        }

    model_config = SettingsConfigDict(env_prefix="POSTGRES_")
