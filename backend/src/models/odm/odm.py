"""ODM model.

This module contains the ODM model, which is used to store the ODMs.

Note that currently only the attributes of the ODM class are stored in the database.
Once there are more than just a single type of ODM the database should be setup for class hierarchies.
See https://docs.sqlalchemy.org/en/20/orm/inheritance.html#single-table-inheritance

"""
from typing import Any

from models.base import Base
from models.dataset.dataset import Dataset
from models.odm.hyper_parameter import HyperParameter
from sqlalchemy.orm import relationship, Mapped, mapped_column


class ODM(Base):
    __tablename__: str = 'odm'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    hyper_parameters: Mapped[list["HyperParameter"]] = relationship()
    deprecated: Mapped[bool]

    def to_json(self) -> dict:
        """Converts the ODM object to a JSON object"""
        return {
            'id': self.id,
            'name': self.name,
            'hyper_parameters': [hp.to_json() for hp in self.hyper_parameters],
            'deprecated': self.deprecated
        }

    def check_params(self, args: dict[str, Any]) -> bool:
        """Checks if the given parameters are valid for this ODM"""
        for param in self.hyper_parameters:
            if repr(type(args[param.name])) != param.param_type:
                return False

    def run_odm(self, subspace: Dataset, hyper_params: dict[str, Any]) -> list[int]:
        """Runs the ODM on the given subspace"""
        raise NotImplementedError
