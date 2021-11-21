from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from app.models.db import db
from app.resources.streamer import StreamerList, Streamer
from app.schemas.ma import ma
from app.load_env import load_env

app = Flask(__name__)
app.config.from_object('app.config.Dev')
api = Api(app)
migrate = Migrate(app, db)
db.init_app(app)
ma.init_app(app)

# load env file
load_env()

# link resources to url
api.add_resource(StreamerList, '/streamers/')
api.add_resource(Streamer, '/streamers/<string:username>')

if __name__ == '__main__':
    app.run()
