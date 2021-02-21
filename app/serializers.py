from flask_marshmallow import Marshmallow
from flask_marshmallow.fields import fields
from app.models import DIDNumber

ma = Marshmallow()

def configure(app):
    ma.init_app(app)


class DIDNumberSchema(ma.SQLAlchemyAutoSchema):
    monthy_price = fields.Float()
    setup_price = fields.Float()

    class Meta:
        model = DIDNumber
        load_instance = True