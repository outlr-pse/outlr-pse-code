from typing import Any

from models.base import Base
from models.odm import hyper_parameter
from models.odm.hyper_parameter import HyperParameter
from sqlalchemy.orm import relationship, Mapped, mapped_column


class ODM(Base):
    __tablename__: str = 'odm'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    hyper_parameters: Mapped[list["HyperParameter"]] = relationship()
    deprecated: Mapped[bool]

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'hyper_parameters': [hp.to_json() for hp in self.hyper_parameters],
            'deprecated': self.deprecated
        }

    # def check_params(self, args: dict[str, Any]) -> bool:
    #     for param in self.hyper_parameters:
    #         if()


