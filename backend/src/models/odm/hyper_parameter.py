from models.base import Base
from sqlalchemy import ForeignKey, Column, Integer, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column



class HyperParameter(Base):
    __tablename__ = 'hyper_parameter'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    odm_id = Column(Integer, ForeignKey('odm.id'))
    odm = relationship("ODM", back_populates="hyper_parameters")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }
