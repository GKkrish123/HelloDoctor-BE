import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .route import appointment_route, slot_route, transcribe_route, mockdb_route
from .database import create_db_engine, create_db_session, generate_rasa_agent

# METADATA TAGS FOR SWAGGER AND DOCS
tags_metadata = [
    {
        "name": "Transcribe",
        "description": "Contains all API's related to transcribing user queries",
    },
    {
        "name": "Appointment",
        "description": "Contains all API's related to appointment",
    },
    {
        "name": "Slot",
        "description": "Contains all API's related to available slots of doctors",
    },
    {
        "name": "Mock DB",
        "description": "Contains all API's related to mock database",
    },
]

# DESCRIPTION OF APP
app_description = (
    "Consists of **HELLO DOCTOR APIs** which performs transcribing and appointment operations."
)

# API MIDDLEWARE
@asynccontextmanager
async def lifespan(app: FastAPI):
    # OPERATIONS ON STARTUP
    print("Starting rasa agent ...")
    generate_rasa_agent()
    print("... Started rasa agent")
    create_db_engine()
    print("... Created database engine")
    yield
    # OPERATIONS ON SHUTDOWN
    # ...

# CREATE FASTAPI APP
app = FastAPI(
    title="HELLO DOCTOR",
    description=app_description,
    version="1.0.0",
    openapi_tags=tags_metadata,
    terms_of_service="gkrish16.a@gmail.com",
    contact={
        "name": "Gokulakrishnan A",
        "url": "https://gokulakrishnan.netlify.app/",
        "email": "gkrish16.a@gmail.com",
    },
    license_info={
        "name": "FastAPI",
        "url": "https://fastapi.tiangolo.com/",
    },
    lifespan=lifespan
)

# APPLY MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MIDDLEWARE OPERATIONS
@app.middleware("http")
async def set_global_session(request: Request, call_next):
    create_db_session()
    response = await call_next(request)
    return response

# CUSTOM VALIDATION ERROR RESPONSE
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "name": err["loc"][1],
            "location": err["loc"][0],
            "detail": err["msg"],
            "type": err["type"],
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"validation_error": errors}),
    )

# INCLUDE ROUTERS
app.include_router(appointment_route.appointment_api)
app.include_router(slot_route.slot_api)
app.include_router(transcribe_route.transcribe_api)
app.include_router(mockdb_route.mockdb_api)

# APP START
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
