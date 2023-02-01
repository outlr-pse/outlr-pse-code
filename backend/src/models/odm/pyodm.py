from typing import Any

from models.odm.odm import ODM
from models.dataset.dataset import Dataset

class PyODM(ODM):
    def run_odm(self, subspace: Dataset, hyper_params: dict[str, Any]) -> list[int]:
        pyODM = eval("pyod.models" + self.name)
        return None
