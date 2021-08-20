from datetime import datetime, timedelta

import jwt
from sqlalchemy.dialects.postgresql import UUID

from app.bcrypt import bcrypt
from app.db import db
from app.mixins import BaseModel
from app.settings import config


users_roles_association = db.Table(
    "users_roles",
    db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("users.id")),
    db.Column("role_id", UUID(as_uuid=True), db.ForeignKey("roles.id")),
)


class User(BaseModel, db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    is_super = db.Column(db.Boolean(), default=False, nullable=False)
    profile = db.relationship("Profile", uselist=False, back_populates="user")
    roles = db.relationship("Role",
                            secondary=users_roles_association,
                            back_populates="users")
    sessions = db.relationship("Session", back_populates="user")

    def __init__(self, password: str, **kwargs):
        super().__init__(**kwargs)
        self.password = bcrypt.generate_password_hash(password).decode()

    @staticmethod
    def decode_token(token):
        return jwt.decode(token, config("SECRET_KEY"), algorithms="HS256")

    def encode_token(self):
        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=config('ACCESS_TOKEN_EXPIRATION', cast=int)),
            'iat': datetime.utcnow(),
            'user_id': str(self.id),
            'roles': self.roles,
            'is_super': self.is_super,
        }
        return jwt.encode(
            payload, config('SECRET_KEY'), algorithm='HS256'
        )


class Profile(BaseModel, db.Model):
    __tablename__ = 'profiles'

    email = db.Column(db.String(128), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='profile')


class Session(BaseModel, db.Model):
    __tablename__ = 'sessions'

    fingerprint = db.Column(db.String(255), nullable=False)
    user_agent = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"))
    user = db.relationship('User', uselist=False, back_populates='sessions')
    expired = db.Column(db.DateTime, nullable=False)


class Role(BaseModel, db.Model):
    __tablename__ = 'roles'

    name = db.Column(db.String(128), nullable=False, unique=True)
    users = db.relationship('User',
                            secondary=users_roles_association,
                            back_populates='roles')
