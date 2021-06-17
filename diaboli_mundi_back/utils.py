import datetime

import jwt
from fastapi import Header, HTTPException

from diaboli_mundi_back.settings import settings

SYSTEM_PRIVATE_KEY = settings.system_private_key_path.read_bytes()
SYSTEM_PUBLIC_KEY = settings.system_public_key_path.read_bytes()


def generator_private_api_token(payload, hour_age):
    payload.update({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=hour_age)
    })
    return jwt.encode(payload, SYSTEM_PRIVATE_KEY, algorithm='RS256')


async def decode_private_api_token(token: str = Header(...)):
    try:
        payload = jwt.decode(token, key=SYSTEM_PUBLIC_KEY, algorithms='RS256')
        return payload
    except Exception as e:
        print(f'invalid private token: {e}, {token}')
