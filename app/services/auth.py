from typing import Optional
from datetime import datetime, timedelta
from uuid import uuid4

from flask import request, make_response, jsonify
import jwt

from app.settings import config
from app.models import User
from app.services.sessions import SessionService
from app.services.users import UserService


session_service = SessionService()
user_service = UserService()


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


def auth_decorator(method_to_decorate):
    def wrapper(self):
        self.get_headers()
        if not all((self.fingerprint, self.user_agent)):
            return make_response(jsonify({'message': 'Не переданы обязательные заголовки.'}), 400)
        method_to_decorate(self)
        return make_response(jsonify(self.generate_tokens(self.user)), 200)
    return wrapper


class AuthService:
    def __init__(self):
        self.fingerprint = None
        self.auth_header = None
        self.user = None
        self.user_agent = None

    def get_headers(self):
        self.fingerprint = request.headers.get('Fingerprint')
        self.user_agent = request.headers.get('User-Agent')
        self.auth_header = request.headers.get('Authorization')

    def generate_tokens(self, user: User):
        access_token = JWTService.encode_token(user=user)
        refresh_token = str(uuid4())
        session = {
            'refresh_token': refresh_token,
            'user': user,
            'fingerprint': self.fingerprint,
            'user_agent': self.user_agent,
        }
        session_service.create(**session)
        return {'access_token': access_token, 'refresh_token': refresh_token}

    @auth_decorator
    def register(self):
        post_data = request.get_json()
        user = user_service.get_user_by_username(post_data.get('username'))
        if user:
            return make_response(jsonify({'message': f'Пользователь {post_data["username"]} уже зарегистрирован.'}), 400)
        self.user = user_service.create(**post_data)

    @auth_decorator
    def auth(self):
        post_data = request.get_json()
        username = post_data.get('username')
        password = post_data.get('password')
        self.user = user_service.get_user_by_username(username)
        if not (self.user and self.user.check_password(password)):
            return make_response(jsonify({'message': 'Неверный пароль.'}), 404)

    @auth_decorator
    def refresh(self):
        post_data = request.get_json()
        refresh_token = post_data.get('refresh_token')
        session = session_service.get_by_refresh_token(refresh_token=refresh_token,
                                                       fingerprint=self.fingerprint,
                                                       user_agent=self.user_agent)
        if not session:
            return make_response(
                jsonify({'message': 'Refresh-токен истек, либо не существует. Нужно залогиниться'}), 400
            )
        self.user = session.user
