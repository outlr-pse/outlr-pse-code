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
            self.__class__.__name__: self._to_json()
        }

    def _to_json(self) -> dict:
        """
        Internal method to create a json representation.
        Use ``to_json`` to actually create the json. This will also include the error type in the json.
        Override ``_to_json`` in more specific execution error classes.
        When overriding provide all important information in the json, but don't include the ``_debug_message``
        Returns:
            Returns a json representation of the error
        """
        return {
            "debug_msg": self._debug_message
        }
