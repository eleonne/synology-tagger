from sqlalchemy import create_engine, text, create_engine
import src.config as config

db_config = config.get()
connection_string = 'postgresql+psycopg2://'+ db_config['user'] +':'+ db_config['password'] +'@'+ db_config['host']
_db_syno = create_engine(connection_string + '/synofoto')

def get_engine(db_name='tagger'):
    if (db_name == 'syno'):
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