from typing import List


class MockUser:
    """ Mocks a user, which has a token and is registered in the database.

    Attributes:
        username: the username the user is identified with
        password: a password string
        token: the token the user is connected to
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None

    def get_token(self):
        """Get the token the user is connected to"""
        return self.token

    def delete_token(self):
        """Deletes the token the user is connected to"""
        self.token = None

    def to_json(self):
        """Returns a dictionary to the object"""
        return {"username": self.username,
                "access_token": self.token}


class MockDatabase:
    """ Mocks a database in which users are stored. When rerun the database is emptied and users
        must be reregistered.

        Attributes:
            database: the mock database, a list of mock users
            token_count: keeps track of the number of tokens, which might be in usage.
        """
    def __init__(self):
        self.database: List[MockUser] = []
        self.token_count = 0

    def user_with_username(self, username):
        """checks if a user with the provided username exists in the mock database

            Args:
                username: the username, after which a user is searched

            Returns:
                True, if a user with the username exists in the mock database
        """
        for user in self.database:
            if username == user.username:
                return True
        return False

    def register_user(self, username, password):
        """register a user with the provided username and password if the username is not already taken

            Args:
                username: the username
                password: the password

            Returns:
                The object of the user, if a user with the provided credentials could be registered to the database
        """
        if self.user_with_username(username):
            return None

        new_user = MockUser(username, password)
        self.database.append(new_user)
        new_user.token = self.token_count
        self.token_count += 1
        return new_user

    def validate_login_data(self, username, password):
        """checks whether a user with the provided username exists and checks if the password connected to the user
            corresponds to the provided password

            Args:
                username: the username
                password: the password

            Returns:
                True, if a user with the username and provided password exists in the database
        """
        for user in self.database:
            if username == user.username and user.password == password:
                return user
        return None

    def login_user(self, username, password):
        """ Logs a user in if valid data is provided, which is mocked by assigning the user a token on success

            Args:
                username: the username
                password: the password

            Returns:
                The object of the user, if a user with the provided credentials exists in the database
        """
        user = self.validate_login_data(username, password)
        if user is None:
            return None

        user.token = self.token_count
        self.token_count += 1
        return user

    def get_user_by_token(self, token):
        """ Gets the user connected to the provided token

                Args:
                    token: the token to look for in the database

                Returns:
                    The object of the user, if a user is connected to the provided token.
        """
        for user in self.database:
            if token == user.token:
                return user
        return None
