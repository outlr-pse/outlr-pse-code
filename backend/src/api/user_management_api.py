"""Defines the user API endpoint.

Endpoints defined:
    /login
    /register
    /logout
    /check-token
"""
from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required

from backend.src.api.mock_classes import MockDatabase
from backend.src.api.models.error import UserManagementError

user_management_api = Blueprint('user_management', __name__)
mock_database = MockDatabase()


@user_management_api.route('/login', methods=['POST'])
def login() -> Response:
    """
    Expects a username and a password in the request. If username and
    password were correct a user json (with the jwt token connected to the user) and the status code "200 OK"
    is returned, status code "401 Unauthorized" otherwise.
    """
    username = request.json['username']
    password = request.json['password']
    user = mock_database.login_user(username, password)
    if user is None:
        login_error = UserManagementError('User with provided credentials does not exist or password not valid', 0, 401)
        response = jsonify(message=login_error.error_message, status=401, error=login_error.to_json())
        response.status = 401
        return response
    return jsonify(user=user.to_json(), message=f'Successfully logged in as {username}', status=200)


@user_management_api.route('/register', methods=['POST'])
def register() -> Response:
    """
    Expects a username and a password in the request. Inserts a new user
    into the database if username and password are valid and returns a user json
    (with the jwt token connected to the user), otherwise "409 Conflict"
    """
    username = request.json['username']
    password = request.json['password']
    user = mock_database.register_user(username, password)
    if user is None:
        register_error = UserManagementError('User with username already exists', 1, 409)
        response = jsonify(message=register_error.error_message, status=409, error=register_error.to_json())
        response.status = 409
        return response
    return jsonify(user=user.to_json(), message=f'Successfully registered user - Welcome {username}!', status=200)

@user_management_api.route('/logout', methods=['POST'])
@jwt_required()
def logout() -> Response:
    """
    Requires JWT token. Logs out the user connected to the JWT Token, which means deleting the access token
    connected to the user.
    """
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    user = mock_database.get_user_by_token(int(token))
    user.delete_token()
    return jsonify(user=user.to_json(), message="Logged out", status=200)


@user_management_api.route('/get-token-identity', methods=['GET'])
def get_token_identity() -> Response:
    """
    Returns the user json of the user connected to the provided JWT Token. In the case of a valid JWT Token
    "202 Accepted" is returned with the user json, otherwise an empty user json and "200 OK" is returned
    """
    headers = request.headers
    bearer = headers.get('Authorization')
    user_to_token = None

    if bearer is not None and len(bearer) >= 1:
        token = bearer.split()[1]
        user_to_token = mock_database.get_user_by_token(int(token))
    if user_to_token is None:
        return jsonify(user={}, message=f'No user linked to token or token missing', status=200)
    else:
        response = jsonify(user=user_to_token.to_json(), message=f'Token is linked to {user_to_token.username}',
                           status=202)
        response.status = 202
        return response
