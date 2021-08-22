from datetime import datetime

from app.models import Session
from app.services.base import AbstractService
from app.models import User


class SessionService(AbstractService):
    model = Session

    def get_by_user(self, user: User, fingerprint: str, user_agent: str) -> Session:
        """Возвращает сессию указанного пользователя."""
        now = datetime.utcnow()
        return self.model.query.filter(
            self.model.user == user,
            self.model.user_agent == user_agent,
            self.model.fingerprint == fingerprint,
            self.model.expired >= now
        ).first()
