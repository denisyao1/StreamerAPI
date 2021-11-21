from __future__ import annotations

from sqlalchemy.sql import func

from .db import db


class StreamerModel(db.Model):
    __tablename__ = 'streamer'

    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    profile_picture_url = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DATETIME(timezone=True), default=func.now())

    def __init__(self, platform: str, username: str, profile_picture_url: str):
        self.platform = platform
        self.username = username
        self.profile_picture_url = profile_picture_url

    def __repr__(self) -> str:
        return f"<streamer {self.id} - {self.platform} - {self.username}>"

    @classmethod
    def find_by_username(cls, username: str) -> StreamerModel:
        return cls.query.filter_by(username=username).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
