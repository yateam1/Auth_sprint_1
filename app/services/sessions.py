from app.models import Session
from app.services.base import AbstractService


class SessionService(AbstractService):
    model = Session
