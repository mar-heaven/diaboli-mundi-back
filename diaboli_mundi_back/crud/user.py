import re
import datetime
import hashlib
import random

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from diaboli_mundi_back.modles.user import UserInDB, UserLogin
from diaboli_mundi_back.modles.obituary import ObituaryCreate
from diaboli_mundi_back.crud.obituary import add_user_obituary
from diaboli_mundi_back.modles.obituary import Status

# from diaboli_mundi_back.api.api_v1 import
# from ..utils import generator_private_api_token

PROJECTION = {"_id": 0, "user_id": 1, "phone": 1, "username": 1}
TABLE_NAME = "users"
ID_TABLE_NAME = "user"


async def hook_after_user_created(db: AsyncIOMotorDatabase,
                                  obituary: dict):
    await add_user_obituary(db, obituary)


async def check_user(
    db: AsyncIOMotorDatabase,
    user: UserInDB
):
    phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    res = re.search(phone_pat, str(user.phone))
    if not res:
        return "手机号不合法"
    if user.password != user.password_repeat:
        return "再次密码不一致！"
    filter_ = {
        "phone": user.phone,
    }
    user_instance = await db[TABLE_NAME].find_one(filter_, projection=PROJECTION)
    if user_instance:
        return "该用户已被注册！"
    return False


async def create_user(
    db: AsyncIOMotorDatabase,
    user: UserInDB
) -> None:
    """
    phone: int
    password: str
    """
    id_instance = await db.id_collection.find_one_and_update(filter={'system': ID_TABLE_NAME},
                                                             update={'$inc': {'max_id': 1}},
                                                             upsert=True,
                                                             return_document=ReturnDocument.AFTER)

    user_id = id_instance['max_id']
    age = random.randint(0, 2)
    user_instance = {
        "user_id": user_id,
        "phone": user.phone,
        "age": age,
        "username": str(user.phone),
        "password": hashlib.sha256(user.password.encode()).hexdigest(),
        "create_at": datetime.datetime.now()
    }
    await db[TABLE_NAME].insert_one(user_instance)

    obituary_instance = {
        "user_id": user_id,
        "age": age,
        "death_reason": None,
        "status": Status.live
    }
    await hook_after_user_created(db, obituary_instance)


async def login(
    db: AsyncIOMotorDatabase,
    user: UserLogin
) -> dict:
    filter_ = {
        "phone": user.phone,
        "password": hashlib.sha256(user.password.encode()).hexdigest(),
    }
    return await db[TABLE_NAME].find_one(filter_, projection=PROJECTION)


async def get_user(
    db: AsyncIOMotorDatabase,
    user_id: int
) -> dict:
    filter_ = {
        "user_id": user_id,
    }
    return await db[TABLE_NAME].find_one(filter_, projection=PROJECTION)
