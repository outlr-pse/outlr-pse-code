from typing import Optional
from sqlalchemy import ForeignKey, Integer, JSON, ARRAY
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.base import Base
from models.odm.odm import ODM
from models.results import ExperimentResult


class Experiment(Base):
    __tablename__: str = 'experiment'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    name: Mapped[str]
    true_outliers = mapped_column(ARRAY(Integer))
    param_values = mapped_column(JSON)
    _subspace_logic = mapped_column(JSON)
    dataset_name: Mapped[Optional[str]]

    odm_id: Mapped[int] = mapped_column(ForeignKey(ODM.id))
    odm: Mapped['ODM'] = relationship()

    experiment_result: Mapped["ExperimentResult"] = relationship(
        foreign_keys=[ExperimentResult.experiment_id, ExperimentResult.user_id],
        primaryjoin="and_(Experiment.id==ExperimentResult.experiment_id, Experiment.user_id==ExperimentResult.user_id)")

    # The dataset cannot have a type annotation. Otherwise, SQLAlchemy will try to create a column for it.
    dataset = None

    # TODO subspace_logic property that (lazily) converts between db json and actual subspace logic instance
    # Can be implemented with the feature backend/models-subspacelogic
    # https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#using-descriptors-and-hybrids
    @property
    def subspace_logic(self):
        return self._subspace_logic

    @subspace_logic.setter
    def subspace_logic(self, subspace_logic: any):
        self._subspace_logic = subspace_logic

    def to_json(self, with_outliers: bool) -> dict:
        exp = {
            'id': self.id,
            'name': self.name,
            'dataset_name': self.dataset_name,
            'odm': self.odm.to_json(),
            'param_values': self.param_values,
            'experiment_result': self.experiment_result.to_json(with_outliers),
        }
        if with_outliers:
            exp['subspace_logic'] = self.subspace_logic
        return exp

    @classmethod
    def from_json(cls, exp_json: dict):
        return cls(
            name=exp_json['name'],
            user_id=exp_json['user_id'],
            dataset_name=exp_json['dataset_name'],
            subspace_logic=exp_json['subspace_logic'],
            odm_id=exp_json['odm']['id'],
            param_values=exp_json['odm']['hyper_parameters'],
        )
