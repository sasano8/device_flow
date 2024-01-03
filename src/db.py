from typing import Optional
from uuid import uuid4

from sqlmodel import Field, SQLModel


class Timestamp(float):
    ...


class Token(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()))
    user_id: str = Field(sa_column_kwargs={"unique": True, "index": True})
    access_token: str = Field(sa_column_kwargs={"unique": True})
    refresh_token: str = Field(sa_column_kwargs={"unique": True})
    expires_at: Timestamp
