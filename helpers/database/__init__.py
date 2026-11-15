import sqlite3
from flask import g
from helpers.application import app
from helpers.environment import environment
from sqlalchemy import create_engine

DB_NAME= environment.get("DB_NAME")
DB_HOST= environment.get("DB_HOST")
DB_PORT= environment.get("DB_PORT")
DB_USER= environment.get("DB_USER")
DB_PASSWORD= environment.get("DB_PASSWORD")

URL_DB = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def getConn():
    conn = create_engine(URL_DB, pool_pre_ping=True)
    return conn

def getConnection():
    conn = create_engine(URL_DB, pool_pre_ping=True)
    
    if conn is not None:
        return conn.connect()

app.teardown_appcontext
def closeConnection(exeption):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()