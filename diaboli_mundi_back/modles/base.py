import datetime
from typing import Optional

from pydantic.main import BaseModel


class PublicBase(BaseModel):
    create_at: None
    title: None
