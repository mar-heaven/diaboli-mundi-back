from enum import Enum
import datetime
from typing import List, Optional

from pydantic import BaseModel


class PostInDB(BaseModel):
    title: str
    content: str


class PostOutDB(BaseModel):
    title: str
    content: str
    create_at: datetime.datetime
    update_at: Optional[datetime.datetime]


class PostReply(BaseModel):
    next_token: str
    logs: List[PostOutDB]

#
# class LogInDB(BaseModel):
#     run_id: int
#     seq: int
#     timestamp: int
#     level: str
#     msg: str
#
#
# class LogTxt(BaseModel):
#     timestamp: int
#     level: str
#     msg: str
#
#
# class LogOut(BaseModel):
#     timestamp: int
#     level: str
#     msg: str
#     seq: int
#
#
# class LogReply(BaseModel):
#     next_token: str
#     logs: List[LogOut]
#
#
# LogTxt_FIELDS = LogTxt.__fields__
