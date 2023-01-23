from abc import ABC


class Serializable(ABC):
    def to_json(self):
        pass


class Deserializable(ABC):
    @classmethod
    def from_json(cls, json: dict):
        pass

