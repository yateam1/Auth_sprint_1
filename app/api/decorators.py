import jwt

from datetime import datetime
from functools import wraps

from app import api
from app.models import User
from app.services import UserService

user_service = UserService()


def login_required(method):
    '''
    Проверяем валидность access_token
    :param method:
    :return:
    '''
    access_token = getattr(method, 'Authorization', None)

    @wraps(method)
    def wrapper(*args, **kwargs):
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

