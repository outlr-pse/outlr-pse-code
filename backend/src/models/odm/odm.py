from models.base import Base
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship


class ODM(Base):
    __tablename__ = 'odm'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    hyper_parameters = relationship("hyper_parameter", back_populates="odm")

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
