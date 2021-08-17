from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from app import db


class TimestampWithUUIDMixin:
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated = db.Column(db.DateTime, onupdate=datetime.utcnow)
