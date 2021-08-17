from app import db
from app.mixins import TimestampWithUUIDMixin


class Session(TimestampWithUUIDMixin, db.Model):
    __tablename__ = 'sessions'

    fingerprint = db.Column(db.String(255), nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255), nullable=False)
    is_removed = db.Column(db.Boolean(), default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", uselist=False, back_populates='sessions')
