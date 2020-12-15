from avista_base.api import bp
from flask import request, jsonify
from avista_data.role import Role
from avista_base.auth import role_required
import avista_base.service as svc


@bp.route('/api/config/<section_id>', methods=['GET'])
@role_required(Role.ADMIN)
def read_config(section_id):
    try:
        response_object = svc.Service.get_instance().get_config(section_id)
    except Exception as e:
        return jsonify(dict(msg=str(e))), 400
    return jsonify(response_object), 200


@bp.route('/api/config/<section_id>', methods=['PUT'])
@role_required(Role.ADMIN)
def update_config(section_id):
    response_object = {'status': 'success'}

    post_data = request.get_json()
    try:
        svc.Service.get_instance().set_config(section_id, post_data)
    except Exception as e:
        return jsonify(dict(msg=str(e))), 400

    response_object['message'] = 'Config Updated!'

    return jsonify(response_object)
