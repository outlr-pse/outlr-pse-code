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


def handle_user_input() -> (Response, int):
    """
    Validates, whether user passed a username and a password with the request and that these are valid. If they are
    not a response is returned, which should explains the problem - otherwise None is returned
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

    return None


@user_management_api.route('/login', methods=['POST'])
def login() -> (Response, int):
    """
    Expects a username and a password in the request. If username and
    password were correct a user json (with the jwt token connected to the user) and the status code "200 OK"
    is returned, status code "401 Unauthorized" otherwise.
    """
    error = handle_user_input()
    if error:
        return error

    username = request.json["username"]
    password = request.json["password"]
    user = database_access.get_user_by_username(username)

    if not check_password_hash(user.password, password):
        return jsonify(error=error.provided_credentials_wrong), error.provided_credentials_wrong["status"]
    access_token = create_access_token(identity=user.name)
    return jsonify(user={"username": user.name, "access_token": access_token})


@user_management_api.route('/register', methods=['POST'])
def register() -> (Response, int):
    """
    Expects a username and a password in the request. Inserts a new user
    into the database if username and password are valid and returns a user json
    (with the jwt token connected to the user), otherwise "409 Conflict"
    """
    error = handle_user_input()
    if error:
        return error

    username = request.json["username"]
    password = request.json["password"]

    password_hashed = generate_password_hash(password, 'sha256')
    user = User(name=username, password=password_hashed)
    # check if username is already linked to User in database
    if database_access.get_user_by_username(username) is not None:
        return jsonify(error=error.username_already_taken), error.username_already_taken["status"]

    # no User in database with username -> create a User with provided username in the database
    database_access.add_user(user)
    access_token = create_access_token(identity=user.name)
    return jsonify(user={"username": user.name, "access_token": access_token})


@user_management_api.route('/logout', methods=['POST'])
@jwt_required()
def logout() -> (Response, int):
    username = get_jwt_identity()
    token = get_token()
    return jsonify(user={"username": username, "access_token": token}, message="Logged out", status=200)


@user_management_api.route('/get-token-identity', methods=['GET'])
@jwt_required(optional=True)
def get_token_identity() -> (Response, int):
    """
    Returns the user json of the user connected to the provided JWT Token. In the case of a valid JWT Token
    "202 Accepted" is returned with the user json, otherwise an empty user json and "200 OK" is returned
    """
    username = get_jwt_identity()
    if username is None:
        response = jsonify(user={}, error=error.token_not_provided_on_identity_check),\
            error.token_not_provided_on_identity_check["status"]
        return response
    user = database_access.get_user_by_username(username)
    if user is None:
        response = jsonify(user={}, error=error.token_not_provided_on_identity_check), \
            error.token_not_provided_on_identity_check["status"]
        return response
    else:
        token = get_token()
        response = jsonify(user={"username": username, "access_token": token})
        response.status = 202
        return response
