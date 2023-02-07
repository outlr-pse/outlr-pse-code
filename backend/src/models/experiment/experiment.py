from typing import Optional

from models.base import Base
from models.odm.odm import ODM
from models.results import ExperimentResult
from models.subspacelogic.subspacelogic import SubspaceLogic

from sqlalchemy import ForeignKey, Integer, JSON, ARRAY
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property


class Experiment(Base):
    """
    Represent an Experiment.
    Attributes:
        id (int): Primary key
        user_id (int): ID of the user that created this experiment
        name (str): Name, assigned by user
        true_outliers: The indices of the datapoints that are outliers according to a ground-truth file
        param_values: Contains all hyperparameter values that the user selected
        _subspace_logic: Subspace logic as JSON. Use the property ``subspace_logic`` instead
        dataset_name (Optional[str])): Name the user assigned to the dataset
        dataset_size (int): Total number of datapoints (rows) in the dataset. Needed for SubspaceLogic evaluation
        odm_id (int): ID of the odm. See attribute ``odm``
        odm (ODM): ODM that for used in this experiment
        experiment_result (Optional[ExperimentResult]): Result of the experiment.
            Is None if the experiment has not yet been run
        dataset (Dataset): Dataset. This attribute is not stored in the database
    """

    __tablename__: str = 'experiment'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str]
    true_outliers = mapped_column(ARRAY(Integer))
    param_values = mapped_column(JSON)
    _subspace_logic = mapped_column(JSON)
    dataset_name: Mapped[Optional[str]]
    dataset_size: Mapped[int]

    odm_id: Mapped[int] = mapped_column(ForeignKey(ODM.id))
    odm: Mapped['ODM'] = relationship()

    experiment_result: Mapped["ExperimentResult"] = relationship(ExperimentResult)

    # The dataset cannot have a type annotation. Otherwise, SQLAlchemy will try to create a column for it.
    dataset = None

    # TODO subspace_logic property that (lazily) converts between db json and actual subspace logic instance
    # Can be implemented with the feature backend/models-subspacelogic
    # https://docs.sqlalchemy.org/en/20/orm/mapped_attributes.html#using-descriptors-and-hybrids
    @hybrid_property
    def subspace_logic(self) -> SubspaceLogic:
        """Property subspace_logic (SubspaceLogic)"""
        subspace_map = {subspace.id: subspace for subspace in self.experiment_result.subspaces}
        return SubspaceLogic.from_database_json(self._subspace_logic, subspace_map)
        #  TODO !!! This does not work. experiment_result is not present. Maybe move subspaces to experiment
        #  TODO !!! How can we get the subspaces from the experiment class. Whats the state in which we get and set subspace_logic
        #  TODO !!! Maybe make this attribute dependent of subspaces if the subspaces always exist in situations where subspace_logic is accessed

    @subspace_logic.setter
    def subspace_logic(self, subspace_logic: SubspaceLogic):
        self._subspace_logic = subspace_logic.to_database_json()

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
