from sqlalchemy.ext.declarative import declarative_base, declared_attr
from datetime import datetime
from .queries import add_table_query, fetch_table_query, edit_table_query, delete_table_query


class CustomBase(object):
    # GENERATE __tablename__ AUTOMATICALLY
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # DECLARE COMMON MODEL METHODS
    def get(cls, primeid):
        try:
            return fetch_table_query(cls.__class__, getbyprimeid=primeid)
        except Exception:
            raise

    def fetch(cls, filters=[]):
        try:
            return fetch_table_query([cls.__class__], filters=filters)
        except Exception:
            raise

    def add(cls, tablevalues, session_close=True):
        try:
            modified_tablevalues = {
                **tablevalues,
                "created_date": datetime.now(),
                "modified_date": datetime.now(),
            }
            return add_table_query(cls.__class__, modified_tablevalues, session_close=session_close)
        except Exception:
            raise

    def edit(cls, filters, tablevalues, session_close=True):
        try:
            modified_tablevalues = {
                **tablevalues,
                "modified_date": datetime.now(),
            }
            return edit_table_query(
                cls.__class__, filters, modified_tablevalues, session_close=session_close
            )
        except Exception:
            raise

    def delete(cls, filters, session_close=True):
        try:
            return delete_table_query(cls.__class__, filters, session_close=session_close)
        except Exception:
            raise


base = declarative_base(cls=CustomBase)
