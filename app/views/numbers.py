from flask import Blueprint, current_app, request, jsonify
from app.serializers import DIDNumberSchema
from app.models import DIDNumber

bp_number = Blueprint('numbers', __name__, url_prefix='/numbers')

@bp_number.route('/', methods=['GET'])
def list_numbers():
    serializer = DIDNumberSchema(many=True)
    results = DIDNumber.query.all()
    return serializer.jsonify(results), 200