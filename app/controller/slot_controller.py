from ..database import Slot
from ..response import get_response


def get_slots_controller(doctorids, booked):
    try:
        slot_filters = []
        if doctorids:
            slot_filters.append(Slot.doctorid.in_(doctorids))
        if booked != None:
            slot_filters.append(Slot.booked == (booked))
        slots_details = Slot().fetch(slot_filters).all()
        slots_string = ""
        for index, slot in enumerate(slots_details):
            slots_string += f'{index + 1}. {slot.slottime_from} to {slot.slottime_to} on {slot.slotdate}, '
        reply_text = "Unfortunately, Currently all the slots are booked. Please contact the office directly. Thanks!"
        if slots_string:
            reply_text = f'The following are the available slot details. Please choose one to book. {slots_string}'
        response_data = {
            "reply_text": reply_text,
            "slots_details": slots_details,
        }
        return get_response("SLOT_RES001", response_data, 200)
    except Exception:
        raise

def add_slot_controller(slot_details):
    try:
        added_slot_details = Slot().add(slot_details)
        return get_response("SLOT_RES002", added_slot_details, 200)
    except Exception:
        raise

def edit_slot_controller(slotid, slot_details):
    try:
        slot_filters = [
            Slot.slotid == slotid,
        ]
        edited_slot_details = Slot().edit(slot_filters, slot_details)
        return get_response("SLOT_RES003", edited_slot_details, 200)
    except Exception:
        raise

def delete_slot_controller(slotid):
    try:
        slot_filter = [
            Slot.slotid == slotid
        ]
        Slot().delete(slot_filter)
        return get_response("SLOT_RES004", None, 200)
    except Exception:
        raise