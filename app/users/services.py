from app.services import AbstractService
from app.users.models import User


class UserService(AbstractService):
    model = User
