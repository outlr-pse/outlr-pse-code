"""Defines the /user API endpoint.

Endpoints defined:
    /user/login
    /user/register
    /user/logout
    /user/check-token
"""

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required

from api.api import mock_jwt_required

user_management_api = Blueprint('user_management', __name__, url_prefix='/user')


@user_management_api.route('/login', methods=['POST'])
def login() -> Response:
    username = request.json['username']
    return jsonify(message=f'Successfully logged in as {username}', status=200)


@user_management_api.route('/register', methods=['POST'])
def register() -> Response:
    username = request.json['username']
    return jsonify(message=f'User {username} registered', status=200)


@user_management_api.route('/logout', methods=['POST'])
@mock_jwt_required()
def logout() -> Response:
    return jsonify(message="Token deleted", status=200)


@user_management_api.route('/check-token', methods=['POST'])
@mock_jwt_required()
def check_token() -> Response:
    return jsonify(message="Token is valid", status=200)
