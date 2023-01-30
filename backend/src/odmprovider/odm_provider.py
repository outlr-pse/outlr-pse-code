from abc import ABC, abstractmethod

from models.odm.odm import ODM


class ODMProvider(ABC):

    @abstractmethod
    def next_odm(self) -> ODM:
        pass
