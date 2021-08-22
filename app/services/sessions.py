from datetime import datetime

from app.db import db
from app.services.base import AbstractService
from app.models import Session


class SessionService(AbstractService):
    model = Session

    def get_by_user(self, user, fingerprint: str, user_agent: str):
        """Возвращает сессию указанного пользователя."""
        now = datetime.utcnow()
        return self.model.query.filter(
            self.model.user == user,
            self.model.user_agent == user_agent,
            self.model.fingerprint == fingerprint,
            self.model.expired >= now
        ).first()

    def get_by_refresh_token(self, refresh_token, fingerprint: str, user_agent: str):
        """Возвращает сессию по рефреш токену."""
        exp_date = self.model.decode_token(refresh_token).get('exp')
        instance = self.model.query.filter(
            self.model.refresh_token == refresh_token,
            self.model.user_agent == user_agent,
            self.model.fingerprint == fingerprint,
        ).first()
        now = datetime.utcnow()

        return instance if datetime.utcfromtimestamp(exp_date) >= now else None

    def delete(self, instance):
        instance.expired = datetime.utcnow()
        db.session.commit()
        return instance



