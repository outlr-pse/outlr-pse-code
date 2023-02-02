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
from backend.src.api.models.error import UserManagementError

user_management_api = Blueprint('user_management', __name__)
mock_database = MockDatabase()

@user_management_api.route('/login', methods=['POST'])
def login() -> Response:
    username = request.json['username']
    password = request.json['password']
    user = mock_database.login_user(username, password)
    if user is None:
        login_error = UserManagementError('User with provided credentials does not exist or password not valid', 0, 400)
        response = jsonify(message=login_error.error_message, status=400, error=login_error.to_json())
        response.status = 400
        return response
    return jsonify(user=user.to_json(), message=f'Successfully logged in as {username}', status=200)


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
