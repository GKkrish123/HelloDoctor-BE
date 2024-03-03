from ..database import Appointment, Slot
from ..response import get_response


def get_appointments_controller(doctorids, scheduled, cancelled):
    try:
        appointment_filters = []
        if doctorids:
            appointment_filters.append(Appointment.doctorid.in_(doctorids))
        if scheduled != None:
            appointment_filters.append(Appointment.scheduled == (scheduled))
        if cancelled != None:
            appointment_filters.append(Appointment.cancelled == (cancelled))
        appointment_details = Appointment().fetch(appointment_filters).all()
        return get_response("APPOINTMENT_RES001", appointment_details, 200)
    except Exception:
        raise

def schedule_appointment_controller(appointment_details):
    try:
        new_appointment_details = {
            **appointment_details,
            "scheduled": True,
            "cancelled": False,
        }
        added_appointment_details = Appointment().add(new_appointment_details, session_close=False)
        slot_filters = [
            Slot.slotid == appointment_details["slotid"]
        ]
        slot_updates = {
            "booked": True
        }
        Slot().edit(slot_filters, slot_updates)
        response_data = {
            "reply_text": f'Your appointment has been scheduled succesfully. Please note your appointment id, {added_appointment_details.appointmentid}. Thanks!',
            "appointment_details": added_appointment_details,
        }
        return get_response("APPOINTMENT_RES002", response_data, 200)
    except Exception:
        raise

def reschedule_appointment_controller(old_appointmentid, new_appointment_details):
    try:
        old_appointment_filter = [
            Appointment.appointmentid == old_appointmentid
        ]
        old_appointment_updates = {
            "scheduled": False,
            "cancelled": True
        }
        old_appointment_details = Appointment().edit(old_appointment_filter, old_appointment_updates, session_close=False)
        old_slot_filters = [
            Slot.slotid == old_appointment_details.slotid
        ]
        old_slot_updates = {
            "booked": False
        }
        Slot().edit(old_slot_filters, old_slot_updates, session_close=False)
        new_appointment_details_toadd = {
            **new_appointment_details,
            "scheduled": True,
            "cancelled": False,
        }
        added_appointment_details = Appointment().add(new_appointment_details_toadd, session_close=False)
        new_slot_filters = [
            Slot.slotid == new_appointment_details["slotid"]
        ]
        new_slot_updates = {
            "booked": True
        }
        Slot().edit(new_slot_filters, new_slot_updates)
        response_data = {
            "reply_text": f'Your appointment has been rescheduled succesfully. Please note your new appointment id, {added_appointment_details.appointmentid}. Thanks!',
            "appointment_details": added_appointment_details,
        }
        return get_response("APPOINTMENT_RES003", response_data, 200)
    except Exception:
        raise

def cancel_appointment_controller(appointmentid):
    try:
        appointment_filter = [
            Appointment.appointmentid == appointmentid,
        ]
        appointment_details = {
            "cancelled": True
        }
        edited_appointment_details = Appointment().edit(appointment_filter, appointment_details, session_close=False)
        slot_filters = [
            Slot.slotid == edited_appointment_details.slotid
        ]
        slot_updates = {
            "booked": False
        }
        Slot().edit(slot_filters, slot_updates)
        response_data = {
            "reply_text": f'Your appointment has been cancelled succesfully. Thanks!',
            "appointment_details": edited_appointment_details,
        }
        return get_response("APPOINTMENT_RES004", response_data, 200)
    except Exception:
        raise
