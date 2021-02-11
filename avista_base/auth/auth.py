from avista_base.auth import bp
from avista_data.user import User
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from flask_cors import cross_origin


@bp.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()

    if not data.get('email', None):
        return jsonify({'msg': 'Missing email parameter'}), 400
    if not data.get('password', None):
        return jsonify({'msg': 'Missing password parameter'}), 400

    user = User.authenticate(data)
    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    token = create_access_token(identity=user.get_email())
    dct = user.to_dict()
    dct['token'] = token
    return jsonify(dct), 200


@bp.route('/api/register', methods=['POST'])
def register():
    response_object = {'status': 'success'}
    return jsonify(response_object)