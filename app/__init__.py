from flask import Flask
from flask_migrate import Migrate
from app.models import configure as config_db
from app.serializers import configure as config_serializer

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/dev.db' 
    config_db(app)
    config_serializer(app)
    Migrate(app, app.db)

    from app.views.numbers import bp_number
    app.register_blueprint(bp_number)
    return app