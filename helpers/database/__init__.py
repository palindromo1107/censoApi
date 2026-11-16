from flask import g
from helpers.application import app
from helpers.environment import environment
from sqlalchemy import create_engine
import psycopg2

DB_NAME= environment.get("DB_NAME")
DB_HOST= environment.get("DB_HOST")
DB_PORT= environment.get("DB_PORT")
DB_USER= environment.get("DB_USER")
DB_PASSWORD= environment.get("DB_PASSWORD")

URL_DB = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def getConnection():
    conn = getattr(g, '_database', None)

    conn = conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

    if conn is not None:
        return conn

app.teardown_appcontext
def closeConnection(exeption):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()