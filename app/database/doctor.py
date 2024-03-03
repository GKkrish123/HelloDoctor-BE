from sqlalchemy import Column, String, Integer, DateTime
from .base import base


class Doctor(base):
    doctorid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    mobilenumber = Column(String, nullable=False)
    email = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)
