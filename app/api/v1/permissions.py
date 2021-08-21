from flask import request
from flask_restx import Namespace, Resource, fields

from app.models import User
from app.services import RoleService

role_service = RoleService()
permissions_namespace = Namespace('permissions')

role = permissions_namespace.model(
    'Role',
    {
        'id': fields.String(readOnly=True),
        'name': fields.String(required=True),
        # 'users': fields.List(User, default=list),
        'created_at': fields.DateTime(readOnly=True),
        'updated_at': fields.DateTime(readOnly=True),
    },
)


class RoleList(Resource):
    @permissions_namespace.marshal_with(role, as_list=True)
    def get(self):
        """Список всех ролей."""
        return role_service.get_all(), 200

    @permissions_namespace.expect(role, validate=True)
    @permissions_namespace.response(201, 'Добавлена новая роль <role_name>.')
    @permissions_namespace.response(400, 'Роль уже существует.')
    def post(self):
        """Добавление новой роли."""
        post_data = request.get_json()
        role_data = role_service.model.filter_kwargs(data=post_data, exclude=['id', 'created_at', 'updated_at'])

        response = {}

        role = role_service.get_role_by_name(role_data.get('name'))
        if role:
            response['message'] = f'Роль с именем {role_data["name"]} уже существует.'
            return response, 400

        role_service.create(**role_data)
        response['message'] = f'Роль {role_data["name"]} добавлена.'
        return response, 201


class RoleDetail(Resource):
    @permissions_namespace.marshal_with(role)
    @permissions_namespace.response(200, 'Успех.')
    @permissions_namespace.response(404, 'Роли <role_id> не существует.')
    def get(self, role_id):
        """Возвращает одну роль."""
        role = role_service.get_by_pk(role_id)
        if not role:
            permissions_namespace.abort(404, f'Роли {role_id} не существует.')
        return role, 200


permissions_namespace.add_resource(RoleList, '/roles')
permissions_namespace.add_resource(RoleDetail, '/roles/<role_id>')
