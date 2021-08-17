from app import bcrypt, db
from app.mixins import TimestampWithUUIDMixin
from app.settings import config


users_roles_association = db.Table(
    "users_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
)


class User(TimestampWithUUIDMixin, db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    is_super = db.Column(db.Boolean(), default=False, nullable=False)
    profile = db.relationship("Profile", uselist=False, back_populates="user")
    roles = db.relationship("Role", secondary=users_roles_association, back_populates="users")
    sessions = db.relationship("Session", back_populates="user")

    def __init__(self, password: str, **kwargs):
        super().__init__(**kwargs)
        self.password = bcrypt.generate_password_hash(password).decode()


class Profile(TimestampWithUUIDMixin, db.Model):
    __tablename__ = 'profiles'

    email = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="profile")


if config("FLASK_ENV") == "development":
    from app import admin
    from app.users.admin import UsersAdminView

    admin.add_view(UsersAdminView(User, db.session))


