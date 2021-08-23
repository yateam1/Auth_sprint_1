from typing import NamedTuple
from datetime import datetime, timedelta
from uuid import uuid4

import factory
import factory.random
import factory.fuzzy

from app.db import db
from app.settings import config
from app.models import Profile, Role, Session, User

factory.random.reseed_random(0)


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session

    id = factory.LazyFunction(uuid4)
    created = factory.LazyFunction(datetime.now)
    updated = None


class RoleFactory(BaseFactory):
    class Meta:
        model = Role
        sqlalchemy_session = db.session

    name = factory.Faker('job')


class UserFactory(BaseFactory):
    class Meta:
        model = User
        inline_args = ('password',)
        sqlalchemy_session = db.session

    username = factory.Faker('user_name')
    active = True
    is_super = False


class ProfileFactory(BaseFactory):
    class Meta:
        model = Profile
        sqlalchemy_session = db.session

    email = factory.LazyAttribute(lambda obj: f'{obj.user.username}@example.com')
    user = factory.SubFactory(UserFactory)


class SessionFactory(BaseFactory):
    class Meta:
        model = Session
        sqlalchemy_session = db.session

    fingerprint = factory.fuzzy.FuzzyText(length=48, prefix='fingerprint_')
    user_agent = factory.Faker('user_agent')
    user = factory.SubFactory(UserFactory)
    refresh_token = factory.fuzzy.FuzzyText(length=12, prefix='refresh_')
    expired = datetime.utcnow() + timedelta(seconds=config('REFRESH_TOKEN_EXPIRATION', cast=int))


class AuthHeaders(NamedTuple):
    fingerprint: str
    user_agent: str

    @property
    def headers(self):
        return {'Fingerprint': self.fingerprint, 'User-Agent': self.user_agent}


class HeaderFactory(factory.Factory):
    class Meta:
        model = AuthHeaders
    fingerprint = factory.fuzzy.FuzzyText(length=48, prefix='fingerprint_')
    user_agent = factory.Faker('user_agent')
