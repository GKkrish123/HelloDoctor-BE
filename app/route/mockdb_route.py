from ..controller import create_mock_db_tables_controller, delete_mock_db_tables_controller
from ..response import get_response
from . import mockdb_api


@mockdb_api.post("")
def create_mock_db_tables():
    try:
        return create_mock_db_tables_controller()
    except Exception as e:
        print("create_mock_db_tables exception : ", e)
        return get_response("MOCK_ERR001", None, 409)

@mockdb_api.delete("")
def delete_mock_db_tables():
    try:
       return delete_mock_db_tables_controller()
    except Exception as e:
        print("delete_mock_db_tables exception : ", e)
        return get_response("MOCK_ERR002", None, 409)
