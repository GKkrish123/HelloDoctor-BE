from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from .base import base
from .doctor import Doctor
from sqlalchemy.orm import relationship


class Slot(base):
    slotid = Column(Integer, primary_key=True, autoincrement=True)
    doctorid = Column(Integer, ForeignKey(Doctor.doctorid))
    slottime_from = Column(String, nullable=False)
    slottime_to = Column(String, nullable=False)
    slotdate = Column(String, nullable=False)
    booked = Column(Boolean, nullable=False)
    created_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)

    doctor = relationship('Doctor', foreign_keys='Slot.doctorid')
