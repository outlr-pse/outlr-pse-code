"""Defines the user API endpoint.

Endpoints defined:
    /login
    /register
    /logout
    /check-token
"""
from functools import wraps

from flask import Blueprint, Response, jsonify, request
from backend.src.api.mock_classes import MockDatabase

user_management_api = Blueprint('user_management', __name__)
mock_database = MockDatabase()


def mock_jwt_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            headers = request.headers
            bearer = headers.get('Authorization')
            user_to_token = None

            if bearer is not None and len(bearer) >= 1:
                token = bearer.split()[1]
                user_to_token = mock_database.get_user_by_token(int(token))

            if user_to_token is None:
                response = jsonify(msg="Token not valid and not linked to a user", status=400)
                response.status = 400
                return response
            else:
                return fn(*args, **kwargs)
        return decorator
    return wrapper


@user_management_api.route('/login', methods=['POST'])
def login() -> Response:
    username = request.json['username']
    return jsonify(message=f'Successfully logged in as {username}', status=200)


@user_management_api.route('/register', methods=['POST'])
def register() -> Response:
    username = request.json['username']
    return jsonify(message=f'User {username} registered', status=200)


@user_management_api.route('/logout', methods=['POST'])
#@jwt_required()
def logout() -> Response:
    return jsonify(message="Token deleted", status=200)


@user_management_api.route('/check-token', methods=['POST'])
#@jwt_required()
def check_token() -> Response:
    return jsonify(message="Token is valid", status=200)
