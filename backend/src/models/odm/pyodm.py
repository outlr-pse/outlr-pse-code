from typing import Any

from models.odm.odm import ODM
from models.dataset.dataset import Dataset
import pyod
import importlib

class PyODM(ODM):
    def run_odm(self, subspace: Dataset, hyper_params: dict[str, Any]) -> list[int]:
        pyOD_module_name, cls_name = self.name.split('.')
        module = importlib.import_module(f'pyod.models.{pyOD_module_name}')
        pyODM_cls = getattr(module, cls_name)
        pyODM = pyODM_cls(hyper_params)

        return pyODM
