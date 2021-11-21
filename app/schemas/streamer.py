from .ma import ma
from app.models.streamer import StreamerModel


class StreamerSchema(ma.SQLAlchemyAutoSchema):
    """
    Marshmallow Schema class of Streamer database's Model
    """
    class Meta:
        model = StreamerModel
        fields = ('platform', 'username', 'profile_picture_url')
        load_instance = True
