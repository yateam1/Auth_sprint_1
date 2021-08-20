from datetime import datetime

from app.services.base import AbstractService
from app.models import Session


class SessionService(AbstractService):
    model = Session

    def get(self, refresh_token: str, fingerprint: str):
        """Возвращает пользователя с юзернеймом username."""
        now = datetime.now()
        return self.model.query.filter_by(refresh_token=refresh_token).filter_by(fingerprint=fingerprint).filter_by(expired<=now).first()
