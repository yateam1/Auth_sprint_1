from app.users.models import User
from app.services import AbstractService


class UserService(AbstractService):
    model = User
