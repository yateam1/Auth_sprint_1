from app.services.base import AbstractService
from app.models import Role


class RoleService(AbstractService):
    model = Role

    def get_role_by_name(self, name: str):
        """Возвращает пользователя с юзернеймом username."""
        return self.model.query.filter_by(name=name).first()
