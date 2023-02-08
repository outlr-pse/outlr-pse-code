"""
PyODM class

This file contains the PyODM class, which is a wrapper for the PyOD library.
"""
from typing import Any

import numpy
import pandas as pd

from models.odm.odm import ODM
import pyod
import importlib


class PyODM(ODM):
    def run_odm(self, subspace: pd.DataFrame, hyper_params: dict[str, Any]) -> numpy.ndarray:
        """Runs the ODM on the given subspace
        Args:
            subspace (DataFrame): The subspace to run the ODM on
            hyper_params (dict[str, Any]): The hyper parameters for the ODM
        Returns:
            list[int]: The labels for the outliers on this subspace
        """
        pyOD_module_name, cls_name = self.name.split('.')
        module = importlib.import_module(f'pyod.models.{pyOD_module_name}')
        pyODM_cls = getattr(module, cls_name)
        pyODM = pyODM_cls(**hyper_params)
        pyODM.fit(subspace)
        return pyODM.labels_
