from fastapi import APIRouter

# CREATE API ROUTERS
transcribe_api = APIRouter(prefix="/transcribe", tags=["Transcribe"])
appointment_api = APIRouter(prefix="/appointment", tags=["Appointment"])
slot_api = APIRouter(prefix="/slot", tags=["Slot"])
mockdb_api = APIRouter(prefix="/mockdb", tags=["Mock DB"])
