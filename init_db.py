import sqlite3

conn = None

try:
    conn = sqlite3.connect('censoescolar.db')
    with open('schema.sql') as file:
        conn.executescript(file.read())
    conn.commit()
    print("Comitado com sucesso!")

except sqlite3.Error as e:
    print(f"Exessão sqlite {str(e)}")

finally:
    if conn is not None:
        conn.close()
        print("Conexão finalizada!")