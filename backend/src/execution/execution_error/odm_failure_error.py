from execution.execution_error import ExecutionError


class ODMFailureError(ExecutionError):
    """
    An ExecutionError indicating that the odm failed internally
    """

    def __init__(
            self,
            odm_message: str
    ):
        self.odm_message = odm_message
        super().__init__(debug_message=f"ODM failed internally with the following message: {odm_message}")

    def to_json(self) -> dict:
        return {
            **super().to_json(),
            "odm_message": self.odm_message
        }
