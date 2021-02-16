""" This package contains the modules containing the route logic for the service """

from functools import wraps
from flask import Blueprint, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from avista_data.role import Role

bp = Blueprint('auth', __name__)


def role_required(role):
    """ Authenticates using a JWT token and a specified user role level

    Used to wrap a route method to allow for authentication

    Args:
        role (Role): the minimum role required
    """
    def decorator(fn):
        """ Wrapping function

        Args:
            fn (Function): The function to be wrapped
        """
        @wraps(fn)
        def wrapper(*args, **kwargs):
            """ The actual rapper function which both validates a jwt token and a role """
            verify_jwt_in_request()
            claims = get_jwt_claims()
            print(f'Role: {claims["role"]}')
            if Role.from_str(claims['role']) < role:
                return jsonify({'msg': 'Role level too low'}), 403
            else:
                return fn(*args, **kwargs)
        return wrapper
    return decorator


from avista_base.auth import auth, user
