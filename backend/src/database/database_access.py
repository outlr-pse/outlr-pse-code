from typing import Type, Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base
from models.experiment import Experiment
from models.odm.hyper_parameter import HyperParameter
from models.odm.odm import ODM
from models.user.user import User

from odmprovider.pyod_scraper import PyODScraper
import config

engine = create_engine(config.db_url)
Base.metadata.create_all(bind=engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session: Session = Session()


def add_experiment(experiment: Experiment) -> Experiment:
    if any(subspace.id is None for subspace in experiment.subspaces):
        # Ensure that all subspace ids are available for the following subspace logic json update
        # Note: It might be better to store the subspace logic as a class hierarchy instead of as a json.
        #       That way SQLAlchemy would load the correct ids on its own
        session.add(experiment)
        session.flush()

    experiment.update_subspace_logic_json()
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
    return session.query(ODM).filter_by(deprecated=False).all()


def setup_db() -> None:
    """Inserts all available ODMs into the database."""
    db_odms: list[Type[ODM]] = get_all_odms()
    for db_odm in db_odms:
        db_odm.deprecated = True
    session.commit()
    odms: Iterator[ODM] = PyODScraper().get_odms()
    for odm in odms:
        db_odm: Type[ODM] = session.query(ODM).filter_by(name=odm.name).first()
        if db_odm is not None:
            session.query(HyperParameter).filter_by(odm_id=db_odm.id).delete()
            for param in odm.hyper_parameters:
                param.odm_id = db_odm.id
                session.add(param)
            new_hyper_params = session.query(HyperParameter).filter_by(odm_id=db_odm.id).all()
            db_odm.deprecated = False
            db_odm.hyper_parameters = new_hyper_params
        else:
            session.add(odm)
    session.commit()
