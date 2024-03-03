from pydantic import BaseModel, Field, root_validator, validator
from ..database import Slot
from datetime import datetime


class schedule_appointment_model(BaseModel):
    slotid: int = Field(..., description="ID of the slot")
    doctorid: int = Field(..., description="ID of the doctor")
    patientname: str = Field(..., description="Name of the patient")
    patientmobilenumber: str = Field(..., description="Mobile number of the patient", min_length=6)

    # @validator("patientdob")
    # def should_be_valid_dob(cls, v):
    #     try:
    #         datetime.strptime(v, "%d/%m/%Y")
    #     except ValueError as e:
    #         raise ValueError(f"Invalid date -> {e}")
    #     return v
    
    # @validator("patientmobilenumber")
    # def should_be_valid_patientmobilenumber(cls, v):
    #     try:
    #         datetime.strptime(v, "%d/%m/%Y")
    #     except ValueError as e:
    #         raise ValueError(f"Invalid date -> {e}")
    #     return v

    @root_validator()
    def should_be_valid_slot(cls, values):
        try:
            slot_filters = [
                Slot.slotid == values["slotid"],
                Slot.doctorid == values["doctorid"],
            ]
            data = Slot().fetch(slot_filters).first()
            if data == None:
                raise ValueError("Please add the slot details for adding appointment")
        except ValueError as e:
            raise ValueError(f"Unregistered slot or doctor -> {e}")
        return values
