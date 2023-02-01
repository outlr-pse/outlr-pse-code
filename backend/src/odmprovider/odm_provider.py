"""This module provides an abstract class for ODM providers."""
from abc import ABC, abstractmethod
from typing import Iterator

from models.odm.odm import ODM


class ODMProvider(ABC):

    @abstractmethod
    def get_odms(self) -> Iterator[ODM]:
        pass
