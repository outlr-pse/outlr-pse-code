import importlib

from models.odm.odm import ODM
from odmprovider.odm_provider import ODMProvider


class PyODScraper(ODMProvider):

    def next_odm(self) -> ODM:
        pyod_module = importlib.import_module("pyod.models")
        pyod_classes = [getattr(pyod_module, c) for c in dir(pyod_module) if c.endswith("Detector")]

        for pyod_class in pyod_classes:
            odm = ODM()
            odm.name = pyod_class.__name__
            yield odm
