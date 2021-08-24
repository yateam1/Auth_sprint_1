from app.models import Role, users_roles_association
from app.services.base import AbstractService


class RoleService(AbstractService):
    model = Role

    def get_role_by_name(self, name: str):
        """Возвращает пользователя с юзернеймом username."""
        return self.model.query.filter_by(name=name).first()

    def is_user_equ_role(self, role, user):
        return users_roles_association.query.filter_by(user_id=user.id, role_id=role.id).first()
