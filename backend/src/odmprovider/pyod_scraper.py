"""This module scrapes the pyod package for ODMs and their hyper parameters.

This module scrapes only those ODMs that use TensorFlow, and not those that use PyTorch.
It accomplishes this by catching the ImportError and skipping the ODM in question.


Typical usage example:

    odm = PyODScraper().get_odms()
    insert odm into database
"""
import importlib
import inspect

import pkgutil
import os.path
from typing import Iterator

import pyod.models

from models.odm import HyperParameter
from models.odm import ODM
from odmprovider.odm_provider import ODMProvider


class PyODScraper(ODMProvider):

    def get_odms(self) -> Iterator[ODM]:
        """Scrapes the pyod package for ODMs and their hyper parameters.

            Returns:
                An iterator of ODMs in the pyod package.
        """
        pkg_path = os.path.dirname(pyod.models.__file__)
        for _, name, _ in pkgutil.iter_modules([pkg_path]):
            try:
                odm_module = importlib.import_module(f'pyod.models.{name}')
            except ImportError:
                continue
            odm_class = next((getattr(odm_module, f) for f in dir(odm_module) if f.lower() == name), None)
            if not odm_class:
                continue
            init_method = getattr(odm_class, '__init__')
            sig = inspect.signature(init_method)
            odm = ODM(name=f'{name}.{odm_class.__name__}')

            for param in sig.parameters.values():
                if param.name == 'self':
                    continue
                hyper_param = HyperParameter(name=param.name)
                if param.default != inspect.Parameter.empty:
                    hyper_param.param_type = repr(type(param.default))
                    hyper_param.optional = True
                else:
                    hyper_param.param_type = 'Any'
                    hyper_param.optional = False

                odm.hyper_parameters.append(hyper_param)
                odm.deprecated = False
            yield odm
