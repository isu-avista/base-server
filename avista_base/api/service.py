from avista_base.api import bp
from flask import jsonify


# sanity check route
@bp.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')
