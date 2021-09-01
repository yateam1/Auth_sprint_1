from typing import Iterable
import secrets
import string

from app.models import Profile, User
from app.services.base import AbstractService


class ProfileService(AbstractService):
    model = Profile

    def get_by_email(self, email: str):
        """Возвращает профиль пользователя с почтой email."""
        return self.model.query.filter_by(email=email).first()


class UserService(AbstractService):
    model = User

    @staticmethod
    def generate_password():
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        return password

    def get_user_by_username(self, username: str):
        """Возвращает пользователя с юзернеймом username."""
        return self.model.query.filter_by(username=username).first()

    def get_by_usernames(self, usernames: Iterable):
        """Возвращает пользователей с совпадающими username с usernames."""
        return self.model.query.filter(self.model.username.in_(usernames))

    def create(self, **kwargs):
        user = super().create(**kwargs)
        profile_service = ProfileService()
        profile_service.create(user=user, **kwargs)
        return user

    def update(self, user, **kwargs):
        if kwargs.get('password'):
            kwargs['password'] = user.hash_password(kwargs['password'])
        return super().update(user, **kwargs)
