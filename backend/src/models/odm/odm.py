from models.base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from abc import ABC, abstractmethod


class ODM(Base, ABC):
    __tablename__ = 'odm'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    hyper_parameters = relationship("HyperParameter", back_populates="odm")
    deprecated: Mapped[bool]

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
