import pkgutil
import os.path

import pyod.models

from models.odm.odm import ODM
from odmprovider.odm_provider import ODMProvider


class PyODScraper(ODMProvider):

    def next_odm(self) -> ODM:
        package_path = os.path.dirname(pyod.models.__file__)
        for _, name, _ in pkgutil.iter_modules([package_path]):
            yield ODM(name)
