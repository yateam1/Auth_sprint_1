from uuid import UUID

from app.bcrypt import bcrypt
from app.models import Profile, User, Role
from app.services.base import AbstractService


class ProfileService(AbstractService):
    model = Profile

    def get_by_email(self, email: str):
        """Возвращает профиль пользователя с почтой email."""
        return self.model.query.filter_by(email=email).first()


class UserService(AbstractService):
    model = User

    def get_user_by_username(self, username: str):
        """Возвращает пользователя с юзернеймом username."""
        return self.model.query.filter_by(username=username).first()

    def create(self, **kwargs):
        user = super().create(**kwargs)
        profile_service = ProfileService()
        profile_service.create(user=user, **kwargs)
        return user

    def update(self, user, **kwargs):
        if kwargs.get('password'):
            kwargs['password'] = bcrypt.generate_password_hash(kwargs['password']).decode()
        return super().update(user, **kwargs)
