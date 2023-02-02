"""When a request fails, an error occurs. Following class provides a format for classifying
the error as well as describing it, which is passed in the http response.
"""
class Error:
    def __init__(self, error_message, error_type, error_id, status_code):
        self.error_message = error_message
        self.error_type = error_type
        self.error_id = error_id
        self.status_code = status_code

    def to_json(self):
        return {
            "message": self.error_message,
            "errorType": self.error_type,
            "errorId": self.error_id,
            "statusCode": self.status_code
        }

"""When a request fails, an error occurs. Following class provides a format for classifying
the error as well as describing it, which is passed in the http response.
"""
class JWTAuthError(Error):
    """
        JWTAuthError class, children of Foo
        Use this when you want to Bar around.
        parent:
        """
    def __init__(self, error_message, error_id, status_code):
        super().__init__(error_message, "JWTAuthError", error_id, status_code)


class UserManagementError(Error):
    def __init__(self, error_message, error_id, status_code):
                super().__init__(error_message, "UserManagementError", error_id, status_code)


class ExperimentError(Error):
    def __init__(self, error_message, error_id, status_code):
        super().__init__(error_message, "ExperimentError", error_id, status_code)


class ODMError(Error):
    def __init__(self, error_message, error_id, status_code):
        super().__init__(error_message, "ODMError", error_id, status_code)
