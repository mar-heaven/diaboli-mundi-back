import re
import datetime
import hashlib

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from diaboli_mundi_back.modles.permission import PermissionCreate, RoleCreate, UserRole, RolePermission
# from ..utils import generator_private_api_token

PROJECTION = {"_id": 0}

PERMISSION_TABLE_NAME = "permissions"
PERMISSION_ID_TABLE_NAME = "permission"

ROLE_TABLE_NAME = "roles"
ROLE_ID_TABLE_NAME = "role"

USER_TO_ROLE_TABLE_NAME = "user_to_role"

ROLE_TO_PERMISSION_TABLE_NAME = "role_to_permission"


async def create_permission(
        db: AsyncIOMotorDatabase,
        permission: PermissionCreate
) -> dict:
    """
    title: str
    permission_url: str
    """
    id_instance = await db.id_collection.find_one_and_update(filter={'system': PERMISSION_ID_TABLE_NAME},
                                                             update={'$inc': {'max_id': 1}},
                                                             upsert=True,
                                                             return_document=ReturnDocument.AFTER)

    instance_id = id_instance['max_id']
    permission_instance = {
        "permission_id": instance_id,
        "permission_url": permission.permission_url,
        "title": permission.title,
        "create_at": datetime.datetime.now()
    }
    return await db[PERMISSION_TABLE_NAME].insert_one(permission_instance)


async def create_role(
        db: AsyncIOMotorDatabase,
        role: RoleCreate
) -> dict:
    # check permissions
    id_instance = await db.id_collection.find_one_and_update(filter={'system': ROLE_ID_TABLE_NAME},
                                                             update={'$inc': {'max_id': 1}},
                                                             upsert=True,
                                                             return_document=ReturnDocument.AFTER)
    instance_id = id_instance['max_id']
    role_instance = {
        "role_id": instance_id,
        "title": role.title,
    }
    return await db[ROLE_TABLE_NAME].insert_one(role_instance)


async def bind_permission(
        db: AsyncIOMotorDatabase,
        role_permission: RolePermission
) -> dict:
    # check permissions
    role_permission_instance = {
        "role_id": role_permission.role_id,
        "permission_id": role_permission.role_id,
    }
    return await db[ROLE_TO_PERMISSION_TABLE_NAME].insert_one(role_permission_instance)


async def bind_role(
        db: AsyncIOMotorDatabase,
        user_role: UserRole
) -> dict:
    # check permissions
    instance = {
        "user_id": user_role.user_id,
        "role_id": user_role.role_id,
    }
    return await db[USER_TO_ROLE_TABLE_NAME].insert_one(instance)
