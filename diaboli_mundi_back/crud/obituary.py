import re
import datetime
import hashlib

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

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
        "user_id": obituary.get("user_id"),
        "age": obituary.get("user_id"),
        "death_reason": obituary.get("death_reason"),
        "status": obituary.get("status")
    }
    return await db[TABLE_NAME].insert_one(obituary_instance)
