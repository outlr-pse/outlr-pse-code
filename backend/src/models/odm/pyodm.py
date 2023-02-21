"""
PyODM class

This file contains the PyODM class, which is a wrapper for the PyOD library.
"""
from typing import Any

import pandas as pd
from numpy.typing import NDArray
import pyod  # maybe this is necessary for importlib
import importlib

from execution.execution_error.odm_failure_error import ODMFailureError
from execution.execution_error.unknown_odm_error import UnknownODMError
from models.odm import ODM


class PyODM(ODM):
    def run_odm(self, subspace: pd.DataFrame, hyper_params: dict[str, Any]) -> NDArray:
        """Runs the ODM on the given subspace
        Args:
            subspace (DataFrame): The subspace to run the ODM on
            hyper_params (dict[str, Any]): The hyper parameters for the ODM
        Returns:
            list[int]: The labels for the outliers on this subspace
        Raises:
            ODMFailureError: If the execution of the odm raised an error
        """
        try:
            pyod_module_name, cls_name = self.name.split('.')
            module = importlib.import_module(f'pyod.models.{pyod_module_name}')
        except Exception as e:
            raise UnknownODMError(odm_name=self.name) from e

        try:
            pyodm_cls = getattr(module, cls_name)
            pyodm = pyodm_cls(**hyper_params)
            pyodm.fit(subspace)
            return pyodm.labels_

        except Exception as e:
            raise ODMFailureError(odm_message=str(e)) from e
