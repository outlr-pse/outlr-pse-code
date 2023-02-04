from models.base import Base
from models.odm.odm import ODM
from models.results.experiment_result import ExperimentResult

from sqlalchemy import ForeignKey, Integer, JSON, ARRAY
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Experiment(Base):
    __tablename__: str = 'experiment'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str]
    true_outliers = mapped_column(ARRAY(Integer))
    odm_id: Mapped[int] = mapped_column(ForeignKey(ODM.id))
    param_values = mapped_column(JSON)
    subspace_logic = mapped_column(JSON)
    experiment_result: Mapped["ExperimentResult"] = relationship(ExperimentResult)
    database = 8

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
