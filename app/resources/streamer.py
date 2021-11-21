from traceback import print_exc

from flask import request, jsonify
from flask_restful import Resource

from app.schemas.streamer import StreamerSchema
from app.models.streamer import StreamerModel
from marshmallow.exceptions import ValidationError
from app.services.twitch import TwitchAPIService


class StreamerList(Resource):
    streamer_list_schema = StreamerSchema(many=True)

    @classmethod
    def get(cls):
        return cls.streamer_list_schema.dump(StreamerModel.query.all())


class Streamer(Resource):
    streamer_schema = StreamerSchema()
    twitch_service = TwitchAPIService()

    @classmethod
    def get(cls, username):
        return cls.streamer_schema.dump(StreamerModel.find_by_username(username))

    @classmethod
    def post(cls, username: str):
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
        streamer: StreamerModel = StreamerModel.find_by_username(username)
        if streamer:
            streamer.delete()
        return {'message': 'streamer deleted'}
