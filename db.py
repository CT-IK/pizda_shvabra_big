import sqlite3
import random

con = sqlite3.connect('DATA_SHA2.sqlite')
cur = con.cursor()

def userdata(username):
    query_table_id = ('SELECT tabel_id FROM dostup WHERE telega=?')
    table_id = cur.execute(query_table_id, (username,)).fetchone()
    if table_id == None:
        return (None,)
    else:
        table_id = table_id[0]
        query = (f'SELECT * FROM {table_id} WHERE telega=?')
        userdata = cur.execute(query, (username,)).fetchall()[0]
        return (userdata, table_id)
    
def usernames():
    query = ('SELECT telega FROM dostup')
    usernames = cur.execute(query).fetchall()
    return usernames