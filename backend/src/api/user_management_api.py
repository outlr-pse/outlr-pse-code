from flask import Blueprint, Response

user_management_api = Blueprint('user_management', __name__, url_prefix='/user')


@user_management_api.route('/login', methods=['POST'])
def login():
    return Response(status=501)


@user_management_api.route('/login', methods=['POST'])
def register():
    return Response(status=501)


@user_management_api.route('/logout', methods=['POST'])
def logout():
    return Response(status=501)


@user_management_api.route('/check_token', methods=['POST'])
def check_token():
    return Response(status=501)
