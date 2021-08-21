from uuid import uuid4
from flask import request
from flask_restx import Namespace, Resource, fields

from app.bcrypt import bcrypt
from app.services import UserService, SessionService


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
        'fingerprint': fields.String(required=True),
        'user_agent': fields.String(required=True),
    },
)

refresh = auth_namespace.model(
    'Refresh token', {'refresh_token': fields.String(required=True)}
)

tokens = auth_namespace.clone(
    'Access and refresh tokens', refresh, {'access_token': fields.String(required=True)}
)

parser = auth_namespace.parser()
parser.add_argument('Authorization', location='headers')


class Register(Resource):
    @auth_namespace.marshal_with(user)
    @auth_namespace.expect(user_with_password, validate=True)
    @auth_namespace.response(201, 'Успех.')
    @auth_namespace.response(400, 'Пользователь уже зарегистрирован.')
    def post(self):
        """Регистрация нового пользователя."""
        post_data = request.get_json()
        # user_data = user_service.model.filter_kwargs(data=post_data, exclude=['id', 'created_at', 'updated_at'])
        user_data = post_data

        user = user_service.get_user_by_username(user_data.get('username'))
        if user:
            auth_namespace.abort(400, f'Пользователь {user_data["username"]} уже зарегистрирован.')
        user = user_service.create(**user_data)

        return user, 201


class Auth(Resource):
    @auth_namespace.marshal_with(tokens)
    @auth_namespace.expect(login, validate=True)
    @auth_namespace.response(200, 'Успех.')
    @auth_namespace.response(404, 'Пользователя не существует.')
    def post(self):
        """Аутентификация пользователя."""
        post_data = request.get_json()
        username = post_data.get('username')
        password = post_data.get('password')
        user = user_service.get_user_by_username(username)
        if not user:
            auth_namespace.abort(404, 'Пользователя не существует.')
        if not bcrypt.check_password_hash(user.password, password):
            auth_namespace.abort(404, 'Неверный пароль.')
        access_token = user.encode_token()
        refresh_token = str(uuid4())
        session = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user,
            'fingerprint': post_data.get('fingerprint'),
            'user_agent': post_data.get('user_agent'),
        }
        session_service.create(**session)

        response = {'access_token': access_token, 'refresh_token': refresh_token}
        return response, 200


class RefreshTokens(Resource):
    # @auth_namespace.marshal_with(user)
    # @auth_namespace.expect(user_with_password, validate=True)
    @auth_namespace.response(201, 'Успех')
    @auth_namespace.response(400, 'Refresh-токен истек, либо не существует')
    def post(self):
        """Генерация новых access и refresh токенов в обмен на корректный refresh-токен"""
        post_data = request.get_json()
        refresh_token = post_data.get('refresh_token')
        fingerprint = post_data.get('fingerprint')
        session = SessionService.get(refresh_token=refresh_token, fingerprint=fingerprint)

        if not session:
            auth_namespace.abort(400, 'Refresh-токен истек, либо не существует')

        SessionService.delete(session)
        access_token = user.encode_token()
        refresh_token = str(uuid4())
        session = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user,
            'fingerprint': post_data.get('fingerprint'),
            'user_agent': post_data.get('user_agent'),
        }
        session_service.create(**session)

        response = {'access_token': access_token, 'refresh_token': refresh_token}
        return response, 200


auth_namespace.add_resource(Register, '/register')
auth_namespace.add_resource(Auth, '/login')
auth_namespace.add_resource(RefreshTokens, '/refresh-tokens')
