"""Defines the user API endpoint.

Endpoints defined:
    /login
    /register
    /logout
    /check-token
"""
from flask import Blueprint, Response, jsonify, request
import re

from flask_jwt_extended import create_access_token, get_jwt_identity
import api.error as error
from werkzeug.security import check_password_hash, generate_password_hash

from database import database_access
from models.user.user import User

user_management_api = Blueprint('user_management', __name__)
username_regex: str = "^[A-Za-z][A-Za-z0-9_]{2,29}$"
password_regex: str = "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{6,})"


def get_token() -> str | None:
    """
        Retrieves the token provided in the last HTTP request, therefore returning either the token
        as string or None
    """
    headers = request.headers
    if headers is None:
        return None
    bearer = headers.get('Authorization')

    if bearer is None or len(bearer) < 1:
        return None
    token = bearer.split()[1]
    return token


def validate_username(username: str) -> bool:
    """
        Checks whether the provided username matches the regex pattern

        Args:
            username: the username for which syntax shall be checked
    """
    if username is None:
        return False
    return bool(re.match(username_regex, username))


def validate_password(password: str) -> bool:
    """
        Checks whether the provided password matches the regex pattern

        Args:
            password: the password for which syntax shall be checked
    """
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

    user = database_access.get_user_by_username(username)

    if not check_password_hash(user.password, password):
        return jsonify(error=error.provided_credentials_wrong), error.provided_credentials_wrong["status"]
    access_token = create_access_token(identity=user.name)
    return jsonify(user={"username": user.name, "access_token": access_token},
                   message=f'Successfully registered user - Welcome {user.name}!', status=200)


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

    password_hashed = generate_password_hash(password, 'sha256')
    user = User(name=username, password=password_hashed)
    if database_access.get_user_by_username(username) is not None:
        return jsonify(error=error.username_already_taken), error.username_already_taken["status"]
    database_access.add_user(user)
    access_token = create_access_token(identity=user.name)
    return jsonify(user={"username": user.name, "access_token": access_token},
                   message=f'Successfully registered user - Welcome {user.name}!', status=200)


# @user_management_api.route('/logout', methods=['POST'])
# jwt_required()
# def logout() -> (Response, int):
#    """
#    Requires JWT token. Logs out the user connected to the JWT Token, which means deleting the access token
#    connected to the user.
#    """
#    headers = request.headers
#    if headers is None:
#        return jsonify(error=error.no_header_provided), error.no_header_provided["status"]
#    bearer = headers.get('Authorization')
#
#    if bearer is None or len(bearer) < 1:
#        return jsonify(error=error.token_not_provided), error.token_not_provided["status"]
#    token = bearer.split()[1]
#    user_to_token = mock_database.get_user_by_token(int(token))
#
#    if user_to_token is not None:
#        user_to_token.delete_token()
#        return jsonify(user=user_to_token.to_json(), message="Logged out", status=200)
#    else:
#        return jsonify(error=error.token_not_linked), error.token_not_linked["status"]


@user_management_api.route('/get-token-identity', methods=['GET'])
def get_token_identity() -> (Response, int):
    """
    Returns the user json of the user connected to the provided JWT Token. In the case of a valid JWT Token
    "202 Accepted" is returned with the user json, otherwise an empty user json and "200 OK" is returned
    """
    username = get_jwt_identity()
    if username is None:
        response = jsonify(user={}, error=error.token_not_provided_on_identity_check),\
            error.token_not_provided_on_identity_check.status
        return response
    user = database_access.get_user_by_username(username)
    if user is None:
        response = jsonify(user={}, error=error.token_not_provided_on_identity_check), \
            error.token_not_provided_on_identity_check.status
        return response
    else:
        token = get_token()
        assert token is not None
        response = jsonify(user={"username": username, "access_token": token}, message=f'Token is linked to {username}',
                           status=202)
        response.status = 202
        return response
