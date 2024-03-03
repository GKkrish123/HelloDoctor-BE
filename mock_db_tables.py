from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from app.config import (
    SQL_DB_SYSTEM,
    DB_USERNAME,
    DB_PASSWORD,
    DB_SERVER,
    DB_HOST,
    DB_PORT,
)

db_string = (
    f"{SQL_DB_SYSTEM}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SERVER}"
)

db = create_engine(db_string)
base = declarative_base()


class Doctor(base):
    __tablename__ = "doctor"

    doctorid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    mobilenumber = Column(String, nullable=False)
    email = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    address = Column(String, nullable=False)
    created_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)


class Slot(base):
    __tablename__ = "slot"

    slotid = Column(Integer, primary_key=True, autoincrement=True)
    doctorid = Column(Integer, ForeignKey(Doctor.doctorid))
    slottime_from = Column(String, nullable=False)
    slottime_to = Column(String, nullable=False)
    slotdate = Column(String, nullable=False)
    booked = Column(Boolean, nullable=False)
    created_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)

    doctor = relationship('Doctor', foreign_keys='Slot.doctorid')


class Appointment(base):
    __tablename__ = "appointment"

    appointmentid = Column(Integer, primary_key=True, autoincrement=True)
    slotid = Column(Integer, ForeignKey(Slot.slotid))
    doctorid = Column(Integer, ForeignKey(Doctor.doctorid))
    patientname = Column(String, nullable=False)
    patientmobilenumber = Column(String, nullable=False)
    scheduled = Column(Boolean, nullable=False)
    cancelled = Column(Boolean, nullable=False)
    created_date = Column(DateTime, nullable=False)
    modified_date = Column(DateTime, nullable=False)

    doctor = relationship('Doctor', foreign_keys='Appointment.doctorid')
    slot = relationship('Slot', foreign_keys='Appointment.slotid')


objects = [
    Doctor(
        name = "Dr. Gokul",
        mobilenumber = "+911234567890",
        email = "gk@gmail.com",
        specialization = "Dental",
        address = "IND...",
        created_date = datetime.now(),
        modified_date = datetime.now(),
    ),
    Doctor(
        name = "Dr. Roshan Patel",
        mobilenumber = "+919876543210",
        email = "roshanPatel@gmail.com",
        specialization = "Cardaic",
        address = "NYC...",
        created_date = datetime.now(),
        modified_date = datetime.now(),
    )
]


def create_mock_tables(session=None):
    base.metadata.create_all(db)
    if not session:
        Session = sessionmaker(db)
        session = Session()
    session.bulk_save_objects(objects)
    session.commit()
    session.close()


def delete_mock_tables():
    base.metadata.drop_all(db)


if __name__ == "__main__":
    create_mock_tables()
    print("\n! MOCK TABLES CREATED SUCCESSFULLY !")
