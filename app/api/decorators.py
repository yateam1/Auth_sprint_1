from datetime import datetime
from functools import wraps

from app.models import User
from app.services import SessionService, UserService

user_service = UserService()
session_service = SessionService()


def login_required(namespace, parser):

    def is_user_login(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            '''
            Проверяем валидность access_token
            :param args:
            :param kwargs:
            :return:
            '''

            args = parser.parse_args()
            access_token = args.get('Authorization')
            fingerprint = args.get('Fingerprint')
            user_agent = args.get('User-Agent')

            user_id = User.decode_token(access_token)['user_id']

            user = user_service.get_by_pk(user_id)
            if not user:
                namespace.abort(404, f'Пользователя не существует.')

            session = session_service.get_by_user(user, fingerprint, user_agent)
            if not session:
                namespace.abort(404, f'У пользователя нет активной сессии на этом устройстве.')

            now = datetime.utcnow()
            expired = user.decode_token(access_token)['exp']

            if expired <= now:
                namespace.abort(404, f'Срок действия access_token истек. Нужно залогиниться')

            return func(args, **kwargs)
        return wrapper

    return is_user_login
