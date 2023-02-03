from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base
from models.experiment.experiment import Experiment
from models.odm.odm import ODM
from models.user.user import User

from odmprovider.pyod_scraper import PyODScraper
import config

engine = create_engine(config.db_url)
Base.metadata.create_all(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session: Session = Session()


def add_experiment(experiment: Experiment) -> Experiment:
    session.add(experiment)
    session.commit()
    return experiment


def get_experiment(exp_id: int) -> Experiment | None:
    return session.get(Experiment, exp_id)


def add_user(user: User) -> User:
    session.add(user)
    session.commit()
    return user


def get_user(user_id: int) -> User | None:
    return session.get(User, user_id)


def add_odm(odm: ODM):
    session.add(odm)
    session.commit()


def get_odm(odm_id: int) -> ODM | None:
    return session.get(ODM, odm_id)


def get_all_odms() -> list[Type[ODM]]:
    return session.query(ODM).all()


def setup_db() -> None:
    """Inserts all available ODMs into the database."""
    session.query(ODM).delete()
    odms = PyODScraper().get_odms()
    for odm in odms:
        add_odm(odm)
