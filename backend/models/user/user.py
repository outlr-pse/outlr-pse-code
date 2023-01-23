from models.base import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)

    # The json representation of the object
    def __dict__(self):
        return {
            "id": self.id,
            "username": self.username
        }
