from sqlalchemy import create_engine, text, create_engine
import src.config as config
import os

db_config = config.get()
connection_string = 'postgresql+psycopg2://'+ db_config['user'] +':'+ db_config['password'] +'@'+ db_config['host']
_db_syno = create_engine(connection_string + '/synofoto')

basedir = os.path.dirname(os.path.realpath(__file__))
connection_string_tagger = 'sqlite:///' + db_config['sqlite'] 
_db_tagger = create_engine(connection_string_tagger)

def get_engine(db_name='syno'):
    if (db_name == 'syno'):
        return _db_syno
    else:
        return _db_tagger

# Use it for SELECT statements
def query(sql, params=None, db_name = 'syno'):
    db = get_engine(db_name)
    with db.connect() as conn:
        result = conn.execute(text(sql), params)
        return result

# Use it for UPDATE and DELETE statements
def execute(sql, params, db_name = 'syno'):
    db = get_engine(db_name)
    with db.connect() as conn:
        conn.execute(text(sql), params)
        conn.commit()