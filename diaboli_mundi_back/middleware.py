import logging
from typing import Union, Optional, List
import re

import jwt
from fastapi import Request
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

from diaboli_mundi_back.db.database import close_mongo_conn, create_mongo_conn, get_mongo
from diaboli_mundi_back.settings import settings
from diaboli_mundi_back.const import WHITE_LIST
from diaboli_mundi_back.crud.permission import ROLE_TO_PERMISSION_TABLE_NAME, USER_TO_ROLE_TABLE_NAME, \
    PERMISSION_TABLE_NAME


async def connect_db() -> None:
    logging.info("connect_db starting")
    create_mongo_conn()
    logging.info("connect_db finished")


async def close_db() -> None:
    logging.info("close_db starting")
    close_mongo_conn()

    logging.info("close_db finished")


async def start_up():
    await connect_db()


async def shutdown():
    await close_db()


async def auth(request, call_next):
    return await token_auth(request, call_next, key=settings.system_public_key_path.read_bytes())


async def token_auth(request: Request, call_next, key=None):
    url = request.url.path
    if url in WHITE_LIST:
        return await call_next(request)
    token = request.headers.get('token')
    if not token:
        return JSONResponse(status_code=403, content="Forbidden")
    try:
        payload = jwt.decode(token, key=key, algorithms='RS256')
        user_id = payload.get('user_id')
        is_valid = await check_rbac(user_id, url)
        if not is_valid:
            return JSONResponse(status_code=403, content="Forbidden")
    except Exception as e:
        logging.warning(f'invalid token: {e}, {token}')
        return JSONResponse(status_code=400, content="invalid token")
    return await call_next(request)


async def check_rbac(user_id, path):
    db = get_mongo()
    roles = await _get_role_by_user(db, user_id)
    if not roles:
        return False
    persmission_ids = await _get_permission_by_roles(db, roles)
    user_permissions = await _get_user_permission_ids(db, persmission_ids)
    return path in user_permissions


async def _get_role_by_user(db, user_id):
    # type: (AsyncIOMotorDatabase, int) -> List[int]
    projection_ = {"role_id": 1, "_id": 0}

    db = get_mongo()
    cursor = db[USER_TO_ROLE_TABLE_NAME].find({'user_id': user_id}, projection=projection_)
    data = await cursor.to_list(None) or []
    data = [d['role_id'] for d in data]
    return data


async def _get_permission_by_roles(db, roles):
    # type: (AsyncIOMotorDatabase, List) -> List[int]
    projection_ = {"permission_id": 1, "_id": 0}
    cursor = db[ROLE_TO_PERMISSION_TABLE_NAME].find({'role_id': {"$in": roles}}, projection=projection_)
    data = await cursor.to_list(None) or []
    data = [d['permission_id'] for d in data]
    return data


async def _get_user_permission_ids(db, persmission_ids):
    # type: (AsyncIOMotorDatabase, List) -> List
    projection_ = {"permission_url": 1, "_id": 0}
    cursor = db[PERMISSION_TABLE_NAME].find({'permission_id': {"$in": persmission_ids}}, projection=projection_)
    data = await cursor.to_list(None) or []
    data = [d['permission_url'] for d in data]
    return data
