from ..database import get_rasa_agent, generate_rasa_agent
from ..response import get_response, responsedetails
import nltk
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import io, os

nltk.download('punkt')
nltk.download('stopwords')

async def process_transcription(audio_bytes, session_data):
    try:
        # for now doctor id as 1
        session_data["doctorid"] = 1
        queried_text = session_data.get("querytext", "")
        if audio_bytes:
            queried_text = await speech_to_text(audio_bytes)
        intended_data = await parse_intent(queried_text)
        response = generate_response(session_data, **intended_data)
        # speak(response["reply_text"])
        return get_response("TRANSCRIBE_RES001", response, 200)
    except sr.UnknownValueError:
        # speak(responsedetails["responseCodeData"]["succCode"]["TRANSCRIBE_RES002"])
        return get_response("TRANSCRIBE_RES002", None, 200)
    except Exception:
        raise

async def speech_to_text(audio_bytes):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        raise
    except sr.RequestError as e:
        print(f'Could not request results from Google Speech Recognition service - {e}')
        raise
    except Exception:
        raise

async def parse_intent(text):
    try:
        rasa_agent = get_rasa_agent()
        parsed_data = await rasa_agent.parse_message(text)
        intent = parsed_data["intent"]["name"]
        confidence = parsed_data["intent"]["confidence"]
        entities = parsed_data["entities"]
        print(f"Predicted intent: {intent} (Confidence: {confidence})")
        print(f"Entities: {entities}")
        return {
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
        }
    except Exception:
        raise

def generate_response(session_data, intent, confidence, entities):
    try:
        main_intent = session_data.get("main_intent", "")
        reply_text = "I'm not able to assist with that yet. Please try contacting the office directly. Thanks!"
        session_data["make_data_call"] = False
        session_data["data_call_payload"] = {}
        if intent is None:
            reply_text = "Sorry, I couldn't understand what you intended."
        elif intent == "greet":
            reply_text = "Hello, how can I help you today?"
            if main_intent:
                reply_text = "Hey, hope you are doing good."
            if main_intent == "provide_availability" or main_intent == "book_appointment" or main_intent == "reschedule_appointment":
                number = next((entity["value"] for entity in entities if entity.get("entity") == "number"), None)
                if session_data.get("slots") and number and number.isdigit() and int(number) <= len(session_data["slots"]):
                    session_data["slotid"] = session_data["slots"][int(number) - 1]["slotid"]
                    session_data["slots"] = []
                elif len(number) > 5 and not session_data.get("patientmobilenumber"):
                    session_data["patientmobilenumber"] = number
        elif intent == "affirm":
            reply_text = "Cool"
            if main_intent:
                reply_text = "Okay, anything I can help you with?"
        elif intent == "deny":
            reply_text = "No worries, please let me if you need assistance."
            if main_intent:
                reply_text = "Hmmm, I'm not able to assist with that yet. Please try contacting the office directly. Thank you!"
        elif intent == "goodbye":
            reply_text = "Okay, Bye Bye, Take Care."
            if main_intent:
                reply_text = "Okay, Thanks for consulting. Please feel free to reach out."
        elif intent == "book_appointment":
            session_data["main_intent"] = intent
            session_data, reply_text, intent = check_values_for_main_intent(intent, session_data)
        elif intent == "cancel_appointment":
            session_data["main_intent"] = intent
            session_data, reply_text, intent = check_values_for_main_intent(intent, session_data)
        elif intent == "reschedule_appointment":
            session_data["main_intent"] = intent
            session_data, reply_text, intent = check_values_for_main_intent(intent, session_data)
        elif intent == "provide_availability":
            session_data["main_intent"] = intent
            session_data, reply_text, intent = check_values_for_main_intent(intent, session_data)
        elif intent == "provide_information":
            session_data["patientname"] = next((entity["value"] for entity in entities if entity.get("entity") == "patientname"), None)
            session_data["patientmobilenumber"] = next((entity["value"] for entity in entities if entity.get("entity") == "patientmobilenumber"), None)
            session_data, reply_text, intent = check_values_for_main_intent(main_intent, session_data)
        elif intent == "provide_name":
            session_data["name"] = next((entity["value"] for entity in entities if entity.get("entity") == "name"), None)
            session_data, reply_text, intent = check_values_for_main_intent(main_intent, session_data)
        elif intent == "provide_phone_number":
            session_data["patientmobilenumber"] = next((entity["value"] for entity in entities if entity.get("entity") == "patientmobilenumber"), None)
            session_data, reply_text, intent = check_values_for_main_intent(main_intent, session_data)
        elif intent == "provide_date_and_time":
            session_data["date"] = next((entity["value"] for entity in entities if entity.get("entity") == "date"), None)
            session_data["time"] = next((entity["value"] for entity in entities if entity.get("entity") == "time"), None)
            session_data, reply_text, intent = check_values_for_main_intent(main_intent, session_data)
        elif intent == "provide_date":
            session_data["date"] = next((entity["value"] for entity in entities if entity.get("entity") == "date"), None)
            session_data, reply_text, intent = check_values_for_main_intent(main_intent, session_data)
        elif intent == "provide_time":
            session_data["time"] = next((entity["value"] for entity in entities if entity.get("entity") == "time"), None)
            session_data, reply_text, intent = check_values_for_main_intent(main_intent, session_data)
        elif intent == "provide_number":
            if main_intent == "book_appointment" or main_intent == "reschedule_appointment":
                number = next((entity["value"] for entity in entities if entity.get("entity") == "number"), None)
                if session_data.get("slots") and number and number.isdigit() and int(number) <= len(session_data["slots"]):
                    session_data["slotid"] = session_data["slots"][int(number) - 1]["slotid"]
                    session_data["slots"] = []
                elif len(number) > 5 and not session_data.get("patientmobilenumber"):
                    session_data["patientmobilenumber"] = number
            session_data, reply_text, intent = check_values_for_main_intent(main_intent, session_data)
        return {
            **session_data,
            "intent": intent,
            "confidence": confidence,
            "entities": entities,
            "reply_text": reply_text,
        }
    except Exception:
        raise

