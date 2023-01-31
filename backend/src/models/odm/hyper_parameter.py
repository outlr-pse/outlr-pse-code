from models.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class HyperParameter(Base):
    __tablename__: str = 'hyper_parameter'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    odm_id: Mapped[int] = mapped_column(ForeignKey('odm.id'))
    name: Mapped[str]

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }
