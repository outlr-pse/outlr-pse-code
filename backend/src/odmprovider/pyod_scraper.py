import importlib
import inspect

import pkgutil
import os.path

import pyod.models

from models.odm.hyper_parameter import HyperParameter
from models.odm.odm import ODM
from odmprovider.odm_provider import ODMProvider


class PyODScraper(ODMProvider):

    def next_odm(self) -> ODM:
        pkgpath = os.path.dirname(pyod.models.__file__)
        for _, name, _ in pkgutil.iter_modules([pkgpath]):
            try:
                odm_module = importlib.import_module(f'pyod.models.{name}')
            except ImportError:
                # print(f'Could not import {name}')
                continue
            try:
                odm_class = getattr(odm_module, name.upper())
            except AttributeError:
                # print(f'Could not find class {name.upper()} in {name}')
                continue
            odm_method = getattr(odm_class, '__init__')
            sig = inspect.signature(odm_method)
            odm = ODM(name=name)
            for param in sig.parameters:
                if param != 'self':
                    hyper_param = HyperParameter(name=param)
                    odm.hyper_parameters.append(hyper_param)

            print(name)
