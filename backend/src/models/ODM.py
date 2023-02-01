from models.base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from abc import ABC, abstractmethod


class ODM(Base):
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


class HyperParameter(Base):
    __tablename__ = 'hyper_parameter'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    odm_id: Mapped[int] = mapped_column(ForeignKey('odm.id'))
    odm = relationship("ODM", back_populates="hyper_parameters")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }
