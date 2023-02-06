from flask import jsonify, Response
from flask_jwt_extended import JWTManager

from backend.src.api import error
from backend.src.api.api import app

jwt = JWTManager(app)

@jwt.invalid_token_loader
def invalid_token_callback(jwt_invalid_reason) -> (Response, int):
    return jsonify(error=error.token_not_valid), error.token_not_valid.status


@jwt.unauthorized_loader
def unauthorized_token_callback(jwt_invalid_reason) -> (Response, int):
    return jsonify(error=error.token_not_found), error.token_not_found.status


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload) -> (Response, int):
    return jsonify(error=error.token_revoked), error.token_revoked.status


@jwt.token_verification_failed_loader
def token_verification_failed_callback(jwt_header, jwt_payload) -> (Response, int):
    return jsonify(error=error.token_authentication_failed), error.token_authentication_failed.status


@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_payload) -> (Response, int):
    return jsonify(error=error.token_in_blocklist), error.token_in_blocklist.status


@jwt.user_lookup_error_loader
def user_lookup_error_callback(jwt_header, jwt_payload) -> (Response, int):
    return jsonify(error=error.user_lookup_failed), error.user_lookup_failed.status

