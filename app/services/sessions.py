from datetime import datetime

from app.services.base import AbstractService
from app.models import Session


class SessionService(AbstractService):
    model = Session

    def get(self, user, fingerprint: str, user_agent: str):
        """Возвращает пользователя с юзернеймом username."""
        now = datetime.utcnow()
        return self.model.query.filter(
            self.model.user == user,
            self.model.user_agent == user_agent,
            self.model.fingerprint == fingerprint,
            self.model.expired >= now
        ).first()

