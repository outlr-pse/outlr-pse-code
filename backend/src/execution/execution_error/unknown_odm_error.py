from execution.execution_error import ExecutionError


class UnknownODMError(ExecutionError):
    """
    An ExecutionError indicating that the requested odm could not be found.
    Attributes:
        odm_name (str): Name of the odm that was requested
    """

    def __init__(self, odm_name: str):
        self.odm_name = odm_name
        super().__init__(debug_message=f"ODM {odm_name} does not exist")

    def _to_json(self) -> dict:
        return {
            "odm_name": self.odm_name,
        }
