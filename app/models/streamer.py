from __future__ import annotations

from sqlalchemy.sql import func

from .db import db


class StreamerModel(db.Model):
    """
    Streamer Database's table  SQLAlchemy schema.
    """
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
        """
        Represent streamer instance as a string.
        """
        return f"<streamer {self.id} - {self.platform} - {self.username}>"

    @classmethod
    def find_by_username(cls, username: str) -> StreamerModel:
        """
        Get streamer by it's username.
        """
        return cls.query.filter_by(username=username).first()

    def save_to_db(self) -> None:
        """
        Save streamer instance to database.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        """
        Delete streamer instance from database.
        """
        db.session.delete(self)
        db.session.commit()
