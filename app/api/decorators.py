import jwt

from datetime import datetime
from functools import wraps

from app import api
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
        access_token = api.users_parser.parse_args().get('Authorization')
        try:
            decode_token = User.decode_token(access_token)
        except jwt.exceptions.DecodeError:
            return api.users_namespace.abort(404, 'Неверный формат токена.')

        user_id = decode_token['user_id']
        expired = decode_token['exp']

        user = user_service.get_by_pk(user_id)
        if not user:
            return api.users_namespace.abort(404, f'Пользователя {user.username} не существует.')
        if expired <= datetime.utcnow():
            return api.users_namespace.abort(404, 'Срок access токена истек. Нужно залогиниться')

        return method(args, **kwargs)
    return wrapper


def user_role(role_name):
    '''
    Проверяем принадлежность пользователя роли
    :param role_name:
    :return:
    '''
    def decorator(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            access_token = api.users_parser.parse_args().get('Authorization')
            decode_token = User.decode_token(access_token)
            user_id = decode_token['user_id']
            user = user_service.get_by_pk(user_id)
            role = role_service.get_role_by_name(role_name)

            if not role_service.is_user_equ_role(role=role, user=user):
                return api.users_namespace.abort(404, f'Пользователю не назначена роль {role_name}')

            return method(args, **kwargs)
        return wrapper
    return decorator
