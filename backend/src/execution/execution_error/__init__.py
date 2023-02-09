class ExecutionError(Exception):
    """
    Represents an error that occurs during the execution of an experiment.
    The error should be sent to the client
    """

    def __init__(self, debug_message: str = ""):
        self._debug_message = debug_message

    @property
    def debug_message(self) -> str:
        """
        A message for debugging purposes only
        """
        return self.__class__.__name__ + ": " + self._debug_message

    def to_json(self) -> dict:
        """
        Returns: Returns a json representation of the error, that can be stored in the database
        """
        return {
            "debug_message": self.debug_message
        }
