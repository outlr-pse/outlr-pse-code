"""
This module contains all models relating to experiments and their results
Because of the relations between the classes in the database it is easier if all of them are in the same file
"""

from datetime import datetime, timedelta
from typing import Optional

from models.base import Base
from models.odm.odm import ODM

from sqlalchemy import Column, Table, Integer, JSON, ARRAY, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship


EXPERIMENT_TABLE_NAME = "experiment"
EXPERIMENT_RESULT_TABLE_NAME = "experiment_result"
SUBSPACE_TABLE_NAME = "subspace"
OUTLIER_TABLE_NAME = "outlier"

# Association table for the many-to-many relationship between Subspaces and Outliers
subspace_outlier = Table(
    "subspace_outlier",
    Base.metadata,
    Column("subspace_id", ForeignKey(f"{SUBSPACE_TABLE_NAME}.id"), primary_key=True),
    Column("outlier_index", Integer, primary_key=True),
    Column("outlier_experiment_result_id", Integer, primary_key=True),
    ForeignKeyConstraint(
        ["outlier_experiment_result_id", "outlier_index"],
        [f"{OUTLIER_TABLE_NAME}.experiment_result_id", f"{OUTLIER_TABLE_NAME}.index"]
    ),
)


class Subspace(Base):
    """
    Represents a Subspace
    Attributes:
        id (int): Primary key
        columns (list[int]): The column indices that define this subspace
        name (Optional[str]): An optional name (assigned by the user)
        experiment_id (int): The id of the experiment that this subspace belongs to. See attribute ``experiment``
        experiment (Optional[Experiment]): The Experiment that this subspace belongs to.
            Is None for the result space
        outliers (list[Outlier]): The Outliers in this Subspace
    """
    __tablename__ = SUBSPACE_TABLE_NAME

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    columns = mapped_column(ARRAY(Integer), default=[])
    name: Mapped[Optional[str]]

    experiment_id: Mapped[Optional[int]] = mapped_column(ForeignKey(f"{EXPERIMENT_TABLE_NAME}.id"))
    experiment: Mapped[Optional['Experiment']] = relationship(
        back_populates="subspaces",
        foreign_keys=[experiment_id]
    )

    outliers: Mapped[list['Outlier']] = relationship(  # many-to-many
        secondary=subspace_outlier,
        back_populates="subspaces"
    )

    def to_json(self) -> dict:
        """
        Convert Subspace to JSON
        Returns: Returns the JSON as a dict
        Example:
            {
                "id": 23,
                "name": null,    # can be something like "subspace1"
                "columns": [0, 1, 3],
                "outliers": [0, 2]
            }
        """
        return {
            "id": self.id,
            "name": self.name,
            "columns": self.columns if self.columns is not None else [],
            "outliers": [outlier.index for outlier in self.outliers],
            "roc_curve": None
        }

    @staticmethod
    def from_client_json(json: dict) -> 'Subspace':
        """
        Parse Subspace form json that was received from a client
        Args:
            json: JSON dict. Only id, columns and name are read.
                Currently, clients cannot send other attributes, like for example outliers
        """
        return Subspace(
            id=json.get("id"),  # Can be None
            columns=list(set(json["columns"])),
            name=json.get("name"),  # Can be None
        )


class Outlier(Base):
    """
    Represents an Outlier
    Attributes:
        index (int): Primary key, Index of the datapoint in the dataset that is represented by this Outlier instance
        experiment_result_id (int): Primary key, See attribute experiment_result
        experiment_result (ExperimentResult): The ExperimentResult that contains this outlier.
            The corresponding id (attribute experiment_result_id) is a primary key
        subspaces (list[Subspace]): All subspaces that this Outlier instance is an outlier in
    """

    __tablename__ = OUTLIER_TABLE_NAME

    index: Mapped[int] = mapped_column(primary_key=True)
    experiment_result_id: Mapped[int] = mapped_column(
        ForeignKey(f"{EXPERIMENT_RESULT_TABLE_NAME}.id"),
        primary_key=True
    )
    experiment_result: Mapped['ExperimentResult'] = relationship(back_populates="outliers")

    subspaces: Mapped[list['Subspace']] = relationship(  # many-to-many
        secondary=subspace_outlier,
        back_populates="outliers"
    )


