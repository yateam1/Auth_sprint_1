from datetime import datetime

from app.models import Social
from app.services.base import AbstractService


class SocialService(AbstractService):
    model = Social