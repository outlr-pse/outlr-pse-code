
class JSONError(Exception):
    """An error that occurs during JSON parsing
    Attributes
        debug_message: A string that contains a message. This message should only be used for debugging purposes
    """

    def __init__(self, debug_message: str):
        """Create a new JSONError
        Args
            debug_message: See attribute debug_message
        """
        self.debug_message = debug_message

    def __str__(self) -> str:
        return f"Error while parsing JSON: {self.debug_message}"
