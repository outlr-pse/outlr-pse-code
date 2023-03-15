from execution.execution_error import ExecutionError


class SubspaceError(ExecutionError):
    """
    An ExecutionError indicating that a columns index of a subspace was out of bounds
    """

    def __init__(self):
        super().__init__(debug_message="A column index of a subspace was out of bounds")

    def _to_json(self) -> dict:
        return {}
