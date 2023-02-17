from typing import Type, Iterator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base
from models.experiment import Experiment
from models.odm import HyperParameter
from models.odm import ODM
from models.user import User

from odmprovider.pyod_scraper import PyODScraper
import config

engine = create_engine(config.db_url)
Base.metadata.create_all(bind=engine, checkfirst=True)

# Documentation on how session should be used:
# https://docs.sqlalchemy.org/en/20/orm/session_basics.html#session-frequently-asked-questions
Session = sessionmaker(bind=engine)


def add_experiment(session: Session, experiment: Experiment) -> Experiment:
    """
    Add an experiment to the database.
    Also sets the id of the experiment and updates the subspace logic json
    Args:
        session: A SQLAlchemy session
        experiment (Experiment): The experiment to add

    Returns: Returns the experiment with the id set and the subspace logic json updated
    """
    session.add(experiment)
    session.flush()
    experiment.update_subspace_logic_json()
    session.commit()
    return experiment


def get_experiment(session: Session, user_id: int, exp_id: int) -> Experiment | None:
    return session.get(Experiment, {'user_id': user_id, 'id': exp_id})


def add_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    return user


def get_user(session: Session, user: int | str) -> Optional[User]:
    """Returns the user with the given id or name.

    Args:
        session: A SQLAlchemy session
        user: Either the user id as an int or the user's name as a str.

    Returns:
        The user or None if no such user exists.
    """
    if isinstance(user, str):
        return session.query(User).filter_by(name=user).first()
    return session.get(User, user)


def add_odm(session: Session, odm: ODM):
    session.add(odm)
    session.commit()


def get_odm(session: Session, odm_id: int) -> ODM | None:
    return session.get(ODM, odm_id)


def get_all_odms(session: Session) -> list[Type[ODM]]:
    return session.query(ODM).filter_by(deprecated=False).all()


def setup_db() -> None:
    """Inserts all available ODMs into the database."""
    with Session() as session:
        db_odms: list[Type[ODM]] = get_all_odms(session)
        for db_odm in db_odms:
            db_odm.deprecated = True  # TODO only ODMs that are to be scraped again should be marked as deprecated
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
