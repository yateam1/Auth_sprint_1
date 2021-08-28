from typing import Optional
from datetime import datetime, timedelta

import jwt

from app.settings import config
from app.models import User


class JWTService:

    @staticmethod
    def decode_token(token: str) -> dict:
        return jwt.decode(token, config("SECRET_KEY"), algorithms="HS256")

    @staticmethod
    def encode_token(user: Optional[User] = None, **kwargs) -> str:
        data = {
            'user_id': str(user.id),
            'roles': [role.name for role in user.roles],
            'is_super': user.is_super,
        } if user else kwargs

        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=config('ACCESS_TOKEN_EXPIRATION', cast=int)),
            'iat': datetime.utcnow(),
            **data,
        }
        return jwt.encode(
            payload, config('SECRET_KEY'), algorithm='HS256'
        )


