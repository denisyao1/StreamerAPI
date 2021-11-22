from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from app.models.db import db
from app.resources.streamer import StreamerList, Streamer
from app.schemas.ma import ma
from app.load_env import load_env

app = Flask(__name__)
app.config.from_object('app.config.Development')
api = Api(app)
migrate = Migrate(app, db)
db.init_app(app)
ma.init_app(app)

# load env file
load_env()

# link resources to url
api.add_resource(StreamerList, '/streamers/')
api.add_resource(Streamer, '/streamers/<string:username>')


# sanity check route
@app.route('/')
def hello_world():
    return 'Welcome to streamerAPI v1.0'


# create all table before first request
@app.before_first_request
def db_create_all():
    with app.app_context():
        db.metadata.drop_all(bind=db.engine)
        db.metadata.create_all(bind=db.engine)
        db.session.commit()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
