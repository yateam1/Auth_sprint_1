from datetime import datetime
from uuid import uuid4

import factory
import factory.random

from app.db import db
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

    fingerprint = factory.LazyFunction(uuid4)
    user_agent = factory.Faker('user_agent')
    user = factory.SubFactory(UserFactory)

