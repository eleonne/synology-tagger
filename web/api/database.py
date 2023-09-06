from sqlalchemy import create_engine, text, create_engine
import src.config as config

db_config = config.get()
connection_string = 'sqlite:////tagger.db'
_db_syno = create_engine(connection_string)

def get_engine():
    return _db_syno

# Use it for SELECT statements
def query(sql, params=None):
    with _db_syno.connect() as conn:
        result = conn.execute(text(sql), params)
        return result

# Use it for UPDATE and DELETE statements
def execute(sql, params):
    with _db_syno.connect() as conn:
        conn.execute(text(sql), params)
        conn.commit()