"""Defines the user API endpoint.

Endpoints defined:
    /login
    /register
    /logout
    /check-token
"""
from flask import Blueprint, Response, jsonify, request
import re

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
import api.error as error
from werkzeug.security import check_password_hash, generate_password_hash

from database import database_access
from models.user import User

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


def handle_user_input() -> (Response, int):
    """
    Validates, whether user passed a username and a password with the request and that these are valid. If they are
    not a response is returned, which should explains the problem - otherwise None is returned
    """
    data = request.get_json()
    if not data:
        return jsonify(error.no_data_provided), error.no_data_provided["status"]

    if "username" not in data:
        return jsonify(error.no_username_provided), error.no_username_provided["status"]

    if "password" not in data:
        return jsonify(error.no_password_provided), error.no_password_provided["status"]
    username = data['username']
    password = data['password']
    if username is None or not validate_username(username):
        return jsonify(error.invalid_username), error.invalid_username["status"]
    if password is None or not validate_password(password):
        return jsonify(error.invalid_password), error.invalid_password["status"]

    return None


def invalidate_token(token: str) -> None:
    """
    Invalidates the token provided in the last HTTP request.
    Tokens currently only automatically expire after a certain time period.
    Invalidating them manually requires storing them in the database which is not implemented yet.
    """
    pass


@user_management_api.route('/login', methods=['POST'])
def login() -> (Response, int):
    """
    Expects a username and a password in the request. If username and
    password were correct a user json (with the jwt token connected to the user) and the status code "200 OK"
    is returned, status code "401 Unauthorized" otherwise.
    """
    input_error = handle_user_input()
    if input_error:
        return input_error

    username = request.json["username"]
    password = request.json["password"]
    user = database_access.get_user(username)
    if user is None:
        return jsonify(error.provided_credentials_wrong), error.provided_credentials_wrong["status"]

    if not check_password_hash(user.password, password):
        return jsonify(error.provided_credentials_wrong), error.provided_credentials_wrong["status"]
    access_token = create_access_token(identity=user.id)
    return jsonify(username=user.name, access_token=access_token)


@user_management_api.route('/register', methods=['POST'])
def register() -> (Response, int):
    """
    Expects a username and a password in the request. Inserts a new user
    into the database if username and password are valid and returns a user json
    (with the jwt token connected to the user), otherwise "409 Conflict"
    """
    input_error = handle_user_input()
    if input_error:
        return input_error

    username = request.json["username"]
    password = request.json["password"]

    password_hashed = generate_password_hash(password, 'sha256')
    user = User(name=username, password=password_hashed)
    # check if username is already linked to User in database
    if database_access.get_user(username):
        return jsonify(error.username_already_taken), error.username_already_taken["status"]

    # no User in database with username -> create a User with provided username in the database
    database_access.add_user(user)
    access_token = create_access_token(identity=user.id)
    return jsonify(user.to_json(access_token))


@user_management_api.route('/logout', methods=['POST'])
@jwt_required()
def logout() -> (Response, int):
    if token := get_token():
        invalidate_token(token)

    return '', 200


@user_management_api.route('/get-token-identity', methods=['GET'])
@jwt_required()
def get_token_identity() -> (Response, int):
    """
    In the case of a valid JWT Token
    the username and the access token are returned with status code "202 Accepted".
    """
    user_id = get_jwt_identity()
    token = get_token()
    user = database_access.get_user(user_id)
    if not user:
        return jsonify(error.token_not_valid), error.token_not_valid["status"]
    response = jsonify(user.to_json(token))
    response.status = 202
    return response
