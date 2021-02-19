from avista_base.auth import bp
from avista_data.user import User
from flask import request, jsonify, current_app
from avista_base.auth import role_required
from avista_data.role import Role


@bp.route('/api/users', methods=['POST'])
@role_required(Role.ADMIN)
def create_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    response_object = {'status': 'success'}
    post_data = request.get_json()
    if post_data is None or post_data == {}:
        response_object['message'] = 'Missing data'
        response_object['status'] = 'failure'
        return jsonify(response_object), 400
    else:
        print("Post Data: " + str(post_data))
        user = User(post_data)
        current_app.session.add(user)
        current_app.session.commit()
        response_object['message'] = 'User added!'
        return jsonify(response_object), 200


@bp.route('/api/users', methods=['GET', 'POST'])
@role_required(Role.ADMIN)
def read_all_users():
    data = []
    for user in current_app.session.query(User).all():
        data.append(user.to_dict())
    response_object = data

    return jsonify(response_object)


@bp.route('/api/users/<int:user_id>', methods=['GET'])
@role_required(Role.USER)
def read_one_user(user_id):
    user = current_app.session.query(User).filter_by(id=user_id).first()
    response_object = user.to_dict()

    return jsonify(response_object)


@bp.route('/api/users/<int:user_id>', methods=['PUT'])
@role_required(Role.USER)
def update_user(user_id):
    response_object = {'status': 'success'}

    post_data = request.get_json()
    user = current_app.session.query(User).filter_by(id=user_id).first()
    user.update(post_data)
    response_object['message'] = 'User updated!'

    return jsonify(response_object)


@bp.route('/api/users/<user_id>', methods=['DELETE'])
@role_required(Role.ADMIN)
def delete_user(user_id):
    response_object = {'status': 'success'}

    user = current_app.session.query(User).filter_by(id=user_id).first()
    current_app.session.delete(user)
    current_app.session.commit()
    response_object['message'] = 'User deleted!'

    return jsonify(response_object)
