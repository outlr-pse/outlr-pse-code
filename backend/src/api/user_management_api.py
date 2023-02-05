"""Defines the user API endpoint.

Endpoints defined:
    /login
    /register
    /logout
    /check-token
"""
from flask import Blueprint, Response, jsonify, request
import re

from backend.src import mock_database
from backend.src.api.models import error

user_management_api = Blueprint('user_management', __name__)
username_regex: str = "^[A-Za-z][A-Za-z0-9_]{2,29}$"
password_regex: str = "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{6,})"


def validate_username(username: str) -> bool:
    if username is None:
        return False
    return bool(re.match(username_regex, username))


def validate_password(password: str) -> bool:
    if password is None:
        return False
    return bool(re.match(password_regex, password))


@user_management_api.route('/login', methods=['POST'])
def login() -> (Response, int):
    """
    Expects a username and a password in the request. If username and
    password were correct a user json (with the jwt token connected to the user) and the status code "200 OK"
    is returned, status code "401 Unauthorized" otherwise.
    """
    data = request.get_json()
    if not data:
        return jsonify(error=error.no_data_provided), error.no_data_provided["status"]

    if "username" not in data:
        return jsonify(error=error.no_username_provided), error.no_username_provided["status"]

    if "password" not in data:
        return jsonify(error=error.no_password_provided), error.no_password_provided["status"]
    username = data['username']
    password = data['password']
    if username is None or not validate_username(username):
        return jsonify(error=error.invalid_username), error.invalid_username["status"]
    if password is None or not validate_password(password):
        return jsonify(error=error.invalid_password), error.invalid_password["status"]

    user = mock_database.login_user(username, password)
    if user is None:
        return jsonify(error=error.provided_credentials_wrong), error.provided_credentials_wrong["status"]
    return jsonify(user=user.to_json(), message=f'Successfully logged in as {username}', status=200)


@user_management_api.route('/register', methods=['POST'])
def register() -> (Response, int):
    """
    Expects a username and a password in the request. Inserts a new user
    into the database if username and password are valid and returns a user json
    (with the jwt token connected to the user), otherwise "409 Conflict"
    """
    data = request.get_json()
    if not data:
        return jsonify(error=error.no_data_provided), error.no_data_provided["status"]

    if "username" not in data:
        return jsonify(error=error.no_username_provided), error.no_username_provided["status"]

    if "password" not in data:
        return jsonify(error=error.no_password_provided), error.no_password_provided["status"]

    username = data['username']
    password = data['password']
    if username is None or not validate_username(username):
        return jsonify(error=error.invalid_username), error.invalid_username["status"]
    if password is None or not validate_password(password):
        return jsonify(error=error.invalid_password), error.invalid_password["status"]

    user = mock_database.register_user(username, password)
    if user is None:
        return jsonify(error=error.username_already_taken), error.username_already_taken["status"]
    return jsonify(user=user.to_json(), message=f'Successfully registered user - Welcome {username}!', status=200)


@user_management_api.route('/logout', methods=['POST'])
# jwt_required()
def logout() -> (Response, int):
    """
    Requires JWT token. Logs out the user connected to the JWT Token, which means deleting the access token
    connected to the user.
    """

    headers = request.headers
    if headers is None:
        return jsonify(error=error.no_header_provided), error.no_header_provided["status"]
    bearer = headers.get('Authorization')

    if bearer is None or len(bearer) < 1:
        return jsonify(error=error.token_not_provided), error.token_not_provided["status"]
    token = bearer.split()[1]
    user_to_token = mock_database.get_user_by_token(int(token))

    if user_to_token is not None:
        user_to_token.delete_token()
        return jsonify(user=user_to_token.to_json(), message="Logged out", status=200)
    else:
        return jsonify(error=error.token_not_linked), error.token_not_linked["status"]


@user_management_api.route('/get-token-identity', methods=['GET'])
def get_token_identity() -> (Response, int):
    """
    Returns the user json of the user connected to the provided JWT Token. In the case of a valid JWT Token
    "202 Accepted" is returned with the user json, otherwise an empty user json and "200 OK" is returned
    """
    headers = request.headers
    bearer = headers.get('Authorization')

    if bearer is None or len(bearer) < 1:
        response = jsonify(user={}, message="No token provided",
                           status=202)
        response.status = 202
        return response
    token = bearer.split()[1]
    user_to_token = mock_database.get_user_by_token(int(token))

    if user_to_token is None:
        response = jsonify(user={}, message="No token provided",
                           status=202)
        response.status = 202
        return response
    else:
        response = jsonify(user=user_to_token.to_json(), message=f'Token is linked to {user_to_token.username}',
                           status=202)
        response.status = 202
        return response
