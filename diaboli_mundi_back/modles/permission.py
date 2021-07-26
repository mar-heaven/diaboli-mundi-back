from typing import List, Optional
import datetime

from pydantic.main import BaseModel

from diaboli_mundi_back.modles.base import PublicBase


class PermissionCreate(BaseModel):
    title: str
    permission_url: str


class PermissionInDB(PermissionCreate):
    title: str
    permission_id: int
    permission_url: str


class RoleCreate(PublicBase):
    title: str


class RoleInDB(RoleCreate):
    role_id: int
    title: str


class RoleCreate(BaseModel):
    title: str


class UserRole(BaseModel):
    user_id: int
    role_id: int


class RolePermission(BaseModel):
    role_id: int
    permission_id: int


class WhiteUrl(BaseModel):
    url: str
