from datetime import timedelta

from sqlalchemy import Column, Float, Integer, DateTime
from sqlalchemy.orm import relationship

from models.base import Base


class ExperimentResult(Base):
    __tablename__ = "experiment_result"
    id = Column(Integer, primary_key=True, autoincrement=True)
    accuracy = Column(Float)
    execution_date = Column(DateTime)
    execution_time = Column(timedelta)
    subspaces = relationship("Subspace", back_populates="experiment_result")
    outliers = relationship("Outlier", back_populates="experiment_result")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "accuracy": self.accuracy,
            "execution_date": self.execution_date,
            "execution_time": self.execution_time,
            "subspaces": self.subspaces,
            "outliers": self.outliers
        }
