from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.experiment import Experiment


class User(Base):
    __tablename__: str = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    password: Mapped[str]
    experiments: Mapped[list["Experiment"]] = relationship()

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }

    @classmethod
    def from_json(cls, json: dict):
        return cls(
            name=json["name"]
        )
