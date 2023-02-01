from models.base import Base
from sqlalchemy import ForeignKey, Integer, JSON, ARRAY
from sqlalchemy.orm import mapped_column, Mapped


class Experiment(Base):
    __tablename__: str = 'experiments'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    name: Mapped[str]
    subspace_logic = mapped_column(JSON)
    odm_params = mapped_column(JSON)
    true_outliers = mapped_column(ARRAY(Integer))

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
