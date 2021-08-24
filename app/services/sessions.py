from datetime import datetime, timedelta

from app.models import History, Session, User
from app.services.base import AbstractService
from app.settings import config


class HistoryService(AbstractService):
    model = History

    def get_by_user(self, user: User) -> Session:
        """Возвращает историю логинов указанного пользователя."""
        return self.model.query.filter_by(user=user)


history_service = HistoryService()


class SessionService(AbstractService):
    model = Session

    def create(self, **kwargs):
        kwargs['expired'] = datetime.utcnow() + timedelta(seconds=config('REFRESH_TOKEN_EXPIRATION', cast=int))
        session = super().create(**kwargs)
        history_service.create(**kwargs)
        return session

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