class ExperimentResult(Base):
    """
    Represents the result of an experiment
    Attributes:
        id (int): Database id (This is assigned by the database, objects that were not added to the database have no id)
        accuracy (float): Accuracy of the experiment (percentage of correct answers)
        execution_date (datetime): Date and time when the execution started
        execution_time (timedelta): Duration of the execution
        experiment_id (
        result_space (Subspace): The subspace that contains the result with applied subspace logic
        outliers (list[Outlier]): Outliers that are part of this result
    Example:
        You can create an instance of this class like this:
        ``result = ExperimentResult(id=2, accuracy=0.89)``
        You can pass a value for all the other attributes likewise
    """
    __tablename__ = EXPERIMENT_RESULT_TABLE_NAME

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    accuracy: Mapped[float]
    execution_date: Mapped[datetime]
    execution_time: Mapped[timedelta]
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiment.id"))
    experiment: Mapped['Experiment'] = relationship(back_populates="experiment_result")

    outliers: Mapped[list['Outlier']] = relationship(
        back_populates="experiment_result"
    )

    result_space_id: Mapped[int] = mapped_column(
        ForeignKey(f"{SUBSPACE_TABLE_NAME}.id", name="foreign_key_result_space"),
    )
    result_space: Mapped['Subspace'] = relationship(
        foreign_keys=[result_space_id],
        # post_update=True  # might be necessary for writes and deletes to work
    )

    def to_json(self) -> dict:
        """Convert ExperimentResult to JSON
        Note that the subspaces and outliers are contained in the subspace logic JSON,
        only the result space is contained in the experiment result JSON
        Example:
            {
                "id": 12,
                "accuracy": 0.89,
                "execution_date": "2023-02-05T21:54:02.038308",     # ISO 8601 format
                "execution_time": 120000000,                        # in μs (microseconds)
                "result_space": {
                    "id": 2343,
                    "name": "result"
                    "columns": [],
                    "outliers": [1, 2, 3]
                }
            }
        """
        return {
            "id": self.id,
            "accuracy": self.accuracy,
            "execution_date": self.execution_date.isoformat(),  # ISO 8601 format
            "execution_time": ExperimentResult.microseconds(self.execution_time),  # in μs (microseconds)
            "result_space": self.result_space.to_json()
        }

    @staticmethod
    def microseconds(duration: timedelta) -> int:
        return int(duration.total_seconds() * 1000000 + duration.microseconds)


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
        subspaces (list[Subspace]): Subspaces that belong to this experiment. Does not contain the result_space
        experiment_result (Optional[ExperimentResult]): Result of the experiment.
            Is None if the experiment has not yet been run
        dataset (Dataset): Dataset. This attribute is not stored in the database
    """

    __tablename__ = EXPERIMENT_TABLE_NAME

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str]
    true_outliers = mapped_column(ARRAY(Integer))
    param_values = mapped_column(JSON)
    _subspace_logic_json = mapped_column(JSON, nullable=True)  # must be nullable because it is written in a second step
    dataset_name: Mapped[Optional[str]]
    dataset_size: Mapped[int]

    odm_id: Mapped[int] = mapped_column(ForeignKey(ODM.id))
    odm: Mapped['ODM'] = relationship()

    subspaces: Mapped[list['Subspace']] = relationship(
         back_populates="experiment",
         foreign_keys=[Subspace.experiment_id]
    )

    experiment_result: Mapped["ExperimentResult"] = relationship(ExperimentResult)

    # The dataset cannot have a type annotation. Otherwise, SQLAlchemy will try to create a column for it.
    dataset = None
    _subspace_logic = None

    @property
    def subspace_logic(self) -> 'models.subspacelogic.SubspaceLogic':
        """Property subspace_logic (SubspaceLogic)"""
        if self._subspace_logic is None:
            # Load _subspace_logic from _subspace_logic_json
            subspace_map = {subspace.id: subspace for subspace in self.subspaces}
            self._subspace_logic = models.subspacelogic.SubspaceLogic.from_database_json(
                self._subspace_logic_json,
                subspace_map
            )
        return self._subspace_logic

    @subspace_logic.setter
    def subspace_logic(self, subspace_logic: 'models.subspacelogic.SubspaceLogic'):
        """subspace_logic property setter
        Note that the internal ``_subspace_logic_json`` is not updated by this setter
        """
        self._subspace_logic = subspace_logic
        self._subspace_logic_json = None  # json is now outdated (set no None to make sure nobody thinks its up to date)

    def update_subspace_logic_json(self):
        """
        Updates the internal ``_subspace_logic_json`` attribute (that is stored in the database)
        If the subspace_logic property was never set, nothing needs to be updated
        """
        if self._subspace_logic is not None:
            self._subspace_logic_json = self._subspace_logic.to_database_json()
        else:
            assert self._subspace_logic_json is not None

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

import models.subspacelogic  # must be at the end because of circular import
