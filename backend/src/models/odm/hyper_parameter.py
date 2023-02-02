""" HyperParameter model

This module contains the HyperParameter model, which is used to store the hyper parameters of an ODM.


"""
from models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class HyperParameter(Base):
    __tablename__: str = 'hyper_parameter'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    param_type: Mapped[str]
    optional: Mapped[bool]
    odm_id: Mapped[int] = mapped_column(ForeignKey('odm.id'))


    def to_json(self) -> dict:
        """Converts the HyperParameter object to a JSON object"""
        return {
            "id": self.id,
            "name": self.name,
            "param_type": self.param_type,
            "optional": self.optional
        }
