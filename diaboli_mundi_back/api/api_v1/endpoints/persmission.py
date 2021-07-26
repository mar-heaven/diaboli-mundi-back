from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends

from diaboli_mundi_back import crud
from diaboli_mundi_back.db.database import get_mongo
from diaboli_mundi_back.modles.permission import PermissionCreate, RoleCreate, UserRole, RolePermission, WhiteUrl
from diaboli_mundi_back.modles.response import Response
from diaboli_mundi_back.utils import generator_private_api_token, decode_private_api_token
from pymongo.errors import DuplicateKeyError

router = APIRouter()


@router.post(
    "/permission/", response_model=Response
)
async def create_permission(permission: PermissionCreate):
    """ 创建permission"""
    db = get_mongo()
    try:
        await crud.permission.create_permission(db, permission)
    except DuplicateKeyError:
        return Response(msg="已有该权限！", status=400)
    return Response(msg="创建权限成功", status=201)


@router.post(
    "/role/"
)
async def create_role(role: RoleCreate):
    """ 创建角色"""
    db = get_mongo()
    try:
        await crud.permission.create_role(db, role)
    except DuplicateKeyError:
        return Response(msg="请勿重复创建", status=400)
    return Response(msg="创建角色成功", status=201)


@router.post(
    "/user_role/"
)
async def bind_role(user_role: UserRole):
    """ 用户绑定角色"""
    db = get_mongo()
    try:
        await crud.permission.bind_role(db, user_role)
    except DuplicateKeyError:
        return Response(msg="用户已绑定角色", status=400)
    return Response(msg="角色绑定成功", status=201)


@router.post(
    "/role_permission/"
)
async def bind_permission(user_role: RolePermission):
    """ 角色分配权限"""
    db = get_mongo()
    try:
        await crud.permission.bind_permission(db, user_role)
    except DuplicateKeyError:
        return Response(msg="角色已有该权限", status=400)
    return Response(msg="权限绑定成功", status=201)


@router.post(
    "/create_white_url/"
)
async def bind_permission(white_url: WhiteUrl):
    """ 创建系统白名单"""
    db = get_mongo()
    try:
        await crud.permission.create_white_url(db, white_url)
    except DuplicateKeyError:
        return Response(msg="白名单已存在！！", status=400)
    return Response(msg="白名单创建成功", status=201)
