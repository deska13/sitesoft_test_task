from uuid import UUID

from pydantic import BaseModel


class HabrSourceUrlDTO(BaseModel):
    id: UUID


class HabrParseContentDTO(BaseModel):
    url: str
    url_habr_parser_id: UUID
