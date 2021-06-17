import datetime

from pydantic import BaseModel


class UserInDB(BaseModel):
    """ 用户注册"""
    phone: int
    password: str
    password_repeat: str
    # todo 手机验证码


class UserLogin(BaseModel):
    """ 用户登录"""
    phone: int
    password: str


class UserOutDB(BaseModel):
    """ 用户返回"""
    user_id: str
    phone: str
    username: str
    password: str
    update_at: datetime.datetime
