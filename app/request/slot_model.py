from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date, datetime
from ..database import Doctor

class edit_slot_model(BaseModel):
    slottime_from: str = Field(..., description="Start time of slot", example="10:00")
    slottime_to: str = Field(..., description="End time of slot", example="11:00")
    slotdate: Optional[str] = Field(
        date.today().strftime("%d/%m/%Y"),
        description="Date of slot",
        example="dd/mm/yyyy",
    )
    booked: Optional[bool] = Field(
        False,
        description="Booked status of slot"
    )

    # @validator("slotdate")
    # def should_be_valid_date(cls, v):
    #     try:
    #         datetime.strptime(v, "%d/%m/%Y")
    #     except ValueError as e:
    #         raise ValueError(f"Invalid date -> {e}")
    #     return v
    
    # @validator("slottime_from", "slottime_to")
    # def should_be_valid_slot_time(cls, v):
    #     try:
    #         datetime.strptime(v, "%H:%M")
    #     except ValueError as e:
    #         raise ValueError(f"Invalid time -> {e}")
    #     return v

class add_slot_model(edit_slot_model):
    doctorid: int = Field(..., description="ID of the doctor")

    @validator("doctorid")
    def should_be_valid_doctor(cls, v):
        try:
            doctor_filter = [
                Doctor.doctorid == v
            ]
            data = Doctor().fetch(doctor_filter).first()
            if data == None:
                raise ValueError("Invalid doctorid. Please add the doctor details for adding slot")
        except ValueError as e:
            raise ValueError(f"Unregistered doctor -> {e}")
        return v
