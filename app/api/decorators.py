import jwt

from datetime import datetime
from functools import wraps

from app.models import User
from app.services import UserService, SessionService

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
            return False

        user_id = decode_token['user_id']
        expired = decode_token['exp']

        user = user_service.get_by_pk(user_id)
        if not user or expired <= datetime.utcnow():
            return False

        return method(args, **kwargs)
    return wrapper

