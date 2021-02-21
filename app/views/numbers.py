from flask import Blueprint, current_app, request, jsonify
from app.serializers import DIDNumberSchema
from app.models import DIDNumber

bp_number = Blueprint('numbers', __name__, url_prefix='/numbers')

@bp_number.route('/', methods=['GET'])
def list_numbers():
    serializer = DIDNumberSchema(many=True)
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        max_per_page = int(request.args.get('max_per_page', 20))
    except ValueError:
        page = 1
        per_page = 20
        max_per_page = 20

    results = DIDNumber.query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=True, 
        max_per_page=max_per_page
    )
    return serializer.jsonify(results.items), 200