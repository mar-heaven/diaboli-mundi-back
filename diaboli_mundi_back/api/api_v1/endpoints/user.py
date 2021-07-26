from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends

from diaboli_mundi_back import crud
from diaboli_mundi_back.db.database import get_mongo
from diaboli_mundi_back.modles.user import UserInDB, UserLogin
from diaboli_mundi_back.modles.response import Response
from diaboli_mundi_back.utils import generator_private_api_token, decode_private_api_token

router = APIRouter()


@router.post(
    "/register/", response_model=Response
)
async def register(user: UserInDB):
    """ 用户注册"""
    db = get_mongo()

    check_validation = await crud.user.check_user(db, user)
    if check_validation:
        raise HTTPException(status_code=400, detail=check_validation)
    await crud.user.create_user(db, user)
    return Response(msg="注册成功", status=201)


@router.post(
    "/login/"
)
async def login(user: UserLogin):
    """ 用户登录"""
    db = get_mongo()
    user = await crud.user.login(db, user)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    payload = {
        'user_id': user['user_id'],
    }
    token = generator_private_api_token(payload, 15 * 24)
    return {"token": token, 'status': 200}


@router.get(
    "/user/"
)
async def get_user(payload: Optional[dict] = Depends(decode_private_api_token)):
    """ 获取用户信息"""
    db = get_mongo()
    if not payload:
        print(f'can not get user info, invalid token')
        raise HTTPException(status_code=401, detail='Permission Deny')
    user = await crud.user.get_user(db, payload['user_id'])
    return {"user_info": user, 'status': 200}
