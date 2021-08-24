from flask import request
from flask_restx import Namespace, Resource, fields

from app.api.decorators import login_required
from app.bcrypt import bcrypt
from app.services import UserService

user_service = UserService()
users_namespace = Namespace('users')


user = users_namespace.model(
    'User',
    {
        'id': fields.String(readOnly=True),
        'username': fields.String(required=True),
        'created': fields.DateTime(readOnly=True),
        'updated': fields.DateTime(readOnly=True),
        'active': fields.Boolean(),
        'is_super': fields.Boolean(readOnly=True),
    },
)

user_post = users_namespace.inherit(
    'User post', user, {
        'password': fields.String(required=True),
        'email': fields.String(required=True),
    }
)

passwords = users_namespace.model(
    'Passwords',
    {
        'old_password': fields.String(required=True),
        'new_password': fields.String(required=True),
    },
)

parser = users_namespace.parser()
parser.add_argument('Authorization', location='headers')
parser.add_argument('User-Agent', location='headers')
parser.add_argument('Fingerprint', location='headers')


class UserList(Resource):

    @users_namespace.marshal_with(user, as_list=True)
    def get(self):
        """Возвращает список всех пользователей."""
        return user_service.get_all(), 200

    @users_namespace.expect(user_post, validate=True)
    @users_namespace.response(201, 'Добавлен новый пользователь <user_username>.')
    @users_namespace.response(400, 'Пользователь уже зарегистрирован.')
    def post(self):
        """Добавляет нового пользователя."""
        post_data = request.get_json()
        response_object = {}

        user = user_service.get_user_by_username(post_data.get('username'))
        if user:
            response_object['message'] = 'Такой пользователь уже зарегистрирован.'
            return response_object, 400

        user_service.create(**post_data)
        response_object['message'] = f'Пользователь {post_data["username"]} добавлен.'
        return response_object, 201


class UserDetail(Resource):
    @users_namespace.marshal_with(user)
    @users_namespace.response(200, 'Успех.')
    @users_namespace.response(404, 'Пользователя <user_id> не существует.')
    def get(self, user_id):
        """Возвращает одного пользователя."""
        user = user_service.get_by_pk(user_id)
        if not user:
            users_namespace.abort(404, f'Пользователя {user_id} не существует.')
        return user, 200


class UserSetPassword(Resource):
    @users_namespace.marshal_with(user)
    @users_namespace.expect(passwords, validate=True)
    @users_namespace.response(201, 'Успех.')
    @users_namespace.response(404, 'Пользователя <user_id> не существует.')
    @login_required
    def post(self, user_id):
        """Меняет у пользователя user_id пароль."""
        user = user_service.get_by_pk(user_id)

        post_data = request.get_json()

        old_password = post_data.get('old_password')
        if not bcrypt.check_password_hash(user.password, old_password):
            users_namespace.abort(404, 'Неверный пароль.')

        new_password = post_data.get('new_password')
        user_service.update(user, password=new_password)

        return user, 201


users_namespace.add_resource(UserList, '')
users_namespace.add_resource(UserDetail, '/<user_id>')
users_namespace.add_resource(UserSetPassword, '/<user_id>/change_password')
