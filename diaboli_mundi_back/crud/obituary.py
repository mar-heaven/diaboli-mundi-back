import re
import datetime
import hashlib

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from diaboli_mundi_back.const import Status
from diaboli_mundi_back.modles.obituary import ObituaryCreate
# from ..utils import generator_private_api_token

PROJECTION = {"_id": 0, "obituary_id": 1}
TABLE_NAME = "obituaries"
ID_TABLE_NAME = "obituary"


async def add_user_obituary(
        db: AsyncIOMotorDatabase,
        obituary: dict,
) -> dict:
    """
    phone: int
    password: str
    """
    id_instance = await db.id_collection.find_one_and_update(filter={'system': ID_TABLE_NAME},
                                                             update={'$inc': {'max_id': 1}},
                                                             upsert=True,
                                                             return_document=ReturnDocument.AFTER)

    obituary_id = id_instance['max_id']
    obituary_instance = {
        "obituary_id": obituary_id,
        "name": obituary.get('name'),
        "user_id": obituary.get("user_id"),
        "age": obituary.get("user_id"),
        "death_reason": obituary.get("death_reason"),
        "status": obituary.get("status")
    }
    return await db[TABLE_NAME].insert_one(obituary_instance)


async def get_obituary_list(
        db: AsyncIOMotorDatabase, skip: int, limit: int
) -> list:

    filter_ = {
        "status": Status.normal,
    }
    projection_ = {
        "_id": 0,
        "obituary_id": 1,
        "age": 1,
        "death_reason": 1,
        "name": 1,
    }
    cursor = db[TABLE_NAME].find(filter_, projection=projection_)
    if skip > 0:
        cursor = cursor.skip(skip)
    if limit > 0:
        cursor = cursor.limit(limit)
    return await cursor.to_list(None) or []
