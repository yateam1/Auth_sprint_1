from uuid import uuid4

from flask import request
from flask_restx import Namespace, Resource, fields

from .parsers import headers_parser
from app.bcrypt import bcrypt
from app.services import SessionService, UserService, JWTService, AuthService


auth_namespace = Namespace('auth')

user_service = UserService()
session_service = SessionService()
auth_service = AuthService()

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

tokens = auth_namespace.clone(
    'Access and refresh tokens', refresh_token, {'access_token': fields.String(required=True)}
)


class Register(Resource):
    @auth_namespace.marshal_with(user)
    @auth_namespace.expect(user_with_password, validate=True)
    @auth_namespace.response(201, 'Успех.')
    @auth_namespace.response(400, 'Пользователь уже зарегистрирован.')
    def post(self):
        """Регистрация нового пользователя."""
        auth_service.register()


class Auth(Resource):
    @auth_namespace.marshal_with(tokens)
    @auth_namespace.expect(login, validate=True)
    @auth_namespace.response(200, 'Успех.')
    @auth_namespace.response(400, 'Не переданы обязательные заголовки.')
    @auth_namespace.response(401, 'Пользователь уже залогинен на этом устройстве.')
    @auth_namespace.response(404, 'Пользователя не существует.')
    def post(self):
        """Аутентификация пользователя."""
        return auth_service.auth()


class Refresh(Resource):
    @auth_namespace.marshal_with(tokens)
    @auth_namespace.expect(refresh_token, validate=True)
    @auth_namespace.response(201, 'Успех')
    @auth_namespace.response(400, 'Не переданы обязательные заголовки.')
    @auth_namespace.response(400, 'Refresh-токен истек, либо не существует')
    def post(self):
        """Генерация новых access и refresh токенов в обмен на корректный refresh-токен"""
        return auth_service.refresh()


auth_namespace.add_resource(Register, '/register')
auth_namespace.add_resource(Auth, '/login')
auth_namespace.add_resource(Refresh, '/refresh')
