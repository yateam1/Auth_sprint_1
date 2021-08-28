from uuid import uuid4

from flask import request
from flask_restx import Namespace, Resource, fields

from .parsers import headers_parser
from app.services import SessionService, UserService


auth_namespace = Namespace('auth')

user_service = UserService()
session_service = SessionService()

user = auth_namespace.model(
    'User',
    {
        'username': fields.String(required=True),
    },
)

user_with_password = auth_namespace.clone(
    'User with password', user, {
        'password': fields.String(required=True),
        'email': fields.String(required=True),
    }
)

login = auth_namespace.model(
    'Login User',
    {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
    },
)

refresh_token = auth_namespace.model(
    'Refresh token', {'refresh_token': fields.String(required=True)}
)

tokens = auth_namespace.model(
    'Access and refresh tokens',
    {
        'refresh_token': fields.String(required=True),
        'access_token': fields.String(required=True)
    }
)


class Register(Resource):
    @auth_namespace.marshal_with(tokens)
    @auth_namespace.expect(user_with_password, validate=True)
    @auth_namespace.response(201, 'Успех.')
    @auth_namespace.response(400, 'Пользователь уже зарегистрирован.')
    def post(self):
        """Регистрация нового пользователя."""

        # Проверяем зоголовки
        args = headers_parser.parse_args()
        fingerprint = args.get('Fingerprint')
        user_agent = args.get('User-Agent')
        if not all((fingerprint, user_agent)):
            auth_namespace.abort(400, 'Не переданы обязательные заголовки.')

        # Проверяем тело запроса, формируем пользователя
        post_data = request.get_json()

        user = user_service.get_user_by_username(post_data.get('username'))
        if user:
            auth_namespace.abort(400, f'Пользователь {post_data["username"]} уже зарегистрирован.')
        user = user_service.create(**post_data)

        # Заводим для нового пользователя сессию
        access_token = user.encode_token()
        refresh_token = str(uuid4())
        session = {
            'refresh_token': refresh_token,
            'user': user,
            'fingerprint': fingerprint,
            'user_agent': user_agent,
        }
        session_service.create(**session)

        response = {'access_token': access_token, 'refresh_token': refresh_token}
        return response, 201


class Auth(Resource):
    @auth_namespace.marshal_with(tokens)
    @auth_namespace.expect(login, validate=True)
    @auth_namespace.response(200, 'Успех.')
    @auth_namespace.response(400, 'Не переданы обязательные заголовки.')
    @auth_namespace.response(401, 'Пользователь уже залогинен на этом устройстве.')
    @auth_namespace.response(404, 'Пользователя не существует.')
    def post(self):
        """Аутентификация пользователя."""
        args = headers_parser.parse_args()
        fingerprint = args.get('Fingerprint')
        user_agent = args.get('User-Agent')
        if not all((fingerprint, user_agent)):
            auth_namespace.abort(400, 'Не переданы обязательные заголовки.')

        post_data = request.get_json()
        username = post_data.get('username')
        password = post_data.get('password')

        user = user_service.get_user_by_username(username)
        if not (user and user.check_password(password)):
            auth_namespace.abort(404, 'Неверный пароль.')

        access_token = user.encode_token()
        refresh_token = str(uuid4())
        session = {
            'refresh_token': refresh_token,
            'user': user,
            'fingerprint': fingerprint,
            'user_agent': user_agent,
        }
        session_service.create(**session)

        response = {'access_token': access_token, 'refresh_token': refresh_token}
        return response, 200


class Refresh(Resource):
    @auth_namespace.marshal_with(tokens)
    @auth_namespace.expect(refresh_token, validate=True)
    @auth_namespace.response(201, 'Успех')
    @auth_namespace.response(400, 'Не переданы обязательные заголовки.')
    @auth_namespace.response(400, 'Refresh-токен истек, либо не существует')
    def post(self):
        """Генерация новых access и refresh токенов в обмен на корректный refresh-токен"""
        args = headers_parser.parse_args()
        fingerprint = args.get('Fingerprint')
        user_agent = args.get('User-Agent')
        if not all((fingerprint, user_agent)):
            auth_namespace.abort(400, 'Не переданы обязательные заголовки.')

        post_data = request.get_json()
        refresh_token = post_data.get('refresh_token')

        session = session_service.get_by_refresh_token(refresh_token=refresh_token,
                                                       fingerprint=fingerprint,
                                                       user_agent=user_agent)
        if not session:
            auth_namespace.abort(400, 'Refresh-токен истек, либо не существует. Нужно залогиниться')
        access_token = session.user.encode_token()
        session_service.delete(session)
        new_refresh_token = str(uuid4())

        session = {
            'refresh_token': new_refresh_token,
            'user': session.user,
            'fingerprint': fingerprint,
            'user_agent': user_agent,
        }
        session_service.create(**session)

        response = {'access_token': access_token, 'refresh_token': new_refresh_token}
        return response, 201


auth_namespace.add_resource(Register, '/register')
auth_namespace.add_resource(Auth, '/login')
auth_namespace.add_resource(Refresh, '/refresh')
