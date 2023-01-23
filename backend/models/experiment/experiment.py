from models.base import Base
from sqlalchemy import Column, Integer, Text, JSON
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship


class Experiment(Base):
    __tablename__ = 'experiments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = relationship("User", uselist=False)
    name = Column(Text, nullable=False)
    subspace_logic = Column(JSON, nullable=False)
    odm = relationship("ODM", uselist=False)
    odm_params = Column(JSON, nullable=False)
    result = relationship("Result", uselist=False)
    true_outliers = Column(ARRAY(Integer))
