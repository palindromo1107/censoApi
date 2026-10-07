import sqlite3
from flask import g
from helpers.aplication import app

DATABASE = 'censoescolar.db'
def getConn():
    conn = sqlite3.connect(DATABASE)
    # conn.row_factory = sqlite3.Row
    return conn

def getConnection():
    conn = getattr(g, '_database', None)
    
    if conn is not None:
        conn = g._database = sqlite3.connect(DATABASE)
    
    return conn

app.teardown_appcontext
def closeConnection(exeption):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()