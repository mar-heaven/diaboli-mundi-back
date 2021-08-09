from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends

from diaboli_mundi_back import crud
from diaboli_mundi_back.db.database import get_mongo
from diaboli_mundi_back.modles.obituary import ObituaryOut
from diaboli_mundi_back.modles.response import Response
from diaboli_mundi_back.utils import generator_private_api_token, decode_private_api_token

router = APIRouter()


@router.get(
    "/obituary_list",
)
async def get_obituary_list(
    skip: int = 0, limit: int = 100
):
    skip = int(skip) if skip else 0
    db = get_mongo()
    obituary_list = await crud.obituary.get_obituary_list(db, skip, limit)
    skip = str(skip + len(obituary_list))
    return {
        "skip": skip,
        "obituary_list": obituary_list,
    }

