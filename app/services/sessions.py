from app.services.base import AbstractService
from app.models import Session


class SessionService(AbstractService):
    model = Session
