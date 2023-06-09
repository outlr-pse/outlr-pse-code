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
import bcrypt
import database.database_access as db
from models.user import User

user_management_api = Blueprint('user_management', __name__)
username_regex: str = "^[A-Za-z][A-Za-z0-9_]{2,29}$"
password_regex: str = "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{6,})"


def generate_password_hash(password: str) -> bytes:
    """
       Generates a salted hash of the password provided as parameter, which is returned by the method
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=14)
    return bcrypt.hashpw(password_bytes, salt)


def check_password_hash(actual_password_hash: str, password: str) -> bool:
    """
        Compares password provided with the password hash it should correspond to and returns whether
        they are the same. password is expected to be of type string. First argument is the hash decoded with utf-8
    """
    password_bytes = password.encode('utf-8')
    hashed_password = actual_password_hash.encode('utf-8')
    passwords_match: bool
    try:
        passwords_match = bcrypt.checkpw(password_bytes, hashed_password)
    except ValueError:
        passwords_match = False
    return passwords_match


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
    with db.Session() as session:
        input_error = handle_user_input()
        if input_error:
            return input_error

        username = request.json["username"]
        # the password hash
        password = request.json["password"]
        user = db.get_user(session, user=username)
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
    with db.Session() as session:
        input_error = handle_user_input()
        if input_error:
            return input_error

        username = request.json["username"]
        password = request.json["password"]

        password_hash_bytes = generate_password_hash(password)
        password_hashed = password_hash_bytes.decode('utf-8')
        user = User(name=username, password=password_hashed)
        # check if username is already linked to User in database
        if db.get_user(session, username):
            return jsonify(error.username_already_taken), error.username_already_taken["status"]

        # no User in database with username -> create a User with provided username in the database
        db.add_user(session, user)
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
    with db.Session() as session:
        user_id = get_jwt_identity()
        token = get_token()
        user = db.get_user(session, user=user_id)
        if not user:
            return jsonify(error.token_not_valid), error.token_not_valid["status"]
        response = jsonify(user.to_json(token))
        response.status = 202
        return response
