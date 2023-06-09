"""This module provides an abstract class for ODM providers."""
from abc import ABC, abstractmethod
from typing import Iterator

from models.odm import ODM


class ODMProvider(ABC):

    @abstractmethod
    def get_odms(self) -> Iterator[ODM]:
        """Collects all ODMs.

        Returns:
            An iterator of ODMs.
        """
        pass
