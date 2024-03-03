from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from .base import base
from sqlalchemy.orm import relationship
from .slot import Slot
from .doctor import Doctor


class Appointment(base):
    appointmentid = Column(Integer, primary_key=True, autoincrement=True)
    slotid = Column(Integer, ForeignKey(Slot.slotid))
    doctorid = Column(Integer, ForeignKey(Doctor.doctorid))
    patientname = Column(String, nullable=False)
    patientmobilenumber = Column(String, nullable=False)
    scheduled = Column(Boolean, nullable=False)
    cancelled = Column(Boolean, nullable=False)
    created_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)

    slot = relationship('Slot', foreign_keys='Appointment.slotid')
    doctor = relationship('Doctor', foreign_keys='Appointment.doctorid')
