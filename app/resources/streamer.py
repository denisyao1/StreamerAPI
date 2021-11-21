from traceback import print_exc

from flask_restful import Resource
from marshmallow.exceptions import ValidationError

from app.models.streamer import StreamerModel
from app.schemas.streamer import StreamerSchema
from app.services.twitch import TwitchService


class StreamerList(Resource):
    """
   Define the routing of HTTP methods for /streamers/ url.
    """
    streamer_list_schema = StreamerSchema(many=True)

    @classmethod
    def get(cls):
        """
        Implements HTTP get method.
        :return: json list of streamers
        """
        return cls.streamer_list_schema.dump(StreamerModel.query.all())


class Streamer(Resource):
    """
    Define the routing of HTTP methods for /streamers/<string:username> url.
    """
    streamer_schema = StreamerSchema()
    twitch_service = TwitchService()

    @classmethod
    def get(cls, username):
        """
        Implements HTTP get method.
        :param username: the streamer username
        :return: Information about the streamer
        """
        return cls.streamer_schema.dump(StreamerModel.find_by_username(username))

    @classmethod
    def post(cls, username: str):
        """
        Implements HTTP post method. Add new streamer to database.
        :param username: the streamer username
        :return: Information about streamer
        """
        if StreamerModel.find_by_username(username):
            return {'message': f'{username} already exits in the database.'}, 400
        try:
            resp_json = cls.twitch_service.retrieve_user_info(username)
            if not resp_json:
                return {}
            new_streamer: StreamerModel = cls.streamer_schema.load(resp_json)
            new_streamer.save_to_db()
        except ValidationError as e:
            print_exc()
            return e.messages, 404
        except Exception as e:
            print_exc()
            return str(e), 500
        return cls.streamer_schema.dump(new_streamer), 201

    @classmethod
    def delete(cls, username: str):
        """
        Implements delete HTTp method. Delete streamer from database
        :param username: the streamer username
        :return: success message
        """
        streamer: StreamerModel = StreamerModel.find_by_username(username)
        if streamer:
            streamer.delete()
        return {'message': 'streamer deleted'}
