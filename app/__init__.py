from flask import Flask
from flask_migrate import Migrate
from app.models import configure as config_db
from app.serializers import configure as config_serializer

def create_app(testing_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if testing_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/dev.db'
    else:
        app.config.from_mapping(testing_config)
    config_db(app)
    config_serializer(app)
    Migrate(app, app.db)

    from app.views.numbers import bp_number
    app.register_blueprint(bp_number)
    return app