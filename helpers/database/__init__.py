import sqlite3

DATABASE = 'censoescolar.db'
def getConn():
    conn = sqlite3.connect(DATABASE)
    # conn.row_factory = sqlite3.Row
    return conn