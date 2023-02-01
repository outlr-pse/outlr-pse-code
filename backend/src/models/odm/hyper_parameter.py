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
        return {
            "id": self.id,
            "name": self.name,
            "param_type": self.param_type,
            "optional": self.optional,
            "odm_id": self.odm_id
        }
