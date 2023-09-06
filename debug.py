from sqlalchemy import create_engine, text, create_engine
import sqlite3
import os
# os.path.join(basedir, 'app.db')
path = os.path.dirname(os.path.realpath(__file__))

connection_string_tagger = 'sqlite:////tagger.sqlite'
conn_str = 'sqlite:///' + path + '/tagger.db'
print(conn_str)
_db_tagger = create_engine(conn_str)

cnx = sqlite3.connect(path + '/tagger.db')
cursor = cnx.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#print(cursor.fetchall())

with _db_tagger.connect() as conn:
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    result = conn.execute(text(sql))
    for r in result:
       print(r.name)