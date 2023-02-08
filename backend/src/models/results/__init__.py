from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import Column, Integer, ARRAY, Table, ForeignKey, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

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
    # UniqueConstraint("outlier_index", "outlier_experiment_result_id"),
    ForeignKeyConstraint(
        ["outlier_experiment_result_id", "outlier_index"],
        [f"{OUTLIER_TABLE_NAME}.experiment_result_id", f"{OUTLIER_TABLE_NAME}.index"]
    ),  # Copied from a StackOverflow answer without knowing what it does
)


class Subspace(Base):
    """
    Represents a Subspace
    Attributes:
        id (int): Primary key
        columns (list[int]): The column indices that define this subspace
        name (Optional[str]): An optional name (assigned by the user)
        experiment_result (Optional[ExperimentResult]): The ExperimentResult that this subspace belongs to.
            Is None for the result space
        outliers (list[Outlier]): The Outliers in this Subspace
    """
    __tablename__ = SUBSPACE_TABLE_NAME

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    columns = mapped_column(ARRAY(Integer), default=[])
    name: Mapped[Optional[str]]

    experiment_result_id: Mapped[Optional[int]] = mapped_column(ForeignKey(f"{EXPERIMENT_RESULT_TABLE_NAME}.id"))
    experiment_result: Mapped[Optional['ExperimentResult']] = relationship(
        back_populates="subspaces",
        foreign_keys=[experiment_result_id]
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
        subspaces (list[Subspace]): Subspaces that are part of this result. Does not contain the result_space
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
    user_id: Mapped[int]
    experiment_id: Mapped[int]
    ForeignKeyConstraint(
        ["user_id", "experiment_id"],
        ["experiment.user_id", "experiment.id"]
    )

    # back_populates means that the experiment_result attribute of a Subspace will be connected
    # to the subspace attribute of ExperimentResult. Changing one in python also changes the other
    subspaces: Mapped[list['Subspace']] = relationship(
        # primaryjoin=Subspace.experiment_result_id == id,
        back_populates="experiment_result",
        foreign_keys=[Subspace.experiment_result_id]
    )
    outliers: Mapped[list['Outlier']] = relationship(
        back_populates="experiment_result"
    )

    result_space_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{SUBSPACE_TABLE_NAME}.id",
            name="foreign_key_result_space"
        ),
    )
    result_space: Mapped['Subspace'] = relationship(
        foreign_keys=[result_space_id],
        #  primaryjoin=result_space_id == Subspace.id,
        # post_update=True  # might be necessary for writes and deletes to work
    )

    def to_json(self, include_result_space: bool) -> dict:
        """Convert ExperimentResult to JSON.
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
        result = {
            "id": self.id,
            "accuracy": self.accuracy,
            "execution_date": self.execution_date.isoformat(),  # ISO 8601 format
            "execution_time": ExperimentResult.microseconds(self.execution_time),  # in μs (microseconds)
        }
        if include_result_space:
            result["result_space"] = self.result_space.to_json()
        return result

    @staticmethod
    def microseconds(duration: timedelta) -> int:
        return int(duration.total_seconds() * 1000000 + duration.microseconds)
