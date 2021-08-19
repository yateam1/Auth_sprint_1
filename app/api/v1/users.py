from flask import request
from flask_restx import Namespace, Resource, fields

from app.services import UserService

service = UserService()
users_namespace = Namespace('users')


user = users_namespace.model(
    'User',
    {
        'id': fields.String(readOnly=True),
        'username': fields.String(required=True),
        'created_at': fields.DateTime(readOnly=True),
        'updated_at': fields.DateTime(readOnly=True),
        'active': fields.Boolean(),
        'is_super': fields.Boolean(readOnly=True),
    },
)

user_post = users_namespace.inherit(
    'User post', user, {'password': fields.String(required=True)}
)


class UserList(Resource):
    @users_namespace.marshal_with(user, as_list=True)
    def get(self):
        """Возвращает список всех пользователей."""
        return service.get_all(), 200

    @users_namespace.expect(user_post, validate=True)
    @users_namespace.response(201, 'Добавлен новый пользователь <user_username>.')
    @users_namespace.response(400, 'Пользователь уже зарегистрирован.')
    def post(self):
        """Добавляет нового пользователя."""
        post_data = request.get_json()
        user_data = service.model.filter_kwargs(data=post_data, exclude=['id', 'created_at', 'updated_at'])

        response_object = {}

        user = service.get_user_by_username(user_data.get('username'))
        if user:
            response_object['message'] = 'Такой пользователь уже зарегистрирован.'
            return response_object, 400

        service.create(**user_data)
        response_object['message'] = f'Пользователь {user_data["username"]} добавлен.'
        return response_object, 201


class UserDetail(Resource):
    @users_namespace.marshal_with(user)
    @users_namespace.response(200, 'Успех.')
    @users_namespace.response(404, 'Пользователя <user_id> не существует.')
    def get(self, user_id):
        """Возвращает одного пользователя."""
        user = service.get_by_pk(user_id)
        if not user:
            users_namespace.abort(404, f'Пользователя {user_id} не существует.')
        return user, 200


users_namespace.add_resource(UserList, '')
users_namespace.add_resource(UserDetail, '/<user_id>')
