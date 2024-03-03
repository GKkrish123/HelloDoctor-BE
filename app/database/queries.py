from .db_conn import get_session


# SQL OPERATIONS
def fetch_table_query(table, filters=[], orderby=None, getbyprimeid=None):
    try:
        db_session = get_session()
        if getbyprimeid:
            data = db_session.query(table).get(getbyprimeid)
            return data
        data = db_session.query(*table).filter(*filters).order_by(orderby)
        return data
    except Exception:
        raise


def add_table_query(table, tablevalues, session_close=True):
    try:
        db_session = get_session()
        data = table(**tablevalues)
        db_session.add(data)
        if session_close:
            db_session.commit()
            return data
        db_session.flush()
        return data
    except Exception:
        session_close = True
        db_session.rollback()
        raise
    finally:
        if session_close:
            db_session.close()


def edit_table_query(table, filters, tablevalues, session_close=True):
    try:
        db_session = get_session()
        table_query = db_session.query(table).filter(*filters)
        data_to_update = table_query.first()
        if data_to_update == None:
            raise Exception(
                f"NO EXISTING RECORD FOUND FOR FITLER TO UPDATE"
            )
        table_query.update(tablevalues)
        if session_close:
            db_session.commit()
        db_session.refresh(data_to_update)
        return data_to_update
    except Exception:
        session_close = True
        db_session.rollback()
        raise
    finally:
        if session_close:
            db_session.close()


def delete_table_query(table, filters=[], session_close=True):
    try:
        db_session = get_session()
        db_session.query(table).filter(*filters).delete()
        if session_close:
            db_session.commit()
    except Exception:
        session_close = True
        db_session.rollback()
        raise
    finally:
        if session_close:
            db_session.close()
