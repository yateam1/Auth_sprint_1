from datetime import datetime
from functools import wraps

import jwt
from flask_restx import namespace

from app.api.v1.parsers import headers_parser
from app.models import User
from app.services import UserService, RoleService

user_service = UserService()
role_service = RoleService()


def login_required(method):
    '''
    Проверяем валидность access_token
    :param method:
    :return:
    '''
    @wraps(method)
    def wrapper(*args, **kwargs):
        access_token = headers_parser.parse_args().get('Authorization')
        try:
            User.decode_token(access_token)
        except jwt.exceptions.DecodeError:
            return namespace.abort(404, 'Неверный формат токена.')
        except jwt.exceptions.ExpiredSignatureErro:
            return namespace.abort(404, 'Срок действия токен истек.')

        return method(args, **kwargs)
    return wrapper


def does_user_have_role(role_name):
    '''
    Проверяем принадлежность пользователя роли.
    Данный декоратор применять после декоратора login_required.
    :param role_name:
    :return:
    '''
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            access_token = headers_parser.parse_args().get('Authorization')
            decode_token = User.decode_token(access_token)
            if role_name not in decode_token['roles']:
                return namespace.abort(404, f'Пользователю не назначена роль {role_name}')

            return method(args, **kwargs)
        return wrapper
    return decorator
