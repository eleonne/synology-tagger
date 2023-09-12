from sqlalchemy import create_engine, text, create_engine
from dotenv import dotenv_values

# class Singleton(type):
#     _instances = {}
#     db_tagger = None
#     db_syno = None
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             dotenv_path = '/app/.env'
#             env = dotenv_values(dotenv_path)
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#             connection_string = 'postgresql+psycopg2://'+ env['PG_USERNAME'] +':'+ env['PG_PASSWORD'] +'@'+ env['SYNOLOGY_HOST']
#             cls.db_syno = create_engine(connection_string + '/synofoto')
#             connection_string_tagger = 'mysql+pymysql://' + env['MYSQL_USER'] + ':' + env['MYSQL_PASSWORD'] + '@127.0.0.1/tagger'
#             cls.db_tagger = create_engine(connection_string_tagger)
#         return cls._instances[cls]
    
class DB():
    db_tagger = None
    db_syno = None

    def get_engine(self, db_name='syno'):
        if (db_name == 'syno'):
            dotenv_path = '/app/.env'
            env = dotenv_values(dotenv_path)
            connection_string = 'postgresql+psycopg2://'+ env['PG_USERNAME'] +':'+ env['PG_PASSWORD'] +'@'+ env['SYNOLOGY_HOST']
            self.db_syno = create_engine(connection_string + '/synofoto')
            return self.db_syno
        else:
            dotenv_path = '/app/.env'
            env = dotenv_values(dotenv_path)
            connection_string_tagger = 'mysql+pymysql://' + env['MYSQL_USER'] + ':' + env['MYSQL_PASSWORD'] + '@127.0.0.1/tagger'
            self.db_tagger = create_engine(connection_string_tagger)
            return self.db_tagger

# Use it for SELECT statements
def query(sql, params=None, db_name = 'syno'):
    db = DB().get_engine(db_name)
    with db.connect() as conn:
        result = conn.execute(text(sql), params)
        conn.close()
        return result

# Use it for UPDATE and DELETE statements
def execute(sql, params, db_name = 'syno'):
    db = DB().get_engine(db_name)
    with db.connect() as conn:
        conn.execute(text(sql), params)
        conn.commit()
        conn.close()