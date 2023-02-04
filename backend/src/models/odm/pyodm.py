"""
PyODM class

This file contains the PyODM class, which is a wrapper for the PyOD library.
"""
from typing import Any

from models.odm.odm import ODM
from models.dataset.dataset import Dataset
import pyod
import importlib


class PyODM(ODM):
    def run_odm(self, subspace: Dataset, hyper_params: dict[str, Any]) -> list[int]:
        """Runs the ODM on the given subspace
        Args:
            subspace (Dataset): The subspace to run the ODM on
            hyper_params (dict[str, Any]): The hyper parameters for the ODM
        Returns:
            list[int]: The labels for the outliers on this subspace
        """
        pyOD_module_name, cls_name = self.name.split('.')
        module = importlib.import_module(f'pyod.models.{pyOD_module_name}')
        pyODM_cls = getattr(module, cls_name)
        pyODM = pyODM_cls(**hyper_params)
        pyODM.fit(subspace.dataset)
        return pyODM.labels_
