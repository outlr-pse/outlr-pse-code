from models.base import Base
from models.json_serializable import Serializable, Deserializable
from sqlalchemy import Column, Integer, String


class User(Base, Serializable, Deserializable):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "username": self.username
        }

    @classmethod
    def from_json(cls, json: dict):
        return cls(
            id=json["id"],
            username=json["username"]
        )
