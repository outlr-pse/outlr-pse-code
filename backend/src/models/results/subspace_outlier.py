from sqlalchemy import Column, Integer, ARRAY, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from models.base import Base

subspace_outlier = Table(
    "subspace_outlier",
    Base.metadata,
    Column("subspace_id", ForeignKey("subspace.id")),
    Column("outlier_index", ForeignKey("outlier.index")),
)


class Subspace(Base):
    __tablename__ = "subspace"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    experiment_result_id: Mapped[int] = mapped_column(ForeignKey("experiment_result.id"))
    columns = Column(ARRAY(Integer))
    outliers: Mapped[list["Outlier"]] = relationship(secondary=subspace_outlier)

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "columns": self.columns,
            "outliers": self.outliers
        }


class Outlier(Base):
    __tablename__ = "outlier"
    index = Column(Integer, primary_key=True)
    experiment_result_id: Mapped[int] = mapped_column(ForeignKey("experiment_result.id"))
    subspaces: Mapped[list["Subspace"]] = relationship(secondary=subspace_outlier)

    def to_json(self) -> dict:
        return {
            "index": self.index,
            "subspaces": self.subspaces
        }
