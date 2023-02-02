from typing import List


class MockUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None

    def get_token(self):
        return self.token

    def delete_token(self):
        self.token = None

    def to_json(self):
        return {"username": self.username,
                "token": self.token}


class MockDatabase:

    def __init__(self):
        self.database: List[MockUser] = []
        self.token_count = 0

    def user_with_username(self, username):
        for user in self.database:
            if username == user.username:
                return True
        return False

    def register_user(self, username, password):
        if self.user_with_username(username):
            return None

        new_user = MockUser(username, password)
        self.database.append(new_user)
        new_user.token = self.token_count
        self.token_count += 1
        return new_user

    def validate_login_data(self, username, password):
        for user in self.database:
            if username == user.username and user.password == password:
                return user
        return None

    def login_user(self, username, password):
        user = self.validate_login_data(username, password)
        if user is None:
            return None

        user.token = self.token_count
        self.token_count += 1
        return user

    def get_user_by_token(self, token):
        for user in self.database:
            if token == user.token:
                return user
        return None
