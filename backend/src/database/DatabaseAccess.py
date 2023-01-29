from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base
from models.experiment.experiment import Experiment
from models.odm.odm import ODM
from models.user.user import User

engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
Base.metadata.create_all(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session: Session


def get_experiment(self, experiment: Experiment):
    return self.session.query(Experiment).filter_by(id=experiment.id).first()


def get_experiment(self, id: int):
    return self.session.query(Experiment).filter_by(id=id).first()


def get_user_experiments(self, user: User):
    return self.session.query(Experiment).filter_by(user=user).all()


def add_user(self, user: User):
    self.session.add(user)
    self.session.commit()


def get_user(self, id: int):
    return self.session.query(User).filter_by(id=id).first()


def add_odm(self, odm: ODM):
    self.session.add(odm)
    self.session.commit()


def get_odm(self, id: int):
    return self.session.query(ODM).filter_by(id=id).first()
