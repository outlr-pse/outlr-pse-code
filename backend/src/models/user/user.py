from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.experiment import Experiment


class User(Base):
    __tablename__: str = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    password: Mapped[str]
    experiments: Mapped[list["Experiment"]] = relationship()

    def to_json(self, jwt_access_token: str) -> dict:
        return {
            "username": self.name,
            "access_token": jwt_access_token
        }