def check_values_for_main_intent(intent, session_data):
    try:
        if not intent:
            return session_data, "Okay, May I know how can I help you?", "greet"
        missing = True
        reply_text = ""

        if intent == "book_appointment":
            if not session_data.get("patientname"):
                reply_text = "Could you please provide your name?"
                if not session_data.get("patientmobilenumber"):
                    reply_text = "Could you please provide your name and mobile number?"
            elif not session_data.get("patientmobilenumber"):
                reply_text = "Could you please provide your mobile number?"
            elif not session_data.get("slotid"):
                reply_text = "Fetching available slots. Please choose a slot to book."
                intent = "provide_availability"
            else:
                session_data["make_data_call"] = True
                session_data["data_call_payload"] = {
                    "slotid": session_data["slotid"],
                    "patientname": session_data["patientname"],
                    "patientmobilenumber": session_data["patientmobilenumber"],
                    "doctorid": session_data["doctorid"],
                }
                missing = False
        elif intent == "cancel_appointment":
            if not session_data.get("appointmentid"):
                reply_text = "Please contact the office directly to confirm your cancellation. Thanks!"
            else:
                missing = False
        elif intent == "reschedule_appointment":
            if not session_data.get("appointmentid"):
                reply_text = "Please contact the office directly to confirm your rescheduling. Thanks!"
            elif not session_data.get("patientname"):
                reply_text = "Could you please provide your name?"
                if not session_data.get("patientmobilenumber"):
                    reply_text = "Could you please provide your name and mobile number?"
            elif not session_data.get("patientmobilenumber"):
                reply_text = "Could you please provide your mobile number?"
            elif not session_data.get("slotid"):
                reply_text = "Fetching available slots. Please choose a slot to book."
                intent = "provide_availability"
            else:
                session_data["make_data_call"] = True
                session_data["data_call_payload"] = {
                    "slotid": session_data["slotid"],
                    "patientname": session_data["patientname"],
                    "patientmobilenumber": session_data["patientmobilenumber"],
                    "doctorid": session_data["doctorid"],
                }
                missing = False
        elif intent == "provide_availability":
            reply_text = "Fetching available slots. Please choose a slot to book."
            session_data["make_data_call"] = True
            session_data["data_call_payload"] = {}
            missing = False
        else:
            missing = False
        if missing:
            session_data["make_data_call"] = False
            session_data["data_call_payload"] = {}
        return session_data, reply_text, intent
    except Exception:
        raise

def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("output.mp3")
        playsound("output.mp3")
        os.remove("output.mp3")
    except FileNotFoundError:
        print("Audio file 'output.mp3' not found for removal.")
    except Exception:
        raise


import asyncio
if __name__ == "__main__":
    # for testing separately
    generate_rasa_agent()
    asyncio.run(process_transcription(None, {}))
    print("\n! MOCK TABLES CREATED SUCCESSFULLY !")
