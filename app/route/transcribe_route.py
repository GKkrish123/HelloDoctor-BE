from fastapi import UploadFile, Body
from typing import Union
import json
from ..controller import process_transcription
from ..response import get_response
from . import transcribe_api

@transcribe_api.post("")
async def transcribe(audio_file: Union[UploadFile, None] = None, session_data: str = Body(...)):
    try:
        audio_bytes = None
        if audio_file:
          audio_bytes = await audio_file.read()
        processed_response = await process_transcription(audio_bytes, json.loads(session_data))
        return processed_response
    except Exception as e:
        print("get_slot exception : ", e)
        return get_response("TRANSCRIBE_ERR001", None, 409)
