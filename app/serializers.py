from flask_marshmallow import Marshmallow
from app.models import DIDNumber

ma = Marshmallow()

def configure(app):
    ma.init_app(app)


class DIDNumberSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = DIDNumber
        load_instance = True