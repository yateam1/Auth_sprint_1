from app import db
from app.mixins import TimestampWithUUIDMixin
from app.users.models import users_roles_association


class Role(TimestampWithUUIDMixin, db.Model):
    __tablename__ = 'roles'

    name = db.Column(db.String(128), nullable=False, unique=True)
    users = db.relationship("User", secondary=users_roles_association, back_populates="chats")