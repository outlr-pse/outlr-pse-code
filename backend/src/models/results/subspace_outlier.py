from sqlalchemy import Column, Integer, ARRAY, Table, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base

subspace_outlier = Table(
    "subspace_outlier",
    Base.metadata,
    Column("subspace_id", ForeignKey("subspace.id"), primary_key=True),
    Column("outlier_index", ForeignKey("outlier.index"), primary_key=True),
)


class Subspace(Base):
    __tablename__ = "subspace"
    id = Column(Integer, primary_key=True, autoincrement=True)
    columns = Column(ARRAY(Integer))
    outliers = relationship("Outlier", secondary="association_table1", back_populates="subspace")
    experiment_result = relationship("ExperimentResult", back_populates="subspaces", primary_key=True)

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "columns": self.columns,
            "outliers": self.outliers
        }


class Outlier(Base):
    __tablename__ = "outlier"
    index = Column(Integer, primary_key=True)
    experiment_result = relationship("ExperimentResult", back_populates="outliers", primary_key=True)
    subspaces = relationship("Subspace", secondary="association_table1", back_populates="outlier")

    def to_json(self) -> dict:
        return {
            "index": self.index,
            "subspaces": self.subspaces
        }
