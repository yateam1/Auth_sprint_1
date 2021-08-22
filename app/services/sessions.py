from datetime import datetime, timedelta

from app.models import Session
from app.services.base import AbstractService
from app.models import User
from app.settings import config


class SessionService(AbstractService):
    model = Session

    def create(self, **kwargs):
        kwargs['expired'] = datetime.utcnow() + timedelta(seconds=config('REFRESH_TOKEN_EXPIRATION', cast=int))
        return super().create(**kwargs)

    def get_by_user(self, user: User, fingerprint: str, user_agent: str) -> Session:
        """Возвращает сессию указанного пользователя."""
        now = datetime.utcnow()
        return self.model.query.filter(
            self.model.user == user,
            self.model.user_agent == user_agent,
            self.model.fingerprint == fingerprint,
            self.model.expired >= now
        ).first()

    def get_by_refresh_token(
            self,
            refresh_token: str,
            fingerprint:str,
            user_agent: str,
    ):
        """Возвращает сессию по рефреш токену."""
        now = datetime.utcnow()
        return self.model.query.filter(
            self.model.refresh_token == refresh_token,
            self.model.user_agent == user_agent,
            self.model.fingerprint == fingerprint,
            self.model.expired >= now
        ).first()
