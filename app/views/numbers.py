from flask import Blueprint, current_app, request, jsonify
from marshmallow import ValidationError
from app.serializers import DIDNumberSchema
from app.models import DIDNumber


bp_number = Blueprint('numbers', __name__, url_prefix='/numbers')


@bp_number.route('/', methods=['GET'])
def list_numbers():
    serializer = DIDNumberSchema(many=True)
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
    except ValueError:
        page = 1
        per_page = 20

    results = DIDNumber.query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=True, 
        max_per_page=20
    )
    response = {
        'results': serializer.dump(results.items),
        'page': page,
        'per_page': per_page
    }
    return response, 200


@bp_number.route('/', methods=['POST'])
def create_number():
    serializer = DIDNumberSchema()

    try:
        number = serializer.load(request.json)
    except ValidationError as error:
        return error.messages, 400

    current_app.db.session.add(number)
    current_app.db.session.commit()
    return serializer.jsonify(number), 201


@bp_number.route('/<pk>', methods=['DELETE'])
def delete_number(pk):
    query = DIDNumber.query.filter(DIDNumber.id == pk)
    if query.value('id'):
        query.delete()
        current_app.db.session.commit()
        return jsonify("Number deleted"), 200
    return jsonify("Not Found"), 404


@bp_number.route('/<pk>', methods=['PUT'])
def update_number(pk):
    query = DIDNumber.query.filter(DIDNumber.id == pk)
    if query.value('id'):
        query.update(request.json)
        current_app.db.session.commit()
        serializer = DIDNumberSchema()
        return serializer.jsonify(query.first()), 200
    return jsonify("Not Found"), 404
