from models.base import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    password = Column(String)

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }

    @classmethod
    def from_json(cls, json: dict):
        return cls(
            name=json["name"]
        )
