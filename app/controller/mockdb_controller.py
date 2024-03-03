from mock_db_tables import create_mock_tables, delete_mock_tables
from ..database import get_session
from ..response import get_response

def create_mock_db_tables_controller():
    try:
        session = get_session()
        create_mock_tables(session)
        return get_response("MOCK_RES001", None, 200)
    except Exception:
        raise

def delete_mock_db_tables_controller():
    try:
        delete_mock_tables()
        return get_response("MOCK_RES002", None, 200)
    except Exception:
        raise