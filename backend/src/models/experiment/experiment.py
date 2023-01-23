from models.base import Base
from sqlalchemy import Column, Integer, Text, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship


class Experiment(Base):
    __tablename__ = 'experiments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship("User", uselist=False)
    name = Column(Text, nullable=False)
    subspace_logic = Column(JSON, nullable=False)
    odm = relationship("ODM", uselist=False)
    odm_params = Column(JSON, nullable=False)
    result = relationship("Result", uselist=False)
    true_outliers = Column(ARRAY(Integer))

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'subspace_logic': self.subspace_logic,
            'odm': self.odm.to_json(),
            'odm_params': self.odm_params,
            'true_outliers': self.true_outliers
        }

    @classmethod
    def from_json(cls, json: dict):
        return cls(
            name=json['name'],
            subspace_logic=json['subspace_logic'],
            odm=json['odm'],
            odm_params=json['odm_params'],
            true_outliers=json['true_outliers']
        )
