from app.services.base import AbstractService
from app.models import User


class UserService(AbstractService):
    model = User
