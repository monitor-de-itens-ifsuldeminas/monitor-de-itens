from app.database import db
from datetime import datetime, timezone

class UidBuffer(db.Model):
    __tablename__ = "uid_buffer"

    id      = db.Column(db.Integer, primary_key=True)
    uid     = db.Column(db.String(50), nullable=False)
    lido_em = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))