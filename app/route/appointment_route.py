from typing import List
from fastapi import Query, Path
from ..response import get_response
from ..request import schedule_appointment_model
from ..controller import get_appointments_controller, schedule_appointment_controller, reschedule_appointment_controller, cancel_appointment_controller
from . import appointment_api


@appointment_api.get("")
async def get_appointments(
    doctorids: List[str] = Query(None, description="Enter the ids of doctors"),
    scheduled: bool = Query(None, description="Enter the scheduled status of the appointment"),
    cancelled: bool = Query(None, description="Enter the cancelled status of the appointment"),
):
    try:
        return get_appointments_controller(doctorids, scheduled, cancelled)
    except Exception as e:
        print("get_appointments exception : ", e)
        return get_response("APPOINTMENT_ERR001", None, 409)

@appointment_api.post("/schedule")
async def schedule_appointment(appointment_details: schedule_appointment_model):
    try:
        return schedule_appointment_controller(appointment_details.dict())
    except Exception as e:
        print("schedule_appointment exception : ", e)
        return get_response("APPOINTMENT_ERR002", None, 409)

@appointment_api.put("/reschedule/{appointmentid}")
async def reschedule_appointment(
    new_appointment_details: schedule_appointment_model,
    appointmentid: int = Path(..., description="Enter the id of appointment"),
):
    try:
        return reschedule_appointment_controller(appointmentid, new_appointment_details.dict())
    except Exception as e:
        print("reschedule_appointment exception : ", e)
        return get_response("APPOINTMENT_ERR003", None, 409)

@appointment_api.delete("/cancel/{appointmentid}")
async def cancel_appointment(
    appointmentid: int = Path(..., description="Enter the id of appointment"),
):
    try:
        return cancel_appointment_controller(appointmentid)
    except Exception as e:
        print("cancel_appointment exception : ", e)
        return get_response("APPOINTMENT_ERR004", None, 409)
