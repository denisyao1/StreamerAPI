from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from app.models.db import db
from app.schemas.ma import ma
from app.resources.sample import HelloWorld
from app.models.streamer import StreamerModel
from app.schemas.streamer import StreamerSchema
from app.resources.streamer import StreamerList

app = Flask(__name__)
app.config.from_object('app.config.Dev')
api = Api(app)
migrate = Migrate(app, db)
db.init_app(app)
ma.init_app(app)

api.add_resource(HelloWorld, '/hello')
# api.add_resource(StreamerList, '/streamers')

if __name__ == '__main__':
    app.run()
