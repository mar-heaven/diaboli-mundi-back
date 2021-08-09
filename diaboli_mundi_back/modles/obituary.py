from enum import Enum
from typing import Optional, Union

from pydantic.main import BaseModel

from diaboli_mundi_back.const import Status


class ObituaryCreate(BaseModel):
    """ 生死簿"""
    user_id: int
    age: int
    death_reason: Union[str, None]
    status: Status


class ObituaryOut(BaseModel):
    """ 生死簿"""
    obituary_id: int
    age: int
    death_reason: str
    name: str
