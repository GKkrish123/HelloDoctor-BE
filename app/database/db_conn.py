from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from rasa.core.agent import Agent
from ..config import (
    SQL_DB_SYSTEM,
    DB_USERNAME,
    DB_PASSWORD,
    DB_SERVER,
    DB_HOST,
    DB_PORT,
)

DB_URL = (
    f"{SQL_DB_SYSTEM}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SERVER}"
)
db_engine = None
session = None
rasa_agent = None


def create_db_engine():
    global db_engine
    db_engine = create_engine(DB_URL)

def get_rasa_agent():
    global rasa_agent
    return rasa_agent

def get_session():
    global session
    return session

def generate_rasa_agent():
    global rasa_agent
    rasa_agent = Agent.load(model_path="app/rasa_models/nlu_engine.tar.gz")

def create_db_session():
    global db_engine
    global session
    db_session = sessionmaker(
        autoflush=True, autocommit=False, bind=db_engine, expire_on_commit=False
    )
    session = db_session()
