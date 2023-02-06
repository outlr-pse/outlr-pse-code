from datetime import datetime, timedelta

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import Base
from models.results.subspace_outlier import Subspace, Outlier


class ExperimentResult(Base):
    __tablename__ = "experiment_result"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiment.id"))
    accuracy: Mapped[float]
    execution_date: Mapped[datetime]
    execution_time: Mapped[timedelta]
    subspaces = relationship(Subspace)
    outliers = relationship(Outlier)

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "accuracy": self.accuracy,
            "execution_date": self.execution_date,
            "execution_time": self.execution_time,
            "subspaces": self.subspaces,
            "outliers": self.outliers
        }
