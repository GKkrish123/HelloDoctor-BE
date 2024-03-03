from fastapi import Query, Path
from pydantic import Field
from typing import List
from ..response import get_response
from ..controller import get_slots_controller, add_slot_controller, delete_slot_controller, edit_slot_controller
from ..request import add_slot_model, edit_slot_model
from . import slot_api

@slot_api.get("")
async def get_slot(
    doctorids: List[str] = Query(None, description="Enter the ids of doctors"),
    booked: bool = Query(None, description="Enter the booked status of the slot"),
):
    try:
        return get_slots_controller(doctorids, booked)
    except Exception as e:
        print("get_slot exception : ", e)
        return get_response("SLOT_ERR001", None, 409)

@slot_api.post("")
async def add_slot(slot_details: add_slot_model):
    try:
        return add_slot_controller(slot_details.dict())
    except Exception as e:
        print("add_slot exception : ", e)
        return get_response("SLOT_ERR002", None, 409)

@slot_api.put("/{slotid}")
async def edit_slot(
    slot_details: edit_slot_model,
    slotid: int = Path(..., description="ID of the slot")
):
    try:
        return edit_slot_controller(slotid, slot_details.dict())
    except Exception as e:
        print("edit_slot exception : ", e)
        return get_response("SLOT_ERR003", None, 409)

@slot_api.delete("/{slotid}")
async def delete_slot(
    slotid: int = Path(..., description="Enter the id of slot"),
):
    try:
        return delete_slot_controller(slotid)
    except Exception as e:
        print("delete_slot exception : ", e)
        return get_response("SLOT_ERR004", None, 409)
