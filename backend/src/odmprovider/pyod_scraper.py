import importlib

from models.odm.odm import ODM
from odmprovider.odm_provider import ODMProvider


class PyODScraper(ODMProvider):

    def next_odm(self):
        pyod_module = None
        try:
            pyod_module = importlib.import_module("models.odm.odm", "pyod.models")
        except Exception as e:
            print(f"Error importing module: {e}")
        else:
            for c in dir(pyod_module):
                print(c)
                getattr(pyod_module, c)
                try:
                    print(pyod_module.__name__)
                except Exception as e:
                    print(f"Error: {e}")
                try:
                    print(pyod_module.__package__)
                except Exception as e:
                    print(f"Error: {e}")
                try:
                    print(pyod_module.)
                except Exception as e:
                    print(f"Error: {e}")
                try:
                    print(pyod_module.odm.__name__)
                except Exception as e:
                    print(f"Error: {e}")
