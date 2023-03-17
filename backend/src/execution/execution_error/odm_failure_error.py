from execution.execution_error import ExecutionError


class ODMFailureError(ExecutionError):
    """
    An ExecutionError indicating that the odm failed internally
    Attributes:
        odm_message (str): The message of the exception that was raised during the execution of the ODM
    """

    def __init__(self, odm_message: str, odm_name: str):
        self.odm_message = odm_message
        super().__init__(debug_message=f"ODM {odm_name} failed internally with the following message: {odm_message}")

    def _to_json(self) -> dict:
        return {
            "odm_message": self.odm_message,
        }
